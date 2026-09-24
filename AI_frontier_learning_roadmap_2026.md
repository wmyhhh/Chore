# 从大学人工智能专业到 Frontier AI：课程体系、技术全景与学习路线

## 一、先给出整体结论

人工智能（Artificial Intelligence, AI）专业不是“学习怎样使用 ChatGPT 或 Claude”，也不是只有 Deep Learning。一个严肃的 AI 本科培养体系，本质上是 **Computer Science + Mathematics + Statistics + Machine Learning + Cognitive/Decision Sciences + Engineering Systems + Ethics** 的交叉组合。Carnegie Mellon University（CMU）的 Bachelor of Science（B.S.）in Artificial Intelligence 同时要求 Mathematics and Statistics Core、Computer Science Core、AI Core、Decision Making and Robotics、Perception and Language、Human-AI Interaction 与 Ethics；Massachusetts Institute of Technology（MIT）的 AI and Decision Making 专业则明确分成 data-centric、model-centric、decision-centric、computation-centric、human-centric 五个中心，并保留 Algorithms、Optimization、Control、Society 等基础；清华、北大、浙大的方案也都强调数理基础、计算机基础、AI 核心、交叉应用和科研实践，而不是只追逐某一代大模型工具。[^1][^2][^3][^4][^5][^6]

今天的 frontier model 也不是单独一张“更大的 neural network”。更准确的对象是一个 **model-system stack**：底层是大规模 pretrained foundation model；中间是 instruction tuning、preference learning、reasoning reinforcement learning、安全对齐和 multimodal training；上层还有 Retrieval-Augmented Generation、tool use、agent loop、memory、sandbox、guardrails、evaluation 与高性能 inference system。用户感知到的“模型能力”，是这些组件共同作用的结果。

截至 2026 年 9 月 15 日，Anthropic 官网列出的最新 Claude 是 Claude Fable 5.1 与 Claude Mythos 5.1；官方说明二者是同一个 underlying model，但 safeguards 的严格程度和允许的专业用途不同。Fable 5.1 面向一般使用，Mythos 5.1 通过 trusted access program 提供更强的 cybersecurity 和 life-science 能力。[^7][^8] 但是 Anthropic 并未公开它的 parameter count、layer count、hidden dimension、attention heads、dense 还是 Mixture-of-Experts、tokenizer、pretraining token 数、optimizer、learning-rate schedule 或完整 compute budget。因此，任何声称“完整拆解 Fable 5.1 architecture”的文章，如果没有 Anthropic 新的一手披露，基本都混入了推测。

从一门入门 Deep Learning 课程走到能够理解和复现 frontier research，真正的鸿沟主要有七个：**数学与优化、Transformer / Large Language Model（LLM）原理、data engineering、distributed systems、post-training 与 reasoning、agent/evaluation engineering、科研方法**。其中前六个可以通过小规模实验逐层补齐；唯独训练 Claude 级模型所需的数据、算力、组织协作与 proprietary knowledge，不可能由个人完整复制。合理目标不是“一个人复刻 Claude”，而是做到：能解释其公开技术栈、能在 open-weight model 上复现关键机制、能设计严谨 evaluation 和 ablation，并能在某个子问题上提出新研究。

---

## 二、AI 专业究竟在研究什么

AI 研究的核心问题可以概括为：**如何让计算系统从 data 和 interaction 中形成 representation，进行 perception、prediction、reasoning、decision making 与 action，并且在不确定环境中可靠、安全地实现目标。** 这一定义比“训练神经网络”更宽，因为 AI 同时包含 symbolic reasoning、probabilistic inference、optimization、control、search、planning、learning、human interaction 和 social governance。

从研究对象看，可以分为以下层次：

| 层次 | 核心问题 | 典型课程或技术 |
|---|---|---|
| Representation | 怎样把 text、image、audio、video、graph、3D scene 或 robot state 表示成可计算结构 | Linear Algebra、Embedding、Representation Learning、Computer Vision、Natural Language Processing |
| Learning | 怎样从有限、噪声、带偏差的数据中学习规律 | Probability、Statistics、Machine Learning、Deep Learning、Self-Supervised Learning |
| Reasoning | 怎样组合知识，完成 multi-step inference、search、proof、program synthesis | Logic、Knowledge Representation、Probabilistic Graphical Models、Transformer reasoning、Neuro-symbolic AI |
| Decision and Action | 怎样在有反馈和长期后果的环境中选择动作 | Reinforcement Learning、Planning、Control Theory、Game Theory、Robotics |
| Interaction | 怎样理解人类 intention，并与用户、软件、其他 agents 协作 | Human-Computer Interaction、Human-AI Interaction、Tool Use、Multi-Agent Systems |
| Systems | 怎样把算法扩展到可靠、高效、可部署的系统 | Algorithms、Operating Systems、Distributed Systems、Databases、Compilers、AI Accelerators、Machine Learning Operations（MLOps） |
| Safety and Society | 怎样评估 bias、misuse、privacy、robustness、alignment 和社会影响 | AI Ethics、Security、Interpretability、Policy、Responsible AI |

因此，AI 专业和计算机科学（Computer Science, CS）专业的关系不是替代关系。CS 提供 programming language、data structure、algorithm、computer architecture、operating system、network、database 和 software engineering；AI 在此之上增加 statistical learning、perception、reasoning、decision 和 domain-specific modelling。缺少 CS foundation 的 AI 学生，往往会“会调 model，不会建 system”；缺少 Mathematics and Statistics 的学生，则容易“会跑 code，不理解为什么有效以及何时失效”。

## 三、国内外代表性高校通常学哪些课程

### 3.1 共同的七层课程结构

不同学校命名不同，但课程可以归并为七层。

#### 第一层：Mathematical Foundations

- Calculus：gradient、Jacobian、Taylor approximation、continuous optimization 的基础。
- Linear Algebra：vector space、matrix decomposition、eigenvalue、singular value、tensor operation；几乎所有 neural network computation 都建立在这里。
- Probability and Statistics：random variable、expectation、variance、conditional probability、Bayesian inference、maximum likelihood、hypothesis testing、regression。
- Discrete Mathematics：logic、set、graph、combinatorics、proof；支撑 algorithms、knowledge representation 和 theoretical CS。
- Optimization：gradient descent、convex optimization、constrained optimization、stochastic optimization。
- 进阶方向还会用到 Information Theory、Numerical Analysis、Game Theory、Causal Inference、Stochastic Process。

CMU 的 AI 本科直接要求 Calculus、Matrices and Linear Transformations、Probability Theory 和 Modern Regression；MIT 要求 Mathematics for Computer Science、Linear Algebra and Optimization、Probability/Inference。[^1][^2] 这说明数理课不是“为了考试先学一下”，而是 AI 的语言。

#### 第二层：Computer Science Foundations

- Programming：通常从 Python 开始做 modelling，但 C/C++、Java 或 Rust 有助于理解 memory、type system、performance 和大型 software design。
- Data Structures and Algorithms：array、linked structure、tree、hash、graph、dynamic programming、search、complexity。
- Computer Systems：computer organization、memory hierarchy、parallelism、operating system、network。
- Software Engineering：testing、version control、Application Programming Interface（API）design、debugging、reproducible environment。
- Database and Data System：Structured Query Language（SQL）、transaction、index、distributed data processing。

CMU 不仅要求 imperative/functional programming 和 parallel/sequential algorithms，还要求 Introduction to Computer Systems 与 theoretical CS；这正是“AI 专业仍然必须是扎实的计算机专业”的典型例子。[^1]

#### 第三层：Classical AI and Machine Learning Core

- Introduction to AI：state-space search、A*、constraint satisfaction、planning、logic、knowledge representation。
- Machine Learning：linear/logistic regression、decision tree、support vector machine、kernel method、ensemble、clustering、dimensionality reduction、generalization。
- Probabilistic Models：Bayesian network、Hidden Markov Model、variational inference。
- Deep Learning：Multilayer Perceptron（MLP）、Convolutional Neural Network（CNN）、Recurrent Neural Network（RNN）、attention、optimization、regularization。
- Reinforcement Learning（RL）：Markov Decision Process、value function、policy gradient、actor-critic、offline RL。

这部分很关键：LLM 并没有让 classical AI 消失。Agent 的 planning、search，reasoning model 的 inference-time search，robot 的 control，alignment 的 reward modelling，仍然会重新调用这些旧问题。

#### 第四层：Perception, Language and Embodied Intelligence

- Computer Vision（CV）：image classification、detection、segmentation、3D vision、vision-language learning。
- Natural Language Processing（NLP）：tokenization、language modelling、syntax/semantics、information extraction、machine translation、LLM。
- Speech and Audio：Automatic Speech Recognition、Text-to-Speech、audio representation。
- Robotics：kinematics、dynamics、state estimation、planning、control、manipulation。
- Multimodal Learning：text-image-audio-video 的 alignment、fusion 和 generation。

Stanford 的 AI track 覆盖 logic、probability、statistics、language、robotics、machine learning、probabilistic inference、speech、vision 与 computational biology；北大通用人工智能实验班把视觉、语言、认知、机器人、机器学习、多智能体列为六个核心领域。[^3][^5]

#### 第五层：AI Systems and Engineering

- Graphics Processing Unit（GPU）programming、parallel computing、distributed training。
- Data pipeline、experiment tracking、model serving、monitoring。
- AI compiler、kernel optimization、hardware architecture。
- Model compression、quantization、distillation、efficient inference。
- Security、privacy、reliability 和 production evaluation。

这是很多入门课程最薄弱、工业界最看重的层。MIT 已将 Hardware Architecture for Deep Learning、Database Systems 等列入 AI+D advanced subjects；清华的新培养方案也设置“AI 软硬件基础”和人工智能安全方向。[^2][^4]

#### 第六层：Human, Society and Interdisciplinary Applications

- Human-AI Interaction、Cognitive Science、Psychology。
- Fairness、Accountability、Transparency、Privacy、AI governance。
- AI + Biology、Medicine、Finance、Manufacturing、Science 等 domain knowledge。

CMU 要求 Human-AI Interaction cluster 和 Ethics elective；MIT 有 AI, Decision Making, and Society；清华提供 AI + 生命科学、脑科学、自动驾驶、集成电路、金融科技等路径；浙大则组织基础、AI 核心、智能感知、智能系统、智能设计五类课程群。[^1][^2][^4][^6]

#### 第七层：Research and Practice

- Reading papers、reproducing baselines、building datasets。
- Formulating hypotheses、designing controlled experiments、performing ablations。
- Error analysis、statistical significance、writing technical reports。
- Internship、capstone、undergraduate research、graduation thesis。

真正拉开培养质量差距的往往不是课程名字，而是学生是否能获得 research mentor、compute、clean datasets、peer group 和反复做 experiment 的机会。

### 3.2 中外培养方案的典型差异

| 维度 | 美国代表性方案 | 中国代表性方案 | 应怎样理解 |
|---|---|---|---|
| 学科组织 | CMU 有独立 BSAI；Stanford 多采用 CS 内的 AI track；MIT 强调 AI and Decision Making | 独立 AI 专业、实验班、书院、AI+X 并存 | 名称不重要，关键看 foundation 和 faculty |
| 基础结构 | CS core、Math/Stats、AI clusters、HCI、Ethics 分层清楚 | 数理、信息、AI 核心、AI 进阶、交叉实践逐渐完善 | 优质方案正在趋同 |
| Decision | MIT 明显强调 inference、optimization、control、society | 清华自动化传统、北大机器人/多智能体也强调 decision | AI 不只是 perception 和 generation |
| Cross-disciplinary | Cognitive Science、Computational Biology、Policy 常被纳入 | AI+生命、金融、制造、脑科学、自动驾驶规模很大 | 必须先学会一个 domain 的问题定义和评价标准 |
| Research practice | undergraduate research、capstone、开放课程材料较成熟 | 实验班、导师制、产教平台和竞赛资源丰富 | 需要检查项目是否真正包含 hypothesis 和 evaluation，而不只是 demo |

选择 AI 专业时，可以用五个问题筛选：

1. Mathematics、Statistics、Algorithms 和 Systems 是否足够硬？
2. Machine Learning、Deep Learning、Reinforcement Learning 是否有完整 prerequisite chain？
3. 是否能进入真实 research group，获得持续 mentor 和 compute？
4. 是否训练 experiment design、evaluation、writing，而非只做 application demo？
5. curriculum 是否能更新，但又不会每年追逐短命 framework？

如果一个“AI 专业”主要教 prompt、低代码平台和调用若干 commercial API，而弱化 Linear Algebra、Probability、Algorithms、Systems 与 experimental methods，它更像短期应用培训，不是面向 frontier research 的本科教育。

---

## 四、Frontier AI 的技术全景：不是一个模型，而是一整套 stack

### 4.0 先区分“当前产品”与“可研究的公开技术”

截至本文资料日期，OpenAI 官方 model catalog 把 GPT-6 Astra 列为面向最困难 end-to-end reasoning 和 coding 的 flagship model，并列出 vision、web/file search、function calling 与 computer use 等能力；Anthropic 当前发布线的最前端则是 Fable 5.1 / Mythos 5.1。[^42][^7] 这些页面能确认产品能力和接口，却不公开足以独立重建模型的 architecture 与 training recipe。

因此，下文采用两类证据：**current commercial models** 用于说明能力已经发展到哪里；Llama、DeepSeek、Gemini 等 **公开 technical reports** 用于解释这些能力可能由哪些可验证技术实现。不能因为某种机制出现在 open model 中，就反推 OpenAI 或 Anthropic 必然使用它；也不能因为厂商没有披露，就断言它没有使用。

### 4.1 Foundation model 与 Transformer backbone

2017 年提出的 Transformer 用 self-attention 取代 recurrent computation，使 sequence modelling 能够高度 parallelize。核心计算是：

$$
\operatorname{Attention}(Q,K,V)
= \operatorname{softmax}\!\left(\frac{QK^{\mathsf T}}{\sqrt{d_k}}\right)V
$$

这里 Query、Key、Value（Q/K/V）都是输入 hidden states 的 learned projection；multi-head attention 让不同 heads 在不同 representation subspaces 中建模关系。Transformer block 通常还包含 feed-forward network、residual connection 和 normalization。原始论文是 encoder-decoder；多数 text-generation LLM 采用 causal decoder-only variant，只能 attention 到当前位置之前的 tokens。[^9]

Pretraining 的基础 objective 看起来非常朴素：给定前面的 tokens，预测下一个 token。

$$
\mathcal{L}_{\mathrm{pretrain}}
= -\sum_t \log p_\theta\!\left(x_t \mid x_{<t}\right)
$$

但当 model、data 和 compute 同时扩大，这个 objective 会迫使模型压缩语言、code、world knowledge 和许多 task patterns。Scaling Laws 发现 loss 与 parameter count、dataset size、compute 之间在很大范围内呈 power-law；Chinchilla 工作进一步指出，固定 compute 下不能只扩 parameter，training tokens 也必须相应扩展。[^10][^11]

今天常见的 backbone 改进包括：

- Rotary Position Embedding（RoPE）：以旋转方式把 relative position 注入 attention。
- Grouped-Query Attention（GQA）或 Multi-Query Attention（MQA）：减少 inference 时 Key-Value cache（KV cache）的体积。
- FlashAttention：通过 Input/Output-aware（I/O-aware）tiling 减少 GPU High-Bandwidth Memory（HBM）读写；它计算的仍是 exact attention，但 wall-clock time 和 memory 更优。[^12]
- Mixture-of-Experts（MoE）：router 只为每个 token 激活少量 experts，使 total parameters 与 per-token compute 部分解耦；代价是 routing、load balancing、all-to-all communication 和稳定性更难。Switch Transformer 展示了这一路线，DeepSeek-V3 则公开了 671B total parameters、每 token 激活 37B，并结合 DeepSeekMoE 和 Multi-head Latent Attention（MLA）。[^13][^14]
- Multi-Token Prediction、better normalization、activation、optimizer、low-precision arithmetic，以及针对 hardware topology 的 model-system co-design。

需要注意：以上是 frontier LLM 的公共技术库，并不等于 Claude Fable 5.1 已被确认采用其中每一项。

### 4.2 Data engineering 已经成为核心算法

模型不是“读了整个互联网”这么简单。现实 pipeline 通常包括 collection、license/permission management、language and domain balancing、quality scoring、deduplication、toxicity/privacy filtering、benchmark decontamination、document packing 和 tokenizer training。Data mixture 会直接决定 code、math、多语言、专业知识与价值倾向。

现代 frontier training 越来越依赖 synthetic data：强模型生成 explanations、problems、solutions、criticisms、preference pairs、tool trajectories，再经 verifier 或 human review 过滤。它能扩大稀缺高质量数据，但也可能造成 model collapse、style homogenization、隐藏错误的自我复制和 benchmark contamination。因此，“更多 tokens”已经让位于“更好的 token budget allocation、curriculum 和 feedback quality”。

公开技术报告展示了数量级：Llama 3 最大公开模型是 405B dense Transformer，支持 128K context，并同时讨论 multilingual、coding、reasoning、tool use 与 multimodal extension；DeepSeek-V3 披露 14.8T pretraining tokens，之后再做 Supervised Fine-Tuning 和 Reinforcement Learning。[^15][^14] 这些开源或开放技术报告是理解 proprietary frontier model 最好的可验证参照，但不能直接当作 OpenAI 或 Anthropic 的内部配方。

### 4.3 从 base model 到 assistant：Post-training

Pretrained base model 学到的是“怎样延续 token distribution”，并不天然知道应该遵循谁的 instruction、何时拒绝、怎样使用 tool 或怎样诚实表达 uncertainty。Post-training 通常有多阶段。

1. **Supervised Fine-Tuning（SFT）**：在高质量 instruction-response demonstrations 上继续训练，让 model 学会对话格式、任务完成方式和基本 tool syntax。
2. **Preference Modelling**：对同一 prompt 的多个 outputs 做 ranking，训练 reward model 或直接训练 preference objective。
3. **Reinforcement Learning from Human Feedback（RLHF）**：用 human preference 训练 reward，再用 Proximal Policy Optimization（PPO）等 RL algorithm 最大化 reward，同时用 Kullback-Leibler divergence（KL divergence）限制 model 不要偏离 reference model。InstructGPT 的经典 pipeline 是 demonstrations → SFT → ranked comparisons → reward model → RLHF；其结果也说明 post-training 质量可以比 parameter count 本身更决定用户体验。[^16]
4. **Direct Preference Optimization（DPO）**：把部分 RLHF 问题改写成对 chosen/rejected pair 的直接 classification-like objective，绕开单独 reward model 和在线 PPO loop，训练更简单稳定。[^17]
5. **Reinforcement Learning from AI Feedback（RLAIF）**：用 AI judge 依据一组原则产生 preference signal，降低全部依靠人工比较的成本。
6. **Rejection Sampling、Distillation、Self-Training**：从多个 candidates 中选择高质量答案，或让小模型学习强模型生成的 traces。

RLHF 不是“让模型获得真理”的算法。Reward model 只近似人类 preference；如果 proxy 有漏洞，policy 可能出现 specification gaming 或 reward hacking。Anthropic 的实验表明，在刻意构造的 training curriculum 中，较轻的 specification gaming 可以罕见地泛化到 reward tampering；这并不证明 production model 会这样做，但说明 post-training 必须同时研究 incentives、monitoring 和 adversarial evaluation。[^18]

### 4.4 Reasoning model 与 test-time compute

普通 LLM 往往在一个 forward-autoregressive trajectory 中快速给答案；reasoning model 则被训练成在输出前或 tool calls 之间使用更长 internal computation。OpenAI 官方文档把 reasoning tokens 描述为模型用于 planning、比较 alternatives、处理 ambiguity、恢复错误和完成 multi-step task 的内部 tokens；较新的模型还支持 interleaved thinking，即在可见输出和 tool calls 之间继续思考。[^19]

这背后包含两类 scaling：

- **Training-time scaling**：扩大 model、data、training compute。
- **Test-time scaling / inference-time compute**：对单个问题投入更多 reasoning tokens、sampling、search、verification、reflection 或 tool interaction。

DeepSeek-R1-Zero 公开展示了仅用大规模 RL 就能涌现较强 reasoning behavior，但存在 readability 和 language mixing；DeepSeek-R1 加入 cold-start data 与 multi-stage training 后再进行 RL，并将 reasoning 能力 distill 到更小 models。[^20] 典型 reasoning RL 使用可自动验证的 reward，例如 math final answer、unit tests、compiler result、formal proof checker，这常称为 Reinforcement Learning with Verifiable Rewards（RLVR）。关键研究问题已经从“能不能生成 Chain-of-Thought（CoT）”转向：

- 怎样避免 reward hacking 和错误 verifier？
- 怎样在 exploration、token cost 和 answer quality 之间分配 compute？
- 怎样把 reasoning 泛化到 open-ended science、software 和 agent task？
- visible CoT 是否忠实反映内部 computation？研究已经表明，自然语言 explanation 可能合理但不 faithful，不能把它直接等同于 model 的真实 causal mechanism。[^21]

### 4.5 Long context、RAG 与 memory

长 context window 让 model 在一次 inference 中处理更多 documents、code、video 或 history。其难点不仅是 nominal token limit，还包括 quadratic attention cost、KV cache、position extrapolation、long-range retrieval、distractor robustness 与“在长文中真正整合信息”。Gemini 1.5 的公开报告展示了跨 text、video、audio 的 million-token context 和长程 retrieval；FlashAttention、sparse/local attention、context parallelism 和 KV compression 则处理系统瓶颈。[^22][^12]

Retrieval-Augmented Generation（RAG）不是扩大 context 的同义词。RAG 先把 external corpus 建成 searchable memory，在回答时 retrieve relevant chunks，再让 generator 根据 evidence 输出；它的优势是 knowledge 可更新、可给 provenance，不必把所有事实写进 weights。经典 RAG 工作将 parametric memory 与 dense-vector non-parametric memory 结合。[^23]

未来系统通常会组合三种 memory：

- **Parametric memory**：存储在 model weights 中，稳定但难精确更新。
- **Contextual working memory**：当前 context window，灵活但昂贵且会溢出。
- **External memory**：search index、database、files、logs、knowledge graph，可更新且可审计，但 retrieval 可能召回错误或遭 prompt injection。

### 4.6 Multimodal model 与 generative world modelling

Multimodal model 的目标不是把 OCR、image classifier 和 chatbot 简单拼接，而是在 shared or coordinated representation space 中对 text、image、audio、video、3D 和 action 建模。

常见技术路径包括：

- Vision Transformer（ViT）把 image 切成 patches，当作 token sequence 处理。[^24]
- Contrastive Language-Image Pre-training（CLIP）用 image-text pairs 训练 image encoder 与 text encoder 在 embedding space 对齐，获得强 zero-shot transfer。[^25]
- Vision encoder + projector/resampler + LLM：把 visual features 映射到 language model 可接收的 token space。
- Native multimodal training：从 pretraining 阶段联合建模多种 modalities，而非事后接一个 vision adapter。
- Image/video generation 常使用 diffusion 或 flow-matching family；Diffusion Transformer（DiT）以 Transformer 替代传统 U-Net backbone，在 latent patches 上执行 denoising。[^26][^27]

更前沿的问题是 **world model**：model 不只识别一帧，而是学习 environment dynamics，预测 action 的 future consequences，并支持 planning。Video generation 提供了部分视觉 dynamics prior，但“生成看起来合理的视频”不等于获得物理上可控、causally correct 的 simulator。

### 4.7 Agentic AI：从回答问题到在环境中完成任务

Agent 通常不是一种全新的 neural architecture，而是 model 与 environment 之间的 closed loop：

$$
\mathrm{observe}
\rightarrow \mathrm{reason/plan}
\rightarrow \mathrm{call\ tool\ or\ act}
\rightarrow \mathrm{receive\ result}
\rightarrow \mathrm{update\ state}
\rightarrow \cdots
$$

ReAct（Reasoning and Acting）研究了 interleaving reasoning traces 与 actions；Toolformer 研究了让 model 学会何时调用 API、传什么 arguments、怎样利用 result。[^28][^29] 在 production system 中，还需要 function calling schema、browser/terminal/database tools、permissions、sandbox、memory、retry、human approval、logging、tracing 和 evaluation harness。OpenAI 的 Agents architecture 也把 model/tool loop、execution environment 与 application server 区分开来；function calling 本质上是让 model 访问 training data 之外的 data 和 actions。[^30][^31]

Agent 的 frontier 不再只是“能不能调用工具”，而是：

- 能否在数小时乃至数天的 long-horizon task 中维持 goal 和 state？
- 能否验证工作、发现失败并 recovery？
- 能否对 irreversible action 请求合适的 human approval？
- 能否抵抗网页、邮件、文档中的 prompt injection？
- 多 agent 是否真的带来 parallel exploration，而不是增加 communication error 和 cost？

### 4.8 Training 与 inference systems

Claude 级 model 的难点有相当一部分是 systems engineering。单卡放不下 weights、gradients、optimizer states 和 activations，因此需要组合：

- Data Parallelism：不同 devices 处理不同 mini-batches，再同步 gradients。
- Tensor Parallelism：把一个 matrix operation 切到多 devices。
- Pipeline Parallelism：把不同 layers 放到不同 stages。
- Expert Parallelism：把 MoE experts 分布到不同 devices。
- Sequence/Context Parallelism：把长 sequence 沿 token dimension 切分。
- Fully Sharded Data Parallel（FSDP）或 Zero Redundancy Optimizer（ZeRO）：shard parameters、gradients 和 optimizer states，降低每个 device 的 memory footprint。[^32]
- Mixed Precision：用 brain floating-point 16-bit（BF16）、IEEE half-precision floating point（FP16）、8-bit floating point（FP8）等格式提高 throughput，同时维护 numerical stability。
- Checkpointing、fault recovery、network topology、collective communication、data-loader throughput 和 observability。

Inference 侧的核心是 latency、throughput、memory 和 cost。KV cache 随 sequence length 增长；PagedAttention 借鉴 operating-system paging 管理动态 KV cache，在其公开实验中让 vLLM 相对当时 systems 提升 2–4 倍 throughput。[^33] 其他技术包括 continuous batching、prefix/prompt caching、quantization、speculative decoding、kernel fusion、model parallel serving 和 routing between small/large models。

### 4.9 Embodied AI 与 AI for Science

Vision-Language-Action model（VLA）把 image、language instruction 和 robot action 接入统一 policy。RT-2 把 robot action 表示为 tokens，并把 Internet-scale vision-language training 与 robot trajectories 联合 fine-tune；OpenVLA 则公开了一个 7B VLA，使用 Llama 2、DINOv2 与 SigLIP，并在 970K real-world robot demonstrations 上训练。[^34][^35] 该方向的瓶颈不是只增大 model：real-world data 昂贵、action representation 与 calibration 易错、closed-loop latency 有限制、安全 failure 会损坏硬件。

AI for Science 则用 specialized architecture、domain constraints 和 experimental feedback 处理科学问题。AlphaFold 3 以更新的 diffusion-based architecture 统一预测 protein、nucleic acid、small molecule、ion 和 modified residue 的 complex structure，展示了 foundation-style learning 与 domain structure 结合的力量。[^36] 下一阶段更困难：从预测已有分布，走向生成 novel hypothesis、设计 experiment、操纵 laboratory tool，并用现实 measurement 闭环验证。

### 4.10 Alignment、safety、security 与 interpretability

能力越强，错误也越可能通过 tools 被放大。Frontier safety 目前至少包括：

- Training-time alignment：SFT、RLHF、RLAIF、Constitutional AI、character training。
- Runtime safeguards：input/output classifier、policy engine、permission、sandbox、rate limit、human approval。
- Evaluation：jailbreak、prompt injection、cyber/bio dual-use、autonomy、deception、sycophancy、bias、privacy。
- Mechanistic Interpretability：研究 internal activations、features 和 circuits，而不是只看输出 explanation。

Anthropic 的 Sparse Autoencoder 工作在 Claude 3 Sonnet 中识别出大量可解释 features，后续 circuit tracing 用 attribution graph 部分追踪 output 的内部计算路径。[^37][^38] 但这仍远未达到“完整读懂模型”：feature coverage、causal completeness、scalability 和 evaluation validity 都是开放问题。

---

## 五、以最新 Claude 为例：到底公开知道什么

### 5.1 先区分 model、reasoning process 与 product system

“Claude”至少有四个层次：

1. **Underlying model weights**：神经网络结构与训练得到的 parameters。
2. **Inference policy**：effort level、reasoning budget、sampling、context management。
3. **Agent scaffold**：system prompt、tools、memory、subtasks、verification loop、Claude Code/Cowork 等 environment。
4. **Safety and product layer**：Constitutional training、runtime classifiers、access tier、fallback、monitoring、policy。

所以，当 Fable 5.1 在 coding 或 long-running research 上显著提高时，原因可能来自更好的 base/pretrained model、更强 post-training、更长 reasoning、更好的 tool-use trajectory、agent harness 改进，或多者共同作用；公开 benchmark 无法唯一识别每一层贡献。

### 5.2 Fable 5.1 / Mythos 5.1 的公开事实

| 问题 | 公开状态 | 可以严谨地说什么 |
|---|---|---|
| 当前 model 身份 | 已公开 | 2026 年 9 月发布；Fable 5.1 与 Mythos 5.1 是同一 underlying model、不同 safeguards/access policy。[^7] |
| 主要能力 | 已公开但多为厂商 self-report | coding、knowledge work、long-running problem solving、agentic scientific research；多个 effort levels 形成 quality-cost trade-off。[^7] |
| Architecture family | 未完整公开 | 可合理推断它继承 modern large-language-model/Transformer lineage，但不能确认 block design、dense/MoE、attention variant 或 parameter count。 |
| Input/output modalities | 产品能力部分公开 | Claude family 支持 language、visual analysis、tools；但不能据此推出 visual encoder、fusion mechanism 或 pretraining mixture。 |
| Pretraining data | Fable 5.1 未披露完整配方 | 较早 Claude 4 system card 披露过 public Internet、third-party non-public data、contractor/labeling data、opt-in user data、Anthropic-generated data，并使用 deduplication/classification；不能自动假定 Fable 5.1 的比例相同。[^39] |
| Alignment training | 方法家族已公开 | Anthropic 公布 Claude 4 使用 human feedback、Constitutional AI 与 selected character traits；2026 Constitution 被用于多个 training stages 和 synthetic-data generation。[^39][^40] |
| Reasoning | family behavior 已公开 | Claude 4 被称为 hybrid reasoning model，支持 standard 与 extended thinking；Fable 5.1 公开提供 effort levels，但内部 reasoning-training recipe 未披露。[^39][^7] |
| Exact training compute | 未公开 | Anthropic 公司层面披露大规模 Trainium 基础设施，但没有把具体 chips、tokens、Floating-Point Operations（FLOPs）和 energy 精确归因到 Fable 5.1。[^43] |
| Full post-training recipe | 未公开 | 不知道 SFT/RL/RLAIF 各阶段数据量、reward composition、online RL environments、sampling policy 和 curriculum。 |

### 5.3 Constitutional AI 是怎样工作的

Constitutional AI（CAI）是 Anthropic 公开最充分、最有辨识度的技术之一。经典版本有两个主要阶段：

1. **Supervised phase**：model 对 harmful prompt 先生成 response；再依据 constitution 中抽取的 principle 进行 self-critique；然后生成 revised response；最后把 revised responses 用于 supervised learning。
2. **Reinforcement phase**：对同一 prompt 采样多个 responses；AI judge 根据 constitution 比较 preference；用这些 AI preferences 训练 preference model；再以其作为 reward 做 RL，因此称 Reinforcement Learning from AI Feedback（RLAIF）。[^41]

它的意义不是把伦理写成 if-else rules，而是用 natural-language principles 产生 scalable supervision。2026 版 Claude Constitution 进一步强调四层 priority：broadly safe、broadly ethical、compliant with Anthropic guidance、genuinely helpful；Anthropic 说明 constitution 不只在 inference 时当 prompt 使用，也参与 synthetic conversations、revisions 和 rankings 等 training data 的生成。[^40]

但 CAI 也有局限：constitution 由谁制定、principles 是否冲突、AI judge 是否理解专业情境、模型会不会学会表面合规、是否过度拒绝，仍需要 human oversight、red teaming 与 runtime safeguards。

### 5.4 如果根据公开行业技术画一个“可能的 Claude training pipeline”

下面是 **conceptual reconstruction，而不是 Fable 5.1 的泄露配方**：

```text
raw text/code/image/data
        ↓
permission + cleaning + filtering + deduplication + quality/domain mixture
        ↓
large-scale self-supervised pretraining
        ↓
continued/mid-training: long context, code, multilingual, multimodal, tools
        ↓
SFT on high-quality instruction and tool trajectories
        ↓
human preference + Constitutional AI / RLAIF + character training
        ↓
reasoning and agent post-training with tasks, verifiers, environments
        ↓
red teaming + capability/safety evaluations + targeted mitigations
        ↓
deployment with effort control, tools, memory, classifiers, sandbox, monitoring
```

这张图中，Anthropic 明确公开过的主要是 Claude lineage 的 broad data categories、human feedback、CAI、character training、hybrid/extended thinking 和 evaluation/safeguard framework；其余细粒度配置只能依据 open technical reports 理解原理，不能冒充 Claude-specific fact。

### 5.5 为什么它看起来比基础 Deep Learning model 强几个时代

差异不只来自 parameter 数量：

- Broad pretraining 让一个 objective 覆盖 language、code、math、knowledge 和 task imitation。
- Scaling 与高质量 data mixture 提高 representation 和 in-context learning。
- Post-training 把“续写器”塑造成 instruction-following assistant。
- Reasoning training 和 test-time compute 让模型在难题上花更多 computation。
- Tools 把静态 weights 扩展到 web、code execution、database 和 computer action。
- Agent scaffold 提供 state、iteration、verification 和 recovery。
- Multimodal training 把 visual/audio evidence 接入 reasoning。
- Distillation、routing、caching 和 optimized serving 让这些能力可负担地交付。
- Safety and evaluation 使模型能在真实用户和高权限 environment 中部署。

因此，“Transformer 就是矩阵乘法，为何 Claude 如此强”与“CPU 也是 transistor，为何 operating system 如此复杂”类似：基本 operation 并不复杂，复杂性来自规模、data、objective、system composition、feedback loop 与 engineering discipline。

---

## 六、从入门 Deep Learning 到 Frontier AI 的具体鸿沟

| 鸿沟 | 入门课通常到哪里 | Frontier 还要求什么 | 达标信号 |
|---|---|---|---|
| Mathematics | gradient descent、basic probability | optimization dynamics、information theory、statistical inference、RL objective、matrix/tensor reasoning | 能从 paper 的 loss 推导 gradient 和 assumptions |
| Model architecture | MLP、CNN、RNN、basic attention | decoder-only Transformer、RoPE、GQA/MQA、MoE、multimodal fusion、long context | 能从零实现并训练小 Transformer |
| Data | 下载 clean dataset | web-scale cleaning、dedup、mixture、synthetic data、decontamination、governance | 能解释性能变化是 data 还是 model 导致 |
| Training | single-GPU training loop | mixed precision、distributed parallelism、checkpoint、failure recovery、profiling | 能稳定训练 multi-GPU model 并定位 bottleneck |
| Post-training | supervised classification | SFT、reward model、DPO/PPO、Group Relative Policy Optimization（GRPO）、RLVR、distillation、safety tuning | 能构建 preference dataset 并做 controlled comparison |
| Inference | `model.generate()` | KV cache、batching、quantization、speculative decoding、serving Service-Level Objective（SLO） | 能测 latency/throughput/memory/quality trade-off |
| Agent | prompt + one API call | tool schema、state machine、memory、permissions、sandbox、retry、eval harness | agent 能在 hidden test tasks 中可靠完成而非只演示一次 |
| Research | 跑通 notebook | hypothesis、baseline、ablation、statistics、error taxonomy、reproducibility | 能回答“为什么有效、何时无效、证据是否足够” |

另外还有三个不能靠多上几门课完全消除的现实差距：

1. **Scale gap**：个人可以训练 10M–500M parameter model、fine-tune 1B–14B open models，却无法独立运行 frontier-scale pretraining。
2. **Tacit knowledge gap**：大模型实验室的 recipe 包含大量未写进 paper 的 data curation、stability debugging、infrastructure 和 evaluation know-how。
3. **Disclosure gap**：closed labs 有意不公开 architecture、data 和 safety-sensitive details；这里的正确能力是区分 evidence 与 inference，而不是填空式猜测。

---

## 七、面向刚开始学习 Deep Learning 的 12–18 个月路线

下面假设每周投入约 12–18 小时；如果只有 6–8 小时，可把时间近似延长一倍。目标是“能读懂并复现一个 LLM/agent/reasoning 子方向的 paper”，不是训练 commercial frontier model。

### Phase 0（持续补齐）：Programming、Math、CS fundamentals

学习内容：Python、PyTorch tensor/autograd、Linux、Git、debugging；Linear Algebra、Calculus、Probability、Statistics；Data Structures and Algorithms。不要等数学全部学完才写 model，而应让公式和 experiment 循环推进。

完成标准：

- 不依赖 high-level trainer，写出 linear regression、MLP、CNN training loop。
- 能解释 forward pass、loss、backpropagation、optimizer step、train/eval mode。
- 能定位 overfitting、data leakage、shape/device/dtype 问题。
- 能读懂 vectorized tensor code，而非只会复制 notebook。

### Phase 1（第 1–3 个月）：扎实掌握现代 Deep Learning

重点学习 representation、optimization、normalization、regularization、residual connection、CNN、sequence model、attention。理解 cross-entropy、maximum likelihood、AdamW、learning-rate warmup、weight decay、dropout、Batch Normalization（BatchNorm）、Layer Normalization（LayerNorm）与 Root Mean Square Layer Normalization（RMSNorm）。

项目：在同一 dataset 上比较 MLP、CNN、small ViT；控制 parameter count 和 training compute，做 error analysis。输出一份短 report，不能只报 best accuracy。

### Phase 2（第 3–5 个月）：从零实现 Transformer 与小型 language model

学习 tokenizer、embedding、causal mask、multi-head self-attention、feed-forward block、residual stream、position encoding、teacher forcing、sampling、perplexity。

项目：

- 自己实现 decoder-only Transformer，不调用现成 Transformer block。
- 在小语料上训练 10M–100M parameter model。
- 比较 context length、model width/depth、data size、learning rate；验证一个小型 scaling curve。
- 加入 KV cache，比较 prefill 与 decode latency。

完成标准：能手画 tensor shapes，解释为什么 training 可 parallelize 而 autoregressive decoding 仍 sequential；能从 loss curve 判断 underfitting、overfitting 和 instability。

### Phase 3（第 5–8 个月）：Open LLM engineering 与 post-training

学习 Hugging Face ecosystem、Parameter-Efficient Fine-Tuning（PEFT）、Low-Rank Adaptation（LoRA）、quantization、instruction template、SFT、preference data、DPO、basic RLHF/RLVR、evaluation。

项目：

- 选择 1B–7B open-weight model，在一个窄 domain 做 LoRA 或 Quantized Low-Rank Adaptation（QLoRA）SFT。
- 建立 train/dev/test split，检查 contamination。
- 用 base、SFT、DPO 三个 checkpoints 做 blind pairwise evaluation。
- 同时报 task success、hallucination、refusal、latency 和 memory，不只报一个 benchmark。

不要把“成功运行 fine-tuning script”视为研究结果。最重要的问题是：improvement 来自新增知识、format imitation、长答案偏好，还是 evaluator bias？

### Phase 4（第 8–11 个月）：Reasoning、RAG 与 agent

学习 Chain-of-Thought、self-consistency、verifier、search、RLVR、RAG、embedding/retrieval、reranking、tool calling、ReAct、agent state、memory、prompt injection、sandbox 和 human-in-the-loop。

建议做两个项目：

1. **Reasoning project**：选数学或 code task，比较 direct answer、CoT、best-of-N、verifier reranking、small-scale GRPO/RLVR；把额外 token cost 纳入横轴。
2. **Agent project**：让 model 在隔离 repository 中修复小 bugs，工具只允许 file read、test 和 patch；用 hidden tasks 测 success rate，并分类 planning、tool、state、verification failures。

完成标准：agent 不是在一个 demo 上“看起来聪明”，而是在固定 budget 下对一组 unseen tasks 有可重复的 success rate。

### Phase 5（第 11–14 个月）：Systems、efficiency 与 reproducibility

学习 GPU memory composition、mixed precision、gradient accumulation、activation checkpointing、FSDP、tensor/pipeline parallelism、profiling、vLLM/PagedAttention、quantization。

项目：对同一个 open model 测 batch size、sequence length、precision、quantization 对 latency、throughput、peak memory 和 quality 的影响；写出 bottleneck analysis。即使你最终研究 alignment 或 multimodal，systems literacy 也会显著提高实验质量。

### Phase 6（第 14–18 个月）：选择一个 specialization 做真正 research

不要同时追所有 frontier。选择一个 narrow question：

- Reasoning and verification
- LLM post-training and alignment
- Long-context and memory
- Agent reliability and security
- Multimodal learning
- Efficient training/inference
- Mechanistic interpretability
- Embodied AI / VLA
- AI for Science

然后完成：literature map → strongest baseline reproduction → failure taxonomy → one hypothesis → matched ablation → statistical analysis → negative-result criteria → paper-style report。能把一个问题做窄、做实，比同时“懂一点所有热门词”更接近 researcher。

## 八、推荐的最小 paper reading chain

阅读论文不要按发布日期随机刷，而应按“一个技术为什么出现”组织。

1. **Transformer**：Attention Is All You Need。目标是能推导 attention shapes、mask 与 complexity。[^9]
2. **Scaling**：Scaling Laws；Chinchilla。目标是理解 model/data/compute allocation。[^10][^11]
3. **Open foundation model**：Llama 3 technical report。目标是看到 architecture、data、post-training、safety 如何组成完整 model family。[^15]
4. **Sparse and efficient architecture**：Switch Transformer；DeepSeek-V3。目标是理解 MoE、routing、MLA 和 systems co-design。[^13][^14]
5. **Instruction and preference alignment**：InstructGPT；DPO。目标是区分 SFT、reward model、RLHF 和 direct preference learning。[^16][^17]
6. **Constitutional AI**：Harmlessness from AI Feedback。目标是理解 critique/revision 和 RLAIF。[^41]
7. **Reasoning RL**：DeepSeek-R1。目标是分析 cold start、RL、distillation 与 reward design。[^20]
8. **Retrieval and tools**：RAG；ReAct；Toolformer。目标是理解 weights 之外的 knowledge/action interface。[^23][^28][^29]
9. **Multimodal**：ViT、CLIP、Gemini 1.5 report。目标是理解 visual tokens、contrastive alignment 与 long multimodal context。[^24][^25][^22]
10. **Interpretability and safety**：Scaling Monosemanticity/circuit tracing、CoT faithfulness、reward tampering。目标是学会不把 plausible explanation 当 causal evidence。[^37][^38][^21][^18]

每读一篇，至少回答六个问题：research question 是什么；strongest baseline 是什么；核心 intervention 是什么；保持了哪些变量相同；metric 是否真的测到 claim；什么结果会 falsify hypothesis。

---

## 九、当前最重要的困难和挑战

### 9.1 Reliability 仍然没有解决

LLM 能在大量 tasks 上表现出色，但仍可能 hallucinate、遗漏 constraint、在 prompt paraphrase 后改变答案。更强 benchmark score 不等于 calibrated confidence，也不等于 high-stakes reliability。Agent 把单步 error 变成多步 compounding error，因此 verification、rollback、permission 和 observability 是核心研究，而非产品附件。

### 9.2 Reasoning 的正确性、成本和 faithfulness 相互纠缠

增加 reasoning tokens 往往提高 accuracy，但也提高 latency/cost，并可能产生更长的错误 rationalization。可验证 task 上 RLVR 很有效，open-ended task 却缺少可靠 reward。Visible CoT 也不应自动被视为 inner reasoning 的忠实解释。[^19][^21]

### 9.3 Long context 不等于 long-term memory

把一百万 tokens 塞进 context 仍可能检索失败、被 distractor 干扰，并产生巨大的 prefill/KV cost。真正 memory system 需要 selection、compression、update、forgetting、provenance 和 privacy policy；这仍是 agent 的主要瓶颈。

### 9.4 Data 正面临质量、版权、隐私和递归污染

高质量 human text/code 有限，synthetic content 占比上升。未来 model 可能越来越多地训练在 model-generated data 上，需要追踪 provenance、过滤低质量 loop，并处理 consent、licensing 和 personal data。

### 9.5 Evaluation 追不上 capability

Static benchmark 会饱和、泄漏或被专门优化。Frontier evaluation 正转向 contamination-resistant、interactive、agentic、expert-designed 和 real-world task；但这也更昂贵、variance 更大、难复现。厂商发布的 benchmark 必须视为 self-reported evidence，而不是独立审计结论。

### 9.6 Interpretability 仍然只照亮局部

Sparse Autoencoder 和 circuit tracing 能找到有意义 features/pathways，但还无法覆盖所有 computation，更无法保证发现隐藏的危险机制。解释工具本身也可能选择性展示易解释的部分。

### 9.7 Physical grounding 与 continual learning 很弱

机器人和 world model 缺少像文本互联网那样便宜、广泛的数据；sim-to-real gap、sensor/action delay、safety constraint 与 hardware variation 都很难。模型还不能像人一样在 deployment 中持续吸收经验而不 catastrophic forgetting 或引入安全回归。

### 9.8 Compute、energy 与 concentration

Frontier pretraining 和 inference 需要巨额 accelerator、electricity、network 与 engineering team，导致 research transparency 与参与门槛下降。算法效率、small model、open evaluation 与共享 compute infrastructure 因此不仅是工程问题，也是科研生态问题。

---

## 十、适合新研究者进入的方向

以下方向按“个人或小组可做出可信实验”的程度排序，而不是按商业热度排序。

| 方向 | 可检验问题示例 | 最小实验 | 资源门槛 |
|---|---|---|---|
| Evaluation and error analysis | 哪类 prompt change 会系统性破坏 reasoning/agent？ | 公开 models + 自建 hidden test + error taxonomy | 低 |
| RAG reliability | long context 与 retrieval 在何种 evidence distribution 下各自失败？ | 同一 generator、matched token budget、可控 corpus | 低 |
| Verifier robustness | verifier 是否奖励形式正确但推理错误的答案？ | 数学/code tasks + adversarial solutions | 低至中 |
| Chinese reasoning/data | 中文专业语境中的 evaluation 是否被 translation artifact 污染？ | bilingual matched benchmark + human audit | 低至中 |
| Agent memory | summary、event log、vector memory 哪种能减少 long-horizon state loss？ | sandbox task suite + fixed model/tool/token budget | 中 |
| Tool security | prompt injection 通过网页/文档如何跨越 instruction hierarchy？ | 隔离 agent environment + attack/defense benchmark | 中 |
| Post-training data quality | 少量高质量 preference data 何时优于大量 synthetic pairs？ | 1B–7B model + SFT/DPO ablation | 中 |
| Mechanistic interpretability | 某类 tool decision 或 refusal 是否存在 causal feature/circuit？ | small open model + activation intervention | 中 |
| Efficient inference | quantization/cache policy 如何影响 long-context quality-cost frontier？ | 单机多配置 profiling | 中 |
| VLA adaptation | action representation 或 temporal alignment 如何影响 closed-loop success？ | simulator 或低成本 robot + open VLA | 中至高 |

最值得避免的“伪研究方向”是：只把一个新 prompt、一个 vector database 或一个 agent framework 接上现成 API，然后在几个 cherry-picked examples 上宣布新 architecture。Reviewer-defensible research 需要 matched baseline、controlled variable、held-out evaluation、uncertainty 和 failure analysis。

## 十一、你现在最应该采取的策略

如果你刚开始 Deep Learning，最优顺序不是每天追最新 model release，而是采用 **T-shaped learning**：横向理解整个 AI stack，纵向先打穿一个小型 Transformer → SFT/DPO → RAG/tool agent → evaluation pipeline。

接下来六个最有价值的 milestones 是：

1. 手写并训练一个 small Transformer。
2. 在 open model 上完成一次有严格 test split 的 LoRA SFT。
3. 完成一次 SFT vs DPO 的 blind evaluation。
4. 构建一个带 citation 的 RAG system，并系统测 retrieval failure。
5. 构建一个 sandboxed tool agent，用 hidden tasks 而不是 demo 测 success。
6. 复现一篇 paper 的主要 table，并做一个原论文没有的、能 falsify claim 的 ablation。

做到这六件事，你与 frontier AI 的差距就不再是“看不懂”，而会转变为更专业、更具体的问题：缺多少 compute、缺哪类 data、哪个 assumption 未验证、哪个 component 产生 improvement。这个转变本身，就是从 course learner 进入 research 的标志。

## 十二、术语速查

- **AI — Artificial Intelligence**：人工智能的总称。
- **ML — Machine Learning**：从 data 学习 prediction/decision rule 的方法。
- **DL — Deep Learning**：以多层 neural network 学习 representation 的 ML 分支。
- **LLM — Large Language Model**：大语言模型。
- **SFT — Supervised Fine-Tuning**：监督微调。
- **RL — Reinforcement Learning**：强化学习。
- **RLHF — Reinforcement Learning from Human Feedback**：使用人类反馈构造 reward 的强化学习。
- **RLAIF — Reinforcement Learning from AI Feedback**：使用 AI feedback 的强化学习。
- **RLVR — Reinforcement Learning with Verifiable Rewards**：使用可程序化验证 reward 的强化学习。
- **CoT — Chain-of-Thought**：模型生成的分步推理文本；不保证 faithful。
- **MoE — Mixture-of-Experts**：每个 token 只激活部分 experts 的 sparse model。
- **RAG — Retrieval-Augmented Generation**：检索增强生成。
- **KV cache — Key-Value cache**：autoregressive decoding 中缓存 attention Key/Value 的内存结构。
- **VLA — Vision-Language-Action model**：从视觉和语言条件产生动作的模型。
- **MLOps — Machine Learning Operations**：训练、部署、监控与维护 ML system 的工程体系。
- **FLOPs — Floating-Point Operations**：浮点运算次数，常用于近似表示 compute。
- **Ablation study**：移除或替换 component，以识别其 causal contribution 的实验。
- **Frontier model**：在广泛能力或关键能力上接近当前最高水平、训练和部署成本很高的 model；它不是严格统一的学术分类。

---

## Sources

[^1]: Carnegie Mellon University, “[B.S. in Artificial Intelligence Curriculum](https://www.cs.cmu.edu/bs-in-artificial-intelligence/curriculum),” accessed 2026-09-15.
[^2]: MIT Course Catalog, “[Artificial Intelligence and Decision Making (Course 6-4)](https://catalog.mit.edu/degree-charts/artifical-intelligence-decision-making-course-6-4/),” accessed 2026-09-15.
[^3]: Stanford Computer Science, “[B.S. Computer Science Tracks Overview — Artificial Intelligence](https://www.cs.stanford.edu/bachelors-compsci-tracks-overview),” accessed 2026-09-15.
[^4]: 清华大学无穹书院，《[2025级人工智能专业培养方案](https://wqc.tsinghua.edu.cn/syjx/pyfa.htm)》，accessed 2026-09-15。
[^5]: 北京大学人工智能研究院，《[为什么选择北大通用人工智能实验班？](https://www.ai.pku.edu.cn/info/1064/1888.htm)》，accessed 2026-09-15。
[^6]: 浙江大学，《[人工智能专业本科课程结构](https://zdzsc.zju.edu.cn/2024/0613/c87523a2932609/page.htm)》，accessed 2026-09-15。
[^7]: Anthropic, “[Claude Fable 5.1 and Claude Mythos 5.1](https://www.anthropic.com/claude-fable-and-mythos-5-1),” September 2026.
[^8]: Anthropic, “[Model System Cards](https://www.anthropic.com/system-cards),” accessed 2026-09-15.
[^9]: Vaswani et al., “[Attention Is All You Need](https://arxiv.org/abs/1706.03762),” NeurIPS 2017.
[^10]: Kaplan et al., “[Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361),” 2020.
[^11]: Hoffmann et al., “[Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556),” 2022.
[^12]: Dao et al., “[FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135),” NeurIPS 2022.
[^13]: Fedus, Zoph, and Shazeer, “[Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](https://arxiv.org/abs/2101.03961),” JMLR 2022.
[^14]: DeepSeek-AI et al., “[DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437),” 2024.
[^15]: Grattafiori et al., “[The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783),” 2024.
[^16]: Ouyang et al., “[Training Language Models to Follow Instructions with Human Feedback](https://arxiv.org/abs/2203.02155),” NeurIPS 2022.
[^17]: Rafailov et al., “[Direct Preference Optimization: Your Language Model Is Secretly a Reward Model](https://arxiv.org/abs/2305.18290),” NeurIPS 2023.
[^18]: Anthropic, “[Sycophancy to Subterfuge: Investigating Reward Tampering in Language Models](https://www.anthropic.com/research/reward-tampering),” 2024.
[^19]: OpenAI Docs, “[Reasoning Models](https://developers.openai.com/api/docs/guides/reasoning),” accessed 2026-09-15.
[^20]: DeepSeek-AI et al., “[DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948),” 2025.
[^21]: Turpin et al., “[Language Models Don’t Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting](https://arxiv.org/abs/2305.04388),” NeurIPS 2023.
[^22]: Gemini Team et al., “[Gemini 1.5: Unlocking Multimodal Understanding Across Millions of Tokens of Context](https://arxiv.org/abs/2403.05530),” 2024.
[^23]: Lewis et al., “[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401),” NeurIPS 2020.
[^24]: Dosovitskiy et al., “[An Image Is Worth 16×16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929),” ICLR 2021.
[^25]: Radford et al., “[Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020),” ICML 2021.
[^26]: Ho, Jain, and Abbeel, “[Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239),” NeurIPS 2020.
[^27]: Peebles and Xie, “[Scalable Diffusion Models with Transformers](https://arxiv.org/abs/2212.09748),” ICCV 2023.
[^28]: Yao et al., “[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629),” ICLR 2023.
[^29]: Schick et al., “[Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761),” NeurIPS 2023.
[^30]: OpenAI Docs, “[Agents API Architecture](https://developers.openai.com/api/docs/guides/agents-api/architecture),” accessed 2026-09-15.
[^31]: OpenAI Docs, “[Function Calling](https://developers.openai.com/api/docs/guides/function-calling),” accessed 2026-09-15.
[^32]: Rajbhandari et al., “[ZeRO: Memory Optimizations Toward Training Trillion Parameter Models](https://arxiv.org/abs/1910.02054),” SC 2020.
[^33]: Kwon et al., “[Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180),” SOSP 2023.
[^34]: Brohan et al., “[RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://arxiv.org/abs/2307.15818),” CoRL 2023.
[^35]: Kim et al., “[OpenVLA: An Open-Source Vision-Language-Action Model](https://arxiv.org/abs/2406.09246),” CoRL 2024.
[^36]: Abramson et al., “[Accurate Structure Prediction of Biomolecular Interactions with AlphaFold 3](https://www.nature.com/articles/s41586-024-07487-w),” Nature 630, 2024.
[^37]: Anthropic, “[The Engineering Challenges of Scaling Interpretability](https://www.anthropic.com/research/engineering-challenges-interpretability),” 2024.
[^38]: Anthropic, “[Open-Sourcing Circuit-Tracing Tools](https://www.anthropic.com/research/open-source-circuit-tracing),” 2025.
[^39]: Anthropic, “[Claude 4 System Card](https://www-cdn.anthropic.com/6be99a52cb68eb70eb9572b4cafad13df32ed995.pdf),” May 2025, pp. 5–7.
[^40]: Anthropic, “[Claude’s Constitution](https://www.anthropic.com/constitution),” January 2026.
[^41]: Bai et al., “[Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073),” 2022.
[^42]: OpenAI Docs, “[Models](https://developers.openai.com/api/docs/models),” accessed 2026-09-15.
[^43]: Anthropic, “[Anthropic and Amazon Expand Collaboration for Up to 5 Gigawatts of New Compute](https://www.anthropic.com/news/anthropic-amazon-compute),” April 2026.
