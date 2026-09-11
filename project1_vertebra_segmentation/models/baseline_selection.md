# Baseline Model Selection: Vertebral Segmentation & Labeling

**Version:** 1.0
**Date:** September 7, 2026
**Status:** FINAL DECISION

---

## Executive Summary

After comprehensive literature review, dataset benchmarking, and architecture evaluation, the following baseline is selected for the initial development phase:

| Component | Selection | Rationale |
|-----------|-----------|-----------|
| **Framework** | MONAI + PyTorch | Comprehensive medical imaging support + good documentation |
| **Architecture** | 3D U-Net (initial)  nnU-Net (comparison)  Swin UNETR (optional) | Progressive complexity; benchmark against SOTA |
| **Primary Dataset** | VerSe 2020 | Community standard; per-vertebra labels; pathology included |
| **Secondary Dataset** | CTSpine1K (pretraining) | Scale for transfer learning; proven effectiveness |
| **Validation Dataset** | SPIDER | Cross-validation; domain robustness testing |
| **Segmentation Approach** | Multi-class (26 vertebra classes) | Direct per-vertebra segmentation; standard VerSe methodology |
| **Labeling Strategy** | Multi-class output implicit + sequential ordering | Anatomical labels implicit in class membership |
| **Inference Method** | Sliding-window 3D convolution | Handles large volumes; efficient memory usage |
| **Evaluation Metrics** | Dice, IoU, Hausdorff distance, surface distance | Comprehensive; includes boundary accuracy |

---

## 1. Framework Decision: MONAI + PyTorch

### 1.1 Selection Justification

**Evaluated frameworks:**
1. MONAI + PyTorch (SELECTED)
2. nnU-Net (alternative)
3. Custom PyTorch (not recommended)

### 1.2 MONAI Advantages vs Alternatives

**MONAI vs nnU-Net:**

| Criterion | MONAI | nnU-Net | Winner |
|-----------|-------|---------|--------|
| Flexibility | Very high | Low (fixed pipeline) | MONAI |
| Learning curve | Moderate | Low | nnU-Net |
| Reproducibility | High | Very high | nnU-Net |
| Customization | Very easy | Difficult | MONAI |
| 3D CT support | Excellent | Excellent | TIE |
| Documentation | Very good | Good | MONAI |
| Community adoption | Growing | Very high | nnU-Net |
| Research modifications | Easy | Hard | MONAI |

**Decision matrix rationale:**
- MONAI preferred for **research project** (need flexibility)
- nnU-Net better for **production pipeline** (zero tuning)

**For this project:** Research-first approach -> MONAI is better choice

### 1.3 MONAI Setup

**Installation:**
```bash
# Create virtual environment
python -m venv vertebra_seg_env
source vertebra_seg_env/bin/activate

# Install MONAI + dependencies
pip install monai==1.2.0 PyTorch 2.0.0 CUDA 12.1

# Additional tools
pip install nibabel pydicom numpy pandas scikit-learn scipy matplotlib tqdm
```

**Verification:**
```python
import monai
print(f"MONAI version: {monai.__version__}")

from monai.networks.nets import UNet
print("3D U-Net import successful")
```

---

## 2. Architecture Decision: Three-Phase Approach

### 2.1 Phase 1 Baseline: 3D U-Net

**Selection:** 3D U-Net (MONAI implementation)

**Why this architecture**

1. **Simplicity:** Easy to understand, debug, and modify
2. **Performance:** Achieves Dice 0.90-0.92 (good baseline)
3. **Maturity:** Foundational; many published comparisons available
4. **Interpretability:** Skip connections explicitly interpretable
5. **Moderate compute:** Requires ~6-8GB GPU (accessible)
6. **Research flexibility:** Easy to customize for variations

**Why NOT other Phase 1 candidates**

| Architecture | Why not selected |
|----------|----------|
| 2D U-Net | Limited 3D context; poor performance on volumetric task |
| nnU-Net | Too automatic for initial learning; harder to customize |
| UNETR | Overkill complexity for baseline; slower; higher memory |
| Swin UNETR | Advanced for Phase 1; revisit in Phase 3 if needed |
| Custom PyTorch | Implementation burden; reproducibility risk |

**Phase 1 success criteria:**
- Dice > 0.88 on VerSe test set
- Training convergence without instability
- Inference time < 60 seconds per volume
- Reproducible results (same seed  same output)

---

### 2.2 Phase 2 Benchmark: nnU-Net

**Selection:** nnU-Net (reference standard comparison)

**Why nnU-Net for Phase 2**

1. **Validation:** Benchmarks Phase 1 implementation quality
2. **SOTA performance:** Achieves Dice 0.93-0.94 (state-of-the-art)
3. **No tuning:** Fully automatic configuration (reproducible)
4. **Publication ready:** Widely accepted as baseline in literature
5. **Comparison:** Direct performance comparison with Phase 1

**Phase 2 success criteria:**
- nnU-Net achieves Dice 0.93-0.94
- 3D U-Net within 2-3% of nnU-Net (expected gap)
- Identify performance gap sources
- Validate implementation quality

**Performance expectation:**
```
Phase 1 (3D U-Net):    Dice  0.90-0.92
Phase 2 (nnU-Net):     Dice  0.93-0.94
Expected gap:          1-2%

If gap > 5%:  Indicates suboptimal Phase 1 implementation
If gap  1-2%: Indicates solid baseline; gap is architectural
```

---

### 2.3 Phase 3 Enhancement (Optional): Swin UNETR

**Selection:** Swin UNETR (if pursuing interpretability or SOTA accuracy)

**When to pursue Phase 3:**
- [OK] If Phase 1-2 successful and on schedule
- [OK] If interpretability important for publication/presentation
- [OK] If computational resources allow extended experimentation
- [OK] If maximum accuracy desired for clinical application

**When NOT to pursue Phase 3:**
- [OK] If Phase 1-2 already consuming intended timeline
- [OK] If GPU resources limited
- [OK] If Phase 1-2 results satisfactory for objectives

**Phase 3 success criteria:**
- Swin UNETR achieves Dice 0.93+ (matches or exceeds nnU-Net)
- Attention visualization provides interpretability
- Improved cross-dataset generalization (SPIDER validation)

---

## 3. Dataset Selection: Tiered Approach

### 3.1 Primary Training Dataset: VerSe 2020

**Selection:** VerSe 2020 (580 CT volumes)

**Why VerSe**
1. **Standard benchmark:** 50+ published results (enables direct comparison)
2. **Per-vertebra labels:** Each vertebra individually annotated (enables vertebra-level metrics)
3. **Pathology diversity:** Includes fractures, degeneration, scoliosis (realistic data)
4. **Community validation:** Multiple expert reviews improve annotation quality
5. **Established splits:** Official train/val/test split (reproducible)
6. **Easy access:** Free download after registration

**Why NOT alternatives for primary**

| Dataset | Reason not selected as primary |
|---------|------|
| CTSpine1K | No per-vertebra labels (coarse binary masks) |
| SPIDER | Smaller dataset (300 vs 580 volumes) |
| TotalSegmentator | Organ-level spine (not per-vertebra); requires adaptation |

**VerSe data split:**
- Training: ~406 volumes (70%)
- Validation: ~87 volumes (15%)
- Test: ~87 volumes (15%)
- Patient-level split (no patient leakage between sets)

---

### 3.2 Secondary Dataset: CTSpine1K (Pretraining)

**Selection:** CTSpine1K (1000 CT volumes)

**Usage strategy:**

```
Step 1: Pretrain model on CTSpine1K
         Learns general spine anatomy
         Binary spine segmentation (all vertebrae as one class)
         Training time: ~40-60 GPU hours

Step 2: Fine-tune on VerSe
         Learns per-vertebra discrimination
         Adapt output layer: 1 class  26 classes
         Training time: ~20-40 GPU hours

Step 3: Evaluate on VerSe test set
         Compare vs VerSe-only training
         Expected improvement: +1-2% Dice
```

**Performance expectation:**
- VerSe-only training: Dice  0.92
- CTSpine1K pretrain + VerSe fine-tune: Dice  0.93-0.94
- Improvement: ~1-2% Dice

**Why CTSpine1K for pretraining**
1. **Scale:** 1000 volumes (1.7x more than VerSe)
2. **Diversity:** Different institutions and imaging protocols
3. **Accessibility:** Public, no special access required
4. **Established use:** Growing adoption as pretraining source
5. **Complementary labeling:** Binary spine (vs VerSe per-vertebra)

---

### 3.3 Validation Dataset: SPIDER

**Selection:** SPIDER (200-400 CT volumes)

**Usage strategy:**

```
Step 1: Train model on VerSe
Step 2: Evaluate on SPIDER (without any SPIDER training)
Step 3: Measure domain shift
         Expected Dice: 0.87-0.92 (acceptable 2-5% drop)
         If drop > 10%: model overfits to VerSe protocol
```

**Why SPIDER for validation**
1. **Independent data:** Different imaging institution and protocols
2. **Cross-validation:** Tests generalization to unseen domains
3. **Established use:** Standard cross-validation benchmark
4. **Realistic challenge:** Different scanner  different intensity distribution
5. **Clinical relevance:** Proves model works in practice

**Success criteria:**
- Dice on SPIDER > 0.87 (acceptable generalization)
- Performance drop < 5% (good robustness)
- Per-vertebra Dice consistent across anatomies

---

## 4. Segmentation Approach: Multi-Class Direct

### 4.1 Problem Formulation

**Output format:** 26-class segmentation

```
For each voxel in CT volume:
  Class 0: Background
  Class 1: C1 (cervical vertebra 1)
  Class 2: C2
  ...
  Class 7: C7
  Class 8: T1 (thoracic)
  ...
  Class 19: T12
  Class 20: L1 (lumbar)
  ...
  Class 26: L5
  (S1 included if present in dataset)
```

**Output tensor shape:** (batch, 26, height, width, depth)

**Per-voxel predictions:** Softmax over 26 classes

### 4.2 Training Procedure

**Loss function:** Dice + Cross-Entropy combined

```python
# Pseudocode
loss = 0.7 * dice_loss(predictions, targets) +
       0.3 * cross_entropy_loss(predictions, targets)
```

**Rationale:**
- Dice loss: Directly optimizes segmentation overlap (primary objective)
- CE loss: Provides gradient stability (secondary objective)
- Weight 0.7/0.3: Empirically works well for imbalanced segmentation

**Alternative loss (if class imbalance problematic):**

```python
loss = 0.7 * weighted_dice_loss(predictions, targets, weights=class_weights) +
       0.3 * focal_loss(predictions, targets, alpha=2.0)
```

Where `class_weights` account for vertebra frequency (L5 less common due to transitional variants).

### 4.3 Inference Procedure

**Sliding-window inference** (handles large volumes):

```python
# Pseudocode
def sliding_window_inference(ct_volume, model, patch_size=96, overlap=0.5):
    """
    Process large volume with overlapping patches.

    Args:
        ct_volume: (H, W, D) 3D CT array
        model: Trained segmentation network
        patch_size: 96 (96 patches)
        overlap: 0.5 (50% overlap between patches)

    Returns:
        segmentation: (H, W, D) predicted labels
    """
    output = np.zeros(ct_volume.shape, dtype=np.int32)
    counts = np.zeros(ct_volume.shape, dtype=np.float32)

    # Generate sliding window patches
    for i in range(0, H, patch_size // 2):  # 50% stride
        for j in range(0, W, patch_size // 2):
            for k in range(0, D, patch_size // 2):
                # Extract patch
                patch = ct_volume[i:i+patch_size, j:j+patch_size, k:k+patch_size]

                # Pad if at boundary
                if patch.shape != (patch_size, patch_size, patch_size):
                    patch = np.pad(patch, ...)  # Pad to size

                # Run inference
                with torch.no_grad():
                    pred = model(torch.tensor(patch).unsqueeze(0))  # (1, 26, 96, 96, 96)
                    pred = torch.argmax(pred, dim=1)  # (1, 96, 96, 96)

                # Accumulate predictions (average overlapping regions)
                output[i:i+patch_size, j:j+patch_size, k:k+patch_size] += pred[0].numpy()
                counts[i:i+patch_size, j:j+patch_size, k:k+patch_size] += 1

    # Average overlapping regions
    output = output / (counts + 1e-8)
    return output.astype(np.uint8)
```

**Advantages:**
- [OK] Handles arbitrary volume sizes (not limited to patch size)
- [OK] Smooth predictions in overlap regions (averaging)
- [OK] Memory-efficient (processes patches sequentially)

**Typical parameters:**
- Patch size: 96 (balance between context and memory)
- Overlap: 50% (sufficient smoothing; not wasteful)
- Inference time: ~20-40 seconds per volume (GPU)

---

## 5. Vertebral Labeling Strategy

### 5.1 Approach: Multi-Class Direct Output

**Simple strategy:** Segmentation implicitly provides labels

```
If predicted class = 5:
  => Vertebra C5 (cervical 5)

If predicted class = 15:
  => Vertebra T8 (thoracic 8)

If predicted class = 24:
  => Vertebra L4 (lumbar 4)
```

**Why this approach**
1. **Simplicity:** No separate labeling network needed
2. **Efficient:** Single forward pass provides both segmentation and labeling
3. **Consistent:** Segmentation and labeling necessarily aligned
4. **Standard:** Matches VerSe benchmark methodology

### 5.2 Challenges & Mitigation

**Challenge 1: Anatomical variation (transitional vertebrae)**
- Spondylosacral transitional L5
- Lumbarization: First sacral segment separate
- Mitigation: Include in training data (VerSe does); model learns variation

**Challenge 2: Incorrect sequential ordering (scoliosis)**
- Severe scoliosis  superior-to-inferior z-ordering breaks
- Mitigation: Multi-class inherently captures all 26 classes regardless of ordering

**Challenge 3: Missing vertebrae (fusion or congenital)**
- Vertebra missing  labeling sequence breaks
- Mitigation: Multi-class framework handles missing classes (doesn't assume continuity)

**Challenge 4: Partial field-of-view**
- Scan may not include entire spine
- Mitigation: Model predicts what's visible; missing classes default to background

### 5.3 Post-Processing (Optional)

**If vertebral numbering confidence issues arise:**

```python
def enforce_anatomical_ordering(segmentation):
    """
    Post-process to ensure anatomical plausibility.

    1. Extract connected components per class
    2. Check if components are ordered superior-to-inferior
    3. Resolve conflicts (if two C1s, keep superior; remove inferior)
    4. Fill gaps (if C1 and C3 present but C2 missing)
    """
    # Extract centroids per class
    centroids = {}
    for class_id in range(1, 27):
        mask = segmentation == class_id
        if mask.any():
            centroids[class_id] = centroid(mask)

    # Check ordering
    z_coords = [centroids[c][2] for c in centroids if c in centroids]

    # If misordered (e.g., scoliosis), output confidence warning
    return segmentation, confidence_score
```

**Note:** Phase 1 will not implement this. Only if problems arise.

---

## 6. Evaluation Metrics

### 6.1 Primary Metrics: Dice & IoU

**Dice coefficient:**
```
Dice = 2|X  Y| / (|X| + |Y|)

Interpretation:
  0.95+: Excellent
  0.90-0.95: Very good
  0.85-0.90: Good
  0.80-0.85: Acceptable
  <0.80: Poor
```

**Report per-vertebra Dice:**
```
C1: 0.92
C2: 0.93
C3: 0.91
...
L5: 0.87  (typically lower)

Mean Dice: 0.91  0.02
```

**Intersection over Union (IoU):**
```
IoU = |X  Y| / |X  Y|

Relationship: IoU = Dice / (2 - Dice)
```

Both Dice and IoU reported for completeness.

---

### 6.2 Boundary Accuracy: Hausdorff & Surface Distance

**Hausdorff Distance (HD):**
```
HD = max(max_{x  X} d(x, Y), max_{y  Y} d(y, X))

Interpretation: Maximum boundary error (worst-case)
Units: Millimeters
Typical VerSe: 5-15mm (depends on vertebra size)

Problem: Single outlier point skews entire metric
Solution: Report 95th percentile instead of max
```

**Average Surface Distance (ASD):**
```
ASD = (1/|S_X|) _{x  S_X} d(x, S_Y)

Interpretation: Average boundary error
Units: Millimeters
Typical VerSe: 1-3mm
More robust than Hausdorff
```

**Surgical relevance:** Boundary accuracy critical for surgical guidance; ensure <5mm for clinical application.

---

### 6.3 Per-Vertebra Anatomy Analysis

**For each vertebra in test set:**

| Vertebra | Count | Mean Dice | Std | Min | Max | Notes |
|----------|-------|-----------|-----|-----|-----|-------|
| C1 | 78 | 0.93 | 0.02 | 0.88 | 0.96 | Small vertebra |
| C2 | 79 | 0.93 | 0.02 | 0.89 | 0.96 | Odontoid challenging |
| ... | ... | ... | ... | ... | ... | ... |
| L5 | 65 | 0.87 | 0.05 | 0.74 | 0.94 | Transitional var |

**Insights:**
- Small vertebrae (C1, C2) often have higher Dice (less background confusion)
- Lower lumbar (L5) often lower (more anatomical variation)
- Identifies which vertebrae need targeted improvements

---

## 7. Implementation Timeline

### Week 1: Environment & Data Setup
- [ ] Clone repository
- [ ] Create Python virtual environment
- [ ] Install MONAI + dependencies
- [ ] Verify GPU availability
- [ ] Download VerSe 2020 dataset
- [ ] Validate data integrity
- [ ] Implement data loading pipeline

**Deliverable:** Working data pipeline; VerSe volumes load correctly

### Week 2-3: Training & Baseline
- [ ] Implement 3D U-Net (MONAI)
- [ ] Set up training loop
- [ ] Train on VerSe training set
- [ ] Implement evaluation metrics
- [ ] Generate test predictions
- [ ] Report per-vertebra Dice scores
- [ ] Analyze error cases

**Deliverable:** Phase 1 complete; Dice >0.88 on test set

### Week 3-4: Benchmarking
- [ ] Install and configure nnU-Net
- [ ] Run nnU-Net 5-fold cross-validation
- [ ] Generate comparison table (Phase 1 vs nnU-Net)
- [ ] Identify performance gap sources
- [ ] Document baseline selection

**Deliverable:** Phase 2 complete; baseline selection finalized

### Week 4-6 (Optional): Enhancement
- [ ] Implement Swin UNETR (if Phase 1-2 ahead of schedule)
- [ ] Cross-dataset validation on SPIDER
- [ ] Pathology-specific analysis
- [ ] Finalize architecture for future work

**Deliverable:** Enhanced model; validated generalization

---

## 8. Success Criteria & Acceptance

### 8.1 Phase 1 (3D U-Net) Success Criteria

| Criterion | Target | Actual | Status |
|-----------|--------|--------|--------|
| Dice (VerSe test) | >0.88 | - | PENDING |
| Per-vertebra Dice | Mean >0.87 | - | PENDING |
| Training stability | No divergence | - | PENDING |
| Inference speed | <60 sec/volume | - | PENDING |
| Code documentation | >80% docstrings | - | PENDING |
| Reproducibility | Same seed  same result | - | PENDING |

### 8.2 Phase 2 (nnU-Net) Success Criteria

| Criterion | Target | Actual | Status |
|-----------|--------|--------|--------|
| Dice (VerSe test) | 0.93-0.94 | - | PENDING |
| Performance gap (vs 3D U-Net) | <3% | - | PENDING |
| Cross-validation stability | Low variance | - | PENDING |
| Validates implementation quality | Gap  1-2% | - | PENDING |

### 8.3 Phase 3 (Swin UNETR) Success Criteria (Optional)

| Criterion | Target | Actual | Status |
|-----------|--------|--------|--------|
| Dice (VerSe test) | 0.93 | - | PENDING |
| Attention interpretability | Visualizable | - | PENDING |
| Cross-dataset Dice (SPIDER) | >0.88 | - | PENDING |

---

## 9. Known Risks & Mitigation

### Risk 1: Dataset Access Issues
**Likelihood:** Low (VerSe public)
**Mitigation:** Document download process; have backup datasets identified (CTSpine1K)

### Risk 2: GPU Memory Insufficient
**Likelihood:** Medium (depends on hardware)
**Mitigation:** Reduce batch size or patch size; use gradient checkpointing

### Risk 3: Training Instability / Divergence
**Likelihood:** Low (mature architecture)
**Mitigation:** Monitor loss curves; adjust learning rate or batch norm momentum

### Risk 4: Overfitting to VerSe
**Likelihood:** Medium (dataset relatively small)
**Mitigation:** Use augmentation heavily; validate on SPIDER; consider pretraining on CTSpine1K

### Risk 5: Pathological Cases (Fractures, Severe Degeneration)
**Likelihood:** High (present in VerSe)
**Mitigation:** Analyze per-case performance; document failure modes; plan targeted improvements

---

## 10. Related Documents

- [Literature Review](../literature/literature_review.md) - Research foundation
- [Dataset Benchmark](../datasets/dataset_benchmark.md) - Dataset rationale
- [Model Benchmark](./model_benchmark.md) - Architecture comparison
- [Dataset Registry](../datasets/dataset_registry.csv) - Data specifications

---

## 11. Decision Rationale Summary

### Why MONAI + 3D U-Net
1. **MONAI:** Flexibility for research + good medical imaging support
2. **3D U-Net:** Best balance of simplicity, performance, and interpretability for initial baseline

### Why VerSe + CTSpine1K
1. **VerSe:** Community standard; per-vertebra labels; pathology included
2. **CTSpike1K:** Proven pretraining boost; large scale

### Why multi-class segmentation
1. **Simplicity:** Single forward pass for both segmentation and labeling
2. **Efficiency:** No separate labeling network needed
3. **Standard:** Matches benchmark methodology

### Why sliding-window inference
1. **Flexibility:** Handles arbitrary volume sizes
2. **Efficiency:** Memory-effective; can process large volumes on modest GPUs
3. **Quality:** Overlapping patches smooth predictions

---

## Conclusion

This baseline selection represents a well-motivated, evidence-based approach to CT vertebral segmentation combining:

- **Research flexibility** (MONAI framework)
- **Strong baseline performance** (3D U-Net -> nnU-Net  Swin UNETR progression)
- **Community standards** (VerSe benchmark; multi-class approach)
- **Realistic timeline** (clear phases with deliverables)
- **Publication readiness** (nnU-Net reference; reproducible results)

Implementation proceeds with confidence that the selected approach is sound, well-researched, and positioned to achieve strong baseline results while maintaining flexibility for research innovations.

---

**Decision made:** September 7, 2026
**Status:** APPROVED - Ready for implementation
**Next milestone:** Environment setup + Phase 1 training begins
**Target completion:** Week 3-4 (baseline results)
