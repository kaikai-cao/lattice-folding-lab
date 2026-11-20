# 20 · B2 联合提取器与批量关系（LB-05T · 任务 A / D）

> LB-05T · 任务 A（联合提取器构造）/ 任务 D（Protocol 7/8 批量关系）。日期：2026-11-20。
> 基线：`docs/19`（B2 联合关系 L1–L5、s/x 分离）、`docs/15`（无 c̄ 累积链边界）、`experiments/s2_anchor_toy.py`（教学 toy）。
> 本轮不重复变量定义、不再比较 B1/B2；只回答两点：(1) 如何得到对完整联合关系工作的**单一**提取器；(2) Protocol 8 Step 5 与 Protocol 7 Step 17 的批量关系如何纳入该 statement。
>
> **结论先行**：
> 1. **联合提取器来自 LNP22 Theorem 5.3 的参数化实例化，不是新协议原语**。Fig10 的通用 statement（(50)–(54) 五类约束）原文就由**一个**提取器一次恢复满足全部约束的共同 opening（PDF L6243–6264）。B2 的 L1–L5 逐条落在 Fig10 模板内：L1 是 (50) 类公开线性约束、L2/L3 是底层承诺 opening、L4 是 (53) exact、L5 是 (54) 二值余量；s₂ 与二进制余量 x 一样"追加进 Ajtai 消息槽"（L5734），故 Theorem 5.3 的提取器直接覆盖 B2 全部关系。
> 2. **"每个子协议各自知识可靠"确实不够**（B1 的缺陷），但 B2 不是两个协议——它是**一个** Fig10 实例。区分点：B1 = 原始 opening proof ∥ 辅助 exact proof（两个提取器、两个 s₂，同一性未证）；B2 = 单一 commit-and-prove statement（一个提取器、一个 s̄₂，同一性由 witness 结构给出，见 §1.3）。
> 3. **批量是现成能力但有边界**：Π_many 原生支持 N 条线性关系一次证明、无额外挑战、无可靠性代价（LBF L2621–2625/L2820–2826）；(k+1)t 与 t 个盐块各自可折叠为单次调用。**但** LBF 原文 exact norm 对 Step 5/Step 17 是"分别 append、两个不同界"（LBF L3130–3139），且 Π_many⁽¹⁾ 不原生支持直接写在 s₂ 上的关系（L1533–1535）——B2 用统一 E_{s₂} 覆盖 (k+2)t 个 s₂ 是 `[待核查]` 外推（§2.5）。
>
> **来源**：LNP22 官方 PDF `C:/Users/dell/AppData/Local/Temp/lb02/lnp22_asia.pdf` 及文本流 `C:/Users/dell/AppData/Local/Temp/pdf_check_lnp22/lnp22.txt`（`PDF L####`）；镜像 `content.md`（`LNP L####`）；LBF 全文镜像 `C:/Users/dell/AppData/Local/Temp/lbf/paper_mirror.txt`（`LBF L####`）。镜像有字形替换（‖→}/p、≤→ď、上划线丢失），以官方文本流为准；未做官方 PDF 逐页视觉核对，用户已核对第 42–43 页。

---

## 0. 基线：B2 联合 statement（来自 docs/19 §2）

```
公开输入: t_A, t_B, t̂_A, t̂_B, A₁,A₂,B, Â_s,Â_x,Â_r,B̂, R₁,R_m, E_{s₂}, p, β
witness:   W = (s₁, s₂, m, r, x)        [σ(s_A) 由 s_A 决定，不单列]

(L1) R₁·s_A + R_m·m_A = [t_A;t_B]        R₁=[A₁ A₂; 0 B], R_m=[0; I_ℓ]
(L2) Â_s·s_A + Â_x·x + Â_r·r = t̂_A      （辅助承诺 Ajtai opening）
(L3) B̂·r + m_A = t̂_B                    （辅助承诺 BDLOP opening）
(L4) ⟨E_{s₂}·s_LNP, E_{s₂}·s_LNP⟩ + ⟨p,x⟩ = β² mod q,   s_LNP=(s_A,σ(s_A),m_A,σ(m_A))
(L5) ⟨x′,x′−1⃗⟩=0 mod q + Fig9 range     （x 二值 + 整数提升）
```
其中 `s_A=(s₁,s₂)` 为 Ajtai 消息（含追加的 x），`m_A=m` 为 BDLOP 消息，r 为新 randomness。

---

## 1. 任务 A：联合提取器构造

### 1.1 为什么"每个子协议各自知识可靠"不够

`[论文事实: PDF L6243–6264, L6597–6600]` LNP22 Fig10 的 soundness 结论形式是：
> "either [the extractor] breaks the binding of the commitment or recovers a valid opening (s̄₂, s̄₁, x̄_s, m̄, …) … satisfying Equations (50) to (54)."

`[推导]` 这是**单个**提取器、**单个** opening、同时满足全部约束。反观 B1（docs/18 §2.1）：原始 opening proof 提 (s̄₁, s̄₂)，辅助 exact proof 提 (s̄₂′, …)，两个证明各自知识可靠**不蕴含** s̄₂ = s̄₂′——这是"共享变量 ≠ 联合 PoK"（用户在 LB-05R 的核心质疑）。B2 若仍是两个协议并行，同样逃不掉该质疑。**因此 B2 必须落到一个 Fig10 实例内，用单一提取器一次性恢复 (s̄₁,s̄₂,m̄,r̄,x̄)。**

### 1.2 Fig10 模板的可联合性（原文依据）

`[论文事实: PDF L5613–5620]` §5.2 开宗明义：
> "a general protocol to prove various quadratic relations on s = (s₁, σ(s₁), m, σ(m)) … **we prove simultaneously** quadratic relations over R_q, quadratic relations over Z_q, approximate bound on the infinity norm, exact bound on the ℓ₂ norm and finally that a vector is binary. All the later statements are gathered in **this single protocol** …"

`[论文事实: PDF L5653–5684]` Fig10 的通用 statement 是五类约束：
```
(50) f_i(s)=0                      i∈[ρ]          R_q 上二次关系（线性是其特例）
(51) F_i(s)=0                      i∈[ρ_eval]     常数系数为零的 evaluation
(52) ‖D_i s − v_i‖_∞ ≤ β_i^(d)    i∈[υ_d]        近似 ℓ∞
(53) ‖E_i s − v_i‖   ≤ β_i^(e)    i∈[υ_e]        精确 ℓ₂
(54) E_bin s − v_bin ∈ {0,1}^{d k_bin}            二值向量
```
`[论文事实: PDF L6243–6264]` Theorem 5.3：**一个**提取器恢复**一个** opening `(s̄₂, s̄₁, x̄_s, m̄, ȳ⁽ᵈ⁾, ȳ⁽ᵉ⁾, b̄⁽ᵈ⁾, b̄⁽ᵉ⁾, c̄)` 同时满足 (50)–(54)。
`[论文事实: PDF L2835–2869, L3999–4042]` Lemma 4.3 / Theorem 4.5 同理：一个提取器恢复一个 witness 满足全部 batched 关系；N 个二次关系经 verifier 挑战 µ 随机线性组合压成一个（L2801–2806）。

`[推导]` **结论**：LNP22 的提取器天然"可联合"——它本就是为一个 statement 里的多个约束设计的，只是覆盖的是**固定模板** (50)–(54)，而非"任意可拆为线性+二次的 R(x,w)"的通用定理。B2 的 L1–L5 恰落在该模板内（§1.3），故直接继承 Theorem 5.3。

### 1.3 B2 → Fig10 逐分量映射（联合提取器存在性的核心论证）

`[推导]` 把 Fig10 模板参数化为 B2，只需把"追加进 Ajtai 消息槽的对象"从 x 扩展为 (s₂, x)：

| Fig10 角色 | 原文维度/来源 | B2 实例 | 合法性 |
|---|---|---|---|
| Ajtai 消息 s₁ | m₁（L5653） | s_A=(s₁,s₂)，维度 m₁*=m₁+m₂ | 参数化扩展；x 已展示"追加进 Ajtai 槽"先例（L5734），s₂ 同法追加 |
| BDLOP 消息 m | ℓ | m_A=m | 原样 |
| randomness s₂ | m₂（L6179） | r（新盐），维度 m₂' | 角色换位：原 randomness 由 r 承担；r 是 fresh 短盐，满足采样界 |
| 二进制余量 x | υe（L5734） | x（υe=1） | 原样 |
| exact 向量 s | (s₁,σ(s₁),m,σ(m))∈R^{2(m₁+ℓ)} | s_LNP=(s_A,σ(s_A),m_A,σ(m_A))∈R^{2(m₁+m₂+ℓ)} | m₁→m₁+m₂ 参数化（用户已接受"通用接口支持"，参数实例化待核查） |
| (50) 二次函数 f_i | 任意公开 f_i | f(s_A,m_A)=R₁s_A+R_m m_A−[t_A;t_B]（L1） | 线性是二次特例；公开常量 −[t_A;t_B] 并入 f 的常数项 |

`[论文事实: LNP L5734]` 决定性原文：
> "the prover appends a commitment to the binary representation vector x … in the Ajtai part of the commitment to (s₁, m)."

`[推导]` 原文已展示"把需要 exact 证明的向量（x）追加进 Ajtai 消息槽、仍由同一提取器恢复"这一模式。B2 对 s₂ 做的是**同一件事**（把 s₂ 也放进 Ajtai 消息槽，使 `E_{s₂}s_LNP=s₂` 落在 (53) 的作用域内）。因此联合提取器 **= Theorem 5.3 在该参数化实例上的直接应用**：
```
联合提取器 E_B2 (rewindable black-box access to B2 prover):
  1. 运行 Fig10 参数化协议（L1–L5 作为 (50)/(53)/(54) 约束，s₁:=s_A, m:=m_A, s₂:=r）
  2. 对最后一个 Π⁽²⁾_eval 挑战 c 做 forking（PDF L10454–10493，[ACK21]），凑 3 个接受转录
  3. 解出共同 opening (s̄_A=(s̄₁,s̄₂), m̄_A, r̄, x̄, …) 满足 (50)–(54)
  4. 由 (L1) 得 A₁s̄₁+A₂s̄₂=t_A、Bs̄₂+m̄_A=t_B → (s̄₁,s̄₂,m̄_A) 是原始承诺 opening
```
`[推导]` **同一性来源**：(L1)–(L5) 的 witness 列表里 s₂ **只有一个变量符号**，提取器输出的 s̄₂ 同时进入 L1（原始 opening）、L4（exact 界）；不存在"两个 s₂ 事后比对"。这是结构性质，但仍需 binding 保证 s̄₂ 与诚实 opening 计算上一致（见 docs/21 §2.3 与 §3）。

### 1.4 协议调用顺序、挑战依赖与提取顺序

`[论文事实: PDF L6064–6157, L10424–10434]` Fig10 的交互阶段（B2 原样继承）：
```
阶段1  P→V: 承诺 (t⁽ᵈ⁾, t̄⁽ᵈ⁾, t⁽ᵉ⁾, t̄⁽ᵉ⁾)        （range/exact 的 mask 承诺）
阶段2  V→P: 挑战矩阵 R⁽ᵈ⁾, R⁽ᵉ⁾ ← Bin_{256×c}^1     （看到承诺后给）
阶段3  P→V: z⃗⁽ᵈ⁾, z⃗⁽ᵉ⁾（Rej₀ 通过才继续）          （依赖 R）
阶段4  P↔V: Π⁽²⁾_eval（自带 µ 批量挑战与最终挑战 c）  （最后运行）
```
Fiat–Shamir 非交互化时按转录前缀逐阶段哈希：`R←RO₁(I₁)`、`γ←RO₂(I₂)`、`µ←RO₃(I₃)`、`c←RO₄(I₄)`（PDF L10424–10434），后一挑战绑定前面全部消息。
`[论文事实: PDF L10454–10493]` 提取顺序：固定 I₁–I₄、只对**最终挑战 c** 分叉，凑 3 个接受转录 → 解二次多项式系数 → 得 s̄_A 等（degree-2 special soundness，[ACK21]）。

`[推导]` **对 B2 的意义**：L1（原始 opening 线性关系）在阶段 4 的 Π⁽²⁾_eval 内作为 (50) 类约束被验证；L4/L5（exact/二值）在阶段 1–3 的 mask+range 协议中处理。**全部在一个协议调用内**——不存在"两个证明共享挑战 c"的问题（该问题在 LB-05R Q5 标 `[待核查]`，B2 规避了它，因为它根本不是两个证明）。用户任务 A 要求的"协议调用顺序、挑战依赖、提取顺序"即上述四阶段 + 最终 c 分叉。

### 1.5 soundness 继承的严格边界（不默认宣称）

`[推导]` "联合提取器由 Theorem 5.3 继承"依赖一个前提：**B2 的参数化实例满足 Fig10 soundness 证明的前提**。逐项核查：

| 前提 | Fig10 原文 | B2 实例 | 状态 |
|---|---|---|---|
| exact 向量是已承诺消息 | s=(s₁,σ(s₁),m,σ(m))，s₁ 是 Ajtai 消息 | s_A=(s₁,s₂) 是 Ajtai 消息，s_LNP 含其 σ 像 | ✓ 结构满足 |
| randomness 短采样 | s₂∈R^{m₂} 短（L6179） | r∈R^{m₂'} fresh 短盐 | ✓ 满足（r 是采样短盐） |
| 追加向量进 Ajtai 槽 | x 追加（L5734） | x 与 s₂ 都追加 | ✓ 同模式；s₂ 追加是扩展 `[参数实例化待核查]` |
| 扩展维度 m₁+m₂ 的接口兼容 | E_i∈R^{p_i×2(m₁+ℓ)}（L1681） | E_{s₂}∈R^{m₂×2(m₁+m₂+ℓ)} | `[参数实例化待核查]`：列数随 m₁→m₁+m₂ 自然扩展，Fig5/Fig8 多线性接口对扩展维度的实例化须在参数阶段验证 |
| Thm5.3 参数（q、B⁽ᵉ⁾、k_bin） | 按 m₁+ℓ 推 | 按 m₁+m₂+ℓ 须重推 | `[待核查]` |

`[推导]` **诚实判定**：结构性前提（消息槽 / randomness 短盐 / 追加模式）满足；**参数化前提**（扩展维度接口实例化、Thm5.3 参数重推）未完成。这属于"同一接口的新参数实例需完成参数验证"，不是"接口不兼容"或"新原语设计"——与用户在 LB-05S 把 E_{s₂} 定为"通用接口支持、参数实例化待核查"的口径一致。因此本轮论证联合提取器**存在性与结构**，不宣称参数层已闭合。

### 1.6 与三层 binding 的衔接

`[推导]` E_B2 输出的 s̄₂ 满足 (L1)：`A₁s̄₁+A₂s̄₂=t_A`。这给出"联合提取结果 ↔ 原始承诺 opening"的关联，但该关联是**计算绑定**（依赖原始承诺 MSIS），不是信息论相等。三层 binding（原始 LBF / 辅助 ABDLOP / 联合关联）的严格证明与 c̄-scaled 界见 `docs/21-b2-mixed-msis-bound.md` §2。

---

## 2. 任务 D：Protocol 7/8 批量关系

### 2.1 承诺计数与盐索引（原文核查）

`[论文事实: LBF L2883–2886]` Protocol 8 Step 5：单个 Π_many 调用覆盖 `N_c=(k+1)t` 个盐块（t 个输入 `C_j` + kt 个新 `C_{i,j}`）；逐个 fresh salt pair `s_{i,j}=(s₁,i,j, s₂,i,j)`（L2876–2877）。
`[论文事实: LBF L2752, L2775–2777]` Protocol 7 Step 17：t 个 mask 承诺 `C_{y,j}`，各一对 fresh salt `(s₁,y,j, s₂,y,j)`。
`[论文事实: LBF L2820–2826]` Remark 4.4：Step 1 的 (K+k)t 个、Step 5 的 (k+1)t 个、Step 17 的 t 个"can be collapsed into a single call to Π_many … vector-batching is free both in soundness and completeness"。
`[推导]` B2 的 `(k+2)t = (k+1)t + t` 计数正确（Step 5 的 (k+1)t + Step 17 的 t）。

### 2.2 Π_many 的拼接 witness 与公开矩阵

`[论文事实: LBF L1443, L1308–1316, L1612–1627]` Π_many 证明 `u = R₁s₁ + R_m m ∈ R_K^N`（full-ring identity，任意 N）。拼接实例：
```
witness:  s₁^cat=(s₁⁽¹⁾,…,s₁⁽ᴺᶜ⁾), s₂^cat=(s₂⁽¹⁾,…,s₂⁽ᴺᶜ⁾), m^cat=(m⁽¹⁾,…,m⁽ᴺᶜ⁾, g)
矩阵:    A₁^cat=blockdiag(A₁,…), A₂^cat=blockdiag(A₂,…), B^cat=blockdiag(B,…)
         R₁=0（anchoring 类）或按关系；R_m 是按关系的 block-row（非块对角）
```
`[论文事实: LBF L2885–2887]` Step 5 的 `R_m` 是 `t×N_c`，第 j 行为 `(1,−1,−b,…,−b^{k−1})` 落在第 j 块——跨块耦合 `C_j` 与 `{C_{i,j}}`。
`[推导]` B2 把 L1 批量化：`R₁^cat=[A₁^cat A₂^cat; 0 B^cat]`、`R_m^cat=[0; I_ℓ^cat]`，`u^cat=[{t_A⁽ᶦ⁾};{t_B⁽ᶦ⁾}]`——每块复现一个原始 opening 关系，N=(k+2)t 条，一次 Π_many 调用，无额外挑战、无可靠性代价（L2623–2625）。**这是原文现成接口，不需新协议。**

### 2.3 辅助承诺：一份覆盖整批，还是逐份？

`[论文事实: LBF L1455–1457, L1645–1655, L1701–1704]` Π_anc（anchoring 聚合）每次调用只在 m 末尾加**一个**垃圾槽 g（`ℓ→ℓ+1`），"no commitment is recomputed: the parties merely repackage openings they already hold"，"no fresh commitment is computed beyond the single garbage slot for g"。
`[推导]` 按原文 batched 接口，**一份**辅助承诺（g 槽）覆盖整批 N_c 个盐块，不是每个 s₂⁽ⁱ⁾ 各一份；这一份可推广到 (k+2)t 块（Definition 3.15 对任意 N_c 成立）。因此 B2 的辅助 ABDLOP 承诺 `t̂_A,t̂_B` 可按拼接 witness 构造，witness 为 `(s_A^cat, x^cat, r^cat, m^cat)`。

### 2.4 盐不相交性

`[论文事实: LBF L2757–2758, L3642–3643, L3648–3649, L3655]` `C_{y,0}`（ Ñ 个开盐承诺）的盐"disjoint from those of {C_{y,j}}"，且"never combined homomorphically with any other commitment"；它是唯一明文开盐的承诺。
`[推导]` 这是**结构/安全要求**（打开 C_{y,0} 会泄露共享盐、破坏 Step 17 PoK 的 hiding），不是分析便利。但对 B2 的 `(k+1)t + t` 两个**秘密盐**集合不构成障碍：它们按 (i,j)/j 独立采样、索引互异。障碍只在两种情形出现：(i) 把开盐的 `C_{y,0}` 塞进同一批；(ii) 为缩减 witness 跨集合复用盐（违背 LBF L1698 "independently sampled"）。**B2 不触碰这两者，盐不相交性满足。**

### 2.5 批量化的边界：哪些可向量化、哪些必须逐个 / 待核查

`[论文事实: LBF L3130–3139]` Remark 4.8 的 exact-norm sketch：作者给 Step 5 与 Step 17 的界**不同**——`kt(B̃−1)√(m₁+m₂)d` 与 `(B̃−1)t(m₁+m₂)d`——且"分别 append to Step 5 / Step 17"，并明确"which we do not instantiate"（L418–419）。
`[论文事实: LBF L1533–1535, L1851–1855, L1864–1867]` Π_many⁽¹⁾ 不原生支持直接写在 s₂ 上的关系；原文路线是 Lemma 3.10 替换 `Bs₂⁽ⁿ⁾=t_B⁽ⁿ⁾−m⁽ⁿ⁾` 转成消息关系；component-wise exact 的二次约束 `‖a‖²+‖b‖²≤β²` 可批量摊销。

`[推导]` 汇总（诚实区分）：

| 项目 | 可向量化？ | 依据 |
|---|---|---|
| (L1) 原始 opening 线性关系 ×(k+2)t | ✓ 单次 Π_many，免费 | LBF L2820–2826 |
| (L2)(L3) 辅助承诺 opening（拼接 witness） | ✓ 一份辅助承诺 + 拼接 salt | LBF L1612–1627, L1701–1704 |
| (L4) exact norm ×(k+2)t，统一 E_{s₂} | `[待核查]` | 原文 Step5/Step17 两个界不同、分别 append；Π_many⁽¹⁾ 不原生支持直接 s₂ 关系（L1533–1535）；统一选择矩阵覆盖全部 (k+2)t 是 B2 外推 |
| (L5) 二值余量 x | ✓ Fig10 (54) 原生批量 | PDF L5653–5684 |
| C_{y,0} 开盐承诺 | ✗ 不可并入 | LBF L3648–3649 "never combined homomorphically" |

`[推导]` **结论**：批量关系在**线性层与二值层**是原文现成能力；**exact-norm 层的统一批量**是 B2 相对 LBF 作者 sketch 的新设计，原文既未实例化、且给出了两个不同的界——这是进入参数阶段前须明确处理的 `[待核查]` 项（保留两处 append / 两个界，或证明统一界可行）。

---

## 3. 边界与待核查（任务 A/D）

- `[参数实例化待核查]` E_{s₂} 的 2(m₁+m₂+ℓ) 扩展维度对 Fig5/Fig8 多线性接口的实例化；Thm5.3 参数（q, B⁽ᵉ⁾, k_bin）按新维度重推。
- `[待核查]` 统一 E_{s₂} 对 (k+2)t 个 s₂ 的批量 exact 界；LBF 原文 Step5/Step17 两界不同的处理。
- `[未证 · 见 docs/21]` 三层 binding 的严谨归约与混合 MSIS 差向量界；联合提取 s̄₂ 与诚实 opening 的计算绑定。
- `[边界]` 联合提取器 = Theorem 5.3 的**结构**继承；不等于 B2 已通过完整安全证明、已参数实例化、已实现；不等于递归无 c̄ 累积（docs/15）。
- 不写"两个独立证明的 s₂ 自动同一"；不把"写在同一 statement"当"已证知识可靠"；不做 Decider/LaZer。
