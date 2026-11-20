# LatticeBlindFold 阅读笔记（工作稿）

状态：初读机制，尚未完成逐消息协议转录和安全证明复核。

## 1. 当前关注的问题

SuperNeo 的知识可靠性不自动意味着零知识。LatticeBlindFold 尝试对格基 Folding 的交互过程加入盲化，以减少 Sum-check transcript 和 Evaluation Hints 对 witness 的信息泄漏。

## 2. 当前识别的机制

- **Polynomial Masking**：对 Sum-check 相关多项式/转录引入随机化。
- **ABDLOP commitments**：承诺 Evaluation Hints，使验证者可以在不直接公开被承诺值的情况下检查相应关系。
- **Rejection sampling / norm handling**：需要结合格基承诺的范数限制理解其参数与分布。

以上是阅读导航，不代替正式协议定义。

## 3. 候选研究问题（未确认）

盲化承诺求值声明能否获得高效 Decider，并在保持知识可靠性与零知识的条件下支持重复组合/递归？

这一问题必须与以下工作逐项排除：NovaBlindFold、SuperNeo、格基 IVC、LaBRADOR/LaZer ZK 工具、LatticeFold 系列及后续发表/预印本。

## 4. 待核查清单

- [ ] 精确抄录协议参与方、轮次、消息和挑战顺序。
- [ ] 明确每个 Evaluation Hint 的定义及维度。
- [ ] 明确 ABDLOP commitment 的参数、承诺消息、随机盐、范数边界与安全假设。
- [ ] 明确 Polynomial Masking 的目标多项式、次数约束、布尔点性质和随机点打开。
- [ ] 明确 Rejection Sampling 的分布目标、接受概率和开销。
- [ ] 列出协议最终输出的每个 claim。
- [ ] 逐字核对作者关于 Decider 和递归/组合接口的限制陈述。
- [ ] 分析是否能用现有 LaBRADOR/LaZer 组件直接构造验证器。
- [ ] 单独分析知识可靠性、零知识、完备性，不能混为一谈。
