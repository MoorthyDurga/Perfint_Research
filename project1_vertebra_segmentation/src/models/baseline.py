"""MONAI 3D U-Net baseline definition."""


def build_baseline(
    in_channels: int = 1,
    out_channels: int = 26,
    channels: tuple[int, ...] = (32, 64, 128, 256, 512),
):
    """Create the selected residual 3D U-Net baseline.

    ``channels`` can be reduced for local smoke tests; retain the default for
    the planned VerSe baseline.
    """
    try:
        from monai.networks.nets import UNet
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install MONAI and PyTorch to build the baseline.") from exc
    return UNet(
        spatial_dims=3,
        in_channels=in_channels,
        out_channels=out_channels,
        channels=channels,
        strides=(2,) * (len(channels) - 1),
        num_res_units=2,
    )
