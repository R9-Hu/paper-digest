---
title: "Imaging-anchored Multiomics in Cardiovascular Disease: Integrating Cardiac Imaging, Bulk, Single-cell, and Spatial Transcriptomics"
authors: ["Minh H. N. Le", "Tuan Vinh", "Thanh-Huy Nguyen", "Tao Li", "Bao Quang Gia Le", "Han H. Huynh", "Monika Raj", "Carl Yang", "Min Xu", "Nguyen Quoc Khanh Le"]
source: "Arxiv"
venue: ""
published: "2026-01-10"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2601.07871"
url: "http://arxiv.org/abs/2601.07871v1"
pdf: "paper/med-foundation/[Arxiv 2026] Imaging-anchored Multiomics in Cardiovascular Disease Integrating Cardiac Imaging, Bulk, Single-cell, and Spatial Transcriptomics.pdf"
---

# Imaging-anchored Multiomics in Cardiovascular Disease: Integrating Cardiac Imaging, Bulk, Single-cell, and Spatial Transcriptomics

## TL;DR
A systematic review proposing an "imaging-anchored multiomics" framework for cardiovascular disease in which cardiac imaging (echocardiography, CMR, CT) acts as the primary spatial reference and bulk, single-cell, and spatial transcriptomics supply cell-type- and location-specific molecular context. The review surveys representation learning per modality, multimodal fusion architectures, radiogenomics pipelines, and spatial alignment strategies. Single-cell and spatial foundation models are highlighted as a near-term pathway toward scalable cardiovascular multiomics.

## Problem
Cardiac imaging and transcriptomic assays are routinely co-generated in large cohorts but remain siloed in separate analysis pipelines, preventing mechanistic interpretation of imaging phenotypes in terms of underlying cell states, gene-expression programmes, and tissue architecture. Classical metrics (ejection fraction, LGE burden) discard the spatial richness that could bridge voxel-level imaging to cell-level molecular biology.

## Method
The review organises the problem into four methodological layers:

1. **Modality characterisation** — echocardiography, CMR, and cardiac CT define a spatial phenotype; bulk and scRNA-seq provide molecular context; spatial transcriptomics (10x Visium, MERFISH, seqFISH) bridges the two by preserving tissue coordinates and enabling co-registration with histology and in vivo imaging.

2. **Representation learning** — CNNs, 3D variants, ViTs, and masked autoencoders (MAEs) encode cardiac images at global, regional, or voxel scale. VAEs (scVI), MOFA+, and large-scale transformer/state-space models (trained on tens of millions of cells) encode omics. Graph convolutional networks (SpaGCN, BayesSpace) encode spatial transcriptomics by passing messages across spot-adjacency graphs.

3. **Multimodal fusion** — Three paradigms reviewed: (a) early (feature concatenation), (b) intermediate (deep canonical correlation analysis, multimodal VAEs with product-of-experts/mixture-of-experts, cross-modal autoencoders), and (c) late (per-modality prediction ensembles). Graph-based fusion links imaging regions to pathway/gene nodes via GNNs. CLIP-style contrastive objectives align imaging embeddings with omics or text embeddings in a shared latent space.

4. **Integrative pipelines** — Radiogenomics maps imaging features to gene/pathway scores via regression, DCCA, or GNNs with biological-prior graphs and Mendelian randomisation for causal inference. Spatial alignment proceeds in stages: histology-to-block-face registration → spot-grid mapping via fiducials → deformable warping of in vivo to ex vivo imaging. Virtual transcriptomics predicts gene-expression modules directly from images, exemplified by predicting inflammatory plaque genes from coronary CT angiography radiomics.

## Key Contributions
- Formal "imaging-anchored" framing that elevates imaging to the primary spatial coordinate system rather than treating it as one of many parallel modalities.
- Comprehensive taxonomy of fusion architectures (early/intermediate/late, graph-based, contrastive) with explicit discussion of missing-modality handling and small-sample constraints.
- Curated table of public multimodal cardiovascular datasets (UK Biobank CMR+genomics ~100k; MESA ~6,800; HCMR ~2,700; MIMIC-IV-ECG ~800k ECGs; EchoNet; Cardiac Atlas Project; spatial myocardial-infarction atlas; coronary plaque spatial-omics resources).
- Review of exemplar frameworks: MOFA+, scVI/totalVI, multimodal VAEs (MVAE, MoPoE-VAE), cross-modal ECG–CMR autoencoders, radiotranscriptomic perivascular fat signatures, and human MI/plaque spatial atlases.
- Positioning of single-cell, spatial, and multimodal medical foundation models as near-term generic encoders for cardiovascular imaging-omics.

## Results
This is a review; no new experimental benchmarks are reported. Cited empirical anchors include:
- Cross-modal cardiovascular autoencoder (ECG + CMR + clinical) scaled to tens of thousands of individuals demonstrating imaging imputation and latent-space GWAS.
- Radiotranscriptomic perivascular fat score (coronary CT radiomics → adipose gene-expression modules) improving cardiac mortality prediction beyond standard CT risk factors.
- Spatial multi-omic MI atlas (31 samples, 23 patients; snRNA-seq + snATAC-seq + Visium) delineating infarct core, border zone, and remote myocardium at single-cell and spatial resolution.
- Coronary plaque spatial transcriptomics studies linking immune niches and inflammatory gene modules to CT/invasive imaging morphology features.

## Limitations
- Review scope is deliberately narrowed to imaging–transcriptomics; proteomics, metabolomics, and epigenomics are mentioned but not systematically surveyed.
- Paired imaging–omics cohorts remain small (tens to hundreds of patients), constraining high-capacity deep fusion models and increasing overfitting risk.
- Spatial alignment pipelines are multi-stage and accumulate registration uncertainty from tissue deformation, sectioning artefacts, and physics differences across scales; probabilistic handling is recommended but not yet standardised.
- Most spatial foundation models and histology–expression prediction architectures are validated in oncology, not cardiac/vascular tissue; large cardiac spatial datasets do not yet exist.
- Benchmarking frameworks with standardised tasks, splits, and cross-centre validation are absent for imaging–omics integration in cardiology.
- Domain shift from scanner and protocol heterogeneity in imaging, and from platform/chemistry variation in omics, remain unsolved for joint models.

## Relevance to Foundation Models in Medicine
The review is directly relevant to foundation model research: it surveys large-scale transformer and state-space single-cell models (trained on tens of millions of cells across tissues and species) as transferable encoders for cardiovascular multiomics, and discusses multimodal medical foundation models (coupling imaging, text, and clinical data) as backbones for adding omic inputs. It frames spatial transcriptomics foundation models—some trained on hundreds of thousands of spots—as the missing link between voxel-level imaging and cell-level molecular biology, pointing to an architectural pattern (pretrained unimodal encoders + cross-modal contrastive or generative fusion) that is already standard in radiology VLMs and now needs extension to molecular channels. The practical gaps identified (small paired datasets, missing modalities, batch effects, no standard benchmarks) are precisely the challenges that future cardiovascular foundation models must address to reach clinical translation.

## Tags
#multiomics #cardiovascular #spatial-transcriptomics #radiogenomics #foundation-models #multimodal-fusion #single-cell-sequencing #representation-learning
