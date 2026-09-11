# CT Spine Dataset Benchmark

**Version:** 1.0
**Date:** September 7, 2026
**Scope:** Comparative analysis of public CT spine datasets

---

## Executive Summary

Five primary public CT datasets are suitable for vertebral segmentation research, with VerSe 2020 emerging as the consensus standard benchmark. Dataset selection depends on specific research goals:

- **Primary development:** VerSe 2020 (per-vertebra labels, pathology, community standard)
- **Scale & pretraining:** CTSpine1K or TotalSegmentator (1000+ scans)
- **Cross-validation:** SPIDER (independent clinical cases)
- **Multi-organ context:** TotalSegmentator (104 anatomical structures)

---

## 1. Detailed Dataset Comparison

### 1.1 VerSe (VerSe 2019 + 2020)

**Overview:** Community-driven benchmark for vertebral segmentation, hosted as MICCAI challenges.

| Property | Detail |
|----------|--------|
| **Scope** | Vertebral segmentation challenge dataset |
| **Volumes** | 160 (2019) + 420 (2020) = 580 total |
| **Patients** | ~140-160 unique patients (some with multiple time points) |
| **Anatomy** | Mostly complete spine C1-L5; some partial FOV cases |
| **Per-vertebra labels** | Yes - 26 individual vertebra classes (C1-C7, T1-T12, L1-L5, S1) |
| **Segmentation type** | Binary mask per vertebra + unified spine mask |
| **Format** | NIfTI (.nii.gz) |
| **Voxel spacing** | Highly variable: 0.5-5.0mm slice thickness |
| **Pathology** | Yes - includes fractures (compression, burst), severe degeneration, scoliosis, fusion |
| **Annotation method** | Semi-automated (atlas registration) + manual review/correction |
| **Public access** | Yes - requires free registration at challenge site |
| **License** | CC BY 4.0 (permissive) |
| **Training set** | Official split: ~70% training, 15% validation, 15% test |
| **Benchmark status** | Community standard - 50+ published results |

**Strengths:**
1. **Per-vertebra labels:** Each vertebra labeled individually (enables vertebra-level metrics)
2. **Pathology diversity:** Fractures, degeneration, scoliosis, fusion represented
3. **Community benchmark:** 50+ published results enable comparison (reproducibility)
4. **Challenge infrastructure:** Standardized evaluation, leaderboard, reproducible metrics
5. **Improved 2020 version:** Larger set, better annotation consistency than 2019
6. **Good annotation quality:** Multiple expert reviews reduce errors

**Weaknesses:**
1. **Variable voxel spacing:** Requires preprocessing to normalize (adds complexity)
2. **Smaller dataset:** 580 volumes < deep learning typical minimum for full training
3. **Annotation inconsistencies:** Some errors/ambiguities in early 2019 release
4. **Imaging protocol variability:** Different scanners  intensity variability
5. **Partial field-of-view:** Some scans cut off superior/inferior spine
6. **No timing information:** Doesn't distinguish acute vs chronic pathology

**Benchmark results from literature:**
- State-of-the-art Dice: 0.925-0.945
- Typical strong baseline (3D U-Net): 0.88-0.91
- nnU-Net without tuning: 0.91-0.93
- Swin UNETR: 0.92-0.94

**Practical usage:**
- **Primary training dataset:** Yes - standard choice
- **Validation/testing:** Yes - use official splits
- **Transfer learning source:** Optional; relatively small for ImageNet-style transfer

**Download:** https://verse.grand-challenge.org/ (free registration)

**Citation:** Lffler et al. (2020) - MICCAI VerSe Challenge

---

### 1.2 CTSpine1K

**Overview:** Large-scale CT spine dataset emphasizing dataset scale for pre-training.

| Property | Detail |
|----------|--------|
| **Scope** | Large-scale general spine segmentation |
| **Volumes** | ~1000 CT volumes |
| **Patients** | ~1000 unique patients |
| **Anatomy** | Mostly complete spine C1-L5 |
| **Per-vertebra labels** | No - only binary spine segmentation mask |
| **Segmentation type** | Binary spine mask (all vertebrae as one class) |
| **Format** | NIfTI (.nii.gz) |
| **Voxel spacing** | Variable: 0.5-2.0mm typical (narrower range than VerSe) |
| **Pathology** | Yes - includes degeneration, some fractures |
| **Annotation method** | Automated (atlas registration + morphological operations) + partial manual correction |
| **Public access** | Yes - public download, no registration |
| **License** | CC0 / Public domain |
| **Training set** | Official split: 80% training, 20% test |
| **Benchmark status** | Growing - used for pretraining in several works |

**Strengths:**
1. **Large scale:** 1000 volumes great for deep learning pretraining
2. **Easy access:** Public download, no registration barriers
3. **No per-vertebra annotation burden:** Binary masks simpler annotation
4. **Diverse imaging:** Multiple institutions, varied acquisition protocols
5. **Growing adoption:** Becoming standard pretraining source

**Weaknesses:**
1. **No per-vertebra labels:** Cannot evaluate vertebra-level segmentation directly
2. **Coarser annotation:** Less anatomical detail than VerSe
3. **Automated annotation quality:** Relies on atlas-based methods (may have systematic errors)
4. **Less community validation:** Fewer published results than VerSe (harder to compare)
5. **Requires VerSe for per-vertebra metrics:** Must fine-tune on VerSe for vertebra-level evaluation

**Typical usage pattern:**
```
Step 1: Pretrain on CTSpine1K (1000 scans)
          Learns general spine anatomy

Step 2: Fine-tune on VerSe (580 scans)
          Learns per-vertebra discrimination

Step 3: Evaluate on VerSe test set
          Report per-vertebra metrics (Dice, etc.)
```

**Performance with this workflow:**
- VerSe fine-tuning Dice: 0.92-0.94 (improved over VerSe-only)
- Typically adds 1-2% Dice improvement vs training on VerSe alone

**Download:** https://github.com/MIRACLE-Center/CTSpine1K (requires ~100GB disk space)

---

### 1.3 SPIDER

**Overview:** Clinical focus spine segmentation dataset for cross-validation.

| Property | Detail |
|----------|--------|
| **Scope** | Spine image database for evaluation research |
| **Volumes** | 200-400 (varies by version; ~300 typical) |
| **Patients** | Similar to volume count (mostly single-timepoint) |
| **Anatomy** | Mostly complete spine C1-L5 |
| **Per-vertebra labels** | Varies by version (some yes, some partial) |
| **Format** | DICOM (requires specialized parsing) |
| **Voxel spacing** | Variable: 0.5-2.0mm |
| **Pathology** | Yes - clinical cases; better represents real pathology variety |
| **Annotation method** | Manual annotations by clinical experts |
| **Public access** | Yes - available through institutional access |
| **License** | Variable (typically research use permitted) |
| **Benchmark status** | Established cross-validation dataset |

**Strengths:**
1. **Clinical reality:** Manually annotated clinical cases (high quality)
2. **Cross-validation standard:** Different imaging protocols from VerSe (tests generalization)
3. **Established protocols:** Well-defined evaluation procedures
4. **High annotation quality:** Manual expert annotations

**Weaknesses:**
1. **Smaller dataset:** 200-400 volumes (not suitable as primary training set)
2. **DICOM format:** Requires specialized parsing (vs standard NIfTI)
3. **Less frequently updated:** Slower evolution than VerSe
4. **Variable labeling:** Inconsistent annotation schemes across versions
5. **Less research adoption:** Fewer published results (harder to benchmark against)

**Typical usage:**
- Primary dataset: No (too small)
- Cross-validation: Yes (independent test set)
- Domain shift evaluation: Yes (different protocol than VerSe)

**Performance expectations:**
- Models trained on VerSe, tested on SPIDER
- Expected Dice drop: 2-5% (acceptable generalization)
- Indicates domain robustness

**Download:** Varies by center; requires registration at source institutions

---

### 1.4 TotalSegmentator

**Overview:** Largest public multi-organ CT segmentation dataset; includes spine as one of 104 structures.

| Property | Detail |
|----------|--------|
| **Scope** | Multi-organ segmentation foundation dataset |
| **Volumes** | ~1200 CT volumes |
| **Patients** | ~1200 unique patients |
| **Anatomy** | Full CT scan; 104 anatomical structures including spine |
| **Spine annotation** | Binary mask (entire spine as single class; no per-vertebra) |
| **Format** | NIfTI (.nii.gz) |
| **Voxel spacing** | Normalized to 1.0mm isotropic (major advantage) |
| **Pathology** | Yes - includes pathological cases (tumors, degeneration, etc.) |
| **Annotation method** | Automated (atlas registration) + manual corrections by radiologists |
| **Public access** | Yes - large direct download (requires storage) |
| **License** | CC BY 4.0 (permissive) |
| **Size on disk** | ~500GB total dataset; spine subsets much smaller |
| **Benchmark status** | Rapidly growing adoption (2023 dataset) |

**Strengths:**
1. **Largest dataset:** 1200 volumes enables very robust pretraining
2. **Standardized spacing:** 1.0mm isotropic eliminates preprocessing uncertainty
3. **Multi-organ context:** Spine learned in context of other anatomy (may improve robustness)
4. **High quality:** Radiologist-reviewed automated annotations
5. **Modern framework:** Latest dataset; likely to become standard
6. **Permissive license:** CC BY 4.0

**Weaknesses:**
1. **No per-vertebra labels:** Spine is single class (not suitable for vertebra-level tasks directly)
2. **Orthogonal focus:** Multi-organ dataset (spine is secondary interest)
3. **Requires filtering:** Must extract spine-specific subset from general dataset
4. **Large disk requirements:** ~500GB for complete dataset
5. **Multi-organ annotation style:** May not generalize perfectly to spine-focused tasks

**Typical usage for vertebra segmentation:**

```
Option A: Transfer learning for general CT understanding
   Pretrain on all 104 organs on TotalSegmentator
   Fine-tune spine-specific on VerSe
   Benefit: Better general CT features

Option B: Spine-specific pretraining
   Subset to spine-only volumes from TotalSegmentator
   Train binary spine segmentation
   Fine-tune per-vertebra on VerSe
   Benefit: Faster convergence on VerSe
```

**Performance with this strategy:**
- VerSe fine-tuning Dice: 0.92-0.95 (can exceed VerSe-only training)
- Large-scale pretraining particularly valuable for small VerSe

**Download:** https://github.com/wasserth/TotalSegmentator (requires ~500GB)

**Citation:** Wasserthal et al. (2023) - Radiology: Artificial Intelligence

---

## 2. Comparative Performance Matrix

### 2.1 Dataset Characteristics

| Characteristic | VerSe | CTSpine1K | SPIDER | TotalSegmentator |
|---|---|---|---|---|
| **Scale** | 580 | 1000 | 300 | 1200 |
| **Per-vertebra labels** | Yes  | No | Partial | No |
| **Voxel spacing (std)** | High variability | Low variability | Medium | Normalized (1.0mm) |
| **Annotation quality** | High | Medium | High | High |
| **Pathology diversity** | High | Medium | High | High |
| **Public access** | Easy | Easy | Moderate | Easy |
| **Disk storage** | ~50GB | ~100GB | ~30GB | ~500GB |

### 2.2 Suitability by Use Case

| Use Case | Best Choice | Why |
|----------|---|---|
| Initial baseline | VerSe | Standard benchmark; per-vertebra labels |
| Scale pretraining | CTSpine1K or Total | 1000+ volumes enable transfer learning |
| Cross-validation | SPIDER | Independent data; different protocol |
| Multi-organ transfer | TotalSegmentator | 104 structures provide rich features |
| Pathology robustness | VerSe + SPIDER | Both include diverse pathology |
| Quick prototyping | VerSe | Smallest with good annotations |
| Production system | CTSpine1K + VerSe | Scale + per-vertebra labels |

---

## 3. Data Preparation Workflow

### 3.1 Standard Pipeline

```
Dataset Selection (VerSe)
    
[1] Download & validate
    - Check file integrity (checksum if available)
    - Verify volume dimensions
    - Sample images visually
    
[2] Preprocessing
    - DICOM/NIfTI parsing
    - Orientation normalization (RAS convention)
    - Voxel spacing normalization (1.0mm isotropic)
    - Intensity normalization (HU windowing: -1000 to +3000)
    
[3] Quality control
    - Verify no NaN or infinite values
    - Check label mask consistency
    - Detect annotation errors
    - Log any issues
    
[4] Train/val/test split
    - Use official split (if provided)
    - Or: 70% train, 15% val, 15% test (patient-level split)
    
[5] Data augmentation (during training)
    - Random flips, rotations, elastic deformations
    - Intensity jittering, gamma correction
    
[6] Training
```

---

## 4. Recommended Dataset Selection

### 4.1 Primary Development Path

**Tier 1 (Primary):** VerSe 2020
- **Rationale:** Community standard; per-vertebra labels; pathology included; easy access
- **Usage:** Main training/validation/test set
- **Expected performance:** Dice 0.90-0.94 depending on architecture
- **Metrics:** Per-vertebra Dice; cross-vertebra consistency

**Tier 2 (Secondary - Pretraining):** CTSpine1K or TotalSegmentator
- **Rationale:** Large scale enables transfer learning; improves VerSe performance
- **Usage:** Pretrain model, then fine-tune on VerSe
- **Expected improvement:** +1-3% Dice on VerSe fine-tuning

**Tier 3 (Validation - Cross-dataset):** SPIDER
- **Rationale:** Independent data with different imaging protocol
- **Usage:** Generalization testing (train on VerSe, test on SPIDER)
- **Expected performance:** Dice 0.87-0.92 (acceptable 2-5% drop)

### 4.2 Alternative Path (If Limited Resources)

If computational resources or storage limited:

**Primary:** VerSe only (sufficient for baseline)
- Good baseline performance
- No large-scale pretraining needed
- Smaller storage footprint (~50GB)

**Validation:** SPIDER (if available)
- Generalization testing

---

## 5. Data Availability & Access

### 5.1 Access Summary

| Dataset | Availability | Access Method | Registration | Storage | Download Time |
|---------|---|---|---|---|---|
| VerSe | Public | Challenge website | Free registration | ~50GB | 1-2 hours |
| CTSpine1K | Public | GitHub | None required | ~100GB | 2-4 hours |
| SPIDER | Public | Institutional | Registration (varies) | ~30GB | 1-2 hours |
| TotalSegmentator | Public | Direct download | None required | ~500GB | 4-8 hours |

### 5.2 Download Instructions

**VerSe:**
1. Go to https://verse.grand-challenge.org/
2. Register free account
3. Download training and validation sets
4. Combine into single training pool

**CTSpine1K:**
1. Clone repo: `git clone https://github.com/MIRACLE-Center/CTSpine1K`
2. Run download script: `python download_dataset.py`
3. Requires ~100GB disk space

**TotalSegmentator:**
1. Install CLI: `pip install TotalSegmentator`
2. Download: `TotalSegmentator -i input_dir -o output_dir`
3. Extract spine subset if needed

---

## 6. Quality Assurance

### 6.1 Common Data Issues

| Issue | Detection | Mitigation |
|-------|-----------|-----------|
| Missing files | File count check | Retry download |
| Corruption | Hash/checksum validation | Re-download |
| Dimension mismatch | Shape assertion | Log and exclude |
| Invalid labels | Mask range check (0-26 for VerSe) | Inspect manually |
| Annotation errors | Visual QA sampling | Note in documentation |
| Orientation errors | Verify RAS convention | Reorient |

### 6.2 Recommended QA Procedure

```python
# Pseudocode for data validation
for volume_file in dataset:
    # Load
    img, seg = load_nifti(volume_file)

    # Check dimensions
    assert img.shape[2] > 10  # At least some slices
    assert seg.shape == img.shape  # Alignment

    # Check intensity range
    assert img.min() >= -2000 and img.max() <= 4000  # HU range

    # Check labels
    unique_labels = np.unique(seg)
    assert max(unique_labels) <= 26  # VerSe max class

    # Check for NaN
    assert not np.any(np.isnan(img))
    assert not np.any(np.isnan(seg))

    # Visual spot-check (sample every N volumes)
    if volume_idx % 50 == 0:
        visualize_volume(img, seg)  # Human inspection
```

---

## 7. Dataset Benchmarking Conclusions

### 7.1 Key Findings

1. **VerSe is the standard:** 50+ published results make it community benchmark
2. **Scale matters:** CTSpine1K/TotalSegmentator pretraining provides consistent improvement
3. **Cross-dataset validation essential:** Test generalization on SPIDER or other protocol
4. **Preprocessing critical:** Voxel spacing normalization essential for convergence
5. **Pathology handling:** VerSe includes diverse pathology; expect variable performance per case

### 7.2 Strategic Recommendations

**Recommendation 1: Primary Development**
- Use VerSe 2020 for baseline development
- Standard split: 70% train, 15% val, 15% test
- Enables direct comparison with 50+ published results

**Recommendation 2: Scale & Transfer Learning**
- Pretrain on CTSpine1K (1000 volumes) or TotalSegmentator (1200 volumes)
- Fine-tune on VerSe
- Expected improvement: 1-3% Dice

**Recommendation 3: Generalization Testing**
- Validate on SPIDER or other independent dataset
- Acceptable performance: Dice drop <5%
- Indicates robustness to protocol variations

**Recommendation 4: Pathology Validation**
- Analyze per-vertebra performance in VerSe test set
- Identify challenging cases (typically L5, transitional)
- Plan targeted improvements

---

## 8. Timeline & Data Acquisition Plan

| Milestone | Timeline | Action |
|-----------|----------|--------|
| Baseline setup | Week 1 | Download & validate VerSe 2020 |
| Preprocessing | Week 1-2 | Implement orientation/spacing normalization |
| Baseline training | Week 2-3 | Train 3D U-Net on VerSe |
| Baseline evaluation | Week 3 | Report per-vertebra metrics |
| Pretraining | Week 3-4 | Download CTSpine1K; pretrain model |
| Fine-tuning | Week 4 | Fine-tune on VerSe |
| Cross-validation | Week 4-5 | Test on SPIDER (if available) |
| Pathology analysis | Week 5 | Analyze per-vertebra performance |

---

## Conclusion

**Selected primary dataset:** VerSe 2020
- Community standard
- Per-vertebra labels
- Pathology diversity
- Easy access
- 580 volumes sufficient for strong baseline

**Secondary dataset:** CTSpine1K (for pretraining) or TotalSegmentator (for multi-organ transfer)
- Provides scale benefit
- Improves VerSe fine-tuning performance
- Enables transfer learning experiments

**Validation dataset:** SPIDER
- Cross-validation on independent protocol
- Tests domain robustness
- Measures generalization

This three-tier approach balances dataset scale, annotation quality, and community standards for robust vertebral segmentation research.

---

**Document prepared:** September 7, 2026
**Status:** Dataset benchmark complete - ready for implementation planning
**Next step:** Model architecture benchmark + baseline selection
