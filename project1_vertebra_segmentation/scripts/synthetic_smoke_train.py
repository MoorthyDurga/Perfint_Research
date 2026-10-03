"""Train a deliberately tiny 3D U-Net on synthetic CT-like volumes.

This verifies the local model, gradient, optimiser, and metric path. It is not
a medical experiment and must never be reported as a VerSe result.
"""

import argparse

import numpy as np
import torch
from torch.nn import CrossEntropyLoss
from torch.utils.data import DataLoader, Dataset

from project1_vertebra_segmentation.src.evaluation.metrics import dice_score
from project1_vertebra_segmentation.src.models.baseline import build_baseline


class SyntheticVertebraLikeDataset(Dataset):
    """Small spheres in noisy volumes, used only for end-to-end smoke testing."""

    def __init__(self, count: int, size: int, seed: int) -> None:
        rng = np.random.default_rng(seed)
        axes = np.ogrid[:size, :size, :size]
        self.items = []
        for _ in range(count):
            center = rng.integers(size // 3, 2 * size // 3, size=3)
            radius = int(rng.integers(max(3, size // 8), max(4, size // 5)))
            mask = sum((axis - coordinate) ** 2 for axis, coordinate in zip(axes, center)) <= radius**2
            image = rng.normal(0.1, 0.03, size=(size, size, size)).astype(np.float32)
            image[mask] = rng.normal(0.8, 0.03, size=int(mask.sum()))
            self.items.append((torch.from_numpy(image[None]), torch.from_numpy(mask.astype(np.int64))))

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int):
        return self.items[index]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=12)
    parser.add_argument("--size", type=int, default=32)
    args = parser.parse_args()

    torch.manual_seed(7)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dataset = SyntheticVertebraLikeDataset(count=8, size=args.size, seed=7)
    loader = DataLoader(dataset, batch_size=2, shuffle=True)
    model = build_baseline(out_channels=2, channels=(8, 16, 32)).to(device)
    optimiser = torch.optim.AdamW(model.parameters(), lr=2e-3)
    # Foreground is deliberately small, mirroring the class-imbalance issue in
    # volumetric segmentation while keeping this smoke test fast on CPU.
    loss_fn = CrossEntropyLoss(weight=torch.tensor([0.2, 1.0], device=device))

    model.train()
    for epoch in range(args.epochs):
        losses = []
        for image, label in loader:
            image, label = image.to(device), label.to(device)
            optimiser.zero_grad()
            loss = loss_fn(model(image), label)
            loss.backward()
            optimiser.step()
            losses.append(loss.item())
        print(f"epoch={epoch + 1} loss={np.mean(losses):.4f}")

    model.eval()
    image, label = dataset[0]
    with torch.no_grad():
        prediction = model(image.unsqueeze(0).to(device)).argmax(dim=1).cpu().numpy()[0]
    dice = dice_score(prediction, label.numpy(), label=1)
    print(f"device={device.type} synthetic_foreground_dice={dice:.4f}")
    if dice < 0.75:
        raise RuntimeError("Synthetic smoke-training Dice is below the expected threshold.")


if __name__ == "__main__":
    main()
