# VerSe Subset Training Smoke Test

**Run date:** October 3, 2026

## Purpose

Confirm that the project can load official VerSe CT/mask pairs, preprocess them,
sample 3D patches, train the MONAI 3D U-Net, and save a checkpoint. This is a
pipeline validation—not a segmentation benchmark.

## Data

- Source: official VerSe 2020 training archive, accessed through the project
  repository's published download endpoint.
- Subset: `sub-gl090` and `sub-gl364`, with paired CT and vertebral masks.
- Downloaded size: about 91 MB for the two CTs and masks.
- Native image dimensions: 512 x 512 x 171 and 512 x 512 x 149.
- License: CC BY-SA 4.0; cite the VerSe dataset in any subsequent report.

## Configuration and result

| Setting | Value |
| --- | --- |
| Device | CPU |
| Model | Small 3D U-Net: channels 8, 16, 32; 29 output classes |
| Preprocessing | RAS orientation, 1 mm spacing, HU [-1000, 400] scaled to [0, 1] |
| Patch size | 32 x 32 x 32 |
| Epochs | 5 |
| Epoch-1 loss | 4.4686 |
| Epoch-5 loss | 4.2178 |
| Checkpoint | `results/outputs/verse_subset_smoke.pt` (local and ignored by Git) |

The subset does not contain every vertebral class, so MONAI reported unavailable
classes during class-balanced patch sampling. That is expected for two
partial-field-of-view scans and confirms why this run cannot provide Dice, IoU,
HD95, labeling accuracy, or generalization claims.

## Next valid experiment

Use a storage location with at least 50 GB free to download and extract the full
training set, retain an untouched validation set, train a full-capacity model on
the official split, and calculate held-out per-vertebra metrics.
