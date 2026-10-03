"""Build a local CSV manifest from the official restructured VerSe archive."""

import argparse
import csv
from pathlib import Path


def find_records(root: Path, split: str) -> list[dict[str, str]]:
    """Find official VerSe CT/mask pairs for one split.

    Expected archive layout: ``<split>/rawdata/sub-*/..._ct.nii.gz`` and
    ``<split>/derivatives/sub-*/..._seg-vert_msk.nii.gz``.
    """
    records = []
    for image in sorted((root / split / "rawdata").glob("sub-*/*_ct.nii.gz")):
        subject = image.parent.name
        derivatives = root / split / "derivatives" / subject
        masks = sorted(derivatives.glob("*_seg-vert_msk.nii.gz"))
        if len(masks) == 1:
            records.append({"id": subject, "split": split, "image": str(image.resolve()), "label": str(masks[0].resolve())})
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verse-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    records = find_records(args.verse_root, "training") + find_records(args.verse_root, "validation")
    if not records:
        raise RuntimeError("No paired VerSe CT/mask files found. Check the archive layout and path.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "split", "image", "label"])
        writer.writeheader()
        writer.writerows(records)
    print(f"Wrote {len(records)} paired CT/mask records to {args.output}")


if __name__ == "__main__":
    main()
