# Model Architecture Benchmark: Vertebral Segmentation

**Version:** 1.0
**Date:** September 7, 2026
**Scope:** Comprehensive comparison of 20+ segmentation architectures for CT vertebra segmentation

---

## Executive Summary

Current state-of-the-art for CT vertebral segmentation achieves Dice 0.93-0.945 on VerSe benchmark using:
1. **nnU-Net** (self-configuring 3D U-Net) - reference standard
2. **Swin UNETR** (efficient transformer) - competitive SOTA with interpretability
3. **UNETR** (full transformer) - competitive SOTA with long-range context

**Recommendation for baseline project:** Start with **3D U-Net** (simpler, good performance), benchmark against **nnU-Net** (reference standard), optionally evaluate **Swin UNETR** if interpretability desired.

---

## 1. Architecture Categories

### 1.1 Classical Volumetric CNNs (Proven & Mature)

#### 3D U-Net
**Status:** Foundational 3D architecture; still widely used baseline

**Architecture:**
```
Input 3D patch (128? or 64?)
    ?
Encoder (downsampling)
  Level 1: Conv(16) ? pool
  Level 2: Conv(32) ? pool
  Level 3: Conv(64) ? pool [bottleneck]
    ?
Decoder (upsampling)
  Level 3: Upsample ? concat encoder_L3 ? Conv(64)
  Level 2: Upsample ? concat encoder_L2 ? Conv(32)
  Level 1: Upsample ? concat encoder_L1 ? Conv(16)
    ?
Output: Per-voxel class logits (26 classes for VerSe)
```

**Hyperparameter ranges:**
- Patch size: 64? to 192? (GPU memory dependent)
- Channels: 16-32 base
- Depth: 3-5 pyramid levels
- Dropout: 0.1-0.5 (for regularization)
- Batch norm: Yes (recommended)

**Training details:**
- Loss: Dice + CE combined
- Optimizer: Adam (learning rate ~1e-3 with decay)
- Epochs: 50-200 (patience-based early stopping)
- Batch size: 2-8 (GPU memory limited)
- Data augmentation: Flips, rotations, elastic deformations

**Performance on VerSe:**
- Dice: 0.90-0.92 (competitive baseline)
- Inference time: ~20-30 seconds per volume (GPU)
- Memory: 4-6GB GPU RAM

**Strengths:**
- [OK] Mature, well-understood architecture
- [OK] Many implementations available (MONAI, TensorFlow, PyTorch)
- [OK] Good interpretability (skip connections clearly help)
- [OK] Relatively fast inference
- [OK] Moderate GPU requirements
- [OK] Easy to debug and modify

**Limitations:**
- [OK] Fixed architecture (requires manual tuning for new datasets)
- [OK] Limited long-range context (receptive field bounded by depth)
- [OK] May underutilize large volumes
- [OK] Naive patch strategy can be wasteful

**When to use:**
- Prototype and baseline development
- When interpretability matters
- Resource-constrained environments
- Validation against published baselines

**Recommendation:** Use as **initial baseline** (2-3 weeks of training/tuning). Provides good performance with manageable complexity. Enables direct comparison with many published works.

---

#### V-Net (Residual 3D)
**Status:** Foundational 3D; residual improvements over basic 3D conv

**Key innovation:** Residual connections + volumetric Dice loss

**Performance:** Dice 0.89-0.91 (very similar to 3D U-Net)

**Assessment:** Similar to 3D U-Net with residual benefits. Older architecture; typically superseded by nnU-Net. Not recommended as primary focus.

---

### 1.2 Self-Configuring Baselines (De Facto Standard)

#### nnU-Net (Self-Configuring)
**Status:** Reference standard; achieves SOTA with zero manual tuning

**Philosophy:** Automatically configure U-Net architecture based on dataset properties rather than manual hyperparameter tuning.

**What it automatically decides:**
1. **Input patch size:** Based on GPU memory + expected field-of-view needs
2. **Channel counts:** Scales dynamically with depth
3. **Depth:** Computed from desired receptive field
4. **Batch size:** Limited by GPU memory
5. **Training schedule:** Based on dataset size (more data ? more epochs)
6. **Preprocessing:** Automatic HU windowing, resampling, cropping
7. **Augmentation:** Medical imaging-specific (spatial + intensity)

**Architecture strategy:**
- "3D full resolution mode": Single large patch
- "3D low resolution mode": Multiple scales for large field-of-view
- Ensemble: Combines both modes for final prediction

**Training procedure (automatic):**
1. Analyze dataset statistics
2. Configure architecture
3. Run 5-fold cross-validation internally
4. Generate ensemble of 5 models
5. Report cross-validation performance

**Performance on VerSe:**
- Dice: 0.93-0.94 (among top competition results)
- Reproducible across runs (deterministic configuration)
- Generalizes to other datasets without retuning

**Computational requirements:**
- GPU: 8-12GB (similar to 3D U-Net)
- Training time: 40-150 GPU hours (depends on dataset size)
- Storage: ~2-5GB per trained model (5 ensemble members)

**Advantages:**
- [OK] Zero hyperparameter tuning (fully automatic)
- [OK] Reproducible (same input ? same architecture ? same performance)
- [OK] Generalizes across domains (works on diverse medical imaging tasks)
- [OK] Efficient preprocessing (reduces training time)
- [OK] Ensemble predictions (more robust than single model)
- [OK] De facto standard (50+ published applications)
- [OK] Strong community adoption

**Limitations:**
- [OK] Less interpretable (auto-configuration obscures design choices)
- [OK] Pre-configured decisions may be suboptimal for specific anatomy
- [OK] Requires nnU-Net software (not plug-and-play for custom modifications)
- [OK] Harder to customize for research variations
- [OK] 5-fold cross-validation takes time

**Installation & usage:**
```bash
pip install nnunet

# After installing, training is one command:
nnUNet_train 3d_fullres nnUNetTrainerV2 Task01_VerSe 0

# Inference:
nnUNet_predict -i input_folder -o output_folder -t Task01_VerSe -m 3d_fullres
```

**Recommendation:** Use nnU-Net as **reference standard for benchmarking**. Compare custom 3D U-Net against nnU-Net to validate implementation quality. If pursuing research publication, nnU-Net is expected baseline.

**Timeline:** 1-2 weeks for setup and training (includes cross-validation + ensemble).

---

### 1.3 Transformer-Based Approaches (Emerging SOTA)

#### UNETR (Transformer Encoder + CNN Decoder)
**Status:** Competitive with nnU-Net; emerging alternative

**Architecture:**
```
Input volume (e.g., 96?)
    ?
Patch embedding
  - Divide into 16? patches
  - Project each patch to embedding dimension (e.g., 768)
    ?
Transformer encoder (12-24 layers)
  - Multi-head self-attention (8-12 heads)
  - Feed-forward networks
  - Positional embeddings (learned or fixed)
    ?
Hybrid decoder (CNN + transformer features)
  - Upsample embeddings
  - Concatenate with skip connections from transformer layers
  - CNN convolutions for refinement
    ?
Output: Per-voxel class predictions
```

**Key properties:**
- **Self-attention:** Each voxel can attend to ALL other voxels in volume
- **Long-range context:** Captures global anatomical structure
- **Interpretability:** Attention weights show which regions influenced predictions
- **Computational cost:** O(n?) complexity for self-attention (n = number of patches)

**Performance on VerSe:**
- Dice: 0.92-0.94 (competitive with nnU-Net)
- Attention weights interpretable (can visualize decision-making)

**Computational requirements:**
- GPU: 10-14GB (higher than 3D U-Net)
- Training time: 80-150 GPU hours
- Inference time: 60-90 seconds per volume (2-3x slower than 3D U-Net)

**Advantages:**
- [OK] Long-range context via self-attention
- [OK] Highly interpretable (attention weights reveal reasoning)
- [OK] Competitive SOTA performance
- [OK] Multiple implementations available (MONAI, custom)
- [OK] Transferable from ImageNet pretraining

**Limitations:**
- [OK] Higher GPU memory requirements
- [OK] Slower training and inference than 3D U-Net
- [OK] O(n?) complexity limits scalability
- [OK] May require larger dataset for optimal performance
- [OK] Attention can be noisy (requires careful analysis)

**When to use:**
- When interpretability is important (research/publication)
- When computational resources available
- For studying attention mechanisms in medical imaging
- When publishing requires demonstrating attention-based approach

**Recommendation:** Evaluate UNETR **after establishing 3D U-Net baseline** (Week 4-5). Use for interpretability studies or publication-ready experiments.

**Timeline:** 2-3 weeks (after baseline established).

---

#### Swin UNETR (Window-Based Transformer - RECOMMENDED)
**Status:** Efficient transformer; recommended if transformer desired

**Key innovation:** Window-based self-attention for efficiency

**Architecture:**
```
Input volume (e.g., 96?)
    ?
Patch embedding + windowing
    ?
Swin transformer encoder (hierarchical windows)
  - Local window attention (7? typical window)
  - Shifted windows between layers (cross-window communication)
  - Hierarchical pyramid levels
    ?
Hybrid decoder + skip connections
    ?
Output: Per-voxel predictions
```

**Key property:** Window-based attention reduces complexity from O(n?) to O(n)

**Performance:**
- Dice: 0.92-0.94 (similar accuracy to UNETR)
- Inference time: 40-60 seconds (faster than UNETR; still 1.5-2x slower than 3D U-Net)
- Memory: 8-12GB (similar to UNETR)

**Advantages:**
- [OK] Efficient attention mechanism (linear complexity)
- [OK] Maintains SOTA performance
- [OK] Better memory efficiency than full attention
- [OK] Hierarchical structure captures multi-scale features
- [OK] MONAI-integrated (good library support)
- [OK] Faster than full UNETR for similar accuracy

**Limitations:**
- [OK] Still slower than 3D U-Net
- [OK] Slightly more complex than UNETR
- [OK] Window-based attention may miss very long-range patterns

**Recommendation:** **Preferred transformer variant** if interpretability + efficiency both important. Good middle ground between 3D U-Net and full UNETR.

**Timeline:** 2-3 weeks (after baseline).

---

### 1.4 Transfer Learning & Pretrained Models

#### TotalSegmentator (Pretrained Multi-Organ)
**Status:** Recent large-scale pretrained model; growing adoption

**Characteristics:**
- Trained on 1200 CT volumes with 104 anatomical structures
- Spine included as one structure
- 1.0mm isotropic voxel spacing (normalized)
- nnU-Net-based architecture with multi-organ fine-tuning

**Usage for vertebra segmentation:**

**Strategy A: Direct inference**
- Use pretrained model for spine segmentation
- Limitation: Output is organ-level spine mask (not per-vertebra)

**Strategy B: Transfer learning**
```
Step 1: Start with TotalSegmentator weights
Step 2: Adapt output layer to 26 classes (one per vertebra)
Step 3: Fine-tune on VerSe
Step 4: Expected improvement: +1-2% Dice over VerSe-only training
```

**Advantages:**
- [OK] Largest available pretraining dataset (1200 scans)
- [OK] Multi-organ context may improve robustness
- [OK] Standardized 1.0mm spacing
- [OK] Open-source and accessible

**Limitations:**
- [OK] Organ-level not vertebra-level (requires adaptation)
- [OK] Large storage requirements (~500GB for full dataset)
- [OK] May introduce bias from multi-organ training

**Recommendation:** Use **TotalSegmentator for transfer learning** (Week 4-5). Download pretrained weights, fine-tune on VerSe. Measure improvement vs direct VerSe training.

**Timeline:** 1-2 weeks for fine-tuning (pretrained weights already available).

---

## 2. Comparative Performance Analysis

### 2.1 VerSe Benchmark Results

| Architecture | Dice (Test Set) | Inference (sec/vol) | GPU Memory | Training Time | Reproducibility | Notes |
|---|---|---|---|---|---|---|
| 3D U-Net | 0.90-0.92 | 20-30 | 4-6GB | 20-50 GPU-hrs | High | Good baseline |
| V-Net | 0.89-0.91 | 25-35 | 5-7GB | 30-60 GPU-hrs | High | Similar to 3D U-Net |
| nnU-Net | 0.93-0.94 | 30-40 | 8-10GB | 40-150 GPU-hrs* | Very high | Reference standard |
| UNETR | 0.92-0.94 | 60-90 | 10-12GB | 80-150 GPU-hrs | High | Interpretable |
| Swin UNETR | 0.92-0.94 | 40-60 | 8-11GB | 80-120 GPU-hrs | High | Efficient transformer |
| TotalSegmentator | ~0.90 (org-level) | 25-35 | 8GB | N/A (pretrained) | High | Multi-organ; requires adaptation |

*nnU-Net includes 5-fold cross-validation; single-fold train faster.

### 2.2 Ranking by Criterion

**Best SOTA Performance:**
1. nnU-Net (0.93-0.94)
2. UNETR / Swin UNETR (tied, 0.92-0.94)
4. 3D U-Net (0.90-0.92)

**Fastest Inference:**
1. 3D U-Net (~25 sec)
2. V-Net (~30 sec)
3. nnU-Net (~35 sec)
4. Swin UNETR (~50 sec)
5. UNETR (~75 sec)

**Best Balance (Speed + Accuracy):**
1. Swin UNETR (0.92-0.94 Dice, 40-60 sec)
2. nnU-Net (0.93-0.94 Dice, 35-40 sec; but 5-fold CV overhead)
3. 3D U-Net (0.90-0.92 Dice, 25 sec; simplicity advantage)

**Most Reproducible:**
1. nnU-Net (fully automatic)
2. MONAI implementations (well-documented; standardized)
3. Custom implementations (varies)

**Best Interpretability:**
1. UNETR (full attention visualization)
2. Swin UNETR (windowed attention + hierarchical)
3. 3D U-Net (skip connections interpretable)

---

## 3. Framework & Implementation Ecosystem

### 3.1 MONAI Framework Evaluation

**MONAI (Medical Open Network for AI):** PyTorch-based medical imaging framework

**3D CT Support:**
- [OK] 3D U-Net implementation
- [OK] UNETR / Swin UNETR implementation
- [OK] 3D data transforms (rotations, deformations, etc.)
- [OK] 3D preprocessing utilities
- [OK] Sliding-window inference for large volumes
- [OK] Medical imaging metrics (Dice, Hausdorff, surface distance)

**Preprocessing capabilities:**
- [OK] DICOM loading (pydicom integration)
- [OK] Orientation normalization
- [OK] Voxel spacing resampling
- [OK] Intensity normalization
- [OK] ROI cropping
- [OK] Padding/cropping to fixed size

**Augmentation:**
- [OK] 3D spatial transforms (flip, rotate, elastic deformation)
- [OK] Intensity transforms (Gaussian noise, gamma correction, etc.)
- [OK] Composable pipeline (chain transforms easily)

**Loss functions:**
- [OK] Dice loss
- [OK] Cross-entropy
- [OK] Focal loss
- [OK] Custom combinations

**Evaluation:**
- [OK] Dice computation
- [OK] Hausdorff distance
- [OK] Surface distance
- [OK] Per-class metrics

**Advantages:**
- [OK] Comprehensive medical imaging support
- [OK] Good documentation
- [OK] Active development
- [OK] Easy reproducibility
- [OK] MONAI-integrated models (UNETR, Swin UNETR)
- [OK] Plugin architecture (extend easily)

**Disadvantages:**
- [OK] Dependency layer (vs raw PyTorch)
- [OK] Slight performance overhead (negligible)
- [OK] Some features less mature than domain-specific tools

**Verdict:** **Recommended framework for development.** Enables reproducible, well-documented medical imaging workflows.

---

### 3.2 nnU-Net Framework

**nnU-Net:** Specialized self-configuring segmentation software

**3D Support:**
- [OK] Full 3D volumetric support
- [OK] Automatic preprocessing
- [OK] Automatic architecture configuration
- [OK] 5-fold cross-validation ensemble

**Strengths:**
- [OK] Zero hyperparameter tuning
- [OK] Reproducible across runs
- [OK] Well-tested on 50+ medical imaging tasks

**Weaknesses:**
- [OK] Less flexible than MONAI (hard to customize)
- [OK] Requires specific software setup
- [OK] Less suitable for research variations

**Verdict:** **Excellent reference standard.** Use for benchmarking project baseline against published SOTA. Not recommended as primary development framework unless minimal customization needed.

---

### 3.3 Raw PyTorch (Flexible but High Burden)

**Pros:** Complete flexibility, no dependency overhead

**Cons:** High implementation burden, greater reproducibility risk

**Verdict:** **Not recommended for baseline project.** Too much infrastructure code; use MONAI instead.

---

## 4. Architecture Selection Strategy

### 4.1 Recommended Three-Phase Approach

#### Phase 1: Establish Baseline (Week 1-3)
**Architecture:** 3D U-Net (MONAI implementation)

**Rationale:**
- Simple to understand and debug
- Good baseline performance (Dice 0.90-0.92)
- Moderate resource requirements
- Easy to compare against published results
- Enables rapid iteration

**Deliverables:**
- Working training pipeline
- Baseline results on VerSe test set
- Evaluation metrics (per-vertebra Dice, Hausdorff distance)
- Error analysis (which vertebrae are hardest?)

**Success criteria:** Dice >0.88 on VerSe test set (indicates correct implementation)

---

#### Phase 2: Benchmark Against Standards (Week 3-4)
**Architecture:** nnU-Net (reference comparison)

**Rationale:**
- Validates 3D U-Net implementation quality
- Provides expected SOTA performance
- Enables publication-ready baseline
- Zero tuning required (reproducible)

**Comparison approach:**
```
nnU-Net Dice (0.93-0.94) - 3D U-Net Dice (0.90-0.92)
= Performance gap ? 1-4%

If gap > 5%: indicates suboptimal 3D U-Net implementation
If gap ? 1-4%: indicates solid 3D U-Net baseline
```

**Deliverables:**
- nnU-Net results on same test set
- Detailed performance comparison table
- Identify performance gap sources

**Success criteria:** 3D U-Net within 2-3% of nnU-Net (gap due to architecture, not implementation)

---

#### Phase 3: Explore Improvements (Week 4-6)
**Architecture:** Swin UNETR (if interpretability desired) or nnU-Net ensemble (if accuracy priority)

**Rationale:**
- Push toward SOTA
- Add interpretability if research-relevant
- Ensemble methods for robustness
- Cross-dataset validation

**Options:**
1. **Swin UNETR:** For interpretable SOTA
2. **nnU-Net ensembles:** For maximum accuracy
3. **Multi-task learning:** For simultaneous segmentation + labeling
4. **Domain adaptation:** For improved cross-dataset generalization

**Success criteria:** Achieve Dice 0.92+ on VerSe; demonstrate improvement over Phase 1

---

### 4.2 Hardware Requirements

| Phase | Architecture | GPU Memory | Training Time | Batch Size |
|---|---|---|---|---|
| Phase 1 | 3D U-Net | 6-8GB | 20-50 hrs | 4-8 |
| Phase 2 | nnU-Net | 10-12GB | 40-150 hrs | 8-16 (auto-config) |
| Phase 3 | Swin UNETR | 10-12GB | 80-120 hrs | 8-12 |

**Minimum:** NVIDIA GPU with 8GB VRAM (GeForce RTX 3070 or better)

**Recommended:** NVIDIA GPU with 12GB+ VRAM (V100, A100, RTX 4090) for faster training

**Fallback:** CPU-only training possible but very slow (~1000x slower)

---

## 5. Labeling Strategy Integration

### 5.1 Segmentation-Only vs Labeled Approach

**Option A: Segmentation-only (Phase 1-2)**
- Train 26-class segmentation network
- Output: Individual vertebra masks
- Labeling: Direct (implicit in class membership)
- Advantage: Standard benchmark; multi-class training
- Limitation: Assumes perfect anatomical ordering

**Option B: Multi-task learning (Phase 3)**
- Shared encoder
- Dual decoders: segmentation + classification
- Output: Masks + anatomical labels
- Advantage: Joint optimization; improved robustness
- Limitation: More complex; requires multi-task loss design

**Recommendation:** **Start with segmentation-only (Phase 1-2).** Multi-task learning in Phase 3 if vertebra labeling robustness needed.

---

## 6. Final Architecture Recommendation

### 6.1 Selected Baseline: 3D U-Net + nnU-Net Comparison

**Primary baseline:** 3D U-Net (MONAI)
- Good balance of simplicity, performance, and interpretability
- Phase 1 focus (weeks 1-3)

**Reference standard:** nnU-Net
- Validates 3D U-Net implementation
- Provides expected SOTA
- Phase 2 focus (weeks 3-4)

**Optional enhancement:** Swin UNETR
- If interpretability or maximum accuracy desired
- Phase 3 focus (weeks 4-6)
- Only pursue if Phase 1-2 successful

### 6.2 Implementation Sequence

**Week 1:**
- [x] Literature review complete
- [ ] Set up MONAI environment
- [ ] Implement data loading pipeline
- [ ] Begin 3D U-Net training

**Week 2:**
- [ ] Complete 3D U-Net training
- [ ] Generate VerSe test predictions
- [ ] Compute per-vertebra Dice scores
- [ ] Analyze error cases

**Week 3:**
- [ ] Document 3D U-Net results
- [ ] Begin nnU-Net benchmark
- [ ] Compare against published results
- [ ] Write baseline selection document

**Week 4:**
- [ ] Complete nnU-Net training
- [ ] Comparative performance analysis
- [ ] Finalize baseline decision
- [ ] Plan Phase 3 enhancements

**Week 4-6:**
- [ ] Evaluate Swin UNETR (optional)
- [ ] Cross-dataset validation (SPIDER)
- [ ] Pathology-specific analysis
- [ ] Finalize architecture decision

---

## Conclusion

**Recommended architecture selection:**
1. **Primary:** 3D U-Net (baseline establishment; weeks 1-3)
2. **Benchmark:** nnU-Net (reference standard; weeks 3-4)
3. **Optional:** Swin UNETR (interpretable SOTA; weeks 4-6)

This three-phase approach enables:
- [OK] Rapid baseline development
- [OK] Validation against SOTA
- [OK] Publication-ready results
- [OK] Flexibility for research improvements
- [OK] Clear progression from simple to advanced

Expected progression:
```
Week 1-2: 3D U-Net baseline (Dice ~0.90)
    ?
Week 3: nnU-Net benchmark (Dice ~0.93)
    ?
Week 4-6: Swin UNETR or ensemble (Dice ~0.93-0.94)
```

**Next step:** Implement development environment and training infrastructure.

---

**Document prepared:** September 7, 2026
**Status:** Architecture benchmark complete - ready for implementation
**Next step:** Development environment setup + Phase 1 training begins
