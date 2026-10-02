"""MONAI 3D U-Net baseline definition."""


def build_baseline(in_channels: int = 1, out_channels: int = 26):
    """Create the selected residual 3D U-Net baseline."""
    try:
        from monai.networks.nets import UNet
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install MONAI and PyTorch to build the baseline.") from exc
    return UNet(spatial_dims=3, in_channels=in_channels, out_channels=out_channels, channels=(32, 64, 128, 256, 512), strides=(2, 2, 2, 2), num_res_units=2)
