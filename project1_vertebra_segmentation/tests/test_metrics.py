import numpy as np

from project1_vertebra_segmentation.src.evaluation.metrics import dice_score, hausdorff95, iou_score


def test_perfect_overlap_metrics():
    mask = np.zeros((8, 8, 8), dtype=np.uint8)
    mask[2:5, 2:5, 2:5] = 1
    assert dice_score(mask, mask, 1) == 1.0
    assert iou_score(mask, mask, 1) == 1.0
    assert hausdorff95(mask, mask, 1) == 0.0


def test_disjoint_masks_have_zero_overlap():
    prediction = np.zeros((8, 8, 8), dtype=np.uint8)
    target = prediction.copy()
    prediction[1:3, 1:3, 1:3] = 1
    target[5:7, 5:7, 5:7] = 1
    assert dice_score(prediction, target, 1) == 0.0
    assert iou_score(prediction, target, 1) == 0.0
    assert hausdorff95(prediction, target, 1) > 0
