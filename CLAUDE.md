# CLAUDE.md

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
Dissertation Structure

---

## 论证主线

1. **问题** — 语言真的是 mind 与 world 之间最好的接口吗？现有范式（text-to-X、X-to-text、语音助手）默认是。
2. **证据** — 不是。这条信道 **两个方向都有损** ：进来的方向是带宽差（说话 100–150 wpm vs 思维 400–800 wpm）与不可言说性，出去的方向由 RepQA 实测论证。
3. **主张** — 造一条绕开语言的直接通路。这需要三件事。
4. **结构** — 先真懂脑信号 → 接到世界的语义空间 → 驱动具身。三个 Part。

---

## 章节骨架

### Ch 1 · Introduction

### Ch 2 · The Premise: The Limits of Language as an Interface

**RepQA** `一作`

把「语言有损」从修辞变成测量。prospectus 目前用 wpm 统计和维特根斯坦支撑前提，那是引文不是证据。

* **用机制，不用效应量。** case study 中模型为降低阅读难度，把胆固醇药物的五个类别压成一句不加区分的话，只留下 statins；酒精依赖那例只留 craving。这是信息在压缩中被丢掉的字面演示。
* **别领着讲数字。** grade level 降 41.4%、professional score 降 73.3%，而准确率只掉 3–5 点（Fact 74.56% → 69.82%），Qwen 上只掉 1.3 点。拿这组数论证「语言有损」，敌意读法立刻来：3 个点换 73%，说明语言是条挺划算的信道。
* **该讲方向与普遍性。** 所有模型、所有类别方向一致，没有配置能免费拿到可读性。论点是 trade-off 系统性、绕不开，不是它很大。这个说法不依赖效应量，砸不掉。

---

### PART 1 · The Foundation — Models for Brain Signals

> **挑战** ：现有方法基本照搬 CV/NLP 模型，不带神经先验，既给不出神经科学洞见，性能也次优。

#### Ch 3 · HyBRiD `一作`

高阶脑区关系处在指数空间中，用 MIMR（maximally informative, minimally redundant）信息论目标端到端求解，兼得可解释性与下游性能（如 IQ 预测）。

#### Ch 4 · MindLLM — I `一作`

Neuro-informed attention：用可学习 query 结合空间信息与神经先验做动态特征提取，解决跨被试 voxel 数目与空间分布不一致的问题。

### PART 2 · The Bridge — From Signals to Representations

> **挑战** ：脑数据稀缺、昂贵、跨被试差异大，需要认知原则支撑的架构 + 有限监督下可行的训练范式。

#### Ch 5 · MindLLM — II `一作`

Brain Instruction Tuning：subject-agnostic 且任务灵活，支持推理、记忆检索与新任务适配，首次把神经信号送进高层语义空间，为后续应用提供统一表征接口。

#### Ch 6 · PRISM `三作`

fMRI 更贴合 **结构化文本空间** （物体／属性／关系）而非视觉 latent 或视觉–语言联合空间。据此做 object-centric diffusion 与属性–关系搜索，提升重建保真度。

> § **D-Edit** `二作` — **必要性论证，不是补丁**
>
> 逻辑链：Part 2 论证了 bridge 的目标空间必须是组合式的（PRISM 有实验支撑）；目标空间一旦是组合式的，下游生成接口就必须能在同样粒度上被控制，否则改一个物体会牵动全图——而这恰好是 D-Edit abstract 开头写的那个问题。D-Edit 建立的就是这个 item 级控制接口。
>
> 接到脑信号明确写成 future work

---

### PART 3 · The Embodiment — From Representations to Interactions

> **挑战** ：① VLA 太重，扛不住实时神经驱动控制；② agent 空间与脑信号空间的结构性鸿沟；③ 神经指令天然欠定，机器必须从稀疏目标补出完整行为且快到能闭环。

#### Ch 7 · SD-VLA `一作`

静／动 token 多级解耦 + recache gate：跨帧只保留一份 static token 以压缩上下文，并复用其 KV cache、按需更新。同时解决长时程建模与推理效率。

#### Ch 8 · EEG World Model `一作`

动作条件的世界模型预训练：从当前 EEG 活动预测想象中未来状态的神经表示。该形式天然对齐 motor imagery，捕捉运动相关的时间动力学而非 volume conduction 一类伪迹。收口于新采数据集上的机械臂连续控制闭环——下游解码、跨被试迁移、实时性。

> § **PHIL** `二作` — **规划层的先行工作**
>
> 逻辑链：EEG 带宽只够指定潜空间里的一个目标，不够指定一条连续轨迹；中间的路由世界模型 + MPC／CEM 补出来（LeWorldModel 一路的做法：把观测与目标编码进潜空间，CEM 优化动作序列最小化潜空间目标匹配代价，执行前 K 步即重规划）；而 MPC rollout 昂贵，实时闭环扛不住，需要学一个 cost-to-go 来截断规划。PHIL 学的 h(node, goal) 在 A* 中扮演的正是同一个函数角色——用学到的代价估计替代昂贵前瞻。
>
> **共享的是机制与功能角色，不是出发点** ，这是它区别于前三次失败安置的地方。

> ⚠️ **未定** — MPC＋CEM 规划路线 vs RL 策略路线。Year 5 计划写的是 RL。这个决定同时锁着 Ch8 的技术内容、脑信号的插入点（target embedding vs reward/actor conditioning）、以及 §PHIL 是否成立。

---

### Ch 10 · Conclusion

收到「神经信号 → 语义 → 动作」的闭环，以及从内在思维到物理具身这条路还差什么。
