"""Report evidence-backed progress against the current research plan.

This script checks repository artifacts and optional local data/checkpoints. It
does not infer clinical performance from the existence of a checkpoint.
"""

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def exists(relative_path: str) -> bool:
    return (ROOT / relative_path).is_file()


def manifest_summary(path: Path) -> tuple[int, int]:
    """Return training and validation counts, or zeroes when no manifest exists."""
    if not path.is_file():
        return 0, 0
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    return sum(row.get("split") == "training" for row in rows), sum(row.get("split") == "validation" for row in rows)


def status(label: str, complete: bool, partial: bool = False, detail: str = "") -> dict:
    state = "COMPLETE" if complete else "PARTIAL" if partial else "NOT STARTED"
    return {"milestone": label, "status": state, "detail": detail}


def build_report(data_root: Path, checkpoint: Path) -> list[dict]:
    research_files = [
        "project1_vertebra_segmentation/literature/literature_review.md",
        "project1_vertebra_segmentation/literature/papers.csv",
        "project1_vertebra_segmentation/models/model_benchmark.md",
        "project1_vertebra_segmentation/models/baseline_selection.md",
    ]
    pipeline_files = [
        "project1_vertebra_segmentation/src/preprocessing/transforms.py",
        "project1_vertebra_segmentation/src/datasets/ct_dataset.py",
        "project1_vertebra_segmentation/src/models/baseline.py",
        "project1_vertebra_segmentation/src/inference/predictor.py",
        "project1_vertebra_segmentation/src/evaluation/metrics.py",
    ]
    project2_files = [
        "project2_navigation/competitor_analysis.md",
        "project2_navigation/competitor_matrix.csv",
        "project2_navigation/navigation_workflows.md",
        "project2_navigation/instrument_taxonomy.md",
        "project2_navigation/opportunity_matrix.csv",
    ]
    manifest = data_root / "manifest.csv"
    train_count, validation_count = manifest_summary(manifest)
    ct_count = len(list(data_root.rglob("*_ct.nii.gz"))) if data_root.is_dir() else 0
    full_split = train_count >= 100 and validation_count > 0

    return [
        status("Project 1 literature, datasets, and baseline selection", all(map(exists, research_files))),
        status("Baseline CT preprocessing, model, inference, and metrics", all(map(exists, pipeline_files))),
        status("Project 2 competitor/workflow/instrument analysis", all(map(exists, project2_files))),
        status(
            "Real VerSe data readiness",
            full_split,
            ct_count > 0,
            f"CT files={ct_count}; manifest training={train_count}; validation={validation_count}",
        ),
        status(
            "Full-split baseline training and held-out evaluation",
            False,
            checkpoint.is_file(),
            "A local checkpoint exists" if checkpoint.is_file() else "No checkpoint found",
        ),
        status("Pedicle identification and screw planning", False, detail="No implementation artifact found"),
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, default=ROOT / "data" / "verse_subset")
    parser.add_argument("--checkpoint", type=Path, default=ROOT / "results" / "outputs" / "verse_subset_smoke.pt")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()
    report = build_report(args.data_root, args.checkpoint)
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print("Current progress check")
    print("=" * 78)
    for item in report:
        suffix = f" — {item['detail']}" if item["detail"] else ""
        print(f"[{item['status']}] {item['milestone']}{suffix}")


if __name__ == "__main__":
    main()
