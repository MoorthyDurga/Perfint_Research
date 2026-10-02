# October 3 Meeting Readiness

## Verified today

- The research decisions are documented: VerSe is the proposed primary dataset, MONAI/PyTorch is the chosen framework, and a 3D U-Net is the selected baseline.
- A runnable implementation baseline now exists for NIfTI loading/orientation, 1 mm resampling, HU windowing, a paired CT/label dataset abstraction, MONAI 3D U-Net construction, sliding-window inference, and Dice/IoU/HD95 metrics.
- Synthetic unit tests cover preprocessing and metrics.

## Not yet verified -- do not describe as results

- No VerSe volume, annotation, split, or data-integrity check is present in this repository.
- No local MONAI/PyTorch runtime or GPU was available when this update was prepared.
- No model has been trained. Therefore Dice, IoU, HD95, labeling accuracy, and inference-time values are all **pending**.

## Demonstration protocol once VerSe and the environment are available

1. Fill a local, untracked manifest using `project1_vertebra_segmentation/configs/dataset_manifest.example.csv`.
2. Run `pytest project1_vertebra_segmentation/tests`.
3. Load one CT and label pair through `CTVolumeDataset`; record shape, spacing, label IDs, and a three-plane QC image.
4. Build the 3D U-Net, run a forward pass and sliding-window inference, and record GPU/device plus elapsed time.
5. Start baseline training only after the official patient-level split and VerSe label mapping have been confirmed.

## Decisions needed from the meeting

1. Confirm access and permitted storage for VerSe 2020; confirm whether CTSpine1K is available later for robustness testing.
2. Confirm the GPU host, available memory, and expected compute allocation.
3. Approve the official label mapping, whether sacrum is included, and the patient-level training/validation/test split.
4. Agree that the next quantitative milestone is baseline validation on VerSe, rather than a clinical/navigation claim.

## Revised near-term milestones

| Milestone | Completion evidence |
| --- | --- |
| Data readiness | Manifest, integrity report, split, and QC images |
| Pipeline readiness | Passing unit tests plus one real VerSe batch |
| Baseline readiness | Reproducible 3D U-Net forward/inference run |
| Quantitative baseline | Held-out Dice, IoU, HD95, per-vertebra metrics, timing, and failure cases |
