# Project Status Report

**As of:** October 3, 2026

**Repository:** Perfint_Research / `main`
**Status:** Research foundation complete; implementation baseline ready for real-data validation

## Executive summary

The project has completed its initial research and technical-design work. The
repository now also contains a first engineering baseline for the CT workflow.
It is ready to be exercised on VerSe data once access, the official label map,
and the MONAI/PyTorch runtime have been verified.

No model has been trained yet. Reported Dice, IoU, Hausdorff distance, labeling
accuracy, and runtime benchmarks are therefore targets from the literature, not
results from this project.

## Project 1: Vertebral segmentation and labeling

| Component | Status | Evidence |
| --- | --- | --- |
| Literature, dataset, and model review | COMPLETE | 25-paper review; VerSe selected as proposed primary dataset |
| Framework and baseline choice | COMPLETE | MONAI/PyTorch and residual 3D U-Net documented |
| CT preprocessing | IMPLEMENTED | RAS-oriented NIfTI loading, resampling to 1 mm, HU windowing/normalization |
| Dataset interface | IMPLEMENTED | Paired CT/label `CTVolumeDataset` plus manifest template |
| Baseline model | IMPLEMENTED, UNTRAINED | Configurable MONAI 3D U-Net |
| Local training smoke test | COMPLETE | CPU synthetic training: loss 0.6160 to 0.1197; Dice 0.8723 (non-clinical) |
| Inference | IMPLEMENTED, UNVALIDATED | Sliding-window predictor |
| Evaluation | IMPLEMENTED | Dice, IoU, HD95; synthetic tests pass |
| Quantitative validation | NOT STARTED | Requires VerSe data, confirmed split/label map, and training runtime |
| VerSe ingestion/training tools | IMPLEMENTED | Manifest builder and MONAI training entry point; dataset download blocked by local storage |
| Anatomical labeling and pedicle planning | NOT STARTED | Starts after segmentation baseline validation |

### Immediate next steps

1. Confirm VerSe 2020 access, permitted data storage, official patient-level split, and label encoding.
2. Populate a local manifest; run preprocessing and data-loader quality checks on paired CT/segmentation volumes.
3. Verify MONAI, PyTorch, CUDA/GPU availability, memory, and a model forward pass.
4. Train the 3D U-Net baseline and report held-out Dice, IoU, HD95, per-vertebra performance, timing, and failure cases.
5. Implement centroid-based instance separation and ordinal/anatomical labeling only after the segmentation baseline is measured.

## Project 2: Navigation analysis

| Component | Status |
| --- | --- |
| Five-platform competitive analysis | COMPLETE |
| 11-stage workflow mapping | COMPLETE |
| Five-category instrument taxonomy | COMPLETE |
| Opportunity matrix for segmentation/navigation integration | COMPLETE |
| Clinical integration or C-Arm prototype | NOT STARTED; dependent on validated Project 1 output |

## Current blockers and decisions

- **Data/storage:** VerSe is publicly available, but its 11.5 GB training archive cannot be safely extracted alongside checkpoints with only 23 GB free. Provide a location with at least 50 GB free, then confirm the label map and split.
- **Compute:** local CPU execution is verified; confirm a MONAI/PyTorch-compatible GPU and available memory/compute allocation for VerSe training.
- **Scope:** agree that the next milestone is a reproducible VerSe baseline, not a clinical or navigation-performance claim.

## Verification

The implementation’s synthetic tests pass with:

```bash
pytest project1_vertebra_segmentation/tests
```

See [meeting readiness](docs/MEETING_READINESS.md) for the live-data demonstration protocol and meeting decisions.
See [local smoke-test evidence](docs/LOCAL_SMOKE_TEST.md) for the reproducible synthetic run.
