"""Sliding-window model inference."""


def predict_volume(model, image, roi_size=(128, 128, 128), overlap=0.25):
    """Return a discrete segmentation from a channel-first batched image."""
    try:
        import torch
        from monai.inferers import sliding_window_inference
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install MONAI and PyTorch for inference.") from exc
    model.eval()
    with torch.no_grad():
        logits = sliding_window_inference(image, roi_size, sw_batch_size=1, predictor=model, overlap=overlap)
    return logits.argmax(dim=1)
