# Biomedical Imaging Research: Vertebral Segmentation & Surgical Navigation

A comprehensive research project on CT-based vertebral segmentation/labeling and surgical navigation system analysis.

## Project Overview

This repository contains foundational research for two parallel workstreams:

### **Project 1: CT Vertebral Segmentation & Anatomical Labeling**
Development of automated methods for:
- **Vertebral segmentation**: Detecting which voxels belong to each vertebra
- **Instance separation**: Distinguishing adjacent vertebrae as individual anatomical units
- **Vertebral labeling**: Assigning anatomical identities (C1-C7, T1-T12, L1-L5)

Clinical relevance: Supporting surgical navigation, preoperative planning, and automated clinical assessment.

### **Project 2: Surgical Navigation Competitive Analysis**
Detailed technical and competitive analysis of spine/surgical navigation systems:
- StealthStation (Medtronic)
- ExcelsiusGPS (Globus Medical)
- Stryker navigation platforms
- Brainlab systems
- 7D Surgical platforms

Focus: Imaging, registration, tracking, planning, and robotic guidance workflows.

## Project Status

| Component | Status |
|-----------|--------|
| Repository initialization | [OK] COMPLETE |
| Literature review | IN PROGRESS |
| Dataset benchmark | IN PROGRESS |
| Model architecture benchmark | IN PROGRESS |
| MONAI framework evaluation | IN PROGRESS |
| Baseline model selection | PENDING |
| Development environment | PENDING |
| CT preprocessing pipeline | PLANNED |
| Dataset interface | PLANNED |
| Inference framework | PLANNED |
| Evaluation metrics | PLANNED |
| Quantitative experiments | PENDING |
| Competitor analysis | IN PROGRESS |
| Navigation workflow mapping | PLANNED |
| Instrument taxonomy | PLANNED |
| Technical opportunity analysis | PLANNED |

## Repository Structure

```
.
??? README.md                          # This file
??? PROJECT_STATUS.md                  # Detailed status tracking
??? CHECKIN_SUMMARY.md                 # Project check-in summary
??? ROADMAP.md                         # Development roadmap
??? requirements.txt                   # Python dependencies
??? environment.yml                    # Conda environment spec
??? pyproject.toml                     # Project configuration
?
??? project1_vertebra_segmentation/
?   ??? literature/
?   ?   ??? literature_review.md       # Comprehensive literature review
?   ?   ??? papers.csv                 # Database of reviewed papers
?   ?   ??? key_papers/                # Important paper summaries
?   ?
?   ??? datasets/
?   ?   ??? dataset_registry.csv       # Registry of available datasets
?   ?   ??? dataset_benchmark.md       # Dataset comparison analysis
?   ?   ??? dataset_selection.md       # Primary/secondary dataset rationale
?   ?
?   ??? models/
?   ?   ??? model_benchmark.md         # Model architecture comparison
?   ?   ??? model_comparison.csv       # Detailed model specs
?   ?   ??? baseline_selection.md      # Selected baseline rationale
?   ?
?   ??? src/
?   ?   ??? preprocessing/
?   ?   ?   ??? __init__.py
?   ?   ?   ??? ct_loader.py
?   ?   ?   ??? transforms.py
?   ?   ?   ??? normalization.py
?   ?   ??? datasets/
?   ?   ?   ??? __init__.py
?   ?   ?   ??? ct_dataset.py
?   ?   ??? models/
?   ?   ?   ??? __init__.py
?   ?   ?   ??? baseline.py
?   ?   ??? inference/
?   ?   ?   ??? __init__.py
?   ?   ?   ??? predictor.py
?   ?   ??? evaluation/
?   ?   ?   ??? __init__.py
?   ?   ?   ??? metrics.py
?   ?   ?   ??? visualizer.py
?   ?   ??? utils/
?   ?       ??? __init__.py
?   ?       ??? config.py
?   ?
?   ??? configs/
?   ?   ??? preprocessing.yaml
?   ?   ??? dataset.yaml
?   ?   ??? training.yaml
?   ?   ??? inference.yaml
?   ?
?   ??? scripts/
?   ?   ??? preprocess_ct.py
?   ?   ??? run_inference.py
?   ?   ??? evaluate.py
?   ?
?   ??? notebooks/
?   ?   ??? 01_dataset_exploration.ipynb
?   ?   ??? 02_preprocessing_validation.ipynb
?   ?   ??? 03_inference_results.ipynb
?   ?
?   ??? results/
?   ?   ??? predictions/
?   ?   ??? visualizations/
?   ?   ??? metrics/
?   ?
?   ??? tests/
?       ??? test_preprocessing.py
?       ??? test_dataset.py
?       ??? test_inference.py
?
??? project2_navigation/
?   ??? competitors/
?   ?   ??? stealthstation.md
?   ?   ??? globus_excelsius.md
?   ?   ??? stryker.md
?   ?   ??? brainlab.md
?   ?   ??? 7d_surgical.md
?   ?   ??? sources.md
?   ?
?   ??? competitor_matrix.csv           # Comparative feature matrix
?   ??? competitor_analysis.md          # Overall competitive analysis
?   ??? navigation_workflows.md         # Workflow stage-by-stage breakdown
?   ??? instrument_taxonomy.md          # Instrument categories and tracking
?   ??? opportunity_matrix.csv          # Technical opportunities
?   ??? figures/                        # Workflow diagrams, matrices
?
??? docs/
?   ??? technical_architecture.md      # Integration of Projects 1 & 2
?   ??? evaluation_protocol.md         # Metrics and validation approach
?   ??? technical_risks.md             # Risk analysis and mitigation
?   ??? research_decisions.md          # Decision log
?   ??? experiment_roadmap.md          # Planned experiments
?   ??? two_week_progress.md           # Two-week progression narrative
?   ??? checkin_slides.md              # Presentation outline
?
??? .github/
    ??? workflows/                      # CI/CD pipelines (future)
```

## Installation & Setup

### Python Environment

```bash
# Clone and navigate
cd /Users/dm/Documents/Perfint_Research

# Create conda environment
conda env create -f environment.yml

# Activate environment
conda activate vertebra_seg

# Install package in development mode
pip install -e .
```

### GPU Support (Optional)

For GPU acceleration, ensure PyTorch is built for your CUDA version:

```bash
# For CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## Quick Start

### 1. Preprocess CT data

```bash
python project1_vertebra_segmentation/scripts/preprocess_ct.py \
    --input data/raw/ct_volumes \
    --output data/processed \
    --config project1_vertebra_segmentation/configs/preprocessing.yaml
```

### 2. Run baseline inference

```bash
python project1_vertebra_segmentation/scripts/run_inference.py \
    --model path/to/baseline_model.pth \
    --input data/processed/ct_volume.nii.gz \
    --output results/predictions
```

### 3. Evaluate predictions

```bash
python project1_vertebra_segmentation/scripts/evaluate.py \
    --predictions results/predictions \
    --ground_truth data/processed/segmentation_masks \
    --output results/metrics
```

## Key Documents

- **[PROJECT_STATUS.md](PROJECT_STATUS.md)**: Current progress tracking
- **[CHECKIN_SUMMARY.md](CHECKIN_SUMMARY.md)**: Executive summary for project review
- **[ROADMAP.md](ROADMAP.md)**: Development timeline and next phases

## Project 1: Literature & Research

- [Literature Review](project1_vertebra_segmentation/literature/literature_review.md)
- [Papers Database](project1_vertebra_segmentation/literature/papers.csv)
- [Dataset Benchmark](project1_vertebra_segmentation/datasets/dataset_benchmark.md)
- [Model Benchmark](project1_vertebra_segmentation/models/model_benchmark.md)
- [Baseline Selection](project1_vertebra_segmentation/models/baseline_selection.md)

## Project 2: Surgical Navigation

- [Competitor Analysis](project2_navigation/competitor_analysis.md)
- [Competitor Matrix](project2_navigation/competitor_matrix.csv)
- [Navigation Workflows](project2_navigation/navigation_workflows.md)
- [Instrument Taxonomy](project2_navigation/instrument_taxonomy.md)
- [Opportunity Matrix](project2_navigation/opportunity_matrix.csv)

## Development Roadmap

### Phase 1 (Complete)
- [x] Repository initialization
- [x] Literature research foundations
- [x] Dataset identification

### Phase 2 (In Progress)
- [ ] Model/framework benchmarking
- [ ] Baseline selection
- [ ] Environment setup
- [ ] Preprocessing implementation

### Phase 3 (Planned)
- [ ] Baseline inference
- [ ] Quantitative evaluation
- [ ] Labeled vertebra classification
- [ ] Cross-dataset validation

## Technical Decisions

See [docs/research_decisions.md](docs/research_decisions.md) for detailed decision log.

**Current selections:**
- Framework: MONAI + PyTorch (evaluation in progress)
- Baseline model: 3D U-Net with encoder improvements (pending final benchmarking)
- Primary dataset: VerSe 2019/2020 (pending verification)
- Evaluation metrics: Dice, IoU, Hausdorff distance, per-vertebra accuracy

## Requirements

- Python 3.9+
- PyTorch 2.0+
- MONAI 1.2+
- CUDA 11.8+ (for GPU support)

See [requirements.txt](requirements.txt) for complete dependency list.

## Contributing

This is an active research repository. All code follows:
- PEP 8 style guidelines
- Comprehensive docstrings
- Type hints where practical
- Automated tests for critical functions

## References & Acknowledgments

Literature sourced from:
- PubMed Central
- IEEE Xplore
- arXiv
- GitHub research repositories
- Official MONAI documentation

Competitor information sourced from:
- Official manufacturer documentation
- FDA regulatory filings
- Peer-reviewed publications
- Clinical research papers

## Status & Next Steps

This repository represents the foundation of a research program in vertebral segmentation and surgical navigation technology.

**For the next project review, see:** [CHECKIN_SUMMARY.md](CHECKIN_SUMMARY.md)

---

**Repository:** https://github.com/MoorthyDurga/Perfint_Research
**Last Updated:** September 7, 2026
**Status:** Active Research in Progress
