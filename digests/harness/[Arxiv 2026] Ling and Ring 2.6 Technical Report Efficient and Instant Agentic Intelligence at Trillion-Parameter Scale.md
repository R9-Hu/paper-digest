---
title: "Ling and Ring 2.6 Technical Report: Efficient and Instant Agentic Intelligence at Trillion-Parameter Scale"
authors: ["Ang Li", "Ben Liu", "Bin Han", "Bin Hu", "Bin Jing", "Binbin Hu", "Bing Li", "Cai Chen", "Caizhi Tang", "Changxin Tian", "Chao Huang", "Chao Zhang", "Chen Liang", "Chen Qian", "Chengfu Tang", "Chengyao Wen", "Chilin Fu", "Chunwei Wu", "Cong Zhang", "Cunyin Peng", "Daixin Wang", "Dalong Zhang", "Deng Zhao", "Dingnan Jin", "Dingyuan Zhu", "Donghao Zhang", "Fan Yuan", "Fangzheng Zhao", "Fanzhuang Meng", "Feifan Wu", "Feng Xu", "Fengbin Fang", "Gangshan Wang", "Guodong Yang", "Hailin Zhao", "Haitao Wang", "Haitao Zhang", "Hanxiao Zhang", "Hanzi Wang", "Hao Dai", "Hao Liu", "Hao Qian", "Hao Wu", "Haoxiong Liu", "Haoyu Xu", "Heng Zhang", "Hong Liu", "Hongliang Zhang", "Hongrui Liu", "Hongxun Li", "Hongzhi Ruan", "Huaidong Xiong", "Huihuang Zheng", "Huikang Tang", "Jia Guo", "Jia Li", "Jia Liu", "Jiameng Wang", "Jiaming Liu", "Jiannan Shi", "Jianping Wei", "Jiaolong Yang", "Jiapeng Wang", "Jie Gao", "Jie Wang", "Jiewei Wu", "Jin Yang", "Jinjin Li", "Jinjing Huang", "Jinquan Sun", "Jinyao Chen", "Juanhui Tu", "Jun Liu", "Jun Mei", "Jun Xu", "Jun Zhou", "Junjie Ou", "Junnan Sipan", "Junpeng Fang", "Kaihong Zhang", "Kaiqin Hu", "Ke Shi", "Kuan Xu", "Kun Tang", "Kunlong Chen", "Lanyin Mei", "Lei Chen", "Lei Liang", "Lei Xu", "Li Tang", "Liang Jiang", "Liangcheng Fu", "Lihui Zhang", "Linfeng Shi", "Lintao Ma", "Liyuan Liu", "Longfei Li", "Longfei Zheng", "Lu Liu", "Lu Yu", "Man Li", "Meiqi Zhu", "Meng Li", "Mengjie Gao", "Mengshu Sun", "Mingming Yin", "Mingyang Zhang", "Mingyuan Fan", "Nuo Xu", "Pan Tang", "Peijie Jiang", "Peilong Zhao", "Peng Lin", "Pingping Liu", "Qi Zuo", "Qian Zhao", "Qiang Cheng", "Qianggang Cao", "Qiaoben Bao", "Qing Cui", "Qingyuan Yang", "Qitao Shi", "Qiyin Huang", "Qizheng Zhou", "Quan Wan", "Runyuan Zhao", "Shaomian Zheng", "Shaowei Wei", "Shengnan Zhang", "Shuaicheng Li", "Shujie Li", "Shuo Zhang", "Sikang Bian", "Tianchu Yao", "Tiange Xu", "Tianshu Wang", "Ting Guo", "Tinghao Wang", "Tingwei Huang", "Tong Zhao", "Tongkai Yang", "Wang Hong", "Wanli Gu", "Wei Lu", "Weichang Wu", "Weiguang Han", "Weiquan Li", "Wenbo Shen", "Wenjing Fang", "Wenzhi Tang", "Xiang Shu", "Xiao Shi", "Xiaodong Yan", "Xiaolu Zhang", "Xiaopei Wan", "Xiaqing Sun", "Xin Zhao", "Xingyu Lu", "Xinxing Yang", "Xinyao Tang", "Xinyu Kong", "Xinyu Liu", "Xiong Xu", "Xuan Sun", "Xudong Han", "Xudong Wang", "Xujie Shen", "Yalin Zhang", "Yangyang Hou", "Yankun Ren", "Yao Zhao", "Ye Chen", "Yeyang Chen", "Yibo Cao", "Yifan Zuo", "Yijie Chen", "Ying Li", "Yingjie Song", "Yingxue Li", "Yiqi Wang", "Yixuan Sun", "Yizhu Xiao", "Yongfei Xu", "Yu Liu", "Yuchen Fang", "Yue Gao", "Yue Yu", "Yue Zhang", "Yuqi Zhang", "Yuxiao He", "Yuxiao Lu", "Yuxin Tian", "Yuxuan Li", "Yuzhuo Fu", "Zhankai Xu", "Zhaoxin Huan", "Zhenduo Zhang", "Zhengke Gui", "Zhengyu Huang", "Zhenjun Ma", "Zhenxuan Pan", "Zheping Qu", "Zhibo Zhu", "Zhidong Fan", "Zhigang Huangfu", "Zhihao Wang", "Zhiqiang Zhang", "Zhizhen Liu", "Zhuyan Zhou", "Zibin Lin", "Zihang Zeng", "Zihao Wang", "Zilong Wang", "Ziqi Liu", "Zitao Xuan", "Zixuan Cheng", "Zujie Wen", "Zuoli Tang"]
source: "Arxiv"
venue: ""
published: "2026-06-13"
published_time: "2026-06-13T03:21:49+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.15079"
url: "http://arxiv.org/abs/2606.15079v1"
pdf: "paper/harness/[Arxiv 2026] Ling and Ring 2.6 Technical Report Efficient and Instant Agentic Intelligence at Trillion-Parameter Scale.pdf"
---

# Ling and Ring 2.6 Technical Report: Efficient and Instant Agentic Intelligence at Trillion-Parameter Scale

*🕒 **Published (v1):** 2026-06-13 03:21 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.15079v1)*

## TL;DR
Ling-2.6 and Ring-2.6 are a trillion-parameter model family for efficient agentic intelligence, produced by retrofitting the Ling-2.0 checkpoint rather than training from scratch. The core innovations span a hybrid Lightning Attention + MLA architecture, token-efficiency-optimizing post-training methods, and KPop—a novel RL algorithm for stable large-scale agentic training. All checkpoints are open-sourced.

## Problem
Training trillion-parameter agentic LLMs from scratch is prohibitively expensive, and existing models face a trilemma: long-context efficiency (GQA attention costs O(n²)), token efficiency (verbose reasoning), and native agentic capability (chat data doesn't transfer to tool/environment grounding). These objectives conflict—longer reasoning improves performance but raises latency and token cost.

## Method
**Architecture.** Starting from Ling-2.0-1T, a four-stage migration pre-training (~400B tokens) retrofits GQA layers into a 7:1 hybrid of Lightning Attention (linear O(n) cost) and MLA (low-rank KV compression). Structural obstacles—QK Norm incompatibility with MLA weight absorption, and Partial RoPE incompatibility with TransMLA—are resolved via calibration-based weight fusion and PCA-based decoupled RoPE treatment respectively. Migration is followed by 8T tokens of continued pre-training and 1.2T tokens of mid-training extending context to 256K.

**Post-training (Ling-2.6, instant model).** A specialization-then-distillation pipeline: (1) cold-start SFT; (2) specialist RL per domain using Evo-CoT (removes redundant reasoning steps), Linguistic Unit Policy Optimization (LPO, shifts credit assignment from tokens to semantic units), Dynamic Length Penalty, Semantic Redundancy Penalty via LLM judge, and GSPO with process reward + zlib compression ratio penalty for agentic tasks; (3) bidirectional preference alignment with a focus reward that dynamically re-weights under-optimized rubric dimensions; (4) shortest-correct-response distillation.

**Post-training (Ring-2.6, reasoning model).** Extends Ling-2.6's pipeline with KPop: replaces the fixed-ratio KL constraint in IcePop with binary KL divergence for training stability, and decouples rollout collection from parameter updates (asynchronous RL) to make long environment-bound trajectories tractable at 1T scale. Adaptive thinking modes (high/xhigh) modulate length penalties by task difficulty.

**Agentic corpora.** Pre-training includes trajectories from 500+ real-world MCP environments (3,000+ tools); post-training uses 200+ executable toolkits with 2,500+ callable functions spanning search, e-commerce, finance, and scientific computation.

## Key Contributions
- **Architectural retrofit pipeline** enabling performance-lossless migration of a 1T-parameter GQA checkpoint to hybrid Lightning Attention + MLA without retraining from scratch
- **7:1 Linear:Full attention ratio** identified via scaling law experiments as optimal for efficiency-quality tradeoff
- **KPop RL algorithm** with binary KL divergence and asynchronous scheduling for stable trillion-parameter agentic RL
- **Evo-CoT + LPO + bidirectional preference alignment + shortest-correct-response distillation** pipeline delivering ~4× token efficiency over Ling-2.0
- **Dynamic Pass Rating (DPR)** adaptive curriculum that classifies task difficulty from live training dynamics rather than static pass rates
- Open-source release of all 2.6-family checkpoints (flash, 1T, Ring-1T)

## Results
- Ling-2.6-1T scores **34** on the Artificial Analysis Intelligence Index using ~16M output tokens, comparable to GPT-5.4 in the non-reasoning setting
- **~4× higher token efficiency** on reasoning workloads vs. Ling-2.0
- Ring-2.6-1T: **87.60** on PinchBench, **63.82** on ClawEval, strong results on GAIA-2 Search and τ²-Bench Telecom
- Base model (Ling-2.6-1T-base) gains on GPQA (+3.1 pp), SimpleQA (+12.73 pp), LongBenchv2 (+9.35 pp) over Ling-2.0-1T-base, without regression on math/code

## Limitations
- Paper is truncated; post-training sections for Ring-2.6 and full agent benchmark comparisons against external baselines (e.g., GPT-4o, Qwen-3) are not fully presented
- Retrofit migration still requires ~400B token migration pre-training + 9.6T total tokens—significant compute even if cheaper than scratch training
- KPop stability improvements are described qualitatively; ablation against vanilla PPO or GRPO at 1T scale is not shown in the provided text
- Adaptive thinking mode selection (high vs. xhigh) appears heuristic; criteria for when to engage each mode are unspecified
- Agentic corpus quality relies on model-based verification, introducing potential distributional bias from teacher models

## Relevance to Harnesses / Meta-Harnesses
KPop and the surrounding agentic RL pipeline constitute a training harness for trillion-parameter agents: asynchronous rollout scheduling, environment-grounded reward collection across coding/search/tool-use/workflow execution domains, and curriculum management via DPR all describe infrastructure that orchestrates agent-environment interaction at scale—the production analog of a meta-harness. The specialization-then-distillation framework (cold-start SFT → specialist RL → distillation) is itself a multi-stage meta-harness for capability assembly. The construction of agentic corpora from 500+ MCP environments mirrors harness design patterns: verifiable tasks, structured tool traces, and rule+model-based trajectory verification are exactly the scaffolding a harness engineer would build. For harness researchers, this paper provides a rare public description of what a production-scale agentic training harness looks like at 1T parameters.

## Tags
#agentic-training #rl-harness #tool-use #moe #long-context #token-efficiency #kpop #training-pipeline
