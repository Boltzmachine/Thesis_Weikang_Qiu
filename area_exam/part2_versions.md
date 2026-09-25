# Part 2 · 当前口播主线与长短版本

此文件统一使用已确认的叙事：**PRISM I → MindLLM → PRISM II → D-Edit**。下面是同一主线的不同长度，不是互相竞争的工作顺序。这里的递进关系表达研究动机和方法设计，不代表四个模型已经组成一套经过整合评测的系统。

## 一句话

PRISM I 启发 fMRI 对齐空间的选择；MindLLM 将 fMRI 对齐到语言；PRISM II 基于语言重建视觉内容；其中按物体组织的表征和生成进一步激励 D-Edit，通过独立 item prompt 与 grouped cross-attention 加强生成端的解耦。

## 约一分钟

第一部分研究脑信号本身，第二部分要把脑活动接到外部世界。先问接到哪个空间：PRISM I 比较已有的视觉和语言表示，为选择语言作为 fMRI 的对齐目标提供依据。接着，MindLLM 用脑指令微调把 fMRI 对齐到语言，让多种脑功能都能以文本格式读出，而不局限于被试想说的话。

语言表征还能用于恢复视觉内容。PRISM II 将解码的语言组织成物体、属性、关系，再用物体中心的生成过程重建场景。这个物体结构又提出下一步问题：能否让生成端把每个物体的条件分得更明确？D-Edit 为每个 item 学习独立的 soft prompt，并用 grouped cross-attention 分开各区域与条件的交互。它在这条主线中的角色是加强逐物体解耦的生成方法，编辑任务展示的是这种局部控制能力。

## 完整口播

### PRISM I → MindLLM：先选空间，再学对齐

第一部分让模型利用脑信号的组织结构。要把这些信号接到外部世界，我们首先需要选择对齐目标。被试看的是图像，并不意味着最合适的目标一定是视觉隐空间。

PRISM I 对候选表示做了比较。在所测的视觉、语言和视觉–语言空间里，语言模型的语义表示更适合与 fMRI 对齐。这个结果给语言对齐提供了依据。它不是说大脑本身就是语言式的，而是在现有候选空间中作选择。

有了这个目标，MindLLM 研究怎样让 fMRI 真正与语言表征对齐。NSD 的被试看的是 MSCOCO 图像；通过共同图像，可以把脑记录和已有标注连接起来，形成 980,610 段多轮对话，不需要新增扫描。脑指令微调把感知、记忆与知识、语言与符号、复杂推理组织到同一种文本读出格式里。

所以 fMRI-to-text 不是简单翻译一个人想说的词。我们要的是可以表达多种脑功能的统一语言表征。

### MindLLM → PRISM II：从语言读出到视觉重建

语言读出建立以后，一个自然的下一步是利用语言重建被试看到的视觉内容。PRISM II 就研究这条路线：把从 fMRI 解码的语言信息作为生成条件。

仅有一段整体描述仍可能把物体和属性糅在一起。PRISM 将语言组织成物体、属性和关系，再按物体生成并组合场景。语言因此不只提供一句答案，还承载视觉重建需要的内容和结构。

### PRISM II → D-Edit：物体结构需要更强的生成解耦

PRISM 的 object-centric generation 已经按物体组织场景。这个设计进一步提出生成端的要求：每个物体是否也有独立的条件，并能与其它物体的注意力交互分开？

D-Edit 为每个 item 学习自己的 soft prompt，再用 grouped cross-attention 限定各区域与对应 prompt 的交互。它从 prompt 和 attention 两层加强逐物体解耦。文本、图像、mask 编辑及物体移除，是检验这种局部控制能力的具体任务。

因此这里引入 D-Edit，是把生成端从物体中心组织推进到更明确的 item 级条件与注意力解耦。不是在一个重建故事后面另加一个独立编辑工具。

## 英文过渡句

- **PRISM I → MindLLM:** The alignment comparison motivates language as a representation space for fMRI. MindLLM learns this alignment through brain instruction tuning.
- **MindLLM → PRISM II:** A language representation can also carry the content needed to reconstruct what a person sees. PRISM II reconstructs visual content from decoded language, organized into objects, attributes, and relations.
- **PRISM II → D-Edit:** Object-centric generation motivates a generator with stronger per-item disentanglement. D-Edit separates item prompts and their cross-attention to give each item more explicit control.

## 表述边界

- 四步是论证顺序，不是论文发表的时间顺序，也不表示四个模型共享或直接传递已经整合好的权重。
- D-Edit 的“更强”指 prompt 与 attention 的解耦机制，不等于已经在 PRISM 的 fMRI 重建实验中测得更高指标。
- 图像编辑是验证 D-Edit 局部控制能力的任务；它在 Part 2 中的角色是解耦生成端。
- 脑信号驱动 D-Edit 的完整整合仍需额外接口与验证，不能描述为已有实验结果。
