"""Deterministic CT preprocessing used by training and inference."""

from typing import Sequence

import numpy as np
from scipy.ndimage import zoom


def resample_to_spacing(volume: np.ndarray, source_spacing: Sequence[float], target_spacing: Sequence[float] = (1, 1, 1), order: int = 1) -> np.ndarray:
    """Resample a volume from source to target voxel spacing."""
    factors = tuple(float(source) / float(target) for source, target in zip(source_spacing, target_spacing))
    return zoom(volume, factors, order=order)


def window_and_normalize(volume: np.ndarray, lower_hu: float = -1000, upper_hu: float = 400) -> np.ndarray:
    """Clip CT Hounsfield units and scale them to [0, 1]."""
    clipped = np.clip(volume, lower_hu, upper_hu)
    return ((clipped - lower_hu) / (upper_hu - lower_hu)).astype(np.float32)


def preprocess_volume(volume: np.ndarray, source_spacing: Sequence[float], target_spacing: Sequence[float] = (1, 1, 1), is_label: bool = False) -> np.ndarray:
    """Resample then normalize CT; labels use nearest-neighbour resampling only."""
    output = resample_to_spacing(volume, source_spacing, target_spacing, order=0 if is_label else 1)
    return output.astype(np.int16) if is_label else window_and_normalize(output)
