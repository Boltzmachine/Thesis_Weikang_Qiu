

Part 1.

这一部分的对象是脑信号本身。现有的脑信号模型基本照搬 CV/NLP 的架构，不带任何神经先验——既给不出神经科学上的洞见，性能也次优。所以这一部分只有两个方向：一是用 ML 去发现图谱里没有记录的结构，二是把神经科学已经确立的结构直接搭进架构里。

先约定脑网络怎么建：节点是按某个图谱分好的脑区（区内体素取平均），边是两两之间的 Pearson 相关。

第一个方向，发现。大部分脑网络工作只做两两交互，但绝大多数脑功能是多个脑区同时参与的。麻烦在于高阶关系的数量是指数的——枚举不了。现有做法要么只枚举低阶（度 ≤ 3），要么按邻近或可重构性去挑，而且超边的数量还被固定成节点数。所以只能学出来。

学成什么样？两个要求：对结果尽可能有信息量，彼此尽可能不冗余——MIMR。信息量那项直接最大化 I(H;Y)；冗余那项用 multi-head drop-bottleneck 给 I(H;X) 一个可计算的上界，两项端到端一起优化。用 CPM 衡量超边质量：ABIDE 上平均 +8.8%，ABCD 的七个数据集上平均 +12.1%。

第二个方向，内建。fMRI 解码的现实障碍是每个被试的响应体素在数量和空间分布上都不一样。现有做法用不可学的池化或采样把尺寸对齐，信息丢了，空间含义也丢了。我们的做法是用可学习的 query 去跨注意力地聚合体素；key 里不放 fMRI 值，只放位置——因为一个体素的位置本身就编码了它的功能角色；再把多套脑图谱的分区嵌入拼进 key，把已确立的分区当先验。收敛更快，而且这个先验是跨被试可共享的。

另一条已经确立的结构是左右镜像对称：左右手运动想象产生的是互为镜像的 EEG。普通编码器得从稀缺数据里把这个对称性重新学出来。我们用 frame averaging 在镜像群上做平均，对称性是精确成立的，不是一个学出来的软偏好，对任何输入、任何 backbone 都成立。省下的容量留给真正的偏侧化信号，而不是去重新发现一个已知的对称。

最后反过来。前面都是把神经科学搬进模型，这一个是把脑网络的性质搬出去，用在一个跟脑完全无关的模型上。以注意力头为节点、以在流体推理题上的激活相似度为边建图，小世界指数越高、流体推理越好，六个开源模型上顺序一致。再用剪枝验证：按 core/bridge 分数决定每个头和每一层的稀疏度，SWA 在六个模型上都把小世界指数保住得最好，WikiText 困惑度在每一个「模型 × 稀疏度」的格子里都最优。


Part 2.

第一部分研究脑信号本身。第二部分把脑活动接到外部世界的语义上，主线是四个相继提出的问题：PRISM I 启发对齐空间的选择，MindLLM 将 fMRI 对齐到语言，PRISM II 基于语言重建视觉内容，D-Edit 则把生成端推进到更强的逐物体解耦。这是研究问题和方法设计的衔接，不意味着四个工作共享已经串接好的模型权重。

先问对齐到哪里。PRISM I 把 fMRI 与预训练的视觉、语言、视觉–语言表征逐一比较；在所测的候选空间中，语言模型的语义空间更适合作为对齐目标。这个结果为后面选择语言作为中间表征提供依据，而不是说大脑本身就是语言式的。

再问如何对齐。MindLLM 用脑指令微调将 fMRI 对齐到语言，让感知、记忆与知识、语言与符号、复杂推理都能以文本这一统一格式读出。这里不是翻译被试想说的话。监督信号来自一次 join：NSD 的被试看的是 MSCOCO 图，图像作为连接键，把 fMRI 记录和已有文本标注连起来，得到 980,610 段多轮对话，不需要新扫描。

语言表征学到了，能否用它恢复视觉内容？PRISM II 基于从 fMRI 解码的语言信息进行视觉重建。单一描述容易把物体和属性糅在一起，所以它把语言组织成物体、属性、关系，再用 object-centric diffusion 按物体生成并组合场景。这样，语言既是多种脑功能的统一读出格式，也可以承载重建图像所需的内容和结构。

这个物体结构进一步提出生成端的问题：PRISM 的 object-centric generation 已经按物体组织生成，但怎样让每个物体的条件和注意力也更明确地分开？D-Edit 为每个 item 学习独立的 soft prompt，再用 grouped cross-attention 限定各区域与对应 prompt 的交互，从 prompt 和 attention 两层加强逐物体解耦。

因此 D-Edit 在这条主线中是更强的解耦生成方法。文本、图像、mask 编辑和物体移除展示了这种局部控制能力；它不只是附在末尾的图像编辑工具。这里的“更强”指解耦机制更明确，并不是未经验证的 PRISM 重建指标提升，也不是已经把 D-Edit 接入 MindLLM 或 PRISM 的实验结果。


Part 3.

前两部分研究脑信号及其语义表征。第三部分从动作层递进到目标层：MWM 通过联合学习 mind model 和 world model，让脑信号表示具有动作含义；但完成任务时，人往往更希望指定期望结果，而不必表达每一步动作。这引出目标层的两个互补方法：PHIL 根据 goal image 所对应的目标状态进行图搜索，DySta 根据 language instruction 和多帧视觉历史直接生成动作。两个目标接口对应第二部分解码出的图像与文本。PHIL 与 DySta 在目标层并行，不是先规划再执行的串接。

MWM 将当前 EEG 编码为 latent action，以当前视觉状态为条件预测未来视觉表征。训练使用同步 EEG 与第一视角视频，不需要动作标注；预测损失与跨模态对齐、偏侧化监督共同学习与动作有关的脑信号表示。其 mind model 用于运动解码，world model 的动作接口另通过 IMU 适配进行评估。

论文的具身接口用 goal image 向 PHIL 指定期望结果，对应第二部分的图像输出。图搜索需要将图像表达的结果落到状态图的目标节点及其特征上。给定起点、目标节点与可搜索的状态图，PHIL 学习到目标的距离启发式，用搜索历史和局部图结构引导 greedy best-first search，减少寻找可行路径所需的节点展开。PHIL 原方法的实验是给定 graph/start/goal 的搜索任务；把解码图像转换成可规划目标属于未来整合，不声称原实验直接接收脑解码图像或原始像素图像。

DySta 是视觉–语言–动作策略，目标输入是 language instruction，对应第二部分的文本输出；策略根据这条语言指令与视觉观察直接预测动作。它区分静态和动态 token，复用静态 KV cache，并用 recache gate 按需刷新；保留多帧动态信息，以较低推理成本完成需要记忆的任务。

结构写作 ACTION LEVEL（MWM）→ GOAL LEVEL（PHIL ∥ DySta）。箭头表达研究问题从动作含义到期望结果的递进，不表示 MWM 的 latent action 已经输入 PHIL 或 DySta；PHIL 的路径也不是 DySta 的输入。三者分别评估，脑控机器人的完整整合属于后续工作。报告顺序为 MWM、PHIL、DySta，不使用“快环／慢环”来定义它们的关系。


衔接：

We start by machine learning models that operate in brain signals, which is the foundation for all following works and real-world applications.

hybrid
| 
| that was a work for discovering neural priors, now i am going to talk about work that incoporate neural priorss
|
neuro-informed attention
|
| that was an example that incoporates existing neural priors for fMRI, now it's for EEG
|
FA-EEG
|
| cannot only improve performance for ML models for brain-related tasks, but also for general machine learning models, e.g., LLM
|
SWA


We talked about models that work within brain signals, for real-world BCI tasks, we need to brige them to representations that align to real world. Talking about real-world modalities, images and text are representative ones. A question is: is fMRI close to text representations or image representations.


PRISM I
|
| The alignment comparison motivates language as a representation space for fMRI.
|
MindLLM
|
| Brain instruction tuning aligns fMRI to language and reads out multiple brain functions in a shared format. Can this language representation also recover visual content?
|
PRISM II
|
| Reconstruct visual content from decoded language, organized into objects, attributes, and relations. Object-centric generation then motivates a generator with stronger per-item disentanglement.
|
D-Edit

D-Edit assigns an independent soft prompt to each item and separates their cross-attention. Its editing tasks demonstrate this generation capability. This is a progression of research questions, not a claim that the trained models have already been integrated or that D-Edit has measured superiority over PRISM on neural reconstruction.


After aligning fMRI with world representations, Part 3 asks how intention can become behavior, progressing from the action level to the goal level:

ACTION LEVEL — MWM jointly learns a mind model and a world model, grounding EEG-derived latent actions in their visual consequences.

Task completion motivates the transition: a person should be able to specify the desired result rather than every action.

GOAL LEVEL — PHIL and DySta study two complementary approaches to realizing that result.
- PHIL uses a goal image as the goal-facing interface in the embodiment framing, with the depicted outcome represented as a goal state for explicit graph search. This corresponds to Part 2 images.
- DySta takes a language instruction, corresponding to Part 2 text, and predicts actions using visual history, efficient inference, and multi-frame memory.

Grounding a decoded goal image in the planner state graph and using decoded text as a policy instruction are future integration steps. The PHIL experiments evaluate supplied graph-and-goal problems.

ACTION LEVEL (MWM) → GOAL LEVEL (PHIL ∥ DySta): the arrow expresses a progression of research questions. The models are evaluated independently; MWM outputs do not feed PHIL or DySta, and PHIL is not DySta's planner.
