"""Train the 3D U-Net baseline from a local VerSe CSV manifest."""

import argparse
import csv
from pathlib import Path


def read_manifest(path: Path, split: str) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return [row for row in csv.DictReader(handle) if row["split"] == split]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--patch-size", type=int, default=96)
    parser.add_argument("--small-model", action="store_true", help="Use a small model for CPU-only subset smoke runs.")
    parser.add_argument("--output", type=Path, default=Path("results/checkpoints/baseline.pt"))
    args = parser.parse_args()
    try:
        import torch
        from monai.data import CacheDataset, DataLoader
        from monai.losses import DiceCELoss
        from monai.transforms import (
            Compose,
            EnsureChannelFirstd,
            LoadImaged,
            Orientationd,
            RandCropByLabelClassesd,
            RandFlipd,
            ScaleIntensityRanged,
            Spacingd,
            ToTensord,
        )
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install PyTorch and MONAI before training.") from exc

    from project1_vertebra_segmentation.src.models.baseline import build_baseline

    records = read_manifest(args.manifest, "training")
    if not records:
        raise RuntimeError("No training rows found in the manifest.")
    patch = (args.patch_size,) * 3
    transforms = Compose(
        [
            LoadImaged(keys=["image", "label"]),
            EnsureChannelFirstd(keys=["image", "label"], channel_dim="no_channel"),
            Orientationd(keys=["image", "label"], axcodes="RAS"),
            Spacingd(keys=["image", "label"], pixdim=(1.0, 1.0, 1.0), mode=("bilinear", "nearest")),
            ScaleIntensityRanged(keys="image", a_min=-1000, a_max=400, b_min=0.0, b_max=1.0, clip=True),
            RandCropByLabelClassesd(keys=["image", "label"], label_key="label", spatial_size=patch, ratios=[1] * 29, num_classes=29, num_samples=1),
            RandFlipd(keys=["image", "label"], prob=0.5, spatial_axis=0),
            ToTensord(keys=["image", "label"]),
        ]
    )
    dataset = CacheDataset(records, transform=transforms, cache_rate=0.1, num_workers=0)
    loader = DataLoader(dataset, batch_size=1, shuffle=True, num_workers=0)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = build_baseline(out_channels=29, channels=(8, 16, 32) if args.small_model else (32, 64, 128, 256, 512)).to(device)
    optimiser = torch.optim.AdamW(model.parameters(), lr=1e-4)
    loss_fn = DiceCELoss(to_onehot_y=True, softmax=True)

    for epoch in range(args.epochs):
        model.train()
        losses = []
        for batch in loader:
            image, label = batch["image"].to(device), batch["label"].to(device)
            optimiser.zero_grad()
            loss = loss_fn(model(image), label)
            loss.backward()
            optimiser.step()
            losses.append(loss.item())
        print(f"epoch={epoch + 1}/{args.epochs} loss={sum(losses) / len(losses):.4f}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"model_state_dict": model.state_dict(), "manifest": str(args.manifest), "epochs": args.epochs}, args.output)
    print(f"Saved checkpoint to {args.output}")


if __name__ == "__main__":
    main()
