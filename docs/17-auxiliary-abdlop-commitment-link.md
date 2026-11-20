# 17 · 路线 B：辅助 ABDLOP 承诺能否闭合 s₂ 范数问题

> **★LB-05R 修订说明（2026-11-20）**：用户复核指出本文三处需收紧，逐条落实如下，**完整修订分析见 `docs/18-auxiliary-abdlop-joint-statement-audit.md`**：
> 1. **辅助承诺漏掉二进制余量 x**：本文初稿 `t'_A=A'₁s₂+A'₂r` 不含 LNP22 §5.2 必需的二进制余量向量 x（LNP L1719/1759/1700）。修正式为 `t'_A=A'_s s₂+A'_x x+A'_r r`，`A'_1=[A'_s A'_x]∈R_q^{n'×(m₂+υe)}`（υe=1）。见 docs/18 §1。
> 2. **"共享变量≠已构造联合 PoK" + "MSIS 非无条件唯一"**：本文结论先行"MSIS binding 保证 witness 唯一"过强。正确说法：共享 s₂ 只是关系定义；联合提取是协议层性质（B1 两独立证明不满足、B2 待证）；MSIS 只在给定矩阵分布/维度/短界条件下给计算绑定，非无条件唯一。见 docs/18 §3。
> 3. **LNP22 先例降级**：本文 §1.4"原文先例"应理解为"原文提供相关组件与设计先例"（L126/L168/L2081），**不是**原文已验证本文完整构造。见 docs/18 §2.3。
> 4. **B1/B2 比较与决策**：新增 B2 扩展版分析（把 (s₁,s₂,x) 共同放进新承诺 Ajtai 消息），LB-05R 决策选 B2 为候选研究路线（非安全结论）。见 docs/18 §2/§5 与修订后的 `decisions/LB-05-decision.md`。
> 本文以下为 LB-05 原始记录，**结论以 docs/18 为准**。

> LB-05 · 任务 B / 任务 C（路线 B 部分）/ 任务 D。日期：2026-11-20。
> 核心问题：能否通过新增 ABDLOP 承诺，把 LBF 原有 `s₂` 转换为 LNP22 exact-norm 证明能处理的**消息向量**，并保持它与原始 opening 的一致性？
> 用户构造：
> ```
> (原承诺)  t_A = A₁s₁ + A₂s₂ ,   t_B = Bs₂ + m
> (辅助承诺) t'_A = A'₁s₂ + A'₂r , t'_B = B'r + m'
> ```
> 结论先行：**数学原理上可行，但必须采用"单次联合 PoK 共享 witness"形式，且需新协议设计 + 参数实例化 + 安全证明，均未完成。** 三点关键：(1) s₂ 在新承诺的 **Ajtai 消息槽**，恰是 LNP22 §5.2 exact-ℓ₂ 的合法作用对象；(2) s₂∈R_F（非 R_K），用 base-ring 自同构 σ 配对即可，**避开 LBF §3.3.4 的 ν 陷阱**；(3) 同一性**不能**靠两个独立证明"事后绑定"（LB-04 的 m₂ 维约束障碍仍适用），但**可以**靠单次联合 PoK 的共享 witness——同一 s₂ 变量同时出现在两组承诺关系中，这时一致性是 statement 的定义层性质。**★LB-05R 修正**：此处原写"MSIS binding 保证 witness 唯一"过强，已删——MSIS 只在给定矩阵分布/维度/短界条件下提供计算绑定，且共享变量属协议层提取性质、与 MSIS 的承诺绑定性质是两回事（详见 docs/18 §3）。
> 决策含义：对应 LB-05 决策 **B 的条件性成立**——直接扩展不可行（docs/16），辅助承诺 + 联合一致性证明**数学可行但无条件未闭合**；若 §6 的必要条件任一不满足，退回 C。
> 一手来源：LNP22 镜像 `md_lnp22_asia/content.md`（`LNP L####`）；LBF 全文镜像 `paper_mirror.txt`（`LBF L####`）。镜像限制同 docs/16 开头。

---

## 1. 任务 B：构造的精确维度、环归属与公开/秘密属性

### 1.1 基础环与符号

```
R_q = Z_q[X]/(X^d+1),  d ∈ {64, 128}   （LBF 承诺环，LBF L503–510）
```
`[论文事实: LBF L508–510]` 关键约定：**"Salts and commitments are always R_F-objects and never R_K-ones"**。因此 s₂ 天然是 R_F 对象——这对路线 B 是决定性的简化（见 §5.3）。

`[论文事实: LBF L3561–3562]` d=128 参数锚点：κ=n=11, κ'=ℓ=16, n+ℓ=27, m₂=53；d=64：n=19, ℓ=16, n+ℓ=35, m₂=83。（m₁ 与辅助承诺维度需查 Table 2 完整行 [待核查]）

### 1.2 原承诺（不变）

| 对象 | 维度 / 环 | 属性 | 证据 |
|---|---|---|---|
| A₁ | `R_q^{n×m₁}` | 公开 | LNP L495；LBF L1082 |
| A₂ | `R_q^{n×m₂}` | 公开 | 同上 |
| B | `R_q^{ℓ×m₂}` | 公开 | 同上 |
| s₁ | `R_q^{m₁}` | 秘密盐 | LBF L503 |
| s₂ | `R_q^{m₂}` | 秘密盐（**本阶段要证 exact 的对象**） | LBF L503 |
| m | `R_q^{ℓ}` | 消息（BDLOP 槽） | LBF L511–515 |
| t_A, t_B | `R_q^{n}`, `R_q^{ℓ}` | 公开承诺 | LNP L495 |

`[论文事实: LBF L1318–1320]` 原承诺 binding：MSIS 下 short opening `(s₁,s₂)` 唯一（注意 s₂ 的 binding 主要来自 `t_A` 的 `A₂s₂` 项；`t_B=Bs₂+m` 中 m 吸收 s₂，故 t_B 对 s₂ 无独立约束）。

### 1.3 辅助承诺（新增）—— 用户构造的完整维度化

用户式 `t'_A=A'₁s₂+A'₂r, t'_B=B'r+m'` 对应 LNP22 ABDLOP 结构 `t_A=A₁s₁+A₂s₂, t_B=Bs₂+m`（LNP Fig4, L495）的角色重映射：

| 原 ABDLOP 角色 | 辅助承诺中的扮演者 | 说明 |
|---|---|---|
| Ajtai 消息 s₁（要证 exact 的槽） | **s₂（原承诺的盐，现作消息）** | 这是路线 B 的核心：把 s₂ 搬进 Ajtai 消息槽 |
| randomness s₂ | **r（新采样盐）** | 为辅助承诺提供 hiding |
| BDLOP 消息 m | m'（新消息，可置 0） | 可为空 |

完整维度表：

```
A'₁ ∈ R_q^{n'×m₂}     : 列数必须 = m₂（匹配 s₂ 长度）；行数 n' 待定
A'₂ ∈ R_q^{n'×m₂'}    : 列数 = m₂'（r 长度）
B'  ∈ R_q^{ℓ'×m₂'}    : ℓ' 可置 0
s₂  ∈ R_q^{m₂}        : 原承诺盐，此处作消息（secret）
r   ∈ R_q^{m₂'}       : 新随机盐（secret）
m'  ∈ R_q^{ℓ'}        : 新消息（secret/public 依应用）
t'_A = A'_s s₂ + A'_x x + A'_r r ∈ R_q^{n'}    （公开）★LB-05R 修正：补入二进制余量 x
t'_B = B'r + m'      ∈ R_q^{ℓ'}    （公开）
σ(s₂) ∈ R_q^{m₂}      : R_F 自同构 X↦X^{−1} 作用于 s₂，**由 s₂ 决定、非独立秘密变量**（LB-05R 修正）
x ∈ R_q^{υe}          : 二进制余量 x_i（每个装 2logβ 位，υe=1）；**必须在 Ajtai 槽与 s₂ 同时承诺**（LNP L1719/1759）
A'_1 = [A'_s  A'_x] ∈ R_q^{n'×(m₂+υe)} = R_q^{n'×(m₂+1)}
```
★完整修正维度表、σ(s₂) 角色、整数提升与参数条件见 `docs/18` §1。

> **★LB-05S 修正**：原稿写 `m₂'>n'` 简化过度。LNP22 的 hiding 堆叠矩阵是 [A₂;B]（n+ℓ 行），且 Extended-MLWE 随协议层级递增维度（L474–476/L763/Thm4.5/Prop5.1/Thm5.3）。正确条件见下；完整分析见 docs/19 §3.1。

`[推导]` **hiding 约束（收紧）**：t'_A=A'_s s₂+A'_x x+A'_r r 要隐藏 s₂，需堆叠矩阵 [A'_r;B'] 作用下的 r 与均匀不可分（Extended-MLWE），其行数至少 `n'+ℓ'`（不是 n'）。按 B2 完整 commit-and-prove transcript 对应层级，准确条件为
```
m₂' > n'+ℓ'                       （承诺层，类比 ABDLOP 的 m₂>n+ℓ）
m₂' > n'+ℓ'+1                     （commit-and-prove，+1 来自 b^T / Rej2 泄露 1 bit）
m₂' > n'+ℓ'+λ'+1  ... > n'+ℓ'+λ'+2(256/d'+1)   （Thm5.3 exact 层，+ 附加承诺与 masking）
```
`m₂'>n'` 不成立为充分条件；n',ℓ',m₂',λ' 未选，`[待核查]` 具体下界不补造数字。这是**新增的维度约束**。
`[推导]` **binding 约束（LB-05R 收紧，LB-05S 再收紧）**：A'_1(s₂,x)+A'_r r=t'_A 的短 opening 唯一性不是无条件成立，而是需 `MSIS_{n', m₂+υe+m₂', B}` 假设（给定矩阵分布、维度、短界 B）。★B 的取值**不是** `2β_s`（未证的 exact 界）：LNP22 提取界是 c̄-scaled（`‖s̄_i c̄‖≤2s_i√(2m_i d)`，Lemma 3.1），binding 论证乘 c̄c̄' 清分母后界为 `8η·s_i√(2m_i d)`；仅被 exact 关系覆盖的分量（B2 的 s₂）可取 exact β。差向量范数与原始/辅助两层 binding 区别见 docs/18 §3.2–3.3、docs/19 §3.5。

### 1.4 与 LNP22 原文机制的对应（★LB-05R 降级为"相关组件与设计先例"）

`[推导/用户复核]` 以下三处是 LNP22 提供的**相关组件与设计先例**，说明本文构造并非凭空；但**不是**原文已验证本文的"原 LBF randomness s₂ 与辅助承诺消息 s₂ 联合提取"完整构造。不得写成"原文先例已验证本构造"。逐接口（线性接口 Eq.6、Ajtai 扩列、任意 E_i、σ 配对、二值余量）核查见 docs/18 §2.3。

`[论文事实: LNP L126]` 一般配方："first commit to s as part of the s₁ part of (5) (i.e. in the 'Ajtai part' of the ABDLOP scheme)"——目标向量放 Ajtai 消息槽。辅助承诺把 s₂ 放 A'₁ 槽正是此配方。
`[论文事实: LNP L2081, Remark 6.2]` 可验证加密先例："since we **commit to r and m using a separate ABDLOP commitment**, we circumvent the relaxation factor by **proving exact norms on r and m**"——**用单独 ABDLOP 承诺 + 证 exact**是 LNP22 已展示的路线，辅助承诺是同类构造。
`[论文事实: LNP L168]` 无自同构时的强制路线："If g is not an automorphism … would require the prover to **commit to both s and g(s), and then also prove the linear relationship between the commitments**"——这是辅助承诺 + 一致性关系的原文理论依据。

---

## 2. 任务 B 核心：联合 commit-and-prove 接口与提取目标

### 2.1 为什么必须是"单次联合 PoK"，而不能是两个独立证明

这是本阶段最重要的判定，直接回答用户"两个承诺中的 s₂ 是否同一"。

`[推导]` **两个独立证明不可行**：若对原承诺跑 Π_many（得 relaxed 提取 `‖c̄s̄₂‖≤β_rlx`）、对辅助承诺单独跑 exact 证明（得 `‖s'₂‖≤β`），二者提取的 s₂ 是**两个变量**。要把它们识别为同一，需要 LB-04 §2.4 证明缺失的 m₂ 维线性约束——标量 anchoring 只给 `ct(ΣwₙBs₂)` 一个泛函，核维数巨大。**LB-04 的负面结论在"两独立证明 + 事后绑定"模型下完全成立。**

`[推导]` **单次联合 PoK 可行**：把两组承诺关系写进**同一个** PoK statement，共享唯一的 witness 变量 s₂：

```
Statement（公开输入）:
  t_A, t_B, t'_A, t'_B, A₁,A₂,B,A'₁,A'₂,B', E, v, p, β, (采样界 B̃)

Witness（秘密，提取目标）:
  W = (s₁, s₂, m, r, m', σ(s₂), x)

Relations（全部由同一 s₂ 串联）:
  (R1) A₁s₁ + A₂s₂ = t_A                          [原承诺 opening]
  (R2) Bs₂ + m = t_B                              [原承诺 opening]
  (R3) A'₁s₂ + A'₂r = t'_A                        [辅助承诺 opening]
  (R4) B'r + m' = t'_B                            [辅助承诺 opening]
  (R5) ⟨E·(s₂,σ(s₂)) − v, E·(s₂,σ(s₂)) − v⟩
         + ⟨p, x⟩ = β²  mod q                     [Eq.59，exact-ℓ₂ 自内积]
  (R6) ⟨x, x − 1⟩ = 0 mod q + approximate range   [Lemma 5.2 + 防回绕，整数提升]
  (R7) ‖c̄s₁‖, ‖c̄r‖ ≤ β_rlx（relaxed，或按需 exact）[其余盐]
```

`[推导]` **同一性判定（正面）**：(R1)(R2) 的 s₂ 与 (R3)(R5) 的 s₂ 是 statement 中**同一个变量**。提取器输出 `W̄=(s̄₁,s̄₂,m̄,r̄,m̄',σ(s̄₂),x̄)`，其中 s̄₂ 同时满足原承诺与辅助承诺关系，且受 (R5)(R6) 的 exact 界 `‖s̄₂‖₂≤β`。**因此 exact 界约束的正是原始 opening 中的 s₂**——不是"另一个向量"。这是路线 B 相对 LB-04 负面结论的实质推进：同一性不靠 anchoring 标量泛函，而靠联合 statement 的变量共享。

### 2.2 同一性的可靠性（MSIS）与一个技术条件

`[推导]` 若作弊者能让同一组公开承诺被接受、但提取出两个不同 `s̄₂≠s̄'₂`（分别满足两组关系），则差向量给出短核：

```
A₁(s̄₁−s̄'₁) + A₂(s̄₂−s̄'₂) = 0
A'₁(s̄₂−s̄'₂) + A'₂(r̄−r̄') = 0
```

即 `MSIS_{n+n', m₁+m₂+m₂', B}` 的一个解（拼接矩阵 `[[A₁,A₂,0],[0,A'₁,A'₂]]`）。故在 MSIS 假设下 witness 唯一，s̄₂ 唯一——**同一性成立**。

`[待核查]` 该拼接矩阵的 MSIS 硬度需按 LBF Table 2 / LNP 定理 5.3 重新实例化；尤其要确认 A₂ 与 A'₁ 的列不产生病态短向量使两个不同 s₂ 同时满足两式。这是**参数层**条件，非代数矛盾；本阶段不做参数实例化（见 §6）。

### 2.3 与 LBF anchoring sketch 的关系

`[论文事实: LBF L3130–3139]` Remark 4.8 说 exact 证书 "reaches the BDLOP randomness s₂ … through the anchoring instantiation of §3.2.1.1"，append bound 维度为 `(m₁+m₂)d`（Step5 `kt(B̃−1)√((m₁+m₂)d)`、Step17 `(B̃−1)t√((m₁+m₂)d)`，镜像缺根号 [待核查]）。
`[推导]` 该 sketch 与本构造的**差异**：
- sketch 说"through anchoring"（标量替换，不新增承诺，LBF L1645–1652 "no commitment is recomputed"）；
- 本构造是**新增辅助承诺 + Ajtai 消息槽 exact**，走 LNP L168/L2081 路线，**不是** anchoring 就地替换。
- sketch 的 bound 维度 `(m₁+m₂)d`（整个 opening）与"只对 s₂ 证 `‖s₂‖≤β`"的对象维度 `m₂` 不同——作者 sketch 的精确对象仍 [待核查]（见 docs/16 §1 问题 4）。
`[推导]` 故本构造是**独立于作者 sketch 的另一条路线**，不应声称"实现了 Remark 4.8"。

---

## 3. 任务 C：安全性与参数成本（路线 B）

### 3.1 五问逐答

| 判据 | 判定 | 依据 |
|---|---|---|
| **Binding：新旧承诺提取同一 s₂？** | **条件成立**：单次联合 PoK 下同一性由变量共享保证，MSIS_{n+n',m₁+m₂+m₂'} 保证 witness 唯一（§2.2）。两独立证明下不成立（LB-04）。 | §2.1–2.2 |
| **Hiding：新增承诺泄露 s₂？** | **需约束**：t'_A=A'₁s₂+A'₂r 要求 m₂'>n'（MLWE）；证 `‖s₂‖≤β` 只泄露范数上界、不泄露 s₂ 本身（LNP22 exact 证明的设计目标）。但 β 取值若为公开常数，泄露量需按应用评估。 | §1.3；LNP L126 |
| **Exact norm：原始 s₂ 的紧界？** | **条件成立**：(R5)(R6) 给 `‖s̄₂‖₂≤β`，无 c̄ 因子（这是 exact 相对 relaxed 的核心优势）。β 须覆盖采样界 `m₂·d·(B̃−1)²` 量级。 | §2.1；LBF L1848–1855 |
| **Component-wise：R_K→R_F² 保持关系？** | **不涉及**：s₂∈R_F（LBF L508–510），路线 B 全程在 R_F 上用 base-ring σ 配对，**不触发** LBF §3.3.4 的 R_K component-wise 分裂，也**避开** `‖a‖²+ν‖b‖²` 的 ν 陷阱（LBF L1841–1847）。若应用侧消息 m' 是 R_K 元素，则 m' 需分裂为两个 R_F 槽，但不影响 s₂ 的 exact 证明。 | LBF L508–510, L1838–1855 |
| **新增安全假设？** | **是**：需新增 MSIS_{n',m₂+m₂'}（辅助承诺 binding）、MLWE_{n',m₂'}（其 hiding），以及扩展 MSIS_{n+n',m₁+m₂+m₂'}（联合 witness 唯一）。均为标准格假设，但**参数未实例化**。 | §1.3, §2.2 |

### 3.2 无 c̄ 累积的有效性（条件性）

`[推导]` 若 §2.1 联合 PoK 成立，则提取 `s̄₂` 带 exact 界（无 c̄），这正是 Remark 4.8 "the extracted salts would then satisfy their bounds with no factor c̄"（LBF L3135）的前提。但**跨轮累积是否真正截断仍需单独证明**：需要 binding 把第 r 轮 certified opening 与第 r+1 轮提取 opening 识别为同一（LBF L3136–3137），且每轮都用联合 PoK。本阶段**只建立单次 s₂ exact**，不证明递归（沿用 docs/15 的边界）。

### 3.3 成本（符号级 + 参数代入说明）

**符号级**（每个 fresh salt 一份辅助承诺）：

| 项 | 增量 |
|---|---|
| 公开矩阵 | A'₁: n'·m₂, A'₂: n'·m₂', B': ℓ'·m₂' 个 R_q 元素 |
| 秘密 witness | r: m₂', σ(s₂): m₂, x: ≈2⌊log β⌋ 个 R_q/bit 元素 |
| 联合 PoK 转录 | 线性关系 (R1)–(R4)：4 组 Σ 轮；exact (R5)–(R6)：LNP Fig10 量级，约 O((m₁+m₂+m₂')·d·log q) |
| 整数提升 | 二进制余数 `2 log β ≤ d`（LNP L1700），依赖 Thm 5.3 的 `B^{(eq)}<q^{1/(4c)}`、`2β²+(B^{(eq)})²−1<q`（LNP L1823–1827） |

`[待核查]` **参数代入**：n', m₂', ℓ', β 未选定，A'₁/A'₂/B' 未按 LBF Table 2 实例化，转录大小未算成具体字节。用户要求"符号级与参数代入估算"——本阶段完成符号级；**参数代入因缺选定值标 [待核查]，不作估计数字**（遵守 LB-04"不以估计证明大小代替参数计算"的禁令）。
`[推导]` 一个量级观察（非结论）：若对 Protocol 8 Step 5 的 `(k+1)t` 个 output salt 各配一份辅助承诺，成本乘 `(k+1)t`；对 Protocol 7 Step 17 的 t 个 mask salt 各配一份，乘 t。这是显著开销来源，需在参数实例化阶段正面处理。

---

## 4. 任务 D：两处 fresh salt 分别分析

`[论文事实: LBF L2883–2893, L2775–2777, L3133–3135]` 两处 PoK 均为"消息 exact + 盐 relaxed"，Remark 4.8 要求追加 exact 界。

### 4.1 Protocol 8 Step 5（输出盐 `s_{2,i,j}`）

- 位置：`N_c=(k+1)t` 个承诺串接的单个 Π_many，fresh salt `s_{i,j}=(s₁,s₂,i,j)` 随 `C_{i,j}=Commit(y_{i,j},s_{i,j})`（LBF L2876–2877）。
- 路线 B 应用：为每个 `s_{2,i,j}` 建辅助承诺 `t'_{A,i,j}=A'₁s_{2,i,j}+A'₂r_{i,j}`，并入联合 PoK。
- 与 Π_many 组合：原 Π_many 的消息恒等式 `y_j−Σb^{i−1}y_{i,j}=0` 保持 exact（Lemma 3.6(3)）；新增 s₂ exact 由 (R5)(R6) 提供。二者在同一联合 statement 内。
- 与 anchoring 组合：不需要——路线 B 不依赖 anchoring 标量替换（§2.3）。
- 成本：`×(k+1)t`。

### 4.2 Protocol 7 Step 17（mask 盐 `s_{2,y,j}`）

- 位置：对 `C_{y,j}=Commit(y_{y,j},s_{y,j})` 的 Π_many PoK；mask 盐在 Step 19 参与 `s_{2,j}=Σρᵢs_{2,i,j}+s_{2,y,j}`（LBF L2775–2777, L2782–2783）。
- 路线 B 应用：为每个 `s_{2,y,j}` 建辅助承诺，并入联合 PoK。
- **不相交性约束**：`[论文事实: LBF L3642–3643, L3648–3649]` LBF 刻意让 `C_{y,0}` 各块 fresh salt 对互不相交、且与 `{C_{y,j}}` 的盐不相交，`C_{y,0}` 从不与其他承诺同态组合。辅助承诺必须保持这种不相交性——不能把不同位置盐的辅助承诺合并共享 witness，否则破坏 LBF 的 blinding 论证。
- 成本：`×t`。

`[推导]` 结论 D（路线 B 版）：两处 fresh salt 都**可**用辅助承诺 + 联合 PoK 获得 s₂ exact 界，但成本分别乘 `(k+1)t` 与 t，且 Protocol 7 侧需保持盐不相交性。**单次正确 ≠ 递归正确**（§3.2）。

---

## 5. 与竞争路线的边界（不外推）

- 本构造是**数学原理路线**，不是 Decider 实现；不产出 `CE_com^k` 的验证器。
- 不做 LaZer/LaBRADOR 工程集成；不声称 Halo2/递归友好。
- 不把"联合 PoK 单次 s₂ exact"外推为"完整 folding 递归的无 c̄ 累积"——后者需每轮联合 PoK + 跨轮 binding 证明（§3.2）。
- 不声称抵抗 TEE/TCB 失陷、管理员联合控制 DB 等（与本研究统一边界一致）。

---

## 6. 路线 B 成立的必要条件与退回判据

`[推导]` 路线 B 判为"条件性数学可行"，须同时满足以下条件才真正闭合 s₂ 范数问题：

1. **联合 PoK 可构造**：(R1)–(R6) 能在单一 Σ-protocol / Fig10 扩展中同时满足，且 s₂ 同时扮演 randomness（原）与消息（辅助）两种角色不破坏 reliability。
2. **参数可实例化**：n', m₂', ℓ', β 满足 hiding（m₂'>n'）、binding（MSIS）、Thm 5.3 界条件（`2β²+(B^{(eq)})²−1<q` 等），且按 Table 2 可行。
3. **拼接矩阵 MSIS 硬度**：`[[A₁,A₂,0],[0,A'₁,A'₂]]` 的短核为空（§2.2 [待核查]）。
4. **成本可接受**：`(k+1)t + t` 份辅助承诺的开销在目标应用内。
5. **跨轮递归证明**（若目标是 IVC）：每轮联合 PoK + binding 识别同一 opening 的严格证明闭合（本阶段未做）。

**退回判据**：任一条件（尤其 1、3）被证伪 → 退回 LB-04 决策 C。本阶段**不满足**条件 2–5（未实例化、未证拼接 MSIS、未算成本、未证递归），故只能是"条件性 B"，不是"已验证可行"。

---

## 7. 待核查与诚实边界

- `[待核查]` 官方 PDF 未逐页核对；Remark 4.8 bound 根号字形缺失，按 docs/16 处理。
- `[待核查]` n', m₂', ℓ', β 未选定；拼接矩阵 MSIS 硬度未实例化；`2 log β ≤ d` 是否成立于选定参数。
- `[推导]` "数学可行"指存在无代数矛盾的清晰构造路径，**不等于**已证明安全、已实例化、已实现。
- 本文不把 relaxed 写成 exact、不把 anchoring 当范数证明、不把两个独立证明的 s₂ 当自动同一、不把单次证明等同递归证明。
