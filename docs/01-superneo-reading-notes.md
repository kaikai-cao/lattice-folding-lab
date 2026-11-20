# SuperNeo 阅读笔记（工作稿）

状态：初读完成，尚未逐项独立复核公式与安全证明。

## 1. 目标

SuperNeo 研究小域上的后量子 Folding，核心构件涉及 CCS、格基承诺、有限域到多项式环的嵌入、求值一致性以及 Sum-check。

## 2. 当前理解的协议依赖

1. **CCS**：以矩阵集合和约束多项式表达计算关系。
2. **Ajtai 型承诺**：通过线性映射承诺环上的向量；安全性依赖有界范数条件及相应格假设。
3. **Embedding / packing**：将有限域向量映射到多项式环表示；需要同时考虑范数和求值对应关系。
4. **Sum-check**：将布尔超立方体上的大量约束压缩为随机点求值检查。
5. **三阶段 Folding**：CCS reduction、随机线性组合（RLC）和 decomposition reduction。

## 3. 安全证明阅读提示

初读时将不同性质分开记录：

- 完备性；
- 知识可靠性及提取器；
- Ajtai 承诺的有界范数 binding / relaxed binding；
- Strong / Weak Interactive Reduction 的定义；
- Strong-Weak composition 的前提条件；
- 交互式协议与 Fiat–Shamir 转换所需的额外论证。

不要仅用“Strong 是输出唯一、Weak 是输入唯一”代替论文正式定义。必须记录正式定义中的关系包含、投影函数、提取器和唯一性条件。

## 4. 待复核问题

- [ ] CCS 的精确语法、矩阵维度和约束多项式条件。
- [ ] 环、分圆多项式、系数范数及参数定义。
- [ ] Packing 的范数保持是在哪种具体范数定义下成立。
- [ ] Evaluation Homomorphism 的完整映射与定理条件。
- [ ] `Π_CCS`、`Π_RLC`、`Π_DEC` 的关系类型、输入输出和参数。
- [ ] Strong / Weak Reduction 的正式定义及 Theorem 的适用条件。
- [ ] 证明者/验证者复杂度与参数增长。

## 5. 重要术语防混淆

- `Π_DEC`：SuperNeo 三阶段构造中的 decomposition reduction。
- Decider：在折叠/累积架构中验证最终声明的组件；与上述 `Π_DEC` 不是同一个概念。
