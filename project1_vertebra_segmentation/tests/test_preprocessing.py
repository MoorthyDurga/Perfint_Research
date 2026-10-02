import numpy as np

from project1_vertebra_segmentation.src.preprocessing.transforms import preprocess_volume, window_and_normalize


def test_windowing_limits_and_scales_hu_values():
    volume = np.array([-2000, -1000, -300, 400, 1000], dtype=np.float32)
    actual = window_and_normalize(volume)
    assert np.allclose(actual, [0, 0, 0.5, 1, 1])


def test_label_preprocessing_preserves_integer_labels():
    labels = np.array([[[0, 1], [2, 3]]], dtype=np.int16)
    actual = preprocess_volume(labels, (1, 1, 1), is_label=True)
    assert actual.dtype == np.int16
    assert np.array_equal(actual, labels)
