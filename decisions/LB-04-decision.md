# D-LB-04 · s₂ → LNP22 Exact-Norm 映射决策

> 日期：2026-11-20。任务包：LB-04。状态：**决策 C（目前无法建立所需映射，方案 B 退回 HOLD）**。
> 依赖：`docs/14-s2-to-lnp22-exact-norm-mapping.md`、`docs/15-exact-norm-extraction-chain.md`；修订 `docs/12`、`docs/13`、`experiments/s2_anchor_toy.py`。
> 本阶段不实现 Decider、不做 LaZer 集成、不扩展到其他路线。

---

## 1. 最终决策

**C：目前无法建立把 LBF 原始 s₂ 接入 LNP22 exact-ℓ₂ statement 的所需映射；方案 B 退回 HOLD，重新评估路线。**

`[推导]` 这不是"路线被证伪"，而是"**用现有 LBF 承诺布局与 anchoring 组件，无法建立映射**"。是否存在需要改变承诺结构的替代路线，见 §4。

---

## 2. 决定性推导（对应任务 B）

### 2.1 候选式 PC=I 不成立

用户候选：`x=[s₁;m]`, `C=[A₂;B]∈R_q^{(n+ℓ)×m₂}`, `J=[A₁ 0;0 I_ℓ]`。

`[论文事实]` `A₂∈R^{n×m₂}`, `B∈R^{ℓ×m₂}`（LNP L495；LBF L1082–1087）→ C 有 n+ℓ 行、m₂ 列。
`[论文事实]` Extended-MLWE 参数 `m₂−n−ℓ−(·)>0`（LNP L730/L1141/L1839）与具体参数（LBF Table 2：d=128 时 n+ℓ=27, m₂=53；d=64 时 35 vs 83；LNP L2015/L2266）一致给出 **`m₂ > n+ℓ`**。

`[推导]` C 是宽矩阵（列>行），`ker(C)` 非平凡，不是单射 → **不存在公开左逆 P 使 PC=I_{m₂}**。候选路线 `s₂=P[t_A;t_B]−PJx` 起点失败。`R_K→R_F` component-wise 展开后（ψ(C) 为 2(n+ℓ)×2m₂）同样无左逆。

### 2.2 这恰是 hiding 的数学要求

`[推导]` 若 PC=I 成立，则任何持有公开承诺 (t_A,t_B) 与消息 x 者可线性解出随机盐 s₂，直接摧毁 ABDLOP 的 Extended-MLWE hiding。故"从承诺线性恢复完整 s₂"在 hiding 承诺方案中**原则上不可能**，与参数无关。用户"禁止假设随机矩阵可逆"的警告被严格验证：不仅不保证可逆，而且**必然不可逆**。

### 2.3 anchoring 替代映射不足

`[论文事实: LBF L2701–2707, Lemma 3.10]` anchoring certifies `u★=ct(ΣₙwₙBs₂⁽ⁿ⁾)`——`Bs₂` 的**标量常数项加权和**（一个 K 元素），经 Lemma 3.10 转为消息侧 `ct(Σwₙm_{ι(n)})=ct(u)`。
`[推导]` 该映射把约 `N_c·m₂` 维的盐空间压成 1 个 K 元素，核维数巨大，**不足以恢复完整 s₂，更不能给出 ‖s₂‖ 的 exact 界**；且 `ker(B)` 非平凡（B 为 ℓ×m₂, ℓ=16<m₂=53），`‖Bs₂‖≤β` 不约束 ker(B) 方向的 s₂ 分量。用户"不能把 Bs₂ 的界当 s₂ 的界"的警告成立。

### 2.4 与作者 sketch 不一致

`[论文事实: LBF L511–515 §2.1]` LBF 明确约定"消息在 BDLOP 槽、ℓ≥1、t_B=Bs₂+m、从不在 Ajtai 槽；s₁ 与 s₂ 都是盐"，并强调 LNP22 自身实例化相反（ℓ=0，消息在 Ajtai 槽）。
`[论文事实]` LNP22 对 randomness 证 exact 范数的唯一展示机制是"把目标向量作为消息额外承诺"（LNP L126 一般配方；L185 群签名把 s₁,s₂,r,μ 放 Ajtai 槽证范数；L2081 VE 用单独 ABDLOP 承诺 r、m 绕开 c̄）。
`[推导]` 因此 Remark 4.8 的 sketch 与用户候选式**都不等价于**这条 LNP22 标准路线；要在 LBF 中复用它，必须**新增把 s₂ 当消息（ℓ≥1）的承诺结构**，违背 LBF 现有约定，且原文未给出。Explore-1 全文核查确认 LBF 无"对 s₂ 本体建立 exact-ℓ₂"的更明确构造。

---

## 3. 任务 D/E 结论

- **两个 fresh salt 位置**（Protocol 8 Step 5 输出盐、Protocol 7 Step 17 mask 盐）：现有 PoK 均为"消息恒等式 exact（Lemma 3.6(3)）+ 盐 relaxed（Lemma 3.6(2)）"（LBF L2891–2893）；exact-norm 证明目标因 §2 映射障碍只能写"待定义"骨架，未写占位公式。见 `docs/15` §1。
- **无 c̄ 累积**：提取链在"extracted opening → exact bound"处断开——盐侧无 exact（问题 2 不成立），anchoring 只保证同标量线性像而非同向量（问题 1 不成立），相邻轮 binding 不能阻止范数放大（问题 3 不成立）。**明确报告未闭合**。见 `docs/15` §2。
- **β 链**：`β_{r+1}≈2T₁(C)β_r`（29.6 倍，d=128）仅作 `[推导]` 示意，论文只给定性 + 单次因子；**不作已证明递推定理**（用户非阻断修订已落实）。

---

## 4. 决策 C 的建设性含义与后续建议

`[推导]` 决策 C 不是说"永远无法对 s₂ 证 exact 范数"，而是说"**在 LBF 当前承诺布局（消息在 BDLOP 槽、s₂ 恒为盐）与现有 anchoring（标量泛函）下无法建立**"。可能的后续路线（均需下一阶段重新评估，本阶段不展开）：

1. **改变承诺结构**：为 fresh salt 新增一个"把 s₂ 作为消息（ℓ≥1）"的 ABDLOP 承诺，按 LNP22 L2081 做法证 exact 范数，再设计与原承诺的完整 s₂ 一致性绑定（需 m₂ 维约束，非现有标量 anchoring）。代价是新增承诺与带宽，需重算成本。
2. **更换研究问题**：承认"在 LBF 布局内做 exact s₂ 证书"受限，转向"是否需要新的承诺布局才能支持递归"的更高层问题。
3. **维持 HOLD**：不进入方案装配，等待新组件或新文献。

无论哪条，都不得为延续 LB-03 方向强行宣称方案 B 可行。

---

## 5. 非阻断修订落实

- `experiments/s2_anchor_toy.py`：ℓ 说明由错误的 `ell=1` 改为与实际 demo 一致的 `ell=2`（两处）。
- `docs/12`、`docs/13`：加入 LB-04 更新说明，明确方案 B 映射失败、编译器前置受阻。
- `docs/15` §2.3：29.6^r 链保持 `[推导]` 示意性标记，明确"论文只给定性与单次因子、无逐轮提取证明"。

---

## 6. 来源诚实边界

ePrint 官方 PDF（`eprint.iacr.org/2022/284.pdf`）本轮仍被 Cloudflare 阻挡，WebFetch 仅返回 "Just a moment..."；本机缺 `fitz`，PDF 截图渲染被安全策略拦截。**所有原文引用来自 ePrint 镜像 PDF 提取文本**（`lnp22_asia.pdf`→`md_lnp22_asia/content.md`；LBF 全文镜像 `paper_mirror.txt`），关键维度用 4 处独立参数表交叉验证，但**明确不是已核验的官方 PDF 逐页版本**。见 `docs/14` 开头与 `logs/2026-11-20-session-05.md`。
