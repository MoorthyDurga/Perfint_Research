"""NIfTI CT input/output helpers."""

from pathlib import Path
from typing import Tuple

import numpy as np


def load_nifti(path: str | Path) -> Tuple[np.ndarray, np.ndarray]:
    """Load a NIfTI image in RAS+ orientation."""
    try:
        import nibabel as nib
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install nibabel to load NIfTI files.") from exc
    image = nib.as_closest_canonical(nib.load(str(path)))
    return image.get_fdata(dtype=np.float32), image.affine


def save_nifti(data: np.ndarray, affine: np.ndarray, path: str | Path) -> None:
    """Save a float32 array as a NIfTI image."""
    try:
        import nibabel as nib
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install nibabel to save NIfTI files.") from exc
    nib.save(nib.Nifti1Image(data.astype(np.float32), affine), str(path))
