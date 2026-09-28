# 四个核心 Chapter · 当前口播主线与长短版本

本文件沿用 `part2_versions.md` 的旧文件名，现在记录整篇 thesis 的四章口播，不再代表 Part 2。固定顺序为 **HyBRiD → MindLLM → MWM → DySta**，四篇一作分别构成一个完整的核心 chapter；其他工作围绕主线提供背景、比较或延伸，不承担核心论证的前提。

贯穿问题是：**如何学习连接脑活动与世界交互的表征？** 四章依次研究脑的组织结构、脑中与世界有关的语义内容、以行动的视觉后果为监督学习动作表征，以及物理世界中的行动。四章围绕从脑信号、语义到行动的递进，服务于将人的意图转化为物理世界交互的总体目标。

## 一句话

HyBRiD 通过学习有用的神经先验提高预测性能，MindLLM 从脑活动读出涵盖感知、语言与知识相关任务的语义内容，MWM 以行动的视觉后果为语义监督学习支持行动意图解码的表征，DySta 则研究如何将人的意图转化为有效且高效的任务执行。

## 约一分钟

我的 thesis 由四篇一作、四个核心 chapter 构成，研究如何学习连接脑活动与世界交互的表征。

HyBRiD 从脑信号的组织方式入手，学习有用的高阶脑区关系并提高预测性能。MindLLM 将研究推进到语义内容，用跨被试的 fMRI 编码器和脑指令微调，支持感知、语言与知识相关的多种文本解码任务。MWM 则从 semantics（行动的视觉后果）推进到 action：用视频中可见的行动后果作为监督，学习 EEG 中的动作表征。具体方法把 EEG 编码成 latent action，再用它预测未来视觉表征，从同步的脑信号与第一视角视频中学习。最后，DySta 承接行动意图解码，研究如何将人的意图转化为有效且高效的任务执行。静态与动态信息的分离支持多帧推理并减少重复计算，让任务完成更有效、更高效。

四章从脑的组织结构走向语义内容，再以视觉后果学习动作表征，最终走向物理行动，各自验证相应的研究问题。

## 完整口播

### HyBRiD：脑信号如何组织成与认知相关的结构？

要理解脑活动，首先需要决定如何组织高维脑信号。许多脑网络方法以两两脑区连接为基本单位，但与认知有关的信息也可能分布在多个脑区的组合中。如何从数量庞大的组合中找到有用结构，是 HyBRiD 的问题。

HyBRiD 用可学习的 masks 识别高阶脑区关系，再根据每个被试的数据计算这些关系的权重。其 multi-head drop-bottleneck 目标要求保留与认知指标相关的信息，同时减少对无关输入信息的保留。共享的关系结构使不同被试可以在同一种组织方式下比较，个体差异则体现在学到的权重中。

这一章建立的是与认知预测相关的结构表征。接下来的问题是：除了预测一个预先指定的认知指标，脑活动中与外部世界有关的具体内容，能否被更灵活地读出？

### MindLLM：脑中的世界语义内容如何被读出？

MindLLM 把跨被试编码与多任务语义读取作为一个完整问题来解决。不同被试的响应体素数量和空间分布不同，因此首先需要一个能够接受这些差异的 fMRI 编码器。MindLLM 用可学习的 queries 聚合体素；attention 的 keys 由位置和脑区信息构成，values 则保留 fMRI 信号，使可共享的功能先验与个体观测在编码过程中各自发挥作用。

编码器需要与读取任务一起学习。MindLLM 通过刺激图像连接 fMRI 记录和既有文本标注，构建 Brain Instruction Tuning 数据，并将脑表征接入语言模型。这样，同一个模型可以根据不同指令完成描述、问答等多种文本解码任务。编码器与 BIT 共同构成这一章：前者解决怎样表示不同个体的脑活动，后者解决怎样按任务读取其中的语义信息。

这一章从脑活动中读取语义内容。接下来，语义表征能否帮助我们理解动作？MWM 利用行动的视觉后果作为语义监督，学习脑信号中的动作表征。

### MWM：如何从行动的视觉后果学习动作表征？

MWM 在主线中连接 semantics 与 action：行动的视觉后果提供语义监督，使脑信号中的表征获得动作含义。具体实现将同步的 EEG 和第一视角视频用于联合学习。mind model 把截至当前时刻的 EEG 编码为 latent action，world model 在当前视觉状态和这一 latent action 的条件下，预测未来帧的视觉表征。未来的视觉变化由此为运动相关脑表征提供学习信号，预训练无需动作类别标注。

FA-EEG 是 MWM 工作自身的内容，纳入本章关于运动 EEG 左右结构与编码方法的讲述。Lateralization-Aware Transformer 分离双侧共享成分与偏侧成分，在视频水平翻转时只交换相应的偏侧特征。这让脑信号的组织方式与跨模态学习目标相互配合。

训练后保留两个模型：mind model 用于下游运动解码，推理时只需 EEG；world model 保留动作条件预测能力，并通过独立测量的 IMU 到其动作接口的适配进行评估。因此，这一章的贡献同时落在运动脑表征和动作条件的世界预测上。

在通过视觉后果学习支持行动意图解码的动作表征之后，最后一章研究如何将人的意图转化为有效且高效的任务执行。

### DySta：怎样将人的意图转化为有效且高效的任务执行？

DySta 研究如何让机器人策略将人的意图转化为有效且高效的任务执行。给定描述期望结果的语言指令和视觉观察，模型决定并输出完成任务所需的机器人动作。只看当前一帧会遗漏任务历史，例如无法判断按钮是否已经按过；直接加入许多过去帧，又会带来很长的上下文和较高的推理开销。

DySta 利用场景信息具有不同时间持续性的特点，将视觉 tokens 分成动态成分和多层静态成分。跨时刻持续存在的静态信息在上下文中只保留一份，动态信息则保留多步历史，从而支持紧凑的多帧输入。静态 tokens 的 KV cache 可以跨步复用，learnable recache gate 决定何时更新，降低重复计算的成本。

这一章通过任务完成率和效率实验，检验策略能否有效且高效地实现指定目标，其中需要历史信息的任务用于测试多帧能力。它以机器人的观察、指令和动作作为研究对象，独立完成物理世界这一端的论证。

四章的联系在于逐步扩展研究对象：从与认知有关的脑组织结构，到脑中的世界语义内容，再通过视觉后果学习动作表征，最后到物理世界中有效且高效地实现指定目标。

## 英文过渡句

- **Opening:** This dissertation studies how to learn representations that connect brain activity with interaction in the world. Its four core chapters examine brain organization, semantic content, learning action representations from visual consequences, and action in the physical world.
- **HyBRiD → MindLLM:** HyBRiD learns higher-order brain structures to improve predictive performance. MindLLM broadens the question to subject-generalizable semantic decoding across perception, language, and knowledge-related tasks.
- **MindLLM → MWM:** MindLLM connects brain activity to semantic content. MWM then bridges semantics and action by using the visual consequences of behavior as supervision for learning action representations from EEG.
- **MWM → DySta:** MWM learns representations for action-intention decoding through the visual consequences of behavior. DySta then studies how robotic policies can translate human intentions into effective and efficient task execution.
- **Closing:** Together, these chapters advance cognitive prediction, semantic decoding, action-intention decoding through visual consequences, and effective and efficient task execution, supporting the broader goal of translating human intentions into interaction with the physical world.

## 表述边界

- 四个核心 chapter 固定为 **HyBRiD → MindLLM → MWM → DySta**。MindLLM 的编码器和 BIT 保持完整；其他工作只作为围绕主线的背景、比较或延伸，不替代四篇一作，也不作为进入下一章必须成立的前提。
- 箭头表达研究问题的递进，不代表发表时间线、同一算法，或已经整合评测的模型流水线。
- HyBRiD 学习与预测相关的高阶结构，不据此宣称发现了因果脑机制；其实验输入仍使用脑区的 pairwise correlation profiles。
- MindLLM 的多任务文本输出不等同于直接验证了被试的内部推理过程。HyBRiD 与 MindLLM 都研究静态表征，二者之间不能写成静态到动态的跨越。
- MWM 在主线中的作用是 semantics（visual consequences）→ action，即以视觉后果提供语义监督来学习动作表征。模型的计算前向仍是 EEG → latent action → 未来视觉表征预测，不把主线方向误写为视觉输入直接生成可执行动作；未来预测也不是其唯一训练监督。世界模型的动作接口仍需更多验证，不能宣称已实现反事实控制或 EEG 到机器人的闭环。
- DySta 的总体目标是将人的意图转化为有效且高效的任务执行；多帧记忆与推理效率是支撑这一目标的具体能力，不能把总体故事缩成选择或保留观测。语言是具体方法的输入，在高层角色与 MWM → DySta 的衔接中不强调语言。总结不主动加入未整合、独立评估或尚待验证的限定。
