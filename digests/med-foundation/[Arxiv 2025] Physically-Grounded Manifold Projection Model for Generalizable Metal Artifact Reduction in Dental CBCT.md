---
title: "Physically-Grounded Manifold Projection Model for Generalizable Metal Artifact Reduction in Dental CBCT"
authors: ["Zhi Li", "Yaqi Wang", "Bingtao Ma", "Yifan Zhang", "Huiyu Zhou", "Shuai Wang"]
source: "Arxiv"
venue: ""
published: "2025-12-30"
published_time: "2025-12-30T14:36:26+00:00"
year: 2025
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2512.24260"
url: "http://arxiv.org/abs/2512.24260v2"
pdf: "paper/med-foundation/[Arxiv 2025] Physically-Grounded Manifold Projection Model for Generalizable Metal Artifact Reduction in Dental CBCT.pdf"
---

# Physically-Grounded Manifold Projection Model for Generalizable Metal Artifact Reduction in Dental CBCT

*🕒 **Published (v1):** 2025-12-30 14:36 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2512.24260v2)*

## TL;DR
PGMP (Physically-Grounded Manifold Projection) is a three-stage framework for metal artifact reduction (MAR) in dental CBCT that replaces stochastic diffusion with a single-step deterministic manifold projection. It combines polychromatic physics simulation for realistic training data, a deterministic ViT-based projector (DMP-Former), and semantic regularization via a frozen medical foundation model (MedDINOv3) to prevent structural hallucinations. The framework targets both image quality and clinical generalizability across unseen scanner protocols.

## Problem
Supervised regression MAR methods suffer from "regression-to-the-mean," producing over-smoothed textures that obliterate fine trabecular bone. Diffusion-based methods achieve better texture realism but require hundreds of iterative sampling steps and introduce stochastic uncertainty incompatible with diagnostic reproducibility. Both paradigms also face a synthetic-to-real domain gap because conventional monochromatic simulations fail to reproduce polychromatic beam hardening of clinical CBCT scanners.

## Method
**AAPS (Anatomically-Adaptive Physics Simulation):** Constructs patient-specific 3D digital twins by inserting high-fidelity CAD models of dental restorations (fillings, crowns, implants, bridges) into clinically valid anatomical zones derived from MICCAI STS tooth segmentation masks. X-ray attenuation is modeled with a polychromatic spectrum at 120 kVp with energy-dependent attenuation coefficients for water, bone, and metal. Photon starvation is simulated via Poisson sampling; scatter is approximated via convolution with a Gaussian kernel (SPR = 0.1, σ = 10 px); electronic noise is additive Gaussian. Reconstruction uses FBP.

**DMP-Former:** An isotropic ViT backbone (constant spatial resolution, no downsampling) that receives the artifact-corrupted volume concatenated with a structural edge mask. Formulates MAR as a single-step direct x-prediction: learning the projection fθ: Y → M onto the clean anatomical manifold via L1 reconstruction loss. Each DMP-Block uses AdaLN-Zero (structural conditioning via learned scale/shift, zero-initialized for stable optimization), RoPE attention (relative spatial encoding, beneficial for bilateral dental symmetry), and SwiGLU feed-forward activations.

**SSA (Semantic-Structural Alignment):** A frozen MedDINOv3 (pretrained on >3M CT slices) acts as a teacher. Student features from deep DMP-Former layers are mapped to teacher feature space via a 3×3 convolutional projector. Alignment is measured as negative cosine similarity after spatial normalization (subtract spatial mean, divide by spatial std) to suppress intensity biases. Combined loss: Ltotal = L1 + 0.2·LSSA + 0.1·Ledge (edge loss is spatially gated to tooth ROI via Medge).

## Key Contributions
- AAPS pipeline: volumetrically consistent 3D digital twins with polychromatic spectral simulation, Poisson noise, and convolutional scatter approximation to minimize the synthetic-to-real domain gap
- DMP-Former: single-step deterministic manifold projection via isotropic ViT with AdaLN-Zero structural conditioning and RoPE attention, bypassing stochastic iterative sampling
- SSA mechanism: spatial-aware feature alignment to frozen MedDINOv3 using iREPA-inspired convolutional projector and spatially-normalized cosine similarity loss
- Dual-track evaluation: patient-level-split synthetic benchmark (9,441 training / 1,153 test slices from STS24) plus multi-center real clinical CBCT with no ground truth, assessed by expert radiologists

## Results
The paper is truncated before quantitative results are reported (text ends mid-sentence in Section 4.1.3 describing evaluation metrics). No benchmark numbers can be extracted from the provided text.

## Limitations
- Scatter model is a convolutional Gaussian proxy (SPR = 0.1 fixed empirically), not full Monte Carlo—angular dependencies of Compton scattering are not captured
- Training is entirely on synthetic (AAPS) data; real clinical test scans have no ground-truth clean images, limiting quantitative evaluation to the synthetic split
- λSSA and λedge weights are set empirically via validation; sensitivity analysis is not described in the provided text
- DMP-Former is 2D slice-based (patches p×p); it is unclear how inter-slice 3D consistency is enforced beyond the structural edge mask

## Relevance to Foundation Models in Medicine
This paper demonstrates a use pattern increasingly common in medical foundation model research: a large pretrained encoder (MedDINOv3, trained on 3M+ CT slices) is frozen and repurposed as a semantic regularizer for a specialized downstream task (MAR) rather than fine-tuned. The domain adaptation argument—that natural-image models like DINOv2 are unsuitable for Hounsfield Unit data and must be replaced by CT-pretrained encoders—is a recurring theme in medical FM deployment. The spatial-aware alignment strategy (iREPA-style, using convolutional projectors instead of global pooling) is a methodological contribution relevant to anyone leveraging FMs as perceptual loss surrogates in medical image reconstruction.

## Tags
#metal-artifact-reduction #dental-cbct #medical-foundation-models #manifold-learning #vision-transformer #physics-simulation #image-restoration #knowledge-distillation
