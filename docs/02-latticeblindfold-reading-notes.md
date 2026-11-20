# LatticeBlindFold 阅读笔记（工作稿）

> 状态更新：2026-11-20（LB-01 任务 F）。原"初读机制/待核查"清单已在 `docs/03`–`docs/07` 中逐项回答；本文件保留导航与修正记录，不替代正式笔记。
> 注意：ePrint 2026/1857 的 PDF 在本环境受 Cloudflare 限制；正文用第三方公开全文镜像与作者技术博客交叉核对，核验方法见 `logs/2026-11-20-session-02.md`。

## 1. 当前关注的问题

SuperNeo 的知识可靠性不自动意味着零知识。LatticeBlindFold 对格基 Folding 的交互过程加入盲化，以减少 Sum-check transcript 和 Evaluation Hints 对 witness 的信息泄漏。

`[论文事实: LBF §1.1, p.4–5]` 关键定位：LBF **不是**新的 Folding scheme 或递归构造，而是**在 SuperNeo 单步上叠加 blinding**（NovaBlindFold 的格基 analogue）。

## 2. 当前识别的机制（已核验，详见 03–07）

- **Polynomial Masking**：`p(X⃗)=a₀+Σ_i p_i(X_i)`，与 `Q` 同 partial degrees，系数私有均匀；承诺 `p` 后取 `ζ`，对 `ζp+Q` 跑 Sum-Check；**关键差别是 `p(r⃗')` 永不打开**，在承诺层认证 `h−ζp(r⃗')=Q(r⃗')`（`04`）。
- **ABDLOP commitments**：`(tA,tB)=(A₁s₁+A₂s₂, Bs₂+y)`，消息任意范数、盐小范数、计算 hiding + ZKPoK；用于承诺所有 evaluation hints 与 mask 系数，通过 cf/ct 线性泛函与 salt-substitution 在承诺层检查（`05`）。
- **Salt（随机盐）**：`s=(s₁,s₂)`，`B̃=2` 三元；折叠时线性组合，Π′DEC 阶段**fresh 重采样**而非分解（避免约 17 个高位盐为零导致承诺退化，Remark 4.5, p.44）。
- **Rejection Sampling**：`y←D_s^{n_F}` 先于 `ρ⃗` 采样；`Rej1` 使 `(v,z)` 条件分布与 `ρ×D_s^{n_F}` 统计距离 ≤2^{−λ}；代价 `k=Θ(log n_F)`（`06`）。
- **Blinding block `e`**：输入 Ajtai 像 `c₁=L(z₁)` 的隐藏靠 witness 末尾追加均匀盲化块（Lemma 3.3），且必须在 unpadded relation（Def 3.28）上由 prover 后采——layout 本身不够。

## 3. 候选研究问题（未确认，但边界已厘清）

盲化承诺求值声明能否获得高效 Decider，并在保持知识可靠性与零知识的条件下支持重复组合/递归？

`[论文事实: LBF §4.3.3 p.52 / §5 p.59]` 作者把此项列为开放问题：Π_LBF 停在 k 个 committed evaluation claims + ABDLOP PoK 转录，两条候选路线（下游线性扫描 / 算术化 ABDLOP 验证）都未实例化；障碍是 exact-ℓ₂ 范数证书与递归接口同源。接口定义见 `docs/07`。

**防混淆（保留原笔记要点）**：SuperNeo 的 `Π_DEC` = decomposition reduction（LBF Prop 2.26 / Protocol 8），**不是** Decider；"blinding/ZK" ≠ "knowledge soundness"；"用了随机多项式" ≠ "协议零知识"；交互式 blinding ≠ Fiat–Shamir 后非交互 ZK（§4.5：需 `K=F_{q⁴}`，round-by-round KS 未证）。

## 4. 原待核查清单 → 当前状态

| 原待核查项 | 状态 | 位置 |
|---|---|---|
| 精确抄录协议参与方、轮次、消息和挑战顺序 | ✅ 完成 | `docs/03` §1–§2（含 25 步转录表） |
| 明确每个 Evaluation Hint 的定义及维度 | ✅ 完成 | `docs/03` §1.3/§3；`docs/05` §C4.1 |
| 明确 ABDLOP commitment 的参数、消息、随机盐、范数边界与安全假设 | ✅ 完成（公式属 LBF recall；原文编号 `[待核查]`） | `docs/05` §C1–C2 |
| 明确 Polynomial Masking 的目标多项式、次数约束、布尔点性质和随机点打开 | ✅ 完成 | `docs/04` §B1–B2 |
| 明确 Rejection Sampling 的分布目标、接受概率和开销 | ✅ 完成 | `docs/06` §1–§5 |
| 列出协议最终输出的每个 claim | ✅ 完成 | `docs/03` §3；`docs/07` §1/§3 |
| 逐字核对作者关于 Decider 和递归/组合接口的限制陈述 | ✅ 完成 | `docs/07` §0/§4 |
| 分析是否能用现有 LaBRADOR/LaZer 组件直接构造验证器 | ◑ 接口分析完成；**未构造、未证明可行** | `docs/07` §4.6–4.7 |
| 单独分析知识可靠性、零知识、完备性 | ✅ 完成 | `docs/03` §4；`docs/04` §B3；`docs/06` §5 |

## 5. 本轮修正记录（必须保留）

1. **NovaBlindFold 文献编号勘误**：任务包原文给出 ePrint **2025/1210**，核查确认该编号是 *A Generalized Approach to Root-based Attacks against PLWE*（Blanco Chacón–Durán Díaz–Martín Sánchez-Ledesma），与 NovaBlindFold 无关。正确入口：HyperNova ePrint 2023/573 §7、Vega ePrint 2025/2094（LBF 记 `[KS23, KS25]`）。已同步修正 `docs/00-literature-map.md` 与日志。
2. **"Decider" 术语再确认**：`Π_DEC`（SuperNeo/LBF 的 decomposition reduction, Protocol 8）与任务包所说的 Decider（验证最终 committed evaluation claims 的组件）是两个东西；本次转录沿用此区分。
3. **mask 机制细节修正**：初读记 Libra-style masking "对 Sum-check 相关多项式/转录引入随机化"过粗。原论文 [XZZ+19] 原型在打开 mask 求值时泄漏 `f(r⃗)`（Remark 3.18(1) / CFW26）；LBF 的实质改进是 **不打开 `p(r⃗')`**、用 ABDLOP PoK 在承诺层完成最终检查。该项在 `docs/04` §B2.4/B4 中纠正。
4. **"三元盐/盐分解" 修正**：初读未区分。LBF Π′DEC **不分解** salt，`B̃=2` fresh 采样；原因是 rejection sampling 放大因子 ≈2^{17.3} 会使分解后约 17 个高位盐为零、承诺退化（Remark 4.5, p.44）。记于 `docs/05` §C3/C4 与 `docs/06` §5。
5. **完备性类型修正**：LBF 因 rejection sampling 从 perfect completeness 变为 **statistical completeness**（`W_max` 耗尽概率 ≤2^{−λ}），不是"完美完备"。

## 6. 未解决 / 待核查

- `[待核查]` 原始 [BDL+16]/[LNP22] 正文的公式编号与维度表（本轮仅核实书目/摘要 + LBF 的 recall）。
- `[待核查]` [CFW26] 的正式定理编号、[KLSS23] 的完整书目、Cyclo / PikkuFold / Hachi / Greyhound 的正文。
- `[待核查]` 第三方 LaZer / LaBRADOR 仓库的当前构建与可复现性（本轮只核链接与 Toolkit 摘要）。
- `[研究假设]` LaBRADOR/LaZer 作为 Decider 后端的候选路线：未构造、未证明、未实测大小。
