

Part 1.

这一部分的对象是脑信号本身。现有的脑信号模型基本照搬 CV/NLP 的架构，不带任何神经先验——既给不出神经科学上的洞见，性能也次优。所以这一部分只有两个方向：一是用 ML 去发现图谱里没有记录的结构，二是把神经科学已经确立的结构直接搭进架构里。

先约定脑网络怎么建：节点是按某个图谱分好的脑区（区内体素取平均），边是两两之间的 Pearson 相关。

第一个方向，发现。大部分脑网络工作只做两两交互，但绝大多数脑功能是多个脑区同时参与的。麻烦在于高阶关系的数量是指数的——枚举不了。现有做法要么只枚举低阶（度 ≤ 3），要么按邻近或可重构性去挑，而且超边的数量还被固定成节点数。所以只能学出来。

学成什么样？两个要求：对结果尽可能有信息量，彼此尽可能不冗余——MIMR。信息量那项直接最大化 I(H;Y)；冗余那项用 multi-head drop-bottleneck 给 I(H;X) 一个可计算的上界，两项端到端一起优化。用 CPM 衡量超边质量：ABIDE 上平均 +8.8%，ABCD 的七个数据集上平均 +12.1%。

第二个方向，内建。fMRI 解码的现实障碍是每个被试的响应体素在数量和空间分布上都不一样。现有做法用不可学的池化或采样把尺寸对齐，信息丢了，空间含义也丢了。我们的做法是用可学习的 query 去跨注意力地聚合体素；key 里不放 fMRI 值，只放位置——因为一个体素的位置本身就编码了它的功能角色；再把多套脑图谱的分区嵌入拼进 key，把已确立的分区当先验。收敛更快，而且这个先验是跨被试可共享的。

另一条已经确立的结构是左右镜像对称：左右手运动想象产生的是互为镜像的 EEG。普通编码器得从稀缺数据里把这个对称性重新学出来。我们用 frame averaging 在镜像群上做平均，对称性是精确成立的，不是一个学出来的软偏好，对任何输入、任何 backbone 都成立。省下的容量留给真正的偏侧化信号，而不是去重新发现一个已知的对称。

最后反过来。前面都是把神经科学搬进模型，这一个是把脑网络的性质搬出去，用在一个跟脑完全无关的模型上。以注意力头为节点、以在流体推理题上的激活相似度为边建图，小世界指数越高、流体推理越好，六个开源模型上顺序一致。再用剪枝验证：按 core/bridge 分数决定每个头和每一层的稀疏度，SWA 在六个模型上都把小世界指数保住得最好，WikiText 困惑度在每一个「模型 × 稀疏度」的格子里都最优。


Part 2.

第一部分全程待在脑内。我们让模型尊重大脑的组织方式,但那些模型解释的是信号自己——没有一个把脑活动接到外部世界的语义上。第二部分做的就是这件事。

第一个问题不是怎么造桥,是造到哪儿，应该用什么世界模态去对齐大脑。我们去测了——把 fMRI 和预训练的视觉、语言、视觉–语言表征逐一比对。fMRI 离语言模型的语义空间更近。 这决定了后面所有工作的落点。


fMRI-to-text并不是简单的翻译被试想说的话，而是学一个尽量丰富的表征——multi-purpose、multi-function。

监督信号来自一次 join。NSD 的被试看的是 MSCOCO 图,而 MSCOCO 被标注了十年。图像就是连接键,把一条 fMRI 记录和早就写好的文本连起来。98 万段多轮对话,15 个数据集,没有新扫一次脑。四族脑功能:感知、记忆与知识、语言与符号、复杂推理。其中一个任务是我们自己推出来的——描述被试上一张看过的图,标签来自 NSD 的试次顺序,是唯一一个问记忆的任务。

captioning +3.32%;通用解码 +12.0%,其中 28.0% 来自 brain instruction tuning;两个 BCI 相关的新任务 +13.5%,BIT 贡献 25.0%;没见过的被试,1–7 训 8 测不微调,+24.5%。那两个 ablation 说明:干活的是训练范式。

表征学到了,拿它做什么（应用）、能怎么样验证。一个自然的下游是把人看到的东西重建出来。

而重建立刻暴露出提问暴露不了的东西:统一的表征会把物体和它的属性糅在一起——被试看到一只灰色虎斑猫,重建出来是一只老虎。 人的视觉是物体中心、组合式的。所以我们把文本结构化成物体、属性、关系,配 object-centric diffusion,用 VLM 搜哪些属性和关系真的被神经活动携带。同一个 backbone 下,NSD、BOLD5000、GOD 上 training-free 指标最好或并列最好,LPIPS 最多低 5.9%,重建 QA 60.54%。

除了原文使用的较为简单的object centric，更进一步地我们需要object解耦的生成端。例如，扩散模型整张图收一个 prompt——你改猫,沙发跟着动,粒度在最后一步全丢。

D-Edit 把图切成 item,每个 item 一条自己的 prompt,grouped cross-attention 让每个区域只看自己那条。文本、图像、mask 三种编辑加物体移除,一个模型全包。item 级文本编辑 LPIPS 降 55.4%,移除任务上 15 位标注者在质量和保真两项都更偏好它。


Part 3.

前两部分把脑信号送进了语义空间。要让它变成动作，瓶颈换了一个，但性质和第二部分是同一个：还是监督信号。运动想象的数据贵在 cue-locked 的试次和逐条标注，量上不去。

Mind World Model 换的是一种能规模化的采集方式：EEG 和第一视角视频可以连续录、不用标注，mind model 和 world model 在同一条流上一起训。mind model 从当前 EEG 出一个动作 a_t = Mind(y_t)，world model 用它预测下一帧 x_{t+1} = World(x_t, a_t)；mind model 自己没有任何标签，唯一的监督是 world model 在下一帧上的预测误差。这和第二部分那次 join 是同一招——不新采数据，把监督从已经存在的东西里挤出来。

而且这个目标天然对着 motor imagery：mind model 只能贡献那些会改变下一帧的东西，所以它学不到 volume conduction 和静态伪迹，只能学运动相关的时间动力学。评测放在 motor-imagery benchmark 上跟 EEG foundation model 比，最后收口在自采数据集上的机械臂连续控制闭环。

有了驱动信号，另一端得接得住——这是这一部分工作量最大的地方。现实里的 VLA 每一步都要过一遍完整的视觉—语言前向；而且一旦要看多帧，上下文就爆：视觉 backbone 每张图吐几百个 token，几帧一拼，注意力的平方复杂度就压垮了。现有的加速手段基本是通用压缩，不看 VLA 自己的结构。

SD-VLA 把 token 按跨帧变不变拆开：静态的跨帧只留一份并复用它的 KV cache，动态的每步重算，一个可学的 recache gate 决定什么时候该更新静态那一份。上下文长度和每步 FLOPs 一起降。SimplerEnv 上成功率比最强基线高 3.9%，推理加速 2.26×；真机上比 base model 高 10.6%，加速 2.21×。多帧整合本身还专门建了 LIBERO-Memory 基准，三类时序依赖的任务，在上面全指标提升 24.5%，真机绝对成功率提升 23.3%。

最后提一句慢环。如果神经信号给出的是一个目标而不是逐步的动作，中间就得有一层规划把它补成路径，而 rollout 规划太贵、闭不上环。学一个 cost-to-go 把前瞻截断，就是 PHIL 在 A* 里做的事。这一层不是这一部分的主体，结尾一带而过。


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


PRISM 1
|
| Therefore, we want to align fMRI by text annotations to a space that is closer to text. However, this is not a speech-decoding task that decode a person want to say, it is a method that make the representations capture multiple brain functions including visual, symbolic processing, knowledge and memory, by decoding them to a uniform format, i.e., text.
|
Brain Instruction Tuning
|
| Aligning fMRI to a text space is not speech decoding, the goal is not to recover the words a person is trying to say, or is reading. It is to use text as a single unified format in which many brain functions can be read out and compared: perception, memory and knowledge, language and symbols, and complex reasoning.
|
PRISM 2
|
| To better decode visual stimulus and reflect the structured text space of fMRI, we want a generation model that could perform more item-level disentangled generations.
|
D-Edit


After we align fMRI with world modalities, we want it to not only reflect semantics, we also want it to interact with the real-world. That is to say, decoding brain signals into movement intentions, and use that to control, for example, neuroprosthetics or embodied AIs.

Mind World Model
|
| Neural signals are fast, VLAs are slow
|
DySta
|
| Besides real-time fast control, sometimes a slow control would be easier for people. Users output sparse intentions or goals.
|
PHIL
