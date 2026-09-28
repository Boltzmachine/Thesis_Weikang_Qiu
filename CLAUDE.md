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

> **叙事来源更新（2026-09-27）：作者明确说明 slides 已过期，当前是在写新的故事。** MWM → DySta 的衔接以当前正文和作者最新指示为准，不能根据旧 slides 加入 action level → goal level 叙事。文中既有 slides 来源记录仅保留为历史或具体素材出处，不作为当前工作关系的权威依据。
>
> **当前确认的主线（2026-09-26）：HyBRiD → MindLLM → MWM → DySta。** 只以这四篇一作作为四个核心研究 chapter，直接按此顺序展开，不再分三个 Part。其他工作只围绕四篇主角提供支撑与延伸（revolve），不承担主线必须经过的转折。用户最新要求优先；`outline.md` 与 `CLAUDE.md` 的 Thesis Outline 同步维护，口播见 `area_exam/part2_versions.md`。
>
> **当前实施阶段：调整 Abstract 与 Introduction 的挑战层次（2026-09-28）。** 按作者要求交换两处挑战段：Abstract 使用原 Introduction 的三项高层研究问题，Introduction 使用展开版，解释高维脑信号中的结构与先验、数据与监督稀缺及个体差异，以及任务执行中的时间记忆与计算成本。两处均服务于 HyBRiD → MindLLM → MWM → DySta 的四项工作主线。
>
> **本轮修改范围。** 交换 `abstract.tex` 与 `Introduction.tex` 中现有的两个挑战段，不改写其内容；同步本文件与 CLAUDE.md。Abstract 概括研究问题，Introduction 解释具体困难。摘要继续按四项核心工作组织，不沿用旧三部分结构、周边工作链或图像／语言目标叙事，也不附加未整合或尚待验证的限定。

## 核心故事

**从脑信号的组织结构出发，由 MindLLM 连接 signals 与 semantics，再由 MWM 利用 visual consequences 的语义监督学习 action 表征，最后由 DySta 研究物理行动。**

四章的研究问题依次是：

**脑信号如何建模 → 如何读出语义 → 如何从视觉语义学习动作表征 → 如何高效地执行行动。**

主线沿着 Signals → Semantics → Actions 展开，这是概念上的推进，不是三个 Part。MindLLM 是 signals → semantics 的桥，MWM 是 semantics（visual consequences）→ action 的桥；DySta 的研究对象位于物理行动一端。

**总览图（2026-09-27，按作者纠正）。** 图表达 **Signals → Semantics → Actions** 的连续递进，必须突出两个端点与中间的桥接关系：**HyBRiD 是纯 signal 端，DySta 是纯 action 端；MindLLM 是连接脑信号与语义内容的 bridge**，不能放入独立的“纯 semantics”类别。MWM 以视觉后果的语义监督学习动作表征，承担 semantics → action 的桥接作用，也不能与 DySta 合并为一个纯 action 分组。图中 HyBRiD、DySta 分别位于 Signals、Actions 端点下，MindLLM、MWM 位于中间连线上；不设三个分类横条或颜色分区，不表示模型已经串接。四篇保留等宽模块及既定章节顺序。 两个桥接模块的图内标题按作者用语明确写成 **MindLLM: From signals to semantics**、**MWM: From semantics to action**，直接标明各自的起点和终点。Side works 仅列名字：HyBRiD 内为 SWA，MindLLM 内为 PRISM、D-Edit，MWM 无，DySta 内为 PHIL。

**Introduction 开头沿用作者原文。** 保留“语言作为多模态接口 → 语言表达的局限与 Kandinsky 例子 → RepQA 展示机器到人的可读性／信息保留问题 → 更直接的 mind–world 接口”四段动机。长期目标按作者最新批注改为无缝人机共生与人类能力增强的未来愿景，以具体应用举例，不在该段讨论论文不足。四篇故事用于贡献组织与章节串联；挑战段按最新批注讨论神经先验、数据与监督、有效且高效的 AI 三项问题，不列方法名。Practical Impact 与长期人机共生愿景合并为一个 paragraph，积极展开广泛的应用价值；删除四场景配图，不再以四个场景限定讨论范围。作者已注释掉独立 Contributions section，保持不启用。Thesis Outline 承担贡献概述：每章在高层说明回应的总体挑战、核心解题思路和全篇角色，引用 `fig:thesis-overview`，不再列组件、训练损失或 benchmark。HyBRiD 回应神经先验并位于 signals 端；MindLLM 以共享脑表征与刺激图像连接的监督实现 signals → semantics；MWM 用 visual consequences 的语义监督实现 semantics → action；DySta 位于 physical action 端，研究有效且高效地实现指定目标。附加工作简述其支撑或延伸角色。

## 四个核心 Chapter

| 核心章节顺序 | 主角 | 核心问题 | 在故事中的位置 |
| --- | --- | --- | --- |
| 1 | HyBRiD | 如何发现神经先验以改善脑信号建模和预测？ | 以高阶脑结构学习研究这一问题 |
| 2 | MindLLM | 如何跨被试读取脑活动中的语义内容？ | signals → semantics，涵盖感知、语言与知识相关任务 |
| 3 | MWM | 如何以 visual consequences 的语义监督学习动作表征？ | semantics → action 的桥接 |
| 4 | DySta | 如何将人的意图转化为有效且高效的任务执行？ | 承接 MWM 的行动意图解码，研究意图到物理行动的转化 |

这里的 1–4 表示四个核心研究 chapter 的相对顺序；论文正式编号按正文中的章节组织确定。每篇作为完整的一章，不拆成跨章的贡献片段。

### HyBRiD — Discovering Meaningful Neural Structure

起点是脑信号本身：如何发现有用的神经先验，例如结构关系，以改善脑信号建模和预测性能？HyBRiD 以脑区之间的高阶结构为具体研究对象。

HyBRiD 用可学习的加权超边表示高阶脑区关系，避免先枚举一小部分候选关系再筛选。通过 maximally informative and minimally redundant（MIMR）目标与 multi-head drop-bottleneck，端到端学习与指定表型相关的结构及其权重。跨受试者共享的 feature-agnostic masks 决定脑区组合，个人的脑信号决定这些组合的权重。

本章的角色是 **neural organization for prediction**：发现有用的神经先验，并将这些结构关系纳入模型以提高预测性能。这里的结果是与预测相关的候选结构，不扩大为已确定的因果脑机制；其输入仍可来自两两相关特征，高阶性体现在学到的组合与关系。

**通向 MindLLM：** 为一个指定的认知指标发现有用结构之后，进一步追问：脑活动包含了什么关于外部世界的信息，能否以可理解、可灵活查询的形式读取？

### MindLLM — Reading Semantic Content from Brain Activity

研究从为预先定义的指标筛选信息，推进到根据不同问题读取脑活动中的语义内容。

MindLLM 作为完整的一章，包含 subject-agnostic neuro-informed encoder 与 Brain Instruction Tuning（BIT）。编码器用 learnable queries 聚合数量和空间分布因人而异的体素；keys 编码位置与多套脑区先验，values 承载实际 fMRI 信号。BIT 利用共享刺激图像连接脑记录与已有标注，扩展多任务语义监督，支持多种文本读出任务。

HyBRiD 与 MindLLM 的方法联系是：把可共享的组织方式与具体观测值分开建模。HyBRiD 学习脑区组合，MindLLM 利用位置和功能分区组织体素信息；两者没有组成同一模型，也不共享一套已验证的统一优化理论。

本章的角色是 **signals → semantics**：从脑活动读出语义内容，任务范围涵盖感知、语言和知识，不将高层定位局限于 perceived world。Neuro-informed encoder 保留在 MindLLM 内部，不再抽出来放入独立的“基础”部分。BIT 中的知识和推理类任务不等于直接恢复了被试脑内真实的推理过程，也不是对被试想说的词逐字解码。

**通向 MWM：** 从脑信号读出语义之后，如何由 semantics 走向 action？MWM 利用动作的 visual consequences 所提供的语义监督，学习运动相关 EEG 中的动作表征。

### MWM — Learning Action Representations from Visual Semantics

MWM 的主线作用明确为 **semantics（visual consequences）→ action**。动作的视觉后果在语义特征空间中提供监督，使 EEG 编码器学习有动作含义的表征。世界动态预测在这里承担训练机制，而不是取代 action 成为叙事终点。

Mind model 将截至当前帧的 EEG 编码为 latent action，world model 以当前视觉状态和该 latent action 为条件预测未来视觉表征。训练使用同步 EEG 与第一视角视频，无需动作标注；新版训练目标结合 masked EEG reconstruction、跨模态对齐与未来预测，共同学习运动相关表征。Lateralization-Aware Transformer 区分 bilateral 与 lateral 成分，在 EEG–视频联合变换中保留共享信息并变换侧别相关信息。

**FA-EEG 是 MWM 工作自身的内容**，在 MWM 章内讲述其 EEG 编码、左右结构与神经先验；不列为围绕 MWM 的周边工作，也不另设独立章节。

MindLLM 将脑活动与语义内容联系起来；MWM 进一步以视觉后果的语义监督学习 action。这里须区分两个方向：叙事／监督方向是 visual consequences → action representations，模型计算前向仍是 EEG → latent action，再与当前视觉状态共同预测未来视觉特征。前者解释 MWM 在论文中的作用，后者解释实现机制。两项研究没有组成已串接的 fMRI–EEG 解码流水线。

本章的角色是 **semantics → action**。MWM 位于 MindLLM 之后、DySta 之前，以 visual consequences 为监督学习动作表征。评估分别落在 mind model 的下游运动解码，以及通过独立 IMU 适配 world model 动作接口的未来预测；不把它描述为已完成机器人执行、反事实控制或脑控闭环。

**通向 DySta：** MWM 通过视觉后果的语义监督学习支持行动意图解码的表征；DySta 接着研究如何让机器将人的意图转化为有效且高效的任务执行。

MWM 章首的收尾须落在 **semantics → action representations**：视觉后果作为监督，学习支持运动解码的动作表征；不写成对 visual semantics 的作用，也不用含糊的 action meaning。随后用一句话预告 DySta，从行动意图解码转向将人的意图转化为有效且高效的任务执行。

### DySta — Acting Efficiently in the Physical World

DySta 研究如何让机器人策略将人的意图转化为有效且高效的任务执行。它在主线中承接 MWM 的行动意图解码，推进到意图的物理实现。语言指令与视觉观察是具体 VLA 方法的输入，在总体故事和章间衔接中不以语言为重点，也不额外添加视觉引导执行的描述。

实现这一目标面临两个具体挑战：某些任务需要时间记忆，而大模型的反复推理带来高延迟。DySta 通过静态／动态 token 分解支持紧凑的多帧输入；复用静态 KV cache，并通过 learned recache gate 按需刷新。这些机制服务于任务完成能力与执行效率，不能替代其总体研究目标。

本章的角色是 **effective and efficient task execution**：将人的意图转化为物理行动。多帧整合提高需要历史信息的任务完成能力，计算复用降低推理成本；两者都是实现目标所需的能力。

DySta 是四章的终点。MWM → DySta 表达从行动意图解码，推进到将人的意图转化为有效且高效的任务执行。PHIL 与 DySta 的目标实现关系保留在章末 Additional Work 中，不改变四个核心章节的组织。

## MWM 最新源码

2026-09-27 从用户指定的 [Overleaf 项目](https://www.overleaf.com/project/6a736986680ecc7e91861ff9) 拉取，版本 `61c25b8`。章标题更新为 **Mind World Models: Joint Learning of Motor EEG Representations and Action-Conditioned World Dynamics**，替换五个正文 section、图表、结果宏及相应文献。

新版评估包含 9 个分类任务和 7 个回归任务，分类／回归 task-averaged 相对提升分别为 5.9%／16.2%；世界模型的两项 L1 相对降幅仍为 23.2%／11.0%。新增侧化分析及消融实验。附录与投稿声明源码保留但不进入正文，正文删除指向未收录附录的句子。具体来源与适配记录见 `MWM/README.md`。

## 三个章节过渡

### HyBRiD → MindLLM：从脑内结构到语义内容

HyBRiD 研究哪些脑区组合对认知预测有用。接下来，我们进一步追问：脑活动包含了什么关于外部世界的信息，能否以可理解、可灵活查询的形式读取？MindLLM 将研究从任务相关结构的发现，推进到跨个体、多任务的语义解码。

> HyBRiD identifies neural structures that are informative for a specified cognitive or phenotypic outcome. MindLLM extends the question to semantic content: how can brain activity be represented so that different questions can read out different aspects of information about the world?

### MindLLM → MWM：从语义表征到动作意图

MindLLM 通过刺激图像关联的标注，把脑活动与语义内容联系起来。MWM 由 semantics 走向 action：视觉后果提供语义监督，训练 EEG 编码器学习可用于运动解码的动作表征。

> MindLLM connects brain signals to semantic content. MWM bridges semantics and action by using visual consequences as supervision for learning action representations from motor EEG.

### MWM → DySta：从动作表征到物理行动

MWM 利用行动的视觉后果学习支持行动意图解码的动作表征。接下来，DySta 研究机器如何将人的意图转化为有效且高效的任务执行。记忆和推理效率作为具体挑战在此目标下展开。

> Following the study of action-intention decoding in MWM, DySta investigates how robotic policies can translate human intentions into effective and efficient task execution. Temporal memory and inference efficiency support this translation.

## 其他工作：围绕主角展开（Revolve）

其他工作只用于相关动机、支持证据、方法呼应或能力延伸，不与四个核心 chapter 并列，也不作为章间过渡的必要中间步骤。拿掉这些工作，四篇主角仍应能独立讲完整。

| 周边工作 | 围绕的主角 | 支撑或延伸的位置 |
| --- | --- | --- |
| SWA | HyBRiD | 结构建模思想向人工网络的延伸；不另立“神经科学与 ML 双向交换”主线 |
| PRISM | MindLLM | 对齐空间比较与视觉重建，为语义联系提供补充讨论；不作为 MindLLM 必须依赖的前置章节 |
| D-Edit | MindLLM | 物体级生成控制的延伸；编辑评估不等于已接入脑解码系统 |
| PHIL | DySta | 按 slides 的目标实现关系并置：PHIL 为目标状态的显式规划，DySta 为语言指令引导的执行；目标图像是概念例子，PHIL 实际评估使用 graph/start/goal |
| RepQA | 引言与既有 prologue | 保留原 Motivation 中的语言接口论证及可读性／信息保留动机，现有正文章节与位置不变 |

**PHIL 与 DySta 的关联依据。** `dissertationv3.pptx` 第 33 页将二者并列为 goal level，第 38 页用目标图像解释 target-state planning，第 39 页及 notes 明确说明这是实现目标的两种方式（target-state planning 与 language-guided execution），第 49 页 notes 再次呼应。6.6 应先承接本章以语言指定目标的方式，再引入目标状态的显式搜索；不以共享记忆或效率机制推导二者关系。此关联用于 DySta 章末的 Additional Work，不改变四个核心 chapter 的顺序，也不把 PHIL 写成 DySta 的规划前级。

用户于 2026-09-27 授权将 SWA、PRISM、D-Edit、PHIL 以 **Additional Work** 小节重新纳入对应核心章末。Additional Work 下不再划分 subsection：单项工作直接写正文，多项工作用 paragraph 标题区分并连续排版。每项约 180–220 英文词，概述问题、方法、主要证据及与主角的联系：HyBRiD 后为 SWA；MindLLM 后为 PRISM 与 D-Edit；DySta 后为 PHIL。保留四项研究的完整源材料，仅输入短摘要，不恢复原有完整章节或章间过渡。MWM 不另设 side-work 小节，FA-EEG 属于其自身方法；RepQA 的原研究正文及位置不变，章节包装前言与过渡按最新授权精简。

## Practical Impact 来源与范围

按 2026-09-27 最新批注，将原 Contributions 后的长期愿景合并到 Introduction 的单个 Practical Impact paragraph。以无缝人机共生为总目标，连接交流与自主行动、无外显反应的指令跟随、想象场景创造、科研协作、远程机器人／额外机械肢体与认知辅助，突出人类能力增强。删除 Practical Impact 的四场景 figure 及正文引用；不再限定于 `deck/dissertationv3.pptx` 第 5 页的四种场景。

交流、机器人控制与主动听觉任务的例子保留既有研究引用，广泛应用以长期愿景与 could 表述，收尾强调人类判断、创造力与机器智能结合所能拓展的能力，不加入实现条件或额外验证要求。保留原始配图资产与 slides 文件，仅移除论文中的展示；additional works 按上节所述仅作为章末短摘要收录。

## Future work 来源与范围

以 `deck/dissertationv3.pptx` 实际第 **50、51 页**的正文与 notes 为依据（按 presentation order 计数）。保留两条连续方向：**多模态脑世界模型预测干预后的脑状态 → 在预测轨迹上进行 Dreamer 式闭环刺激策略学习**，以慢性疼痛的 tFUS 作为具体研究愿景。

前者研究跨模态、跨被试的共享脑状态及刺激／干预条件下的动态预测；后者从脑源 latent/recurrent states 读出策略与价值，以疼痛相关解码提供反馈，并用新的脑记录闭合干预回路。这些是未来研究设想，不作为已验证的干预效果或直接解码生物脑内策略与价值的结论。

删除旧的 decoded-image/text-to-goal integration、brain grounding for AI、geometric grounding for AI 三项未来主方向；不据此改动 deck 或四篇论文正文。Future Work 图的具体素材曾由 v3 第 50、51 页更新，但不能把 slides 整页版式搬进论文。按 2026-09-27 最新要求，Figure 7.2 依据当前 Conclusion 的内容以 TikZ 重绘为论文双面板图：actor–critic learning 与 closed-loop intervention。删除演讲标题、横幅、应用列表、示意曲线与参数，必要定义放入图注；图源为 `figures/future_directions/brain_closed_loop.tex`。Figure 7.1 保持原状。

## 工作串联概述（不替换 Introduction 开篇）

我的研究从脑信号的组织结构出发，逐步走向物理世界中的智能行为。首先，HyBRiD 发现有助于预测的高阶脑结构；随后，MindLLM 将脑信号连接到语义内容，MWM 用视觉后果的语义监督学习动作表征；最后，DySta 研究如何将人的意图转化为有效且高效的任务执行。

## 写作约束

- 主线固定为 **HyBRiD → MindLLM → MWM → DySta**，四篇一作各占一个完整的核心 chapter，不再设置三个 Part。
- RepQA 前言等总括句必须覆盖四项工作的角色：脑信号建模、signals → semantics、以 visual consequences 学习 action 表征，以及有效且高效地实现指定目标；不能只以 neural representations 和 physical action 两个端点代替完整主线。
- MindLLM 的 encoder 与 BIT 留在同一章；MWM 必须在 DySta 前；DySta 明确定位为纯物理世界研究。
- 箭头表示研究问题与视角的递进，不表示模型权重、输出或监督信号已经逐章串接，也不表示论文发表时间顺序。
- Summary 与总体贡献积极说明四项工作如何推进整体目标；不主动添加 separate settings、尚未整合或仍待验证的限定，也不声称已经实现联合系统。
- HyBRiD → MindLLM 从神经结构推进到语义内容；MindLLM → MWM 必须表述为 semantics → action。visual consequences 提供语义监督，世界模型预测是动作表征学习的机制，不把 MWM 的主线定位写成 world dynamics。
- 其他工作只 revolve，不恢复 PRISM I → MindLLM → PRISM II → D-Edit 的旧章节链。PHIL 的目标状态规划与 DySta 的语言引导执行，按 slides 作为两种目标实现方式在 Additional Work 中讨论。
- 四篇故事只改变工作之间的组织与串联；Introduction 原有动机框架应保留，局部措辞与三项挑战按作者 comments 修改；长期目标按最新批注聚焦无缝人机共生、人类能力增强及宏观未来应用。Practical Impact 与长期愿景合并为一个 paragraph，删除四场景配图，积极展开更广泛的人类能力增强应用。
- 后续若修改叙事，同步本文件与 `CLAUDE.md` 的 Thesis Outline。MWM 最新稿、Conclusion 的 future work、对应章末 Additional Work 及 paragraph 格式均保持现状。工作之间的过渡写在各独立工作的章标题之后、正式 Introduction 之前，参照 Rex thesis 的短前言写法，不在 Thesis Outline 中补写；RepQA 前言保持精简。
