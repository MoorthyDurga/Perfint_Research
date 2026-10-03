# Local Synthetic Training Smoke Test

**Run date:** October 3, 2026  
**Purpose:** Verify that the local 3D U-Net model, loss, optimizer, backward
pass, and Dice metric run end to end. This is not a VerSe or clinical result.

## Command

```bash
PYTHONPATH=.:/private/tmp/vertebra-smoke-deps \
python project1_vertebra_segmentation/scripts/synthetic_smoke_train.py --epochs 12 --size 16
```

## Result

| Measure | Value |
| --- | ---: |
| Device | CPU |
| Initial epoch loss | 0.6160 |
| Final epoch loss | 0.1197 |
| Synthetic foreground Dice | 0.8723 |

The script used eight generated 16-cubed noisy volumes with a simple spherical
foreground. It has no patient data, anatomical labels, or clinical meaning.

## Next real-data run

After VerSe access, official label mapping, and the patient-level split are
confirmed, replace this synthetic dataset with a manifest-backed VerSe loader
and record the exact environment, split, checkpoint, held-out metrics, runtime,
and failure cases.
