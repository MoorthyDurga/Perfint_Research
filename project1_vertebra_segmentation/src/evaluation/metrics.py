"""Small, transparent segmentation metrics for baseline evaluation."""

import numpy as np
from scipy.ndimage import binary_erosion, distance_transform_edt


def _binary_masks(prediction: np.ndarray, target: np.ndarray, label: int) -> tuple[np.ndarray, np.ndarray]:
    if prediction.shape != target.shape:
        raise ValueError("Prediction and target must have the same shape.")
    return prediction == label, target == label


def dice_score(prediction: np.ndarray, target: np.ndarray, label: int) -> float:
    """Compute binary Dice; two empty masks are a perfect match."""
    pred, truth = _binary_masks(prediction, target, label)
    size = pred.sum() + truth.sum()
    return 1.0 if size == 0 else float(2 * np.logical_and(pred, truth).sum() / size)


def iou_score(prediction: np.ndarray, target: np.ndarray, label: int) -> float:
    """Compute binary intersection-over-union."""
    pred, truth = _binary_masks(prediction, target, label)
    union = np.logical_or(pred, truth).sum()
    return 1.0 if union == 0 else float(np.logical_and(pred, truth).sum() / union)


def hausdorff95(prediction: np.ndarray, target: np.ndarray, label: int, spacing=(1, 1, 1)) -> float:
    """Compute symmetric 95th-percentile surface distance in millimetres."""
    pred, truth = _binary_masks(prediction, target, label)
    if not pred.any() and not truth.any():
        return 0.0
    if not pred.any() or not truth.any():
        return float("inf")
    pred_surface = np.logical_xor(pred, binary_erosion(pred))
    truth_surface = np.logical_xor(truth, binary_erosion(truth))
    pred_to_truth = distance_transform_edt(~truth_surface, sampling=spacing)[pred_surface]
    truth_to_pred = distance_transform_edt(~pred_surface, sampling=spacing)[truth_surface]
    return float(np.percentile(np.concatenate([pred_to_truth, truth_to_pred]), 95))
