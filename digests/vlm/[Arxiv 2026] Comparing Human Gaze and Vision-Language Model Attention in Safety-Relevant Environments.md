---
title: "Comparing Human Gaze and Vision-Language Model Attention in Safety-Relevant Environments"
authors: ["Marta Vallejo", "Siwen Wang"]
source: "Arxiv"
venue: ""
published: "2026-06-13"
published_time: "2026-06-13T08:55:48+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.15202"
url: "http://arxiv.org/abs/2606.15202v1"
pdf: "paper/vlm/[Arxiv 2026] Comparing Human Gaze and Vision-Language Model Attention in Safety-Relevant Environments.pdf"
---

# Comparing Human Gaze and Vision-Language Model Attention in Safety-Relevant Environments

*🕒 **Published (v1):** 2026-06-13 08:55 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.15202v1)*

## TL;DR
This paper evaluates whether GPT-4o and three other VLMs (Gemini Pro, Gemini Flash, Claude) can predict where humans look in safety-relevant scenes, without any eye-tracking training data. Eye-tracking data from 10 participants viewing 33 diverse scene images are converted to population-averaged gaze heatmaps and compared against VLM-generated saliency maps using four standard metrics. All models exceed chance performance, with Gemini Pro leading on spatial localisation and GPT-4o producing the closest distributional match to human gaze.

## Problem
Existing saliency prediction work focuses on general visual salience rather than safety perception, and prior eye-tracking datasets are domain-specific (e.g., construction sites, driving). It is unknown whether modern VLMs prompted for risk reasoning can spatially approximate human visual attention across diverse everyday environments without task-specific training.

## Method
**Eye-tracking dataset construction:** 10 participants (Pupil Invisible glasses, ~200 Hz binocular) viewed 33 scene images (streets, corridors, public spaces, green areas; 1,536×1,024 px, 10 s each). Raw gaze coordinates were filtered, temporally segmented, remapped to stimulus space via manually annotated monitor bounding boxes, then converted to per-participant fixation density maps (Gaussian σ=30 px). Pixel-wise averaging across participants produced 33 population-level ground-truth heatmaps.

**VLM saliency generation:** Each stimulus image was Base64-encoded and sent to GPT-4o via the OpenAI Vision API with a structured prompt instructing the model to return a JSON array of 20–25 fixation points with normalised coordinates (x,y ∈ [0,1]) and saliency weights (w ∈ [0.1,1.0]). Points were rasterised as weighted disks (r=40 px), then Gaussian-smoothed (σ=60 px) and normalised to [0,1]. The same pipeline was applied identically to Gemini Pro, Gemini Flash, and Claude for cross-model comparison.

**Evaluation:** Four complementary metrics compared AI saliency maps against human heatmaps: Pearson correlation (linear spatial agreement), NSS (AI map values at human fixation locations), KL divergence (distributional overlap), and AUC-Judd (binary fixation discrimination at 100 thresholds).

## Key Contributions
- New eye-tracking dataset: 33 diverse safety-relevant scenes, 330 individual heatmaps, 33 population-averaged ground-truth maps spanning multiple environment types under a unified protocol.
- Automated Python pipeline converting VLM JSON fixation outputs to saliency maps comparable with eye-tracking heatmaps, without any training on gaze data.
- First systematic four-metric cross-model comparison of GPT-4o, Gemini Pro, Gemini Flash, and Claude against human gaze in safety-relevant scenes.
- Evidence that VLM spatial predictions are consistent with negativity bias—models concentrate predictions at risk-relevant regions that humans also fixate.

## Results
**GPT-4o vs. human gaze (n=33 images):**
- Pearson r = 0.515 ± 0.117 (range: 0.19–0.78)
- NSS = 0.988 ± 0.323 (range: 0.28–1.74)
- KL divergence = 1.766 ± 0.844 (range: 0.59–4.16)
- AUC-Judd = 0.806 ± 0.076 (range: 0.54–0.92); chance = 0.5

**Cross-model comparison (mean ± SD):**
- Gemini Pro: r=0.571, NSS=1.131, KL=2.750, AUC-Judd=0.840 — best on three of four metrics
- Gemini Flash: r=0.514, NSS=1.006, KL=2.018, AUC-Judd=0.821 — intermediate
- GPT-4o: r=0.515, NSS=0.988, KL=1.766, AUC-Judd=0.806 — best KL (closest distributional match)
- Claude: r=0.425, NSS=0.827, KL=2.355, AUC-Judd=0.779 — weakest overall
- All models exceed AUC-Judd=0.5 and produce positive NSS

**Scene-level findings:** Strongest alignment on images with spatially localised risk elements (e.g., Image 05: r=0.78, NSS=1.74; Image 02: AUC-Judd=0.92, KL=0.59). Weakest alignment on diffuse scenes (Image 22: KL=4.16).

## Limitations
- Small participant sample (n=10 university students), limiting generalisability of population-averaged ground truth.
- AI saliency maps derived from sparse JSON fixation points (20–25) rasterised as disks; fine-grained spatial detail in dense human gaze is not captured.
- Results are sensitive to prompt design; different prompts may yield different spatial predictions.
- API sampling variability can introduce run-to-run differences.
- No expert-annotated risk-level labels, precluding subgroup analysis by scene risk severity.
- Static images only; ecological validity for dynamic real-world environments is not assessed.
- Only 33 stimuli—insufficient for robust statistical testing of alignment differences across scene categories.

## Relevance to Vision-Language Models
This study provides a direct empirical assessment of VLMs' spatial grounding ability in a safety-critical domain, revealing that prompt-driven saliency prediction from models like GPT-4o and Gemini Pro meaningfully correlates with human fixation behaviour without any gaze-specific fine-tuning. The cross-model comparison quantifies capability gaps—Gemini Pro leads on localisation while GPT-4o better matches distributional shape—which is directly informative for selecting VLMs in safety-aware perception pipelines. The finding that alignment degrades for diffuse scenes highlights a key failure mode of the JSON-fixation paradigm, motivating richer spatial output formats (e.g., dense attention maps or segmentation masks) in future VLM design. For the broader VLM community, this work establishes a reproducible evaluation framework linking structured VLM outputs to established saliency metrics, which can be extended to video, robotics, and autonomous driving contexts.

## Tags
#vlm #visual-saliency #eye-tracking #safety-perception #gpt4o #human-ai-alignment #spatial-grounding #multimodal
