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

> **当前确认的主线（2026-09-26）：HyBRiD → MindLLM → MWM → DySta。** 只以这四篇一作作为四个核心研究 chapter，直接按此顺序展开，不再分三个 Part。其他工作只围绕四篇主角提供支撑与延伸（revolve），不承担主线必须经过的转折。用户最新要求优先；`outline.md` 与 `CLAUDE.md` 的 Thesis Outline 同步维护，口播见 `area_exam/part2_versions.md`。
>
> **本轮只更新 Markdown 叙事记录。** 论文正文、LaTeX 章节组织与演示文件暂不修改；现有论文结构尚未迁移到新故事，不能用它覆盖本记录。

## 核心故事

**从脑活动的组织结构出发，通过语义内容和行动相关的世界动态建立脑与世界的联系，最终走向物理世界中的智能行为。**

四章的研究问题依次是：

**脑如何组织信息 → 脑中的世界内容 → 脑与世界变化的联系 → 世界中的行动。**

研究视角沿着 Mind → Mind–World → World 向外展开。这是概念上的移动，不是三个 Part 的章节划分。MindLLM 和 MWM 分别通过语义与动态关系连接脑和世界；DySta 的研究对象完全位于物理世界一端。

开场直接提出：**机器学习如何从理解脑活动，逐步走向理解并支持世界中的交互？** 不再以“语言有损”或 RepQA 为整篇论证的必要前提。

## 四个核心 Chapter

| 核心章节顺序 | 主角 | 核心问题 | 在故事中的位置 |
| --- | --- | --- | --- |
| 1 | HyBRiD | 脑活动中，与认知相关的信息如何组织？ | 发现与认知预测相关的高阶脑结构 |
| 2 | MindLLM | 脑活动包含的世界信息，怎样通过语义读取？ | 建立脑与世界内容的语义联系 |
| 3 | MWM | 脑活动怎样与行动相关的世界变化建立联系？ | 通过未来预测学习脑与世界动态的联系 |
| 4 | DySta | 智能体怎样组织持续到来的观测，高效地行动？ | 纯物理世界中的时间表征、记忆与行动 |

这里的 1–4 表示四个核心研究 chapter 的相对顺序；论文正式编号在后续修改正文时确定。每篇作为完整的一章，不拆成跨章的贡献片段。

### HyBRiD — Discovering Meaningful Neural Structure

起点是脑信号本身：观测到了许多脑区的活动，哪些脑区应该放在一起理解，才能提取与认知预测有关的信息？

HyBRiD 用可学习的加权超边表示高阶脑区关系，避免先枚举一小部分候选关系再筛选。通过 maximally informative and minimally redundant（MIMR）目标与 multi-head drop-bottleneck，端到端学习与指定表型相关的结构及其权重。跨受试者共享的 feature-agnostic masks 决定脑区组合，个人的脑信号决定这些组合的权重。

本章的角色是 **neural organization**：发现对任务有用的组织结构，为理解高维脑观测提供一种方法。这里的结果是与预测相关的候选结构，不扩大为已确定的因果脑机制；其输入仍可来自两两相关特征，高阶性体现在学到的组合与关系。

**通向 MindLLM：** 为一个指定的认知指标发现有用结构之后，进一步追问：脑活动包含了什么关于外部世界的信息，能否以可理解、可灵活查询的形式读取？

### MindLLM — Reading Semantic Content from Brain Activity

研究从为预先定义的指标筛选信息，推进到根据不同问题读取脑活动中的语义内容。

MindLLM 作为完整的一章，包含 subject-agnostic neuro-informed encoder 与 Brain Instruction Tuning（BIT）。编码器用 learnable queries 聚合数量和空间分布因人而异的体素；keys 编码位置与多套脑区先验，values 承载实际 fMRI 信号。BIT 利用共享刺激图像连接脑记录与已有标注，扩展多任务语义监督，支持多种文本读出任务。

HyBRiD 与 MindLLM 的方法联系是：把可共享的组织方式与具体观测值分开建模。HyBRiD 学习脑区组合，MindLLM 利用位置和功能分区组织体素信息；两者没有组成同一模型，也不共享一套已验证的统一优化理论。

本章的角色是 **semantic content**：通过语义建立脑活动与世界内容的联系。Neuro-informed encoder 保留在 MindLLM 内部，不再抽出来放入独立的“基础”部分。BIT 中的知识和推理类任务不等于直接恢复了被试脑内真实的推理过程，也不是对被试想说的词逐字解码。

**通向 MWM：** 世界不仅有可以描述的内容，还会随行为不断变化。能否从语义对应进一步走向动态联系，让脑信号提供关于接下来世界变化的信息？

### MWM — Grounding Neural Representations in World Dynamics

MWM 从脑与世界内容的语义联系，推进到脑与行动相关的世界变化之间的联系。给定当前视觉状态，脑活动能够提供哪些预测未来视觉状态的信息？

Mind model 将截至当前帧的 EEG 编码为 latent action，world model 以当前视觉状态和该 latent action 为条件预测未来视觉表征。训练使用同步 EEG 与第一视角视频，无需动作标注；未来预测与跨模态对齐、偏侧化相关监督共同学习运动相关表征。Lateralization-Aware Transformer 区分 bilateral 与 lateral 成分，在 EEG–视频联合变换中保留共享信息并变换侧别相关信息。

**FA-EEG 是 MWM 工作自身的内容**，在 MWM 章内讲述其 EEG 编码、左右结构与神经先验；不列为围绕 MWM 的周边工作，也不另设独立章节。

MindLLM 与 MWM 建立两种互补联系：前者通过已有语义标注联系脑活动与世界内容，后者通过同步经验和未来预测联系脑活动与世界动态。这里从语义内容推进到动态过程，不把 fMRI 与 EEG 写成同一条已经串接的解码流水线。

本章的角色是 **mind–world dynamics**。MWM 位于 MindLLM 之后、DySta 之前，是从脑走向物理世界的桥接研究。评估分别落在 mind model 的下游运动解码，以及通过独立 IMU 适配 world model 动作接口的未来预测；不把它描述为已完成机器人执行、反事实控制或脑控闭环。

**通向 DySta：** 建立脑活动与世界动态的联系之后，研究视角进一步移向物理交互本身：智能体应该怎样组织不断到来的观测，才能兼顾历史记忆与及时行动？

### DySta — Acting Efficiently in the Physical World

DySta 是 **pure physical-world research**：研究对象是物理世界中的视觉–语言–动作智能体。它根据语言指令和视觉历史预测动作，输入不包含 EEG，也不依靠脑解码输出来确立研究意义。

本章先讲“应该记住什么、更新什么”：行动可能需要过去的观测，但不断追加完整图像会增加上下文和重复计算。DySta 通过静态／动态 token 分解，保留时间上稳定的信息并组织多帧动态信息；复用静态 KV cache，通过 learned recache gate 按需刷新。

本章的角色是 **physical-world interaction**：利用时间结构同时支持有效记忆与高效推理。加速是这种表征设计带来的结果之一，多帧整合与时间依赖任务同样是核心贡献。

DySta 是四章的终点。它不是 MWM 的下游控制器、MindLLM 的脑控应用，也不是 PHIL 的执行模块。MWM → DySta 表达研究对象从脑与世界动态的联系，转向物理世界中的行动；不再以“动作层 → 目标层”或“PHIL ∥ DySta”组织主线。

## 三个章节过渡

### HyBRiD → MindLLM：从脑内结构到语义内容

HyBRiD 研究哪些脑区组合对认知预测有用。接下来，我们进一步追问：脑活动包含了什么关于外部世界的信息，能否以可理解、可灵活查询的形式读取？MindLLM 将研究从任务相关结构的发现，推进到跨个体、多任务的语义解码。

> HyBRiD identifies neural structures that are informative for a specified cognitive or phenotypic outcome. MindLLM extends the question to semantic content: how can brain activity be represented so that different questions can read out different aspects of information about the world?

### MindLLM → MWM：从语义联系到动态联系

MindLLM 通过刺激图像关联的标注，把脑活动与世界的语义内容联系起来。MWM 将这种联系推进到时间维度：给定当前视觉状态，利用脑信号预测接下来的视觉变化，通过世界动态学习运动相关表征。

> MindLLM connects brain activity to semantic information about the world. MWM extends this connection to dynamics, learning motor-related neural representations by using EEG-derived latent actions to predict future visual states.

### MWM → DySta：从脑与世界的联系到物理交互本身

MWM 把研究推进到脑活动与世界变化的联系。接下来，DySta 将研究对象完全移向物理世界中的智能体：为了持续而及时地行动，应该保留哪些历史信息，更新哪些变化，并复用哪些计算？

> After studying the relationship between neural activity and world dynamics, we turn to physical interaction itself. DySta asks how an embodied agent can organize a stream of observations to support both temporal memory and efficient action.

## 其他工作：围绕主角展开（Revolve）

其他工作只用于相关动机、支持证据、方法呼应或能力延伸，不与四个核心 chapter 并列，也不作为章间过渡的必要中间步骤。拿掉这些工作，四篇主角仍应能独立讲完整。

| 周边工作 | 围绕的主角 | 支撑或延伸的位置 |
| --- | --- | --- |
| SWA | HyBRiD | 结构建模思想向人工网络的延伸；不另立“神经科学与 ML 双向交换”主线 |
| PRISM | MindLLM | 对齐空间比较与视觉重建，为语义联系提供补充讨论；不作为 MindLLM 必须依赖的前置章节 |
| D-Edit | MindLLM | 物体级生成控制的延伸；编辑评估不等于已接入脑解码系统 |
| PHIL | DySta | 物理世界目标实现中显式图搜索的相关方法；原评估使用给定 graph/start/goal，不是 DySta 的规划前级 |
| RepQA | 引言或讨论 | 与语言接口有关的补充动机；不再独立承担整篇成立的前提 |

周边工作的具体篇幅与位置在后续改论文时决定；本轮不移动或删除其论文内容。

## 可直接使用的开场

我的研究从脑活动的组织结构出发，逐步走向物理世界中的智能行为。首先，我研究如何发现与认知相关的高阶脑结构；随后，通过语义解码和动作条件的未来预测，分别建立脑活动与世界内容、世界动态之间的联系；最后，我将研究推进到物理交互本身，研究智能体如何组织时间信息，实现有记忆且高效的行动。

## 写作约束

- 主线固定为 **HyBRiD → MindLLM → MWM → DySta**，四篇一作各占一个完整的核心 chapter，不再设置三个 Part。
- MindLLM 的 encoder 与 BIT 留在同一章；MWM 必须在 DySta 前；DySta 明确定位为纯物理世界研究。
- 箭头表示研究问题与视角的递进，不表示模型权重、输出或监督信号已经逐章串接，也不表示论文发表时间顺序。
- 四篇各有独立验证范围；脑控整合属于未来工作，不作为已有贡献或统一实验结果。
- HyBRiD → MindLLM 不是静态到动态的转折；时间动态的推进放在 MindLLM → MWM。
- 其他工作只 revolve，不恢复 PRISM I → MindLLM → PRISM II → D-Edit 或 ACTION LEVEL（MWM）→ GOAL LEVEL（PHIL ∥ DySta）的旧主线。
- 后续若修改叙事，同步本文件与 `CLAUDE.md` 的 Thesis Outline，并更新相应口播；用户另行要求之前，不据此修改论文或演示文件。
