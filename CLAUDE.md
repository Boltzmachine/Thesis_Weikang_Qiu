# CLAUDE.md

When making slides, keep text minimal and sufficient.

Yale PhD dissertation (LaTeX). Main document: `Disseration.tex` (note the typo in the
filename — it is intentional, do not "fix" it).

## Build

```
make          # latexmk -> build/Disseration.pdf
make watch    # latexmk -pvc, continuous preview
make view     # build and open the PDF
make clean    # latexmk -c   (aux files)
make distclean# latexmk -C   (everything, incl. build/)
```

- Engine is **pdflatex + bibtex** (`.latexmkrc`), output goes to `build/`.
- Always build the whole document (`Disseration.tex`), never a chapter file alone.
- When checking a change compiles, run `make` and look for `!` / `.tex:LINE:` errors in
  the log; warnings about badboxes and undefined refs on a first pass are normal.

## Layout

- `Disseration.tex` — preamble, title/advisor/date metadata, and the `\include` /
  `\input` list of chapters.
- `macros.tex` — all extra packages and custom commands shared by the chapters
  (`\alg`, `\sail`, `\etal`, `\xhdr`, math operators, algorithm2e config).
  New macros go here, not in a chapter file.
- `abstract.tex`, `acknowledgements.tex`, `Introduction.tex` — front matter and Ch. 1.
- `PHIL/` — one example paper turned into a chapter group. `PHIL/main.tex` sets the order of
  `000intro`, `002preliminaries`, `001related_work`, `003approach`, `004experiments`,
  `005conclusion` (the file numbering does **not** match the reading order — follow
  `main.tex`). Figures live in `PHIL/figures/` and are referenced as
  `figures/xxx.png` thanks to `\graphicspath` in `Disseration.tex`.
- `bibfile.bib` — the single bibliography; style is `plainnat` with `natbib`.
- `yalephd.cls` — the Yale GSAS class file. Treat as vendored: don't edit it; if
  formatting needs to change, do it in the preamble of `Disseration.tex`.

## Conventions

- Citations use natbib: `\citep{key}` for parenthetical, `\citet{key}` inline.
- New references get appended to `bibfile.bib`; keep keys in the existing style and
  don't reformat or reorder unrelated entries.
- Labels are prefixed by kind: `chapter:`, `sec:`, `fig:`, `tab:`, `eq:`.
- `macros.tex` defines review-annotation commands (`\rex`, `\jure`, `\michal`,
  `\update`) that render colored inline notes. Don't leave new ones in final text.
- Adding a chapter: create the `.tex`, then `\include`/`\input` it from
  `Disseration.tex` (or from `PHIL/main.tex` for that group).

## Writing

- Academic prose, third person, past tense for experiments. Match the voice of the
  surrounding chapter rather than imposing a new one.
- Don't silently rewrite passages that were not asked about; edits should be scoped to
  what the user requested.

## `[C: ...]` author notes

The author leaves inline notes in the `.tex` source as `[C: 说明]` — an instruction
about the sentence or paragraph the note sits in, written in English or Chinese. A note
is never text to be inserted into the document.

To resolve one: revise the surrounding prose so it satisfies the note, delete the note
and any doubled space it leaves, and leave every other paragraph byte-identical.

`tools/cwatch.sh` is a background daemon that does this automatically — it polls the
`.tex` files, waits for a file to stop changing, backs it up to `.cwatch/backups/`, and
runs a headless `claude -p` on it. Controls: `make cwatch` / `cwatch-stop` /
`cwatch-status` / `cwatch-log`. It gives up on a note after two failed passes.

把https://www.overleaf.com/project/65b48eb2ee466089c846f6eb也加入dissertation，

## General Notes

合并paper时，appendix统一先不放（但是下载要下载的）
macro全文统一
如果你要copy一些东西，请不用verbose的输出内容，以免出现错误。尽量使用程序，例如cat来合并bib。但是，你需要保证rewind的时候也能撤销这些。

overleaf的token在@.latex_token

# Thesis Outline

**Weikang Qiu** · Department of Computer Science, Yale University

> **`outline.md` 是结构的唯一权威来源。** 本节只是它的摘要；两者不一致时以 `outline.md` 为准，
> 并回来同步这一节。dissertation 的结构后面还会改，所以**章节编号未定**——下面只固定 Part 的
> 划分和 Part 内的顺序，不要在正文、图或幻灯片里写死 "Ch N"。

---

## 论证主线

1. **问题** — 语言真的是 mind 与 world 之间最好的接口吗？现有范式（text-to-X、X-to-text、语音助手）默认是。
2. **证据** — 不是。这条信道 **两个方向都有损** ：进来的方向是带宽差（说话 100–150 wpm vs 思维 400–800 wpm）与不可言说性，出去的方向由 RepQA 实测论证。
3. **主张** — 造一条绕开语言的直接通路。这需要三件事。
4. **结构** — 先真懂脑信号 → 接到世界的语义空间 → 驱动具身。三个 Part。

---

## 章节骨架

### Introduction

### The Premise: The Limits of Language as an Interface

**RepQA** `一作`

把「语言有损」从修辞变成测量。prospectus 目前用 wpm 统计和维特根斯坦支撑前提，那是引文不是证据。

* **用机制，不用效应量。** case study 中模型为降低阅读难度，把胆固醇药物的五个类别压成一句不加区分的话，只留下 statins；酒精依赖那例只留 craving。这是信息在压缩中被丢掉的字面演示。
* **别领着讲数字。** grade level 降 41.4%、professional score 降 73.3%，而准确率只掉 3–5 点（Fact 74.56% → 69.82%），Qwen 上只掉 1.3 点。拿这组数论证「语言有损」，敌意读法立刻来：3 个点换 73%，说明语言是条挺划算的信道。
* **该讲方向与普遍性。** 所有模型、所有类别方向一致，没有配置能免费拿到可读性。论点是 trade-off 系统性、绕不开，不是它很大。这个说法不依赖效应量，砸不掉。

---

### PART 1 · The Foundation — Models for Brain Signals

> **挑战** ：现有方法基本照搬 CV/NLP 模型，不带神经先验，既给不出神经科学洞见，性能也次优。

脑网络的约定：节点是按某个图谱分好的脑区（区内体素取平均），边是两两之间的 Pearson 相关。

三个方向：**发现**（图谱没记录的结构）→ **内建**（已确立的结构搭进架构）→ **反向搬出**。

**1. HyBRiD** `一作` — 发现。

大部分脑网络工作只做两两交互，但绝大多数脑功能是多个脑区同时参与；高阶关系的数量是指数的，枚举不了，现有做法要么只枚举低阶（度 ≤ 3）要么按邻近/可重构性挑，超边数量还被固定成节点数——所以只能学出来。目标是 MIMR：对结果尽可能有信息量（直接最大化 I(H;Y)）、彼此尽可能不冗余（multi-head drop-bottleneck 给 I(H;X) 一个可计算上界），两项端到端一起优化。用 CPM 衡量超边质量：ABIDE 平均 +8.8%，ABCD 七个数据集平均 +12.1%。

**2. Neuro-informed attention（MindLLM 编码器）** `一作` — 内建，fMRI。

障碍是每个被试的响应体素在数量和空间分布上都不一样；现有做法用不可学的池化或采样把尺寸对齐，信息和空间含义一起丢。做法：可学习 query 跨注意力聚合体素；**key 里不放 fMRI 值，只放位置**——一个体素的位置本身就编码了它的功能角色；再把多套脑图谱的分区嵌入拼进 key，把已确立的分区当先验。收敛更快，且该先验跨被试可共享。

**3. FA-EEG** — 内建，EEG。

左右手运动想象产生的是互为镜像的 EEG。普通编码器得从稀缺数据里把这个对称性重新学出来；用 frame averaging 在镜像群上做平均，对称性是**精确**成立的，不是学出来的软偏好，对任何输入、任何 backbone 都成立。省下的容量留给真正的偏侧化信号。

**4. SWA** — 反过来：把脑网络的性质搬到一个跟脑完全无关的模型上。

以注意力头为节点、以流体推理题上的激活相似度为边建图：小世界指数越高、流体推理越好，六个开源模型上顺序一致。再用剪枝验证：按 core/bridge 分数决定每个头和每一层的稀疏度，SWA 在六个模型上都把小世界指数保住得最好，WikiText 困惑度在每一个「模型 × 稀疏度」的格子里都最优。

### PART 2 · The Bridge — From Signals to Representations

> **挑战** ：Part 1 全程待在脑内——那些模型解释的是信号自己，没有一个把脑活动接到外部世界的语义上。而脑数据稀缺、昂贵、跨被试差异大，监督信号才是瓶颈。

**1. PRISM — I（对齐到哪儿）** `三作`

第一个问题不是怎么造桥，是造到哪儿。把 fMRI 和预训练的视觉、语言、视觉–语言表征逐一比对：**fMRI 离语言模型的语义空间更近**。这决定了后面所有工作的落点。辩护时用弱结论：在我们**实际拥有**的表示空间里，文本是 fMRI 最容易被学出来的那个；不是说大脑本身是语言式的（比较的一侧是人写的 caption、另一侧是图像，不是同类比较）。

**2. Brain Instruction Tuning（MindLLM）** `一作`

fMRI-to-text 不是简单翻译被试想说的话，而是学一个尽量丰富的 multi-purpose / multi-function 表征。监督来自一次 **join**：NSD 的被试看的是 MSCOCO 图，而 MSCOCO 被标注了十年——图像就是连接键，把一条 fMRI 记录和早就写好的文本连起来。98 万段多轮对话、15 个数据集，**没有新扫一次脑**。四族脑功能：感知、记忆与知识、语言与符号、复杂推理；其中「描述被试上一张看过的图」是自己推出来的任务，标签来自 NSD 的试次顺序，是唯一一个问记忆的任务。

captioning +3.32%；通用解码 +12.0%（其中 28.0% 来自 BIT）；两个 BCI 相关的新任务 +13.5%（BIT 贡献 25.0%）；没见过的被试（1–7 训、8 测、不微调）+24.5%。那两个 ablation 说明：干活的是训练范式。

**3. PRISM — II（重建）** `三作`

重建暴露出提问暴露不了的东西：统一的表征会把物体和它的属性糅在一起——被试看到一只灰色虎斑猫，重建出来是一只老虎。人的视觉是物体中心、组合式的。所以把文本结构化成物体／属性／关系，配 object-centric diffusion，用 VLM 搜哪些属性和关系真的被神经活动携带。同一 backbone 下，NSD、BOLD5000、GOD 上 training-free 指标最好或并列最好，LPIPS 最多低 5.9%，重建 QA 60.54%。

**4. D-Edit** `二作`

除了原文使用的较为简单的 object-centric，更进一步需要一个 object 解耦的**生成端**：扩散模型整张图收一个 prompt——你改猫，沙发跟着动，粒度在最后一步全丢。D-Edit 把图切成 item，每个 item 一条自己的 prompt，grouped cross-attention 让每个区域只看自己那条。文本、图像、mask 三种编辑加物体移除，一个模型全包。item 级文本编辑 LPIPS 降 55.4%；移除任务上 15 位标注者在质量和保真两项都更偏好它。接到脑信号明确写成 future work。

---

### PART 3 · The Embodiment — From Representations to Interactions

> **挑战** ：前两部分把脑信号送进了语义空间。要让它变成动作，瓶颈换了一个，但性质和 Part 2 是同一个——还是监督信号。运动想象的数据贵在 cue-locked 的试次和逐条标注，量上不去。

**1. Mind World Model** `一作`

换一种能规模化的采集方式：EEG 和第一视角视频可以连续录、不用标注，mind model 和 world model 在同一条流上一起训。mind model 从当前 EEG 出一个动作 `a_t = Mind(y_t)`，world model 用它预测下一帧 `x_{t+1} = World(x_t, a_t)`；**mind model 自己没有任何标签，唯一的监督是 world model 在下一帧上的预测误差**。这和 Part 2 那次 join 是同一招——不新采数据，把监督从已经存在的东西里挤出来。

而且这个目标天然对着 motor imagery：mind model 只能贡献那些会改变下一帧的东西，所以它学不到 volume conduction 和静态伪迹，只能学运动相关的时间动力学。评测放在 motor-imagery benchmark 上跟 EEG foundation model 比，最后收口在自采数据集上的机械臂连续控制闭环。

**2. DySta** `一作`（目录 `DYSTA/`；曾用名 SD-VLA）

现实里的 VLA 每一步都要过一遍完整的视觉–语言前向；一旦要看多帧，上下文就爆：视觉 backbone 每张图吐几百个 token，几帧一拼，注意力的平方复杂度就压垮了。现有加速手段基本是通用压缩，不看 VLA 自己的结构。

DySta 把 token 按跨帧变不变拆开：静态的跨帧只留一份并复用它的 KV cache，动态的每步重算，一个可学的 recache gate 决定什么时候该更新静态那一份。上下文长度和每步 FLOPs 一起降。SimplerEnv 上成功率比最强基线高 3.9%、推理加速 2.26×；真机上比 base model 高 10.6%、加速 2.21×。多帧整合另建了 LIBERO-Memory 基准（三类时序依赖任务），全指标提升 24.5%，真机绝对成功率提升 23.3%。

**3. PHIL** `二作` — **慢环；不是这一部分的主体，结尾一带而过。**

如果神经信号给出的是一个目标而不是逐步的动作，中间就得有一层规划把它补成路径，而 rollout 规划太贵、闭不上环。学一个 cost-to-go 把前瞻截断，就是 PHIL 在 A* 里做的事。

> ⚠️ **顺序** — PHIL 在 Part 3 的**最后**，是与快环并列的慢环旁支，**不是** Mind World Model 与 DySta 之间的一级。图和幻灯片里不要把它画成串联的中间节点，也不要给它编造一个交给执行器的输出对象。

> ⚠️ **未定** — 规划路线（MPC＋CEM）vs RL 策略路线；`outline.md` 没有结论。这个决定锁着 Mind World Model 的技术内容和脑信号的插入点（target embedding vs reward/actor conditioning）。无论走哪条，PHIL 都保持旁支、一带而过。

---

### Conclusion

收到「神经信号 → 语义 → 动作」的闭环，以及从内在思维到物理具身这条路还差什么。
