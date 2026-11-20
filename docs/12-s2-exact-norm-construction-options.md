# 12 · s₂ Exact-Norm 构造路线与 R_s₂ 目标关系

> LB-03 · 任务 B / C / E。日期：2026-11-20。
> 依赖：`docs/11-s2-anchoring-mathematical-audit.md`（anchoring 审计）、LB-02 `docs/08`。
> 一手来源：LBF 全文镜像 `C:/Users/dell/AppData/Local/Temp/lbf/paper_mirror.txt`（行号 `L####`）；LNP22 正文 `C:/Users/dell/AppData/Local/Temp/lb02/md_lnp22_asia/content.md`（行号 `LNP L####`）。镜像排版注同 `docs/11` §0。
>
> **LB-04 重要更新（2026-11-20）**：本文方案 B（anchoring + 就地追加 exact）曾被列为"最小缺口、作者方向"，但 LB-04 的严格映射分析（`docs/14`）证明：`C=[A₂;B]` 是 `(n+ℓ)×m₂` 宽矩阵（`m₂>n+ℓ`，由 hiding 要求），**不存在公开左逆 `PC=I`**；anchoring 只覆盖 `Bs₂` 的**标量常数项线性泛函**，不足以恢复或约束完整 `s₂`；且 LBF §2.1 明确消息在 BDLOP 槽、s₂ 恒为盐，与 LNP22"把目标放 Ajtai 消息槽"的标准做法相反。因此方案 B 的映射在现有承诺布局下**不成立**，LB-04 决策为 C（退回 HOLD）。本文方案 B 的比较表保留为历史记录，结论以 `docs/14`/`decisions/LB-04-decision.md` 为准。

---

## 1. B1 · LNP22 exact-ℓ₂ 的实际覆盖范围（消除 LB-02 表述歧义）

### 1.1 s₂ 在 LNP22 Figure 10 中的五个精确问题

用户要求正面解决的表述歧义：**"LNP22 Figure 10 协议涉及 s₂，但不等于对 LBF 所需的 s₂ 提供可直接复用的 exact-norm 证书。"** 逐项判定如下。

| # | 问题 | 判定 | 一手证据 |
|---|---|---|---|
| 1 | s₂ 是否出现在协议输入？ | **是。** Fig10 "Private information: (s₁,m,s₂) ∈ R^{m₁+m₂+ℓ}_q so that ‖s₁‖≤α, s₂←χ^{m₂}" | LNP L1814 caption、L495（Fig4）、L530（Fig5） |
| 2 | s₂ 是否出现在 ABDLOP opening relation？ | **是，但作为 randomness。** `(i) A₁s₁+A₂s₂=t_A, Bs₂+m=t_B`；`s₂` 是随机数，非被证明范数的消息 | LNP L1814、式(3)/(5) L55/L86、L474 |
| 3 | s₂ 是否参与证明者承诺？ | **是，作为承诺随机性进入 t_A 的 A₂ 项与 t_B 的 B 项；不是被承诺的消息分量** | LNP 式(5) L86；LBF 式(2.5) L1104–1107 |
| 4 | s₂ 是否被具体范数关系覆盖？ | **仅被 relaxed 覆盖**：`‖s_i c̄‖ ≤ 2s_i√(2m_i d)`（i=1,2），即 Fig10 caption (ii) 与 Fig4 结论(2)；exact-ℓ₂ 的对象向量**不含 s₂** | LNP L1814 (ii)、L505、L521；LBF Lemma 3.6(2) L1315 |
| 5 | 提取器保证 s₂ 什么严格界？ | **无 exact 界。** 提取 `(s̄₂, c̄)` 满足 relaxed `‖c̄ s̄₂‖₂ ≤ 2s₂√(2m₂ d)`；c̄⁻¹ 存在但不一定短，故不能除掉 c̄ 得到 `‖s̄₂‖` 的紧界 | LNP L732、L521；LBF L2155–2159 |

### 1.2 exact-ℓ₂ 对象向量与矩阵维度（核心铁证）

`[论文事实]` LNP22 §5.2（LNP L1690–1700）：Figure 10 证明的知识向量是

```
s = (s₁, σ(s₁), m, σ(m)) ∈ R_q^{2m₁} × R_q^{2ℓ}          (不含 s₂)
```

exact-ℓ₂ 关系（Eq.53）为 `‖E_i s − v_i‖ ≤ β_i^{(e)}`，其中 `E_i` 作用于上述 `2(m₁+ℓ)` 维向量。LBF §2.5.2 把 LNP22 的承诺结构记法为 `s=(s₁,σ(s₁),m,σ(m))`（LBF L1260 附近），"the committed part (s₁,m)"（LBF L3132）。

`[论文事实]` LNP22 Fig10 caption（LNP L1814）：协议对"messages (s₁,m) ∈ R^{m₁+ℓ}_q, randomness s₂ ∈ R^{m₂}_q 且 c̄ ∈ C̄"是 commit-and-prove，条件 (i) 承诺打开关系、(ii) relaxed 范数 `‖s_i c̄‖ ≤ 2s_i√(2m_i d)` for i=1,2。

`[推导]` **定性结论**：用户与 LB-02 的表述 **准确但需要精确化**。准确的陈述是：

> s₂ 在 LNP22 Figure 10 中作为 ABDLOP randomness 出现在承诺打开关系与 relaxed opening 界 (ii) 中；但 LNP22 的 exact-ℓ₂ 机制（Eq.53/59，Fig10 的 exact 部分）作用对象是 `s=(s₁,σ(s₁),m,σ(m))`，其 `E_i` 矩阵维度 `2(m₁+ℓ)` 不含 s₂ 列。因此 LNP22 **原生不提供**对 s₂ 的 exact-ℓ₂ 证书——s₂ 只有 relaxed 界 `‖c̄ s₂‖₂ ≤ β_rlx`。这正是 LBF Remark 4.8（L3132）"s₂ untouched by [LNP22]'s norm machinery"的含义。

`[推导]` **但这不等于"无法触及"**：LBF Remark 4.8（L3130–3139）给出组合路径——用 §3.2.1.1 anchoring 的 salt/message substitution（`Bs₂ = t_B − m`）把 s₂ 的线性像转为承诺消息，然后 §3.3.4 的 R_K exact-ℓ₂ 翻译可对转换后的对象证明紧界。"untouched"指 LNP22 原生向量不含 s₂，不是指组合后永远够不着。

### 1.3 一个容易被忽略的界大小差异

`[推导]` LBF 原文（L3686）指出 anchoring call 的界仅 26.8/26.4 bit，远小于 β_rlx 的 36.6/35.2 bit——说明 anchoring 关系本身在参数上"更紧"，具备作为 exact 证书基础的余量；但这是不同调用的参数，不能直接当作 s₂ exact 界已成立。

---

## 2. B2 · 三个候选路线

### 方案 A：直接扩展 LNP22 exact-norm 证明对象到 s₂

**思路**：把 s₂ 并入 exact-ℓ₂ 的证明向量，设 `s' = (s₁,σ(s₁),m,σ(m), s₂, σ(s₂))`，对 `E' s' − v` 做 Fig10 的 exact 证明，使提取器直接给出 `‖s₂‖₂ ≤ β₂` 的紧界。

- **可行性**：`[推导]` 结构上可行——LNP22 Fig10 的 `E_i` 是任意公开矩阵，理论上可加列覆盖 s₂；但 s₂ 需先在 Ajtai 承诺槽被承诺（当前 s₂ 在 BDLOP 随机槽，不在 `s=(s₁,m)` 消息向量内）。
- **额外自同构**：`[推导]` 需对 s₂ 也做 automorphism stacking `(σ^i(s₂))_{i∈[k]}`，与 s₁/m 的处理相同（LNP L1826–1833；LBF §3.3.3.4 L1822–1833）。
- **二进制余量**：`[推导]` 每个新的 exact 关系 `‖E'_i s'−v_i‖` 需一个二进制余量 `x_i'`，用 Eq.59 的 `β² − ⟨·,·⟩ = ⟨p_i',x_i'⟩` 编码，并用 Fig9 approximate range proof 保证无 wraparound（LNP L1700、Eq.59 L1727、Thm 5.3 L1823）。
- **新增承诺**：`[推导]` 二进制分解向量 `x'` 需追加到 Ajtai 承诺（LNP L1719 "appends a commitment to the binary representation vector x in the Ajtai part"）；若 s₂ 本身也要进 exact 向量，需要为 s₂ 增加一个 Ajtai 承诺槽（改变 `A₁` 宽度），这是**非平凡的承诺结构改动**。
- **Module-SIS 绑定界**：`[推导]` 承诺宽度 m₁ 增加会抬高 MSIS 参数（LNP L482、LBF Lemma 3.16 的 B^anc）；需重算 `MSIS_{n, m₁+m₂+Δ, B}`  hardness。
- **判定**：**部分可行但代价大**——它把 s₂ 从"随机槽"搬到"消息槽"，改变承诺布局；不是"最小缺口"。与 LBF 作者 sketch 的方向（用 anchoring 就地触及 s₂）不同。

### 方案 B：利用现有 anchoring 建立变换后的 exact-norm 关系（LBF sketch 路线）

**思路**：不改承诺布局，沿用 §3.2.1.1 的 `Bs₂ = t_B − m`：anchoring 已把 s₂ 的线性像绑定为"公开 t_B − 消息 m"。对提取出的 `s̄₂`，用 binding 唯一性把它与已承诺消息关联，再对**转换后的量**做 exact 证明。

- **变换函数**：`[论文事实]` Lemma 3.10：`m̄⁽ⁿ⁾ := t_B⁽ⁿ⁾ − B s̄₂⁽ⁿ⁾`；anchoring 关系 `ct(Σₙ wₙ m̄_{ι(n)}) − u = 0`（LBF L1545、L1662）。
- **公开关系**：`[论文事实]` `u = Σₙ wₙ (t_B⁽ⁿ⁾)_{ι(n)} − u★·1`，V 可算（L1545–1548）。
- **秘密见证**：`[论文事实]` `(s̄₁⁽ⁿ⁾, s̄₂⁽ⁿ⁾, m̄⁽ⁿ⁾)` + exact 证书辅助（二进制余量 x、mask）（Lemma 3.16、LNP L1719）。
- **范数推导（关键陷阱）**：`[推导]` **不能因 `m̄ = t_B − B s̄₂` 就推断 `‖s̄₂‖` 与 `‖m̄‖` 有相同界**——B 是随机矩阵，`Bs₂` 会放大/混合范数，且 m̄ 中还含任意范数的消息 m。LBF sketch 的真实机制不是"由 m̄ 界推 s₂ 界"，而是：**对 s₂ 本身追加一个 exact-ℓ₂ 证明**（在它当前的随机槽位置，通过 anchoring 把它纳入可证明关系），使提取直接得到无 c̄ 的 `‖s₂‖` 紧界（Remark 4.8 L3135–3137 "extracted salts would then satisfy their bounds with no factor c̄"）。这是用户强调的"不能因代数联系就推断相同范数界"的正解。
- **完备性条件**：`[论文事实]` 诚实证明者的盐 `‖s_j‖∞ < B̃=2`，满足 LBF sketch 给的两个 append 界 `k t(B̃−1)√(m₁+m₂)d`、`(B̃−1)t√(m₁+m₂)d`（L3133–3135）。
- **知识提取条件**：`[推导]` 需证明追加 exact-ℓ₂ 后，提取器给出 `‖s̄₂‖₂ ≤ β_exact`（无 c̄），从而 binding `A₁s̄₁+A₂s̄₂=t_A` + `m̄=t_B−Bs̄₂` 识别同一 opening，"nothing accumulates"（L3135–3137）。这一步 LBF 只 sketch，未证明。
- **成本**：`[论文事实]` Π_anc 本身 `O(N_c(m₁+m₂)d)`（L1703）；exact-ℓ₂ 追加成本由 LNP22 §5.2 + §3.3.4 决定，LBF 未给合成数字 → `[待核查]`。
- **判定**：**最小缺口、与作者方向一致**——这就是 Remark 4.8 的 "One would append it"。缺的是把 sketch 变成完整协议 + 安全证明，而非新发明范数机制。

### 方案 C：Component-wise Base-Ring 证明

**思路**：对 LBF 的 `R_K = R_F[Y]/(Y²−ν)` 扩域元素，拆成 `(a,b) ∈ R_F²` 分别用 base-ring exact-ℓ₂ 证明，再合并。

- **扩域分解**：`[论文事实]` `x = a + bY`，`Y² = ν`（ν 二次非剩余），`R_K` 是 `R_F` 上秩 2 自由模（LBF L1719–1722，式 3.2）。
- **范数定义**：`[论文事实]` `‖x‖² := ‖a‖² + ‖b‖²`（{1,Y} 基的系数向量 ℓ₂），φ 是 exact isometry（LBF L1838–1840）。
- **自同构作用**：`[论文事实]` **不能直接套 K 层恒等式**——`σ̂_K(x)·x` 的 F 部分是 `‖a‖² + ν‖b‖²`（ν≠1），证到错误量，必须避免（LBF L1841–1847）。正确做法：对 a、b 分别用 base-ring `σ⁻¹(a)a = ‖a‖²`、`σ⁻¹(b)b = ‖b‖²`（LBF L1848–1850）。
- **合并**：`[论文事实]` 联合约束 `‖a‖²+‖b‖² ≤ β²`，"by the same machinery as any other exact-norm statement in [LNP22, §5.2] with no adaptation beyond summing the two independent square-norm terms"（LBF L1851–1855）。
- **判定**：**已解决的子问题**——component-wise exact-ℓ₂ 的翻译 LBF 已给出且正确（修正 LB-02 措辞）。它不是 s₂ 缺口的独立解法，而是方案 A/B 在 R_K 上的**必要实现细节**：无论把 s₂ 放进消息槽（A）还是就地追加（B），只要 s₂ 是 R_K 元素，就必须走这条 component-wise 路线。

### 2.4 三路线统一比较

| 维度 | 方案 A（扩展证明对象） | 方案 B（anchoring + 就地追加，LBF sketch） | 方案 C（component-wise base-ring） |
|---|---|---|---|
| 数学正确性 | 可行但需重设承诺布局 | 可行，符合作者 sketch；"由 m̄ 推 s₂ 范数"是错误推断，须对 s₂ 本体追加证明 | 正确且已由 LBF §3.3.4 给出 |
| 完备性 | 诚实 s₂ 短则满足（需重算界） | 满足（B̃=2，append 界原文给出） | 满足（exact isometry，无失真） |
| 知识可靠性 | 需重算 MSIS 界；提取给出 ‖s₂‖ 紧界 | 需新证明"无 c̄、不累积"；LBF 未证 | 依赖 base-ring LNP22 提取（relaxed→exact 需 Eq.59+Fig9） |
| 零知识 | 否（引入新承诺/打开，需重做模拟） | 保持（Π_anc HVZK，追加 exact 证书需模拟器，未证） | 保持（component-wise 逐块，LBF L1855） |
| 参数兼容 | 差：改 Ajtai 宽度、MSIS 参数 | 好：沿用现有承诺与 anchoring | 好：base-ring 参数不变 |
| 额外承诺 | 多（s₂ 消息槽 + 二进制余量） | 少（仅二进制余量追加到 Ajtai） | 中（每分量余量） |
| 证明大小 | 大（向量加长 + 更多余量） | 中（exact 证书增量，LBF 未给数字 → 待核查） | 中（两份 RF exact 证明） |
| 计算成本 | 高 | `O(N_c(m₁+m₂)d)` + exact 增量（待核查） | 两份 base-ring exact（待核查） |
| 递归适用性 | 可（若紧界成立） | 可，且正是 LBF 目标的 salt-side 修复 | 是 A/B 在 R_K 的必备细节 |

`[推导]` **路线判定**：方案 C 是已解决的基础设施；方案 A 代价大、偏离作者方向；**方案 B 是最小缺口路线**，与 LBF Remark 4.8 的 sketch 一致，应选为 LB-03 的主推进方向，但须明确它仍缺"完整协议 + 安全证明 + 成本估算"三件，不可直接宣布可行。

---

## 3. C · s₂ 的目标关系 R_s₂(x, w)

`[推导]` 基于上述，定义需在递归每轮对 fresh salt 证明的关系 `R_{s₂}(x,w)=1`。它不是一个已有协议，而是**本阶段提取出的规格**（供任务 F 编译器使用）。

### 3.1 公开输入 x

- ABDLOP 公共参数 `pp`；公开矩阵 `A₁ ∈ R_q^{n×m₁}, A₂ ∈ R_q^{n×m₂}, B ∈ R_q^{ℓ×m₂}`；
- 已有承诺分量 `t_A, t_B`（本轮输入承诺）；
- Anchoring 公开数据：权重 `w_n ∈ R_K`、行指示 `ι(n)`、`u★`（或 V 算出的 `u = Σₙ w_n (t_B⁽ⁿ⁾)_{ι(n)} − u★·1`）；
- 范数参数：`B̃=2`、`B_fold = (K+k)T(C)(B̃−1)+B̃`、`β`、`β_i^{(e)}`；
- 挑战与派生：`c̄ ∈ C̄\{0}`（relaxed 用）、`ρ` 系挑战、`r′`、`ζ,δ₀,δ₁` 等。

### 3.2 秘密见证 w

- `s₂`（待证明 salt，R_K 或 R_F 分量）与 `s₁`；
- opening：`m = t_B − B s₂`；
- anchoring 辅助：`m̄⁽ⁿ⁾ = t_B⁽ⁿ⁾ − B s̄₂⁽ⁿ⁾`、`s̄₁⁽ⁿ⁾`；
- Norm Certificate 辅助：二进制余量 `x_i`（Eq.59/58）、mask `y`、逐分量 `a,b` 的 exact 证明见证。

### 3.3 五类约束（逐条写明数学结构/变量/范数界/假设）

1. **Commitment Consistency**
   - 结构：`R_q` 上线性；变量 `t_A=A₁s₁+A₂s₂`, `t_B=Bs₂+m`；输出：公开承诺与见证一致。
   - 假设：ABDLOP relaxed binding（MSIS_{n,m₁+m₂,B}，LBF Lemma 3.6 / Lemma 3.16）。
2. **Anchoring Equation**
   - 结构：`R_K` 上常数项线性；`ct(Σₙ wₙ m̄⁽ⁿ⁾_{ι(n)}) − u = 0`（LBF Lemma 3.16）；输入 `m̄⁽ⁿ⁾=t_B⁽ⁿ⁾−B s̄₂⁽ⁿ⁾`、公开 `w_n,ι(n),u`；输出：salt 聚合绑定。
   - 假设：Extended-MLWE（HVZK）+ MSIS（binding）；soundness error 比 Lemma 3.6 多 `1/|K|`。
3. **Exact Norm Constraint**（缺失的核心）
   - 结构：`R_F`（component-wise R_K）上二次 + approximate range；`‖E_i s − v_i‖₂ ≤ β_i^{(e)}`，对 s₂ 本体或其 R_K 分量 `(a,b)`；输入 s₂（或 a,b）、公开 E_i,v_i,β_i；输出：无 c̄ 的紧界 `‖s₂‖₂ ≤ β_exact`。
   - 假设：LNP22 §5.2 exact-ℓ₂（Fig10/Thm5.3），R_K 翻译见 LBF §3.3.4；Fiat–Shamir 下 ROM/QROM 边界 `[待核查]`。
4. **Binary Remainder Constraint**
   - 结构：`Z`（提升到整数）；`⟨x_i, x_i − 1_n⟩ = 0 ⇒ x_i ∈ {0,1}^n`（LNP Lemma 5.2，LNP L1704）；Eq.58 `⟨x',x'−1⟩=0 mod q` + Fig9 小范数；输入 x_i；输出：余量为二进制。
   - 假设：范围条件 `B² + √((υ_e+k_bin)d)B < q`（LNP L1717）。
5. **Mod-q Integer-Lifting Condition**
   - 结构：`Z_q → Z` 提升；Eq.59 `⟨E_i s−v_i, E_i s−v_i⟩ + ⟨p_i,x_i⟩ = (β_i^{(e)})² mod q`（LNP L1727）+ Eq.60 小范数条件；输出：exact-ℓ₂ 在整数上成立（非仅 mod q）。
   - 假设：Theorem 5.3 参数条件（`B^{(e)} < q^{1/(4c^{(e)})}` 等，LNP L1823）。

### 3.4 能否转成 LNP22 可证明关系（明确结论）

`[推导]` **能，且分两步**：
1. s₂ 组件自身（或其 `(a,b)` 分量）可作为 LNP22 §5.2 的 exact-ℓ₂ 对象——只要把它放进被承诺/被证明的向量并配好 `E_i, v_i, β_i`；R_K 上走 §3.3.4 component-wise 翻译（已解决）。
2. 通过 anchoring（`Bs₂ = t_B − m`）把 s₂ 的线性像与承诺消息关联，使第 1 步的紧界能嵌入 LBF 的公共验证关系（Remark 4.8 L3130–3139）。

**但**"能转成 LNP22 可证明关系" ≠ "已得到可支撑递归的 s₂ exact-norm 证明"。缺的是：把上述五约束装配成每隔轮协议、证明提取无 c̄ 累积、给出成本——这正是方案 B 的未闭合缺口。

---

## 4. E · 安全性质审查

### E1 完备性
`[论文事实+推导]` 诚实证明者 `‖s₂‖∞ < B̃=2`，满足 LBF sketch 的两个 append 界（L3133–3135）；component-wise exact 翻译无失真（LBF L1839）；Π_anc 完备（Lemma 3.16）。**结论**：诚实者可完成，前提是把 exact-ℓ₂ 协议正确追加（未实例化，故为条件性完备）。

### E2 知识可靠性（区分三类 bound）
`[论文事实]` 现有提取给 relaxed `‖c̄ s̄₂‖₂ ≤ β_rlx`（Lemma 3.6(2)），c̄⁻¹ 不一定短（L2155–2159）。
`[推导]`
- **Relaxed Norm Bound**：`‖c̄ s‖₂ ≤ β`，含挑战差，单次提取可得；
- **Exact Norm Bound**：`‖s‖₂ ≤ β_exact`，无 c̄，需 Eq.59 + Fig9 + Thm5.3，方案 B 追加后可得（LBF sketch，未证）；
- **仅诚实证明者成立的 Bound**：`‖s‖∞ < B̃`，是 RoK 成员假设，非提取认证（Remark 4.8 L3116–3124）。
**结论**：现有协议只给 relaxed；要递归必须升级到 exact（无 c̄），这是未闭合点。

### E3 Binding
`[论文事实]` 两 relaxed opening 给 `A₁∆s₁+A₂∆s₂=0, 0<‖(∆s₁,∆s₂)‖₂≤2β_rlx`，即 `MSIS_{κ,m₁+m₂,2β_rlx}` 解（L2187–2191）；anchoring 的 binding 参数 `B^anc`（Lemma 3.16）。
`[推导]` 新增 anchoring 仍依赖**同一承诺唯一性**（Lemma 3.6 的 (s̄₁,s̄₂) 唯一）；若方案 A 扩展承诺宽度，需重算 MSIS 界；方案 B/C 不改承诺宽度，binding 界基本沿用，但追加 exact 证书的参数仍需重算（待核查）。

### E4 Hiding
`[论文事实]` ABDLOP hiding 来自 Extended-MLWE：`[(A₂;B), (A₂;B)s₂]` 与均匀不可区分（LNP L474、L476–478）；Π_anc HVZK 由 S_ABDLOP + Lemma 3.8 逐块 hybrid，损失因子 N_c（LBF L1688–1699）。
`[推导]` 风险：anchoring 把 `Bs₂` 写成 `t_B − m` 是**公开等式**（u 由 V 算），不额外打开 s₂；但 exact-ℓ₂ 证书若需发送 s₂ 的线性打开（如 z=c s₂+y 已由 rejection sampling 隐藏），须确认模拟器中 c̄ 的处理不泄漏。结论：**未见必然泄漏，但完整模拟器未证**（待核查）。

### E5 递归组合（β 链）
`[论文事实]` Remark 4.8 L3125–3129：每轮贡献 c̄（Lemma 3.6(2)）+ (ρᵢ−ρ'ᵢ)（Lemma 2.19），支撑 O(1) 轮；式(3.15) `β_rlx⁽³⁾=2T₁(C)β_rlx`（L2208）；B_fold（L4237–4243）。
`[推导]` **松弛链**：
```
β₀ = β_rlx = 2 s₂ √(2N_c m₂ d)                 (单次提取, 式3.14)
β₀' = β_rlx⁽³⁾ = 2T₁(C)·β₀                      (Π′RLC/Π′DEC 接口一次放大, 式3.15)
递归每轮: β_{r+1} ≈ 2T₁(C)·β_r                   (本文推导; 论文只给定性 + 接口单次因子)
d=128: 2T₁(C)=29.6 (L3694) ⟹ 每轮约 +4.9 bit, β_r ≈ 29.6^r·β₀
q ≈ 2^64 ⟹ 数轮后逼近 MSIS/绑定上限 ⟹ O(1) 轮
```
若按 Remark 4.8 实例化 exact-ℓ₂ 证书：每项以精确界获得、无 c̄ 除法，binding 识别相邻轮 opening，链截断为 `β_{r+1}=β_r`（L3135–3137）——**但该实例化缺失**。
**结论**：单次调用正确性 ≠ 递归。现有机制下递归不可行（O(1) 轮）；exact-ℓ₂ 证书是理论上的截断器，但未装配。

---

## 5. 待核查与边界

- `[待核查]` LBF 镜像公式编号已与正文交叉引用自洽，正式 PDF 页码未逐页核对。
- `[待核查]` 方案 B 的两个 append 界（`k t(B̃−1)√((m₁+m₂)d)` 等）与 LNP22 exact-ℓ₂ 的 Theorem 5.3 参数条件联合可满足性——LBF 只 sketch，未算联合参数。
- `[待核查]` 追加 exact-ℓ₂ 后的证明大小 / prover / verifier 增量成本，LBF 未给合成数字。
- `[推导]` 本文所有 β_r≈29.6^r 外推为本文推导，论文只给定性陈述与单次因子 2T₁(C)。
- 遵守：不把 relaxed 写成 exact、不把 anchoring 等同范数证明、不把单次等同递归。
