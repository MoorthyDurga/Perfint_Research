"""PyTorch dataset for paired CT and vertebra-label NIfTI files."""

from pathlib import Path
from typing import Iterable

import numpy as np

from ..preprocessing import load_nifti, preprocess_volume


class CTVolumeDataset:
    """Load paired image/label paths and return channel-first tensors."""

    def __init__(self, records: Iterable[dict], target_spacing: tuple[float, float, float] = (1, 1, 1)):
        self.records = list(records)
        self.target_spacing = target_spacing

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, index: int) -> dict:
        try:
            import torch
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Install PyTorch to use CTVolumeDataset.") from exc
        record = self.records[index]
        image, affine = load_nifti(record["image"])
        spacing = tuple(np.sqrt((affine[:3, :3] ** 2).sum(axis=0)))
        image = preprocess_volume(image, spacing, self.target_spacing)
        item = {"image": torch.from_numpy(image[None]), "id": record.get("id", Path(record["image"]).stem)}
        if record.get("label"):
            label, _ = load_nifti(record["label"])
            label = preprocess_volume(label, spacing, self.target_spacing, is_label=True)
            item["label"] = torch.from_numpy(label.astype(np.int64))
        return item
