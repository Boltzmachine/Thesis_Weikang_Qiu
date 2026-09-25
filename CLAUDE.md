# CLAUDE.md

When making slides, keep text minimal and sufficient.
Transition callouts use a distinct style: Yale navy (#00356B) fill, white main text, small rounded corners, and light-blue/gold secondary labels. Ordinary explanatory callouts use light backgrounds and accent bars.

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
- Keep all backups and intermediate deck copies outside OneDrive, under
  `~/Thesis_Backups/Thesis_Weikang_Qiu/`. Do not create backup directories or
  duplicate backup decks inside this project.
- Preserve the shared `deck/dissertationv2.pptx` file when publishing edits.
  Edit and validate a working copy outside OneDrive, then update the existing
  file's contents in place. Do not rename the original to a backup, delete and
  recreate it, or publish via `os.replace`/a temporary-file rename. Keep its
  filesystem identity and metadata, and verify the existing OneDrive sharing
  link shows the new content after synchronization when browser access is available.

## `[C: ...]` author notes

The author leaves inline notes in the `.tex` source as `[C: 说明]` — an instruction
about the sentence or paragraph the note sits in, written in English or Chinese. A note
is never text to be inserted into the document.

To resolve one: revise the surrounding prose so it satisfies the note, delete the note
and any doubled space it leaves, and leave every other paragraph byte-identical.

`tools/cwatch.sh` is a background daemon that does this automatically — it polls the
`.tex` files, waits for a file to stop changing, backs it up to
`~/Thesis_Backups/Thesis_Weikang_Qiu/cwatch/`, and
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

> **用户在当前会话中的最新叙事要求优先。** `outline.md` 与本节记录已确认的主线，后续修改时同步两处，不能用旧文件覆盖用户的更正。Part 2 固定为 PRISM I → MindLLM → PRISM II → D-Edit 的研究问题递进；Part 3 为 ACTION LEVEL（MWM）→ GOAL LEVEL（PHIL ∥ DySta）：从动作含义递进到指定期望结果。箭头和并列符号表达研究问题关系，不代表已经整合的模型流水线。章节编号以当前主文件为准，不在可复用说明中写死。

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

**统一主线：PRISM I → MindLLM → PRISM II → D-Edit。** 四步依次回答对齐空间、语言对齐、语言驱动的视觉重建，以及更强的生成解耦。不要把它们拆成互不相关的语言／重建／编辑三条线。

**1. PRISM — I（选择对齐空间）** `三作`

比较 fMRI 与预训练的视觉、语言、视觉–语言表示。在所测候选空间中，语言模型语义表示更适合作为 fMRI 的对齐目标。这为语言对齐提供依据，不是说大脑本身是语言式的，也不把论证顺序当作论文发表时间线。

**2. MindLLM（将 fMRI 对齐到语言）** `一作`

通过脑指令微调，把 fMRI 与语言表征对齐，使感知、记忆与知识、语言与符号、复杂推理能用统一的文本格式读出。它不是语音或被试想说的词的解码。NSD 与 MSCOCO 的共享图像连接 fMRI 和既有标注，构成 980,610 段多轮对话，无须新增扫描。

**3. PRISM — II（基于语言重建视觉内容）** `三作`

从 fMRI 解码的语言信息还可以用于恢复视觉内容。PRISM 把描述组织为物体、属性、关系，再用 object-centric generation 生成并组合场景。它将语言表征用于视觉重建，同时显出保持物体结构对生成端的重要性。

**4. D-Edit（加强生成端的逐物体解耦）** `二作`

PRISM 的物体中心生成进一步引出更明确的 object-disentangled generator。D-Edit 为每个 item 学习独立 soft prompt，用 grouped cross-attention 分开不同区域与条件的交互，从 prompt 与 attention 两层加强局部控制。文本、图像、mask 编辑及物体移除是这种生成能力的验证；不要只把它写成一个独立图像编辑工具。

这里“更强”指解耦机制，不暗示已经在 PRISM 的脑重建任务上取得更高指标，也不宣称 MindLLM、PRISM、D-Edit 的模型权重或输出已被整合评测。

---

### PART 3 · The Embodiment — From Representations to Interactions

**结构：ACTION LEVEL（MWM）→ GOAL LEVEL（PHIL ∥ DySta）。** 动作层中，MWM 联合学习 mind model 和 world model，通过动作的视觉后果把脑信号与动作含义连接起来。完成任务时，人往往更希望指定期望结果，而不必表达每一步动作；这一需求把研究问题推进到目标层。PHIL 与 DySta 在目标层研究两个互补接口：**PHIL：goal image → target graph state → graph search**；**DySta：language instruction + multi-frame visual history → policy actions**。图像与语言目标对应第二部分解码出的图像与文本。箭头表示研究范围递进，不是 MWM 输出流向后两者；PHIL 与 DySta 也不是规划器—执行器串接，不能写成快环／慢环。

**MWM** `一作` 把当前 EEG 映射为 latent action，以此预测未来视觉表征。同步 EEG 与第一视角视频提供无需动作标注的预训练数据，损失包括未来预测、跨模态对齐和偏侧化相关监督。mind model 用于运动解码，world model 的动作接口通过独立 IMU 适配评估。不要声称预测损失是唯一监督、模型保证排除全部伪迹，或已经完成 EEG 到机器人的闭环。

**PHIL** `二作` 在论文具身接口中以 **goal image** 指定期望结果；图像所表达的结果需要对应状态图中的目标节点及其特征。给定起点、目标节点和状态图时，PHIL 用局部图结构及搜索记忆预测到目标的距离，指导 greedy best-first search。原方法实验评估给定 graph/start/goal 的搜索任务；将第二部分解码图像转换成可规划目标是未来整合。不要把这一接口对应写成已经评估的图像输入或脑控系统，也不要改写原方法的图搜索定义。PHIL 不是 DySta 的前置模块。

**DySta** `一作` 的目标输入是 **language instruction**，对应第二部分的文本输出；策略根据语言指令与视觉观察直接预测动作。静态／动态 token 分解、静态 KV cache 复用与 learned recache gate 降低推理开销，多帧动态信息支持需要记忆的任务。它与 PHIL 分别评估；将脑解码文本作为指令仍是未来整合，输入不是 PHIL 路径或 MWM latent action。

---

### Conclusion

总结脑信号建模、语义对齐与具身行为的研究贡献，并明确各自的验证范围，以及把这些能力整合为脑控系统仍需完成的工作。
