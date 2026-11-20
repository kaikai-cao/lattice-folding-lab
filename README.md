# Lattice Folding Lab

格基 Folding 与零知识证明研究记录仓库。

> **研究状态：探索阶段（2026-11-20）**  
> 本仓库用于保存论文阅读笔记、协议结构、可复现实验和研究决策。当前研究假设尚未被确认具有论文创新性；任何“研究空白”都必须经过原论文、后续工作和实现核查。

## 当前研究主线

暂定关注：**格基 Folding 中盲化承诺声明的可组合零知识验证**。

核心阅读对象：

- SuperNeo — *Neo and SuperNeo: Post-quantum Folding with Pay-per-Bit Costs over Small Fields*，IACR ePrint 2026/242。
- LatticeBlindFold — *LatticeBlindFold: A Lattice-Based Analogue of NovaBlindFold*，IACR ePrint 2026/1857。

候选研究问题：LatticeBlindFold 产生的盲化承诺求值声明，能否构造高效、知识可靠且保持零知识的 Decider，并进一步支持可组合/递归使用？

**注意：这只是待验证假设，不是已确认的创新点。** 必须排除通用格基 IVC、LaBRADOR/LaZer 零知识工具、NovaBlindFold 及后续工作已经覆盖的部分。

## 仓库结构

```text
lattice-folding-lab/
├── README.md
├── RESEARCH_PLAN.md
├── docs/
│   ├── 00-literature-map.md
│   ├── 01-superneo-reading-notes.md
│   └── 02-latticeblindfold-reading-notes.md
├── experiments/
│   ├── README.md
│   ├── hint_leakage_demo.py
│   └── test_hint_leakage_demo.py
├── logs/
│   └── 2026-11-20-session-01.md
├── decisions/
│   └── DECISIONS.md
├── references/
│   └── README.md
└── .gitignore
```

## 快速运行

要求 Python 3.9+，实验仅使用标准库：

```bash
python -m unittest discover -s experiments -v
python experiments/hint_leakage_demo.py
```

预期测试：线性求值提示在一个刻意构造的二维有限域例子中足以恢复原始向量。

这只是**教学用线性代数示例**，不是 LatticeBlindFold 安全性失败的攻击，也不是对论文协议的实现。

## 研究记录规范

每条结论尽量标记为以下一种：

- **[论文事实]**：能定位到原论文定义、定理、算法或页码。
- **[实现事实]**：能由指定版本代码或可复现实验验证。
- **[推导]**：由已有定义推导得到，需写明假设。
- **[假设]**：尚未验证的研究设想。
- **[待核查]**：资料不足，暂不下结论。

新增实验必须记录：环境、版本/commit、输入规模、运行命令、原始输出、重复次数和限制。不要把单次玩具实验描述为密码学安全证明。

## 当前边界

1. 不复制或重新分发论文 PDF、第三方仓库源码或受版权保护的材料；只记录链接、书目信息和自己的笔记。
2. 在完成安全模型与已有工作的排除前，不宣称 Decider 构造是新贡献。
3. 先完成小规模数学建模和原型，再决定是否建立完整实现。
4. 不将 SuperNeo 的 Decomposition Reduction（`Π_DEC`）与 LatticeBlindFold 讨论中的 Decider 混为一谈。
