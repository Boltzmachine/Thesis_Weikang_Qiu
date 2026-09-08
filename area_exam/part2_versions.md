# Part 2 · 六个版本(中文口播稿)

| 版本 | 总分 | 三个视角 |
|---|---|---|
| ⑥ 无约束 | **24.3** | defensibility 8.5  /  no-part1-repeat 7.9  /  live-and-strategic 7.9 |
| ① 数据拿不到,所以每个工作都在绕开数据 | **21.8** | defensibility 5.5  /  no-part1-repeat 9.0  /  live-and-strategic 7.3 |
| ④ 一个工作当画框 | **19.6** | defensibility 2.5  /  no-part1-repeat 8.4  /  live-and-strategic 8.7 |
| ② PRISM 打头,当审计 | **18.5** | defensibility 6.5  /  no-part1-repeat 7.0  /  live-and-strategic 5.0 |
| ⑤ 按问题组织,不按论文 | **18.5** | defensibility 7.5  /  no-part1-repeat 5.3  /  live-and-strategic 5.7 |
| ③ D-Edit 打头,当规格书 | **13.7** | defensibility 4.0  /  no-part1-repeat 6.2  /  live-and-strategic 3.5 |



---

## ⑥ 无约束　`总分 24.3`

**[第 27 页 — 分隔页]**

第一部分给了我们能够读取大脑的模型。第二部分问一个更难的问题：读成**什么**？

**[第 28 页 — 已有的 fMRI-to-text 工作]**

在我们之前的工作，一次只回答一个任务：为被试看到的图像生成描述，或者把它检索出来。任务被写死在解码器里，换一个问题就要换一个模型，通常还要重新扫描一次。这才是瓶颈。不是架构，是监督信号。脑数据稀缺且昂贵；你不可能每想到一个新问题就回一趟扫描仪。

**[第 29 页 — MindLLM 总览]**

MindLLM 的回答是：大部分监督信号本来就存在，你只需要注意到它在哪里。编码器就是第一部分讲过的神经科学启发的注意力机制，我不再重复。这里新的是我们喂给它的东西。

**[第 30–31 页 — BIT 数据集]**

Natural Scenes Dataset 的被试看的是 MSCOCO 图像。而 MSCOCO 已经被标注了十年：caption、物体、问题、关系。所以图像就是一把**连接键**。它把一条 fMRI 记录和别人早就写好的文本连了起来。Brain Instruction Tuning 就建在这把键上：来自十五个数据集的 980,610 段多轮对话，没有新扫一次脑。

它覆盖四类脑功能。感知与场景理解。记忆与知识检索。语言与符号处理。复杂推理。有一个任务是我们自己推导出来的：为被试**上一张**看过的图像生成描述。它不存在于任何标注文件里，它是从 NSD 的试次顺序里落出来的。它是唯一一个问记忆、而不是问当下感知的任务。

**[第 32–33 页 — captioning、通用解码]**

Brain captioning 平均提升 3.32%。通用解码相对基线提升 12.0%，而我真正在意的是这个数：其中 28.0% 由 brain instruction tuning 贡献。是训练范式，不是编码器。

**[第 34–36 页 — 新任务、未见被试]**

这一页是我对自己领域的抱怨：很多任务和真实应用是脱节的。所以我们测了向两个按 BCI 相关性挑选的任务的适配——识别场景中有用的物体，以及读出他人的情绪：13.5%，其中 BIT 贡献 25.0%。还有一个模型从未见过的被试：在 1 到 7 号上训练，在 8 号上评测，不做任何微调，相对其他 subject-agnostic 架构提升 24.5%。它的机制属于第一部分；在这里它只是一个结果。

**[PRISM 新增页 A]**

于是我们落在了文本空间。我们是不是只因为标注恰好在那儿，才落在那儿？我们回头做了测量。把 fMRI 与预训练的视觉、语言、视觉—语言表示在既有的对齐指标下做比较，fMRI 与语言模型的文本空间对齐得最紧。这个 caveat 让我先说：那个比较的一侧是人写的 caption，另一侧是图像，所以它不是同类比较。我要辩护的是更弱、也更有用的那个结论：在我们**实际拥有**的表示空间里，文本是 fMRI 最容易被学出来的那个。而不是说大脑本身是语言式的。

**[PRISM 新增页 B、C]**

更锋利的发现是关于**结构**的。单一的统一表示会把物体和它的属性混在一起。被试看到的是一只灰色虎斑猫，模型重建出一只老虎。人的视觉是以物体为中心、组合式的，不是整体式的。所以 PRISM 让生成也变成组合式的：object-centric diffusion，加上一个用 VLM 搜索与神经活动相符的属性和关系的模块。在 NSD、BOLD5000、GOD 上，在**同一个 backbone**（Stable Diffusion 2.1）下，在 training-free 指标上取得最好或并列最好；LPIPS 最多比最强基线低 5.9%；重建 QA 准确率 60.54%，比第二名高 2.89 个点。

**[第 38–44 页 — D-Edit]**

这对下游有一个直接后果。如果目标空间是组合式的，那么"一整张图配一条 prompt"就是错的接口：你改猫，沙发跟着动。D-Edit 把图像切成 item，每个 item 有自己的 prompt，并用 grouped cross-attention 让每个区域只关注属于自己的那条 prompt。基于文本、基于图像、基于 mask 的编辑，以及物体移除，都在一个模型里，而且不需要整张图的完整文字描述。Item 级文本编辑：LPIPS 降 55.4%，CLIP-T 升 6.3%。移除任务我们做了**用户研究**，15 位标注者、30 组图像对：质量 4.01 对 3.26，保真度 4.44 对 2.42。

**[第 37 页那句话，放在最后讲]**

这里，第二部分接回了序章。完美的 prompt 永远无法被语言穷尽——那就不要让它是语言。让每个 item 的 prompt 成为一个**连续的**、可优化的 soft prompt。我们没有修好语言这条信道；我们是在控制的那一点上把离散的 token 拿掉了。最终产生那个向量的，是大脑。那就是第三部分。

---

**评委指出的硬伤:**

- None. Two repairable overreaches: the flat 'not architecture, supervision' line sits in tension with Part 1's own thesis, and authorship position is never spoken.
- The spine is a sequence of moves rather than an argument: supervision bottleneck, then 'did we land in text only because the annotations were there,' then the item-level consequence. It works, but nothing in it forces the next thing, so PRISM ends up demoted to an audit with the least stage time -- which its own analysis concedes understates the finding the committee is most likely to be curious about.
- No held tension. The spine is three claims joined by semicolons — supervision bottleneck, then audit, then consequence — so the listener always knows why they are hearing the current block but never carries a question across blocks. It is followable and forgettable: nothing in it makes the audience wait for anything. That is a real cost in a talk where Part 2 must feel like one argument rather than three well-ordered papers, and it is exactly the gap H4's frame fills.


---

## ① 数据拿不到,所以每个工作都在绕开数据　`总分 21.8`

第一部分建好了一个能读大脑的模型。第二部分要问的是：把它接到哪儿去。而这里撞上的墙，跟架构没关系。做对齐需要成对数据，而脑—文本的配对数据根本不存在：扫描慢、贵，而且每个大脑都是自己的一套坐标系。这个问题采不出来。所以这一部分的每项工作，都是在用不同的方式，绕开那些你拿不到的数据。

以往的 fMRI-to-text 工作，是先挑一个任务，再训练一个照着这个任务成型的解码器。这样得到的是一个 captioner，不是一个接口：人的意图不会按你的任务清单事先分好类。

先看 MindLLM，ICML 2025 —— 在这一部分里，它不是一个架构，而是一个数据集加一套训练范式。一个现成的、冻住的 LLM，前面接第一部分那个 neuroscience-informed 编码器，把 fMRI 变成 token，拼在指令前面。编码器我就只说这一句。

监督信号来自一次 join。NSD 的被试躺在扫描仪里看的是 MSCOCO 图片，而 MSCOCO 已经被标注了十年。图片就是那把钥匙：它把一段 fMRI 记录，和别人早就写好的文本连了起来。没有新采一次扫描。最后是 980,610 段多轮对话，来自 15 个已有数据集，覆盖感知、记忆与知识、语言与符号，以及推理。

只有一个任务是我们自己造的：描述被试在这一张之前看到的那张图。这个标签不在任何标注文件里，它来自 NSD 的试次顺序。它是这里唯一一个关于记忆、而不是当下感知的任务，也是一个只看当前刺激的 captioner 装不出来的任务。

结果。Brain captioning，平均 +3.32%。Versatile decoding，相对基线 +12.0%，其中 brain instruction tuning 本身贡献了 28.0%。模型从没见过的新任务 —— utility/affordance，以及 sentiment understanding，两个都是按 BCI 的需要挑的 —— +13.5%，其中训练范式贡献 25.0%。还有留出被试：用 1 到 7 号训练，在 8 号上测，不做任何 finetune，相对其他 subject-agnostic 架构 +24.5%；这里它是一个结果，不是一个新机制。

真正重要的是那两个 ablation。除了训练数据，什么都没变。所以做事的是范式，不是架构。

但这个目标空间，是我们在拿到证据之前就选定的：我们把大脑映射进语言模型的空间，是因为我们想要语言输出。PRISM，ICLR 2026，第三作者，直接检验了这件事 —— 在通行的对齐指标下，把 fMRI 分别和预训练的视觉、语言、视觉—语言表示做比较。最接近的是语言模型的文本空间。这张表要小心地读 —— 一边是人写的 caption，另一边是图像，并不是同一量纲的比较 —— 所以我们要的是那个窄一点的结论：在我们现成能用的表示空间里，文本是 fMRI 最容易被学到的那一个。这是第二次绕开：目标空间是别人已经预训练好的，用的是我们永远采不到的数据。

PRISM 接着把这个目标做细。一个统一的隐表示会把物体和它的属性混在一起：被试看到的是一只灰色带虎纹的猫，生成出来的是一只老虎；而人的视觉是以物体为中心、组合式的。所以 PRISM 把文本结构化成物体、属性和关系，配上 object-centric 的 diffusion，以及一个用 VLM 去搜索哪些属性和关系真正成立的模块。在三个 fMRI 数据集上，用同一个 backbone、Stable Diffusion 2.1，它在 training-free 指标上最好或并列最好：LPIPS 最多比最强基线低 5.9%，重建的 QA 准确率 60.54%，比第二名高 2.89 个点。

这就带出最后一个问题，也就是这页写的：一个完美的 prompt，永远没法被语言穷尽。如果桥是组合式的，生成端就必须能在同样的粒度上被控制 —— 而且必须在没有完整描述的前提下工作，因为大脑永远不会给你一段完整描述。那就干脆不写。D-Edit，AAAI 2025，第二作者：把图切成 item，每个 item 给它自己的 prompt，是连续的、可优化的，而不是一句话；grouped cross-attention 保证每个区域只关注属于它自己的 prompt。文本编辑、图像编辑、mask 编辑和物体移除，都在一个模型里。文本 item 编辑把 LPIPS 降了 55.4%，图像 item 编辑降了 26.9%；物体移除上，15 位标注者的 user study 在质量和保真两项上都更偏好它。

今天这些 prompt 来自分割和优化。这一部分要说的是：这个插槽的形状现在是对的 —— 连续、按 item、永远不用写出来 —— 正好留给神经信号去填。第三部分，从"你看到了什么"转到"你想做什么"。

**评委指出的硬伤:**

- The spine — 'each work here is a different way of not needing the data you cannot get' — is retrofitted and does not hold under one push. PRISM as 'the second escape: the target space was already pretrained, on data we could never collect' is not what PRISM shows; PRISM measures alignment, and the 'already pretrained' property is equally true of the vision latent PRISM argues against, so the framing does not discriminate between the options it claims to adjudicate. D-Edit as an escape from data scarcity is a third stretch — it escapes needing a full CAPTION, not needing SCANS. A committee member asking 'how is PRISM a data-scarcity result?' gets no answer.
- PRISM is reduced to two sentences of framework and one of results, so a reconstruction-minded examiner will feel underserved and will ask about the modules. And the part ends with ~90 seconds of image editing with no brain data in it -- slide 37's line is the only thing preventing the audience from remembering Part 2 as 'and then a diffusion paper.'
- Two frames running at once. The announced spine is data scarcity, but the spine that actually carries PRISM into D-Edit is compositional granularity, and those are different arguments. Escape #2 is where they pull apart: PRISM does not claim 'use text because it was pretrained on data we could never collect' — it claims fMRI aligns most closely with text space and that structure pays. The data reading is imposed on the paper, and a listener tracking the announced frame will find the D-Edit handoff arrives from a premise (compositionality) the frame never promised. Also the longest draft in the set — closer to 790 words than the stated 700, which at ~6.5 minutes is a real overrun — and it ends with roughly ninety seconds of image editing with a closing line ('the slot is now the right shape') noticeably weaker than H4's spec or H6's discrete-token clause.


---

## ④ 一个工作当画框　`总分 19.6`

我想从这一部分的结尾讲起，先说那句我最后会回来的话。

当你想让生成模型画出某个人脑子里的那幅画时，你要给它写一个 prompt。而一个完美的 prompt 永远无法被语言穷尽——总还差一个形容词。所以这座桥交给世界的东西，不会是一句话。它必须是一个 soft prompt：连续的、可优化的，并且最终由神经信号产生。现在这还只是一句口号；请记住它。

首先是"怎么过去"。MindLLM 把第一部分那个 subject-agnostic 的 fMRI encoder——也就是 neuroscience-informed attention——产生的 token，前置到一个冻结的现成 LLM 的指令前面。只有 encoder 参与训练，所以这个系统会做什么，全都是从数据里学来的。而瓶颈在监督信号：扫描时间很贵，所以几乎每个 fMRI 解码器都只在一个任务上训练，通常是 captioning，最后就长成了那个任务的形状。

我们做 Brain Instruction Tuning，没有采集任何一次新的扫描。NSD 的被试当时看的是 MSCOCO 图像，而 MSCOCO 图像本身就带有大量文本标注。图像是一把 join key：它把一次脑活动记录，和别人早就写好的文本连接起来。把这把钥匙在十五个数据集上转一圈，就得到 980,610 段多轮对话，覆盖四类脑功能：知觉与场景理解、记忆与知识检索、语言与符号加工、复杂推理。

有一个任务不在任何标注文件里：给被试**上一张**看到的图写 caption。它是从 NSD 的试次顺序里直接掉出来的，而且是这里唯一一个关于记忆、而不是关于当下知觉的任务。

结果。Brain captioning，平均提升 3.32%。Versatile decoding，比基线高 12%，其中 brain instruction tuning 本身贡献 28%。两个全新任务，都是按 BCI 的需要挑的——找出场景里有用的物体，以及读懂别人的情绪——提升 13.5%，其中 tuning 贡献 25%。还有一个模型从没见过的被试：用 1 到 7 号训练，在 8 号上评测，不做任何 finetune，比其他 subject-agnostic 架构高 24.5%。为什么能迁移，第一部分已经解释过了；在这里它只是一个结果。

请看这些消融。让这个解码器具备任务灵活性的，不是架构，是数据。

用文本做监督，本来是机会主义——它正好躺在那儿。PRISM 要问的是：它是不是也恰好是对的。

这个领域默认中间空间应该与刺激同模态：要重建图像，就对齐到视觉 latent。而把 fMRI 与预训练的视觉、语言、视觉—语言表示放在一起比较，fMRI 与语言模型的文本空间最接近。这里有一个请大家盯住我的 caveat：那个比较的一边是人写的 caption，另一边是图像，并不是同等条件的对比。我要辩护的是更弱的说法——在我们能拿到的表示空间里，文本是 fMRI 最容易被学出来的那一个；而不是说大脑本身就是语言式的。

第二个发现说明了为什么单纯的文本也不是答案。一个统一的隐向量会把物体和它的属性混在一起：被试看到的是一只灰色的、带虎纹的猫，模型生成了一只老虎。人的视觉是以物体为中心、组合式的，所以 PRISM 让生成也变成组合式的：object-centric diffusion，加上由 VLM 辅助的属性与关系搜索。在 NSD、BOLD5000 和 GOD 上，在同一个 backbone（Stable Diffusion 2.1）下，它在 training-free 指标上最好或并列最好：LPIPS 比最强基线低最多 5.9%，重建的 QA 准确率 60.54%，比第二名高 2.89。

这就把我带回到 prompt。

如果终点是组合式的——物体、属性、关系——那么生成端的接口就必须在同样的粒度上可控，否则一个意思是"是猫不是虎"的向量，会把整张图一起拖走。D-Edit 把图像切成 item，每个 item 有自己的 prompt，靠 grouped cross-attention 让每个区域只关注属于自己的那条。item 级的文本编辑把 LPIPS 降低 55.4%，CLIP-T 提高 6.3%；在一个 user study 里，十五位标注者给它的物体移除在 fidelity 上打 4.44，对照是 2.42。

所以，回到开头那句话。它听起来像是在抱怨语言不够用；其实它是一份规格说明。这座桥的落点必须是连续的、由物体而不是句子来组织的、并且可以一个 item 一个 item 地寻址——而第二部分把这三件事都建出来了。让神经信号去驱动这些 item prompt，是 future work：那就是第三部分。

---

**评委指出的硬伤:**

- The frame indicts the part's own flagship. It asserts 'what this bridge hands to the world is not a sentence' and closes 'the bridge has to land in something continuous, structured by objects rather than by sentences... and Part 2 built all three.' MindLLM's entire output IS sentences — captions, VQA answers, previous-captions. The first-author work that occupies the most airtime fails the spec the frame just declared, and the narrative has no answer to 'then what is MindLLM for, on your own account?' The analysis's defense makes it worse, since BIT's supervision is itself discrete text. Second, independent hole: 'Only the encoder trains, so whatever this system can do, it learned from the data' is directly contradicted by the source, which freezes the LLM precisely 'to preserve the LLM's language modeling prior' (Parts/part2.tex:46) — the system's capability is largely web pretraining, not BIT. Third, it silently drops slide 28 without listing that in its costs.
- Both rhetorical peaks -- the open and the close -- go to the second-author paper, and the first-author flagship sits in the middle, the weakest emphasis position. For a lens that asks whether BIT is presented as what it is, structurally demoting it is a real cost even when the labeling is correct. Also the most deck surgery: the slide-37 line must move to slide 27 and slide 37 be re-cut as a deliberate callback, or the line lands twice and weakly.
- Both rhetorical peaks — open and close — belong to a second-author paper's slide, and the first-author flagship sits in the structurally weakest middle position. The draft's own analysis concedes this. It is defused rather than solved: slide 37's line is the candidate's own framing authored for this talk, not D-Edit's contribution, so framing on it is synthesis rather than centring someone else's paper — but the speaker has to make that distinction audible or a committee member will read the part as 'the thesis of your bridge chapter is an image-editing paper.' Secondary: the frame is a promissory note that only Part 3 discharges.


---

## ② PRISM 打头,当审计　`总分 18.5`

第一部分给了我们在神经模态内部读取脑信号的模型。第二部分要问的是：把这些信号写进哪个空间。

这个领域有一个默认答案，自然到几乎没人去审它：被试看的是图像，那就解码到图像的 latent 里。那就先审它。这是 PRISM，我是第三作者，我会严格说清楚它证明了什么。

PRISM 用既有的对齐指标，把 fMRI 分别和预训练的视觉、语言、视觉—语言表示做比较。结果是：fMRI 与语言模型的文本空间对齐得更紧。先说 caveat，因为这也是我自己第一个会攻击的地方：那张表的一侧是人写的 caption，另一侧是图像，不是同类对同类。它真正站得住的结论要窄得多——在我们手上真正可用的这几个空间里，文本是 fMRI 相关性最高、也最容易被学出来的那个。不是说大脑本身就是语言式的。

第二个发现让它落地：当文本和生成模型都被适配到组合结构——物体、属性、关系——重建质量会提升。一个统一的隐表示会把物体和它的属性混在一起，于是被试看的是一只灰色虎斑猫，模型生成的是一只老虎。人的视觉是以物体为中心的，不是整体式的。所以有了 object-centric diffusion，加上一个 VLM 辅助的属性/关系搜索。在 NSD、BOLD5000、GOD 上，在同一个 backbone、也就是 Stable Diffusion 2.1 之下，training-free 指标上最好或并列最好；LPIPS 最多比最强基线低 5.9%。我们没有做过"把视觉 latent 拿掉"的消融，所以结论不是视觉 latent 没用。结论是：目标空间是结构化的、组合式的、文本形状的。

记住这个目标。这一部分剩下的内容，一半是怎么朝它训练，一半是怎么消费它。

朝它训练的是 Brain Instruction Tuning，我自己的工作，ICML 2025。只回头一句，然后就不再重复：第一部分那个 subject-agnostic 的注意力把 fMRI 变成 token，放在 instruction 和一个冻结的现成 LLM 前面。按时间顺序，这个工作其实在那次测量之前；我给的是逻辑顺序，不是年表。

新的东西不是架构，是监督信号——而且没有采一次新的扫描。NSD 的被试看的是 MSCOCO 图像，而 MSCOCO 图像本来就带着丰富的文本标注，所以图像就是一把 join key，把一次 fMRI 记录和已经存在的文本连起来。这样得到 980,610 组多轮对话，来自 15 个数据集，覆盖四类脑功能：感知与场景理解，记忆与知识提取，语言与符号处理，复杂推理。其中有一个任务在任何标注文件里都不存在：给被试上一张看过的图写 caption。它是从 NSD 的试次顺序里推出来的，它关的是记忆，不是当下的感知。

真正起作用的是这套范式，不是架构。brain captioning 提升 3.32%。versatile decoding 比基线提升 12.0%，其中 instruction tuning 本身贡献 28.0%。适配到全新任务——utility/affordance，以及 sentiment understanding，都是按 BCI 相关性选的——提升 13.5%，其中 instruction tuning 贡献 25.0%。用被试 1 到 7 训练，在一个模型从没见过的被试上评测，不做任何 finetune：比其他 subject-agnostic 架构高 24.5%。这件事的机制在第一部分讲过了；在这里它只是一个结果。换来的是一个 task-flexible、而不是 task-shaped 的解码器。

如果目标空间是组合式的，那么消费它的那一端就必须能在同样的粒度上被控制，否则改一个物体会重写整张图。这就是 D-Edit，我是第二作者。把图像切成若干 item，每个 item 有自己的 prompt，grouped cross-attention 让每个区域只注意属于它的那个 prompt。一个模型同时覆盖基于文本、基于图像、基于 mask 的编辑和 item 移除，而且不需要整张图的完整文字描述。item 级的文本编辑把 LPIPS 降低 55.4%，CLIP-T 提高 6.3%。移除任务上，在一次 user study 里，fidelity 是 4.44 对 2.42。

这就是 D-Edit 放在这一部分收尾的原因。一个完美的 prompt 永远无法被语言穷尽——这是开场那句话又回来了。出路是 soft prompt：连续的、可优化的，不是一个词。连续——也就是说它根本不必被打出来。今天这些 token 是从像素里优化出来的；而一个 item 级的连续 prompt，恰好就是神经信号有可能产生的那种东西。这个接口，就是第二部分交给第三部分的东西。

第二部分把信号带到了一个世界能读的表示。第三部分要问的是：当输出不是图像，而是动作。

---

**评委指出的硬伤:**

- Structural, and it is a defensibility flaw not merely a rhetorical one: it makes the confounded claim the part's FIRST PREMISE. Every downstream sentence then inherits the caption-vs-image asymmetry, and the speaker spends the rest of the part standing on a table he has already conceded is not like-for-like. Its own analysis admits this — 'the part's opening move now inherits PRISM's caveat.' It also makes the arithmetic error explicit ('instruction tuning itself contributes 28.0% of that'), and it opens on third-author work, which invites the authorship question at the moment the audience is forming its judgment of the part.
- It makes the caveated third-author table the load-bearing premise of the entire part, and opens with it. Its own analysis names this as the first hostile attack and then has to spend move 2 arguing that BIT's ablation survives if the table is thrown out -- which concedes the premise was never really load-bearing, undercutting the ordering that motivated putting it first. Compounding it: the part's opening two minutes are about image reconstruction in a part whose payload is representation, and 90 seconds elapse before the audience hears any first-author work.
- Worst opening in the set for this candidate, and the damage is done in the first thirty seconds. The second sentence of Part 2 is 'This is PRISM; I am third author, and I will be precise about what it shows,' immediately followed by conceding the captions-versus-images confound. The first thing the audience learns about the part is a disclaimer attached to a paper the candidate did not lead — that is the exact 'what did you do on this one' moment the lens asks about, staged voluntarily and up front. Then it compounds the error by speaking a negative result on stage — 'No ablation deletes the vision latent' — which raises a doubt nobody had asked about and hands the room a follow-up for free; that concession belongs in the analysis and in Q&A, not in the narration. Structurally it also breaks the Part 1 handoff (Part 1 ends on the encoder; Part 2 spends its first ninety seconds on pixels) and puts the first-author flagship in the middle. H5 does the same ordering with better scaffolding and a less self-damaging opening.


---

## ⑤ 按问题组织,不按论文　`总分 18.5`

Part 1 一直待在脑信号内部。Part 2 是它与世界相遇的地方。三个问题。脑表征应该落到哪个空间？在脑数据稀缺、昂贵、且因被试而异的情况下，监督从哪里来？以及，接收端必须能做什么？

第一：落到哪里？这个领域的默认答案是与刺激的模态对齐——你要拿回一张图像，所以你把 fMRI 对齐到视觉 latent。PRISM——ICLR 2026，我是第三作者——质疑这个默认。我们用已有的对齐指标，把 fMRI 分别与预训练的视觉、语言、视觉—语言表征作比较；fMRI 与语言模型的文本空间最接近。有一点必须说清楚：这个比较的一侧是人写的 caption，另一侧是图像，并非严格同类对比。它能支持的结论是：在我们手上现有的这些表征空间当中，fMRI 最容易被学到、相关性最高的是哪一个——而不是说大脑本身就是语言的。

只有扁平的文本也不够。单一的统一隐表征会把物体和它的属性混在一起：被试看到的是一只灰色的、有虎纹的猫，模型生成了一只老虎。人的视觉是以物体为中心、组合式的。所以 PRISM 的第二个发现是：当文本和生成模型都被适配到这种结构——物体、属性、关系——重建质量会提升。于是有了 object-centric diffusion，以及 VLM 辅助的属性搜索。在 NSD、BOLD5000 和 GOD 上，backbone 全程固定为 Stable Diffusion 2.1，PRISM 在 training-free 指标上最好或并列最好：LPIPS 最多比最强基线低 5.9%，NSD 重建 QA 为 60.54，高出 2.89。

结构化的、类文本的、组合式的。那么这样的监督从哪来？没人会出钱去扫十万次新的脑。我们一次都没扫。NSD 的被试看的是 MSCOCO 图像，而 MSCOCO 是世界上标注最密集的语料之一。图像就是一把 join key：它连接一次 fMRI 记录和已经存在的文本。转动这把钥匙，就得到来自 15 个数据集的 980,610 段多轮对话，覆盖四类脑功能：感知与场景理解，记忆与知识检索，语言与符号处理，复杂推理。有一个任务只属于我们：previous caption——为被试在这一张之前看到的那张图写 caption。它不在任何标注文件里，它来自 NSD 的试次顺序；它也是唯一一个关于记忆、而不是关于当下感知的任务。

这就是 MindLLM，ICML 2025，我是第一作者：一个冻结的现成 LLM，前面接 Part 1 那个 subject-agnostic 编码器，把 fMRI 变成 token 拼在指令前面。那个编码器是 Part 1 的贡献；这里的主张是——真正起作用的是训练范式。Brain captioning，提升 3.32%。Versatile decoding，比基线高 12——消融把其中的 28 归给 instruction tuning 本身。新任务适配，提升 13.5，其中 BIT 贡献 25——新任务是 utility and affordance 与 sentiment understanding，两个都是按 BCI 的需要挑的。还有一个模型从未见过的被试：在 1 到 7 上训练，在 8 上测试，不做任何微调，比其他 subject-agnostic 架构高 24.5。编码器自始至终是同一个。数据集和范式才是贡献。

第三：接收端必须能做什么？一个组合式的目标空间，只有在接收它的东西能在同样粒度上被控制时才有用——否则改一个物体就会把整张图拖着走。这就是 D-Edit——Feng 和我，AAAI 2025。它把图像切成若干 item，给每个 item 各自的 prompt，而不是整张图一个 prompt；grouped cross-attention 让每个区域只 attend 到属于它自己的那个。一个模型就覆盖了基于文本、基于图像、基于 mask 的编辑以及 item 移除，而且不需要对整张图的完整文字描述。Item 级的文本编辑把 LPIPS 降低 55.4%，同时 CLIP-T 提升 6.3；基于图像的编辑是 26.9 和 10.3。至于移除，一个 15 人标注者的 user study 在质量和保真度上都更偏好它。

这就回答了开场。完美的 prompt 永远无法被语言穷尽——所以 item prompt 不是一个词，而是一个 soft prompt：连续的、可优化的。开场说语言是一条有损的信道，这一部分并不收回那句话：落点是文本空间那个连续的、结构化的邻域，而不是词本身——而连续的 prompt，正是神经信号能够产生的东西。那就是 Part 3。

---

**评委指出的硬伤:**

- The concession lives only in the analysis, not on stage. The spoken text chains 'Structured, text-like, compositional. So where does that supervision come from?' — a 'So' that implies BIT's text target was derived from PRISM's finding. That is chronologically false, and unlike H1, H2, H4 and H6, H5 never says so aloud. A committee member who knows the venue dates (ICML 2025 before ICLR 2026) gets a free hit the speaker has no scripted answer for.
- It is the only draft that presents PRISM as BIT's premise while never disclosing on stage that PRISM postdates it -- the one honesty move H1, H2, H4 and H6 all make aloud. Its own analysis knows the exposure ('the licensing is retrospective'), so the narrative leaves open a hit the writer had already seen. Weakest ablation emphasis of the six: 'Same encoder throughout' is a trailing clause after the numbers, not a beat, so the paradigm claim never gets the stress the lens demands. And the hinge transition -- 'Structured, text-like, compositional. So where does that supervision come from?' -- is a non-sequitur: PRISM's finding implies nothing about where supervision comes from, so the braid is three answers in sequence rather than three constraints on each other.
- The three-question scaffold is a taxonomy, not a thesis. Announcing three questions tells the audience the part has three parts; it does not tell them what the part claims, so Part 2 becomes a well-labelled survey and the listener leaves with a structure rather than a sentence. Compounding it: PRISM-first means the third-author paper with the conceded confound opens the part, the candidate's ICML first-author work lands in the weakest middle slot, and the handoff from Part 1 — which ends on MindLLM's encoder — is broken by ~90 seconds of image-reconstruction material before MindLLM is named again. Also strands slide 28, which the source shows carries the cleanest justification for previous-captioning.


---

## ③ D-Edit 打头,当规格书　`总分 13.7`

我想从这一部分的末端讲起，因为输出端最后反过来规定了输入端。

D-Edit。把一张图切成若干 item，每个 item 有自己的 prompt，而不是整张图共用一个 prompt。分组交叉注意力让每个区域只关注属于自己的那个 prompt。于是一个模型就同时支持基于文本、基于图像、基于 mask 的编辑以及物体移除，而且不需要对整张图做完整的文字描述。

但这一行才是重点。一个完美的 prompt 永远无法被语言穷尽。所以我们真正优化的那个把手不是一个词，而是一个 soft prompt：连续的、可优化的，活在 embedding 空间里，不在词表里。这就是开场关于语言的那个论断，以工程约束的形式重新出现。既然它是连续的，接下来的问题就是：还有什么能产生它？在 D-Edit 里，是优化产生的。在这篇论文里，它应该由神经信号产生。

反过来读，D-Edit 就是一份规格说明。我们把大脑解码成的东西，必须是连续的而不是一句话；必须在 item 这个粒度上有结构，因为接口就是这个粒度；而且不能被某一个任务塑形，因为在这里，编辑、描述、移除是同一个模型。有两项工作满足这份规格——各满足一半。

PRISM 回答的是：解到哪个空间？领域里的默认假设是中间 latent 应该与刺激同模态：输入是图像，就对齐到视觉 latent。在既有的对齐度量下，fMRI 与语言模型文本空间的接近程度，高于它与预训练视觉表示或视觉—语言表示的接近程度。有一个 caveat，请务必揪住我：这个比较的一边是人写的 caption，另一边是图像，所以它不是同类相比。我要辩护的是一个很窄的结论——在我们能拿到的这些空间里，文本空间是 fMRI 最可学的那一个——而不是大脑真的是语言式的。

第二个发现才是满足规格的那一个。当文本和生成模型都被适配到组合式结构——物体、属性、关系——重建质量会提升。它所修复的那个失败很有诊断性：一个统一的隐表示会把物体和它的属性混在一起——被试看到的是一只灰色虎斑猫，模型生成的却是一只老虎。人的视觉是以物体为中心的，不是整体式的。所以：object-centric diffusion，加上一个由 VLM 辅助的属性与关系搜索。在 NSD、BOLD5000、GOD 上，在相同 backbone（Stable Diffusion 2.1）下，training-free 指标上最好或并列最好：LPIPS 比最强 baseline 最多低 5.9%；NSD 重建 QA 60.54%，比第二名高 2.89。

D-Edit 是从「可控生成需要什么」走到 item 级结构的；PRISM 则是从对大脑的测量走到同一个粒度的。两个独立的约束，指向同一个接口。

规格的另一半是监督信号，那就是 Brain Instruction Tuning。编码器就是第一部分那个 subject-agnostic 的编码器，把一次扫描变成若干 token，拼在指令 token 前面，送进一个冻结的 LLM。这一部分新的东西，是一个数据集和一个训练范式。

一个任务灵活的 bridge 需要任务多样的监督，而扫描时间是最贵的数据。我们没有采集任何一次新的扫描，就把它建出来了。NSD 的被试看的是 MSCOCO 图像，而 MSCOCO 图像本身已经带着丰富的文本标注。图像因此是一把 join key：它把一次脑记录，和别人早就写好的文本连接起来。在十五个数据集上转动这把钥匙，得到 980,610 段多轮对话，覆盖四类脑功能——知觉与场景理解，记忆与知识检索，语言与符号处理，复杂推理。

有一个任务在任何标注文件里都不存在：为被试上一张看过的图写 caption。它是从 NSD 的试次顺序里掉出来的，而且是这里唯一一个关于记忆、而非当下知觉的任务。

是范式，还是架构？消融给出答案。Brain captioning：平均提升 3.32%。Versatile decoding：比 baseline 高 12.0%，其中 brain instruction tuning 贡献 28.0%。两个全新的任务，都是按 BCI 相关性挑的——识别场景中有用的物体，以及读出他人的情绪——提升 13.5%，其中 tuning 贡献 25.0%。还有一个模型从没见过的被试：在 1 到 7 号被试上训练，在 8 号被试上评测，不做任何 finetune，比其它 subject-agnostic 架构高 24.5%。让这个解码器具备任务灵活性的不是架构，是数据。

所以这座桥两半都有了：一个按输出接口的要求被结构化的目标空间，以及一种不采新扫描就能大规模监督它的办法。用神经信号去驱动那些 item prompt，仍然是 future work。而这一部分的一切最终仍然停在一张图或一句话上；第三部分要问的是，当末端不再是图像、而是一具身体，会发生什么。

**评委指出的硬伤:**

- The 'D-Edit is a specification' derivation contains an equivocation with no answer. Its third clause reads: the decoder must be 'not shaped to one task, because here editing, describing and removing are one model.' D-Edit's coverage of multiple EDITING OPERATIONS has no bearing on whether a brain decoder should span perception, memory and reasoning; the word 'task' means two unrelated things across that 'because'. Asked 'why does supporting mask edits imply my decoder should do memory retrieval?' the speaker is stuck. Compounding it, the item-level requirement is derived from an output interface that was itself an arbitrary design choice — the specification is circular. It also drops slide 28, and its own analysis concedes this costs the UMBRAE contrast, which is the cleanest justification for the previous-caption task.
- The spec frame holds for PRISM and breaks at BIT. D-Edit's interface can specify continuity, item granularity, and task-independence; it cannot specify anything about where supervision comes from, so 'The other half of the spec is supervision' is a joint the frame does not actually reach -- and it fails precisely at the first-author work the lens cares most about. It also opens a part titled 'The Bridge' with a second-author image-editing paper containing no brain data, lands the flagship last where any overrun eats it, and its own analysis concedes it loses slide 28's UMBRAE contrast, which is the cleanest justification for the previous-caption task.
- It opens a part titled 'The Bridge,' immediately after Part 1 ended on a brain encoder, with a second-author image-editing paper containing no brain data, and gives the audience no reason to care for roughly the first sixty to ninety seconds — the longest unresolved question in the set, in the position where a live audience is least willing to hold one. It then puts the ICML first-author flagship dead last, where any overrun eats it, which under this lens is close to disqualifying. The spec frame is also over-claimed: 'not shaped to one task, because here editing, describing and removing are one model' does not actually specify BIT's task-flexibility — D-Edit's multi-task coverage and BIT's instruction diversity are unrelated properties, so one third of the spec is a rhetorical bridge with no load. Largest deck surgery (37-44 before 29-36), and it explicitly strands slide 28's UMBRAE contrast, which the source shows is the cleanest available motivation for the previous-caption task. Finally, the prologue payoff is spent in the first minute and never returns, so the part drifts away from its own strongest moment.