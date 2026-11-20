# 19 · B2 Exact-Norm Witness 分离与安全审计（LB-05S）

> **★LB-05T 修订说明（2026-11-20）**：用户复核确认 s/x 分离正确，并提出两点调整——(1) `E_{s₂}` 不是"接口兼容性待核查"，而是"通用 E_i 接口支持、参数实例化待核查"（m₁*=m₁+m₂ 的参数化实例）；(2) §3.5 "exact 覆盖的分量在 MSIS 中可直接使用 exact β" 一句过强——binding 双 opening 差仍带 c̄c̄′ 放大，exact β 是单 opening 谓词。本轮就地收紧这两处，并把联合提取器状态更新为"结构继承自 Thm5.3（见 docs/20），三层 binding 归约骨架已写、形式化未证（见 docs/21）"。决策更新见 `decisions/LB-05T-decision.md`。原 LB-05S 论证保留作历史。
>
> LB-05S · 任务 A / B / C / D / E。日期：2026-11-20。
> 基线：`docs/17`（辅助承诺初稿）、`docs/18`（LB-05R 联合关系审计，含本轮待修正的定义错误）、`decisions/LB-05-decision.md`（B2 候选路线）。
> 本轮只修正 B2 的数学规格，不扩大到 Decider、不做 LaZer 集成、不进入递归证明。
>
> **结论先行**：
> 1. **docs/18 §2.2 的变量定义确有一个实质错误**：写 `ŝ₁=(s₁,s₂,x)` 后又定义 `s_full=(ŝ₁,σ(ŝ₁),m̂,σ(m̂))`，把 x 与 σ(x) 一起塞进了 exact-norm 关系向量。这与 LNP22 Figure 10 不符——原文 s=(s₁,σ(s₁),m,σ(m)) **不含 x**（官方 PDF 文本流 PDF L5653/L6179）。修正为 s_A=(s₁,s₂)、s_LNP=(s_A,σ(s_A),m_A,σ(m_A))，x 只作额外承诺消息 + 二进制余量，无 σ(x)（任务 A）。
> 2. **E_{s₂}∈R_q^{m₂×2(m₁+m₂+ℓ)} 是本轮的设计外推，LNP22 原文无此对象**：原文 E_i∈R^{p_i×2(m₁+ℓ)}，且 Figure 10 中 s₂ 只作 randomness、从不进入 exact 向量（PDF L6179 / L1772）。B2 把 s₂ 提升为消息、并把 s 维度从 2(m₁+ℓ) 推广到 2(m₁+m₂+ℓ)，是**超出原文逐字的结构推广**，须在安全证明阶段验证 Fig5/Fig8 接口对扩展维度的实例化（任务 A/B/E）。
> 3. **两处安全论证已收紧**：辅助承诺 hiding 不能用 `m₂'>n'`——按 Extended-MLWE 层级为 `m₂'>n'+ℓ'`（承诺层）→`>n'+ℓ'+1`（commit-and-prove）→`>n'+ℓ'+λ'+2(256/d'+1)`（exact 层）（任务 C.1）；MSIS 差向量不能用未证的 `‖Δs‖≤2β`——LNP22 提取界是 c̄-scaled（Lemma 3.1 st.2，PDF L1545），binding 论证须乘 c̄c̄' 清分母（L511–521）（任务 C.2/C.5）。
>
> **来源**：LNP22 官方 PDF `C:/Users/dell/AppData/Local/Temp/lb02/lnp22_asia.pdf`，其文本流 `C:/Users/dell/AppData/Local/Temp/pdf_check_lnp22/lnp22.txt`（标注 `PDF L####`）；镜像 `C:/Users/dell/AppData/Local/Temp/lb02/md_lnp22_asia/content.md`（标注 `LNP L####`）。本轮用官方 PDF 文本流对关键行（s 定义、Extended-MLWE 维度、Lemma 3.1）做了交叉核对，**未做逐页视觉核对**；用户已核对官方 PDF 第 42–43 页截图。两者结论一致。

---

## 0. 记号与基线维度

```
R_q = Z_q[X]/(X^d+1), d∈{64,128}；σ: s(X)↦s(X^{−1}) 为 R_q 自同构
主承诺: A₁∈R_q^{n×m₁}, A₂∈R_q^{n×m₂}, B∈R_q^{ℓ×m₂}
        t_A=A₁s₁+A₂s₂∈R^n,  t_B=Bs₂+m∈R^ℓ
LBF 参数: d=128: n=11,ℓ=16,n+ℓ=27,m₂=53;  d=64: n=19,ℓ=16,n+ℓ=35,m₂=83
υe = exact 关系条数（本阶段只证 ‖s₂‖≤β，故 υe=1）
```

`[论文事实: PDF L5653/L6179, LNP L1690/L1814]` **LNP22 Figure 10 的基础对象**：
```
s = (s₁, σ(s₁), m, σ(m)) ∈ R_q^{2m₁} × R_q^{2ℓ},   s₁∈R^{m₁}（Ajtai 消息）, m∈R^ℓ（BDLOP 消息）
E_i ∈ R^{p_i×2(m₁+ℓ)},  ‖E_i s − v_i‖ ≤ β_i^{(e)}       (Eq.53)
```

---

## 1. 任务 A：修复 s 与 x 的变量定义

### 1.1 错误定位（docs/18 §2.2）

docs/18 第 98、111–113 行写：
```
ŝ₁ = (s₁, s₂, x) ∈ R^{m₁+m₂+υe}
s_full = (ŝ₁, σ(ŝ₁), m̂, σ(m̂)) ∈ R^{2(m₁+m₂+υe+ℓ')}
E_{s₂} ∈ R^{m₂×2(m₁+m₂+υe+ℓ')} 选取 ŝ₁ 中 s₂
```
`[推导]` 这里把 x 和 σ(x) 纳入了 s_full，于是 Eq.(59) 的 exact 关系隐式作用到了 x 上。用户指出：这与 LNP22 Figure 10 中 s 的定义不一致——x 虽追加进 Ajtai 承诺，但不属于 s。核查证实用户正确。

### 1.2 LNP22 官方 PDF 的三条直接证据（s 与 x 分离）

`[论文事实: PDF L5653]` Figure 10 general statement：
> "The general statement proven in Figure 10 includes the knowledge of a vector s := (s₁, σ(s₁), m, σ(m)) ∈ R_q^{2m₁} × R_q^{2ℓ} …"

四个分量，无 x、无 σ(x)。

`[论文事实: PDF L6179 / LNP L1814–1816]` Figure 10 图注：
> "s := (s₁, σ(s₁), m, σ(m)) verifies Equations (50) to (54)."

`[论文事实: LNP L1727 Eq.59, L1751 Eq.66, L1843]` exact 关系的结构：
```
⟨E_i s − v_i, E_i s − v_i⟩ + ⟨p⃗_i, x⃗_i⟩ = (β_i^{(e)})² mod q      (Eq.59)
I_i(s, x) = T(E_i s − v_i, E_i s − v_i) + T(p⃗_i, x⃗_i) − (β_i^{(e)})²  (Eq.66)
```
`I_i` 的函数签名就是 `(s, x)` 两个独立实参：`E_i` **只作用于 s**；x⃗_i 仅作为独立加法项 ⟨p⃗_i,x⃗_i⟩（二进制重建差值 `(β_i^{(e)})²−‖E_i s−v_i‖²`）出现，**不参与 E_i 矩阵乘法、不出现在任何 σ 配对中**。

`[论文事实: LNP L1772]` 承诺布局——x 确实追加进 Ajtai 承诺：
```
t = [A₁ | 0]·[s₁ ; x] + [A₂ ; B]·s₂ + [0 ; m]
```
`[推导]` 这正是用户强调的区分：**承诺槽里追加了 x，但 s 向量不含 x**。两者是两个对象。

### 1.3 修正后的变量定义（B2）

```
基础消息:    s_A = (s₁, s₂) ∈ R_q^{m₁+m₂}       （Ajtai 消息，Ajtai 部分含 s_A 与 x）
             m_A = m      ∈ R_q^{ℓ}             （BDLOP 消息）
二进制余量:  x ∈ R_q^{υe}, υe=1, 每 x_i 装 2logβ 位（x_i∈{0,1}^{2logβ}）
随机盐:      r ∈ R_q^{m₂'}                      （新 ABDLOP randomness）

辅助承诺（Ajtai 部分承诺 s_A 与 x）:
             t̂_A = Â_s·s_A + Â_x·x + Â_r·r ,  Â₁=[Â_s Â_x]∈R_q^{n'×(m₁+m₂+υe)}
             t̂_B = B̂·r + m_A ,                 B̂∈R_q^{ℓ'×m₂'}

基础 exact-norm 向量（不含 x、无 σ(x)）:
             s_LNP = (s_A, σ(s_A), m_A, σ(m_A)) ∈ R_q^{2(m₁+m₂+ℓ)}
             σ(s_A)=(σ(s₁),σ(s₂)) 由 s_A 经自同构唯一决定，非独立变量（LNP L587/L141）
```

`[推导]` 关键修正点：`s_LNP` 只由基础消息 s_A=(s₁,s₂) 与 m_A=m 及其 σ 像构成，x 与 σ(x) **均不在其中**。这与 LNP22 原文"承诺 Ajtai 部分含 x、但 s=(s₁,σ(s₁),m,σ(m)) 不含 x"的结构完全一致。

### 1.4 E_{s₂} 的维度修正与设计外推声明

```
用户建议并修正:  E_{s₂} ∈ R_q^{m₂×2(m₁+m₂+ℓ)},   E_{s₂}·s_LNP = s₂
错误版本(docs/18): E_{s₂} ∈ R_q^{m₂×2(m₁+m₂+υe+ℓ')}  （多计 x 的一列）
```

`[论文事实: LNP L1681/L1688/L1774]` 原文 E_i∈R^{p_i×2(m₁+ℓ)}，列数严格为 2(m₁+ℓ)，**不含 x 的任何列**。
`[论文事实: LNP L1681/L1688/L1774]` LNP22 Figure 10 中**不存在名为 E_{s₂} 的对象**：原文 s₂ 是 randomness，只通过 [A₂;B]s₂（L1772）与 masking 矩阵参与。**但**（★LB-05T 用户复核）E_{s₂} 不是新证明原语，而是原文通用矩阵接口的**参数化实例**：
```
原文通用接口: E_i ∈ R_q^{p_i × 2(m₁+ℓ)},  公开可任意选取，作用于 s=(s₁,σ(s₁),m,σ(m))  (Eq.53)
B2 参数化:   m₁* = m₁+m₂（把 s₂ 像 x 一样追加进 Ajtai 消息槽, cf. L5734）
             E_{s₂} ∈ R_q^{m₂ × 2(m₁+m₂+ℓ)},  选 s_LNP 中 s₂ 分量
```
`[推导]` 因此正确定性是"**通用 E_i 接口支持，参数实例化待核查**"（用户 LB-05S 复核原文），而非"接口不兼容待核查"。两步参数化——(1) s₂ 提升为消息加入 s_A；(2) s 维度从 2(m₁+ℓ) 扩到 2(m₁+m₂+ℓ)——在结构层与原文"任意公开 E_i 作用于 s"一致，非原文逐字。须在安全证明阶段验证 Fig5/Fig8 多线性接口对扩展维度的**实例化**与 Thm5.3 参数重推（见 docs/20 §1.5）。E_{s₂} 不含 x 列，符合原文"E_i 列数不含 x"。

### 1.5 x 不需要 σ(x) 配对

`[论文事实: LNP L1704/L1708 Lemma 5.2, L1710, L1725 Eq.58]` x 的二值性走独立路径：
```
⟨x′, x′−1⃗⟩ = 0 mod q  (Eq.58)  →  Lemma 5.2  ⟨x⃗,x⃗−1⃗⟩=0 ⇒ x⃗∈{0,1}ⁿ  →  Fig9 approximate range proof
```
Figure 10 规范与实例化部分（L1721–L1757）**σ 出现 0 次**，全文无任何 σ(x)。
`[推导 · 论文事实归纳]` s 需要 σ 是因为 R_q 上元素范数 ‖s‖² 要由 s(X)·σ(s(X)) 的常数项捕捉（LNP L126/L113–115）；x⃗_i 是逐系数 Z_q bit 向量，二值性由 Eq.58 + Fig9 在 Z_q 层确立，不经过 R_q 自同构。因此 B2 中 x **不需要 σ(x) 配对**。

### 1.6 exact 关系、整数提升与参数条件（更新）

```
(R-exact)  ⟨E_{s₂}·s_LNP, E_{s₂}·s_LNP⟩ + ⟨p, x⟩ = β² mod q,   p=(1,2,…,2^{2logβ−1},0,…,0)
           其中 E_{s₂}·s_LNP = s₂,  ⟨p,x⟩ = β² − ‖s₂‖²（整数，非负）
```
`[论文事实: LNP L1700, L1729 Eq.60, L1827 Thm5.3]` 模 q → 整数提升条件（用 Fig9 approximate range proof 排除回绕）：
```
2·(max β_i^{(e)})² + (B^{(e)})² − 1 < q,
且 2logβ ≤ d（打包：每 x_i∈R_q 装 2logβ 位 ≤ d 个系数）
```
`[推导]` 本阶段 υe=1；消息维度从原文 2(m₁+ℓ) 扩展到 2(m₁+m₂+ℓ) 后，B^{(e)} 的噪声增长须按 LNP Prop5.1 重推，`[待核查]` 本阶段不代入具体参数、不虚报证明大小（遵守 LB-04"不以估计证明大小代替参数计算"禁令）。

`[推导]` β 量级校核：s₂ 采样界 ‖s₂‖∞<B̃=2（LBF L2876），‖s₂‖₂²≲m₂·d·(B̃−1)²=m₂·d；d=128 时 ≈53·128≈6784，2logβ≈13≪d=128，打包条件满足。

---

## 2. 任务 B：完整 B2 联合关系

### 2.1 用 LNP22 Eq.(6) 线性接口表达原始 opening

用户建议的矩阵（本节验证其是否合法）：

```
s_A=(s₁,s₂),  m_A=m
R₁ = [ A₁  A₂ ; 0  B ]  ∈ R_q^{(n+ℓ)×(m₁+m₂)}
R_m = [ 0 ; I_ℓ ]        ∈ R_q^{(n+ℓ)×ℓ}

R₁·s_A + R_m·m_A = [ A₁s₁+A₂s₂ ; Bs₂+m ] = [ t_A ; t_B ]  ✓
```

`[论文事实: LNP L86/L90 Eq.6, L495, PDF L240–245]` ABDLOP 线性关系接口：
```
R₁·s₁ + R_m·m = u mod q,   R₁∈R^{N×m₁}, R_m∈R^{N×ℓ}, u∈R^N 均公开
```
`[论文事实: LNP L92, PDF L240–245]` **关键性质**：
> "the proof size is not affected by the sizes of R₁ and R_m … the proof size for proving linear relations over R_q is the same as the proof size of just proving knowledge of the committed values."

`[推导]` 因此把 R₁ 的列数从 m₁ 扩展到 m₁+m₂、u 从单向量扩展到 [t_A;t_B]（N=n+ℓ），**证明大小不随矩阵尺寸增长**。用户建议的 R₁/R_m 是 Eq.(6) 的合法实例。

### 2.2 同一 commit-and-prove statement 中的三组关系

```
公开输入:  t_A, t_B, t̂_A, t̂_B, A₁,A₂,B, Â₁,Â_r,B̂, R₁,R_m, E_{s₂}, p, β
witness:   W = (s₁, s₂, m, r, x)      [σ(s_A) 由 s_A 决定，不单列]

(L1) R₁·s_A + R_m·m_A = [t_A;t_B]              [原始 opening, Eq.6 线性接口]
(L2) Â₁·(s_A, x) + Â_r·r = t̂_A                 [辅助承诺 Ajtai opening]
(L3) B̂·r + m_A = t̂_B                           [辅助承诺 BDLOP opening]
(L4) ⟨E_{s₂}·s_LNP, E_{s₂}·s_LNP⟩ + ⟨p,x⟩ = β² mod q   [Eq.59, s_LNP 不含 x]
(L5) ⟨x′, x′−1⃗⟩ = 0 mod q + Fig9 range          [Eq.58, x 二值 + 整数提升]
```
`[推导]` **这是 B2 相对 B1 的实质推进**：(L1) 把原始 opening 的 A₁s₁+A₂s₂ 与 Bs₂+m 变成对同一组 witness (s_A,m_A) 的公开线性约束，(L4)(L5) 对同一 witness 中的 s₂ 施加 exact 界。所有关系作用于**同一个 (s₁,s₂,m)**，不存在"两个证明各提一个 s₂ 再假设相等"的问题（该问题属 B1，docs/18 §2.1）。

### 2.3 是否真能通过 LNP22 commit-and-prove 机制实现——逐接口核查（不默认可行）

| 必需接口 | 原文依据 | B2 是否满足 | 状态 |
|---|---|---|---|
| 公开线性 `R₁s₁+R_m m=u` | L90 Eq.6；L92 证明大小与矩阵尺寸无关；L495 维度 | (L1) 正是此形式，s₂ 在 s_A（Ajtai 消息），可被 R₁ 乘 | **原文支持**（结构层） |
| Ajtai 部分追加 x | L1772 `t=[A₁|0][s₁;x]+…`；L1719 | (L2) Â₁=[Â_s Â_x] 扩列装 x | **原文支持** |
| s 不含 x、x 无 σ | PDF L5653/L6179；L1727 Eq.59 的 I_i(s,x) | s_LNP=(s_A,σ(s_A),m_A,σ(m_A)) 不含 x；x 只在 (L4)(L5) | **原文支持**（本轮修正后一致） |
| 任意 E_i 选分量做 exact | L1681/1688/1774 E_i∈R^{p_i×2(m₁+ℓ)}，公开可任意选取 | (L4) m₁*=m₁+m₂ 参数化，选 s₂ | **通用接口支持**：任意 E_i 是原文能力；扩展维度实例化 `[参数实例化待核查]`（用户 LB-05S 复核） |
| E_{s₂} 作为选出 s₂ 的对象 | 原文无此名字，但通用 E_i 接口覆盖（L1681/L1774） | (L4) s₂ 像 x 一样追加进 Ajtai 消息（L5734） | **参数化实例**（非新原语）：两步参数化见 §1.4；Thm5.3 参数重推 `[待核查]` |
| 二值余量 x | L1719/1759/1700/L1708 Lemma 5.2 | (L5) x 在 Ajtai 部分，Eq.58+Fig9 约束 | **原文支持** |
| σ 配对 / 挑战集 | L141 σ(c)=c；L168 非自同构才需双承诺 | s₂∈R_F，σ 为 base-ring 自同构 | **原文支持**（避开 R_K ν 陷阱） |
| 参数界重推 | L1827 Thm5.3；Prop5.1 | 消息维度扩大 → B^{(e)}, q 条件须重推 | **未做** `[待核查]` |

`[推导]` **判定**：修正变量定义后，B2 在结构层命中 LNP22 的 Eq.(6) 线性接口、Ajtai 追加 x、s/x 分离、二值余量、σ 配对五个接口；E_{s₂} 属**通用 E_i 接口的参数化实例**（用户复核口径）；剩余为**参数重推**（扩展维度的 Fig5/Fig8 实例化、Thm5.3 参数），属安全证明阶段任务。但必须明确：**"写在同一 statement 中"不等于"已证明对该联结关系知识可靠"**——L1–L5 的联合提取器存在性与可靠性、三层 binding 归约在 `docs/20`/`docs/21` 给出结构骨架，**形式化仍未闭合**（见 LB-05T 决策）。

### 2.4 与用户 sketch / 作者 Remark 4.8 的关系

`[论文事实: LBF L3130–3139]` 作者 sketch：exact 证书 "reaches s₂ … through the anchoring instantiation of §3.2.1.1"，bound 维度 (m₁+m₂)d。
`[推导]` B2 走"把 s₂ 提升为消息 + Eq.6 线性接口统一"，不是 anchoring 的标量替换（LBF L1645–1652 "no commitment is recomputed"），故是**独立于作者 sketch 的候选路线**，不声称实现 Remark 4.8。

---

## 3. 任务 C：重算 Extended-MLWE 与 MSIS

### 3.1 辅助承诺 hiding：不能用 `m₂'>n'`

`[论文事实: LNP L474–476, PDF L1499–1510]` ABDLOP hiding 的堆叠矩阵是 **[A₂;B]（n+ℓ 行）**，不是 n 行：
> "The hiding property … follows from the MLWE problem when s₂ … such that ([A₂;B], [A₂;B]·s₂) is indistinguishable from uniform."

`[论文事实: LNP L763, PDF L2438]` commit-and-prove 层：
```
Extended-MLWE_{n+ℓ+1, m₂−n−ℓ−1, χ, C, s₂}   (C=[A₂;B;b^T], n+ℓ+1 行)
```
`[论文事实: PDF L3984 Thm4.5, L1625 Prop5.1, PDF L6277 Thm5.3]` 随协议层数递增的维度条件：
```
m₂ > n+ℓ                         (承诺层)
m₂ > n+ℓ+1                       (Fig6 commit-and-prove, +1 来自 b^T / Rej2 泄露 1 bit)
m₂ > n+ℓ+λ+1                     (Thm4.5)
m₂ > n+ℓ+λ+256/d+2               (Prop5.1, exact 层)
m₂ > n+ℓ+λ+2(256/d+1)            (Thm5.3, 末项符号 PDF 渲染歧义 [待核查])
```
`[推导]` **修正 docs/17 §1.3 与 docs/18 的简化**：辅助承诺 hiding 条件不能写 `m₂'>n'`，应按 B2 完整 commit-and-prove transcript 对应层级，至少 `m₂'>n'+ℓ'`（承诺层），加入 masking 与 exact 层后更高。n',ℓ',m₂',λ' 未选，`[待核查]` 具体数值不补造。

### 3.2 辅助承诺 binding

`[推导]` 若 (s_A,x,r) 与 (s'_A,x',r') 同为 t̂_A,t̂_B 的短 opening：
```
Â_s Δs₁ + Â_s' Δs₂ + Â_x Δx + Â_r Δr = 0,    B̂ Δr + Δm_A = 0
```
m_A 是无限制消息，Δm_A 吸收 B̂Δr → 第二式对 r 无独立短约束；binding 约束落在 short 部分 (Δs_A,Δx,Δr)∈ker[Â_s Â_x Â_r]，需 `MSIS_{n', m₁+m₂+υe+m₂', B}` 成立，B 按 §3.5 的 c̄-scaled 界取值（非 2β）。docs/18 §3.3(b) 的 B1 binding 分析（m₂+υe+m₂' 列）对应 B1；B2 的列数为 m₁+m₂+υe+m₂'。

### 3.3 原始 LBF commitment binding

`[推导]` 若 (s₁,s₂,m)、(s'₁,s'₂,m') 同为 t_A,t_B 的 opening：
```
A₁ Δs₁ + A₂ Δs₂ = 0,        B Δs₂ + Δm = 0
```
m 吸收 BΔs₂，binding 只来自第一式，需 `MSIS_{n, m₁+m₂, B}` 成立（B 按 c̄-scaled 界，见 §3.5）。这与 docs/18 §3.3(a) 一致。

### 3.4 联合 PoK 的知识可靠性（B2 待证项）

`[推导]` L1–L5 写在同一 statement 中，只保证"若存在单一 witness W 满足全部关系，则 exact 界约束该 witness 的 s₂"。**这不等于**已证明"对该联结关系存在知识可靠 PoK"。须给出单一提取器 E，使对任意 accepting transcript，E 输出 W̄=(s̄₁,s̄₂,m̄,r̄,x̄) 同时满足 L1–L5，且 ‖s̄₂‖₂≤β（exact，无 c̄）。此项 `[未证]`，是进入正式安全证明的首要任务；B1 的两个独立证明不满足此条（docs/18 §2.1）。

### 3.5 MSIS 差向量：c̄-scaled 提取界 vs exact 界（用户核心要求）

`[论文事实: PDF L1544–1547 / LNP L480/L507, Lemma 3.1 st.2]`
> "‖s̄_i·c̄‖ ≤ 2s_i√(2m_i d) for i=1,2"

提取界是 **‖s̄_i·c̄‖ 的界**，不是 ‖s̄_i‖ 的界。s̄_i=z̄_i/c̄，但原文只对乘积 z̄_i=s̄_i c̄ 给界；c̄=c−c' 是两次回绕的挑战差，只满足 ‖c̄‖∞≤2κ（PDF L792），**除以 c̄ 不保范数**（可除 ≠ 保界）。

`[论文事实: LNP L511–521, Eq.25–27]` binding 论证的实际做法：从 A₁s̄₁+A₂s̄₂=A₁s'₁+A₂s'₂ 出发，**乘以 c̄c̄' 清分母**，化为对短量 z̄_i c̄'−z'_i c̄（=(s̄_i−s'_i)c̄c̄'）的 MSIS 断言，其界为 `8η·s_i√(2m_i d)`（§Lemma 2.15 乘 c∈C 放大 ℓ2 范数至多 η 倍）。原文**从不**对 Δs 直接给 ‖Δs‖≤2β。

`[论文事实: PDF L1522–1524, L7340–7344 Remark6.2, L7946 fn.22]` 原文明确区分两层：
- 底层 ABDLOP PoK 只给 relaxed 提取 `A s̄ = c̄ t mod q`、c̄-scaled 界（"the norm of the extracted s̄ is noticeably larger … presence of extra multiplicand c"）；
- exact 界 ‖s‖≤β 只在叠加的 exact-norm proof（Prop5.1/§5.2 Fig9–10）中成立（"we circumvent the relaxation factor by proving exact norms"）。

`[推导]` **修正 docs/18 §3.2 的 `‖Δs_i‖≤2β_s`**：不能对所有提取 opening 直接写该式。正确区分：
1. **honest short opening**（采样界，exact）：‖s₂‖₂≤β_honest（如 m₂·d 量级）——这是诚实生成者满足的界，非提取器保证。
2. **协议提取 relaxed opening**：‖c̄·s̄_i‖≤2s_i√(2m_i d)；MSIS 差向量界应取 c̄-scaled 形式 `8η·s_i√(2m_i d)`，不是 2β。
3. **exact 覆盖的 s₂**：在 B2 中 s₂ 由 (L4)(L5) 的 exact 证明覆盖，**单个提取 opening** 的界 ‖s̄₂‖₂≤β **无 c̄**（这是 exact 相对 relaxed 的核心收益）；但未覆盖的 s₁、r 仍走 relaxed、带 c̄。

`[推导 · ★LB-05T 收紧]` **纠正上一段可能的误读**：`‖s̄₂‖≤β`（无 c̄）只描述**单个提取 opening**，**不能**直接当作两个 opening 差的 MSIS 界。binding 比较仍处理 `(s̄₂−s̄′₂)c̄c̄′`，其界为 `‖(s̄₂−s̄′₂)c̄c̄′‖ ≤ 2β‖M_c̄M_c̄′‖_{2→2} ≤ 8η²β`（用原文部件 `‖M_c̄‖≤2η`），**带放大**。原文 binding 恒用 c̄c̄′（Lemma 3.1 式26/27，PDF L1691–1717），exact 界在原文只覆盖消息 s、是单 opening 谓词（PDF L5653/L6588–6596）。完整混合界 `B_orig=√((8η·s₁√(2m₁d))²+(8η²β)²)` 与 exact/relaxed 路线的紧性比较见 `docs/21 §1`。

`[推导]` 因此 MSIS binding 的界 B 应区分：relaxed 分量取 c̄-scaled `8η√(…)`；exact 覆盖的 s₂ 分量取**带 c̄c̄′ 放大**的 `2β‖M_c̄M_c̄′‖`（保守 `8η²β`），**不是**裸 β。二者不能混用。**单次正确 ≠ 递归正确**：即使 s₂ 单次 exact 无 c̄，跨轮 binding 识别同一 opening 与无累积链仍未证明（docs/15 边界）。

---

## 4. 任务 D：参数与成本

### 4.1 保留的锚点

- LBF 参数：`d=128, m₂=53`；`d=64, m₂=83`（LBF L3561–3562）。
- x 每个 exact-norm 关系占 **1 个 R_q 环元素**（υe=1，装 2logβ 位，2logβ≤d）。
- 辅助承诺份数 **`(k+2)t`**（Protocol 8 Step5: (k+1)t + Protocol 7 Step17: t；保持盐不相交性，docs/18 §4.1/§4.6）。

### 4.2 三类维度必须区分（本轮新增区分）

| 类别 | 含义 | B2 表达式 |
|---|---|---|
| **扩展 Ajtai 消息维度** | 辅助承诺 Ajtai 部分承诺的消息长度（witness 侧） | m₁+m₂+υe |
| **实际 exact-norm 向量维度** | s_LNP 的长度（**不含 x**） | 2(m₁+m₂+ℓ) |
| **公开矩阵元素数** | 支撑扩展所需的公共承诺矩阵（公钥侧） | Â₁∈R^{n'×(m₁+m₂+υe)}、Â_r∈R^{n'×m₂'}、R₁∈R^{(n+ℓ)×(m₁+m₂)} |

`[推导]` 修正 docs/18 §4.2/§4.4：此前把 x 计入 exact 向量（2(m₁+m₂+υe+ℓ')），现修正为 exact 向量 **2(m₁+m₂+ℓ)**（不含 υe），但**辅助承诺 Ajtai 消息仍为 m₁+m₂+υe**（x 物理上仍占一列）。承诺布局未减少，只是"承诺中追加的变量"与"范数关系使用的变量"分开。

### 4.3 维度代入（d=64/128）

| 项 | d=128 (m₂=53, n+ℓ=27) | d=64 (m₂=83, n+ℓ=35) |
|---|---|---|
| 辅助 Ajtai 消息维度 (含 x) | m₁+54 | m₁+84 |
| 实际 exact 向量维度 s_LNP | 2(m₁+53+ℓ) | 2(m₁+83+ℓ) |
| E_{s₂} 维度 | R_q^{53×2(m₁+53+ℓ)} | R_q^{83×2(m₁+83+ℓ)} |
| x 每 exact 关系新增 Z_q 系数 | 128 | 64 |
| 辅助承诺份数 | (k+2)t | (k+2)t |
| x 打包位数 | 2logβ≈13 ≪ 128 | 2logβ≈13 ≪ 64 |

### 4.4 无法数字化的项 `[待核查]`

- n'（辅助承诺行数）、m₂'（新盐维度）、ℓ'（BDLOP 消息长度）、λ'（附加承诺数）、k、t 未选 → 公钥矩阵元素总数、承诺大小、PoK 转录大小不能给具体数。
- Thm5.3 参数（B^{(e)}, c^{(e)}, k_bin, q）按新维度 2(m₁+m₂+ℓ) 未重推 → proof size 不虚报。
- Extended-MLWE 层级的 m₂' 下界（`>n'+ℓ'` 起，协议层更高）无法给具体值。

---

## 5. 任务 E：最终决策

**选择 B2-READY**：关系、变量角色、PoK 接口（结构层）与必要参数条件（形式层）已明确，可进入更深入的安全证明。**这不是安全性结论，不代表递归无 c̄ 累积，不代表已实例化/已实现。**

| 判据 | 本轮状态 |
|---|---|
| 变量角色（s 与 x 分离、无 σ(x)） | ✓ 已修正，与 PDF L5653/L6179/L1772 一致（§1） |
| B2 联合关系（Eq.6 线性 + Eq.58/59 + Eq.53） | ✓ 已写出 L1–L5，逐接口核查命中原文（§2） |
| PoK 接口 | 结构层 ✓（Eq.6 线性、Ajtai 追加 x、任意 E_i、σ 配对、二值余量）；E_{s₂} 扩展维度为 `[设计外推]`（§2.3） |
| 必要参数条件 | 形式层 ✓（Extended-MLWE 层级、MSIS c̄-scaled 界、Thm5.3 q 条件）；具体值 `[待核查]`（§3–§4） |

`[推导]` **为何不是 B2-HOLD**：B2-HOLD 的定义是"仍存在无法澄清的协议接口或数学障碍"。本轮修正后，用户发现的核心障碍（s/x 变量定义错误）已闭合；剩余两项（E_{s₂} 扩展维度、Thm5.3 参数）是**可明确陈述、可在安全证明阶段处理的待办**，不是"无法澄清的矛盾"。且 L92 明确证明大小与矩阵尺寸无关，降低了扩展 R₁ 列数的结构性风险。故选 READY 而非 HOLD。

`[推导]` **进入安全证明前须完成的清单**（READY 的准入条件，未完成不得宣称 B2 可行；★LB-05T 更新各项状态）：
1. 给出对联结关系 L1–L5 的**单一联合提取器**及知识可靠性证明（§3.4）——**LB-05T 已给结构继承论证（docs/20 §1：Thm5.3 参数化实例），形式化未闭合**。
2. 验证 E_{s₂} 的 2(m₁+m₂+ℓ) 扩展维度能被 Fig5/Fig8 多线性接口原样实例化（§1.4/§2.3）——**定性为通用 E_i 接口支持、参数实例化待核查（用户 LB-05S 复核）**。
3. 按新维度重推 Thm5.3 参数与本阶段 Extended-MLWE 层级的具体 m₂' 下界（§3.1/§4.4）——**未做**。
4. 区分 honest / relaxed / exact 三种界，在 binding 论证中使用 c̄-scaled 界（§3.5），不得用未证的 ‖Δs‖≤2β——**LB-05T 已给混合界与三层 binding 骨架（docs/21），形式化未闭合**。

任一清单项发现结构性矛盾（如联合 PoK 不可构造、扩展维度接口不兼容）→ 退回 B2-HOLD。LB-05T 未发现此类矛盾，但三项形式化（联合提取器、三层 binding、参数重推）仍未完成，故未宣称 B2 已通过安全证明。

---

## 6. 待核查与边界

- `[待核查 · 设计外推]` E_{s₂} 与 2(m₁+m₂+ℓ) 维度：LNP22 原文无 E_{s₂}、s₂ 只作 randomness（PDF L6179/L1772/L1774）；B2 的两步推广须在安全证明阶段验证。
- `[待核查]` Thm5.3 末项符号（PDF L6277 渲染歧义）；Prop5.1 参数按新维度重推；Extended-MLWE 具体 m₂' 下界。
- `[推导]` 本文所有"可行/适合/READY"均指**候选构造可进入安全证明**，不等于已验证、已实例化、已实现、已证明安全。
- 不把 x 或 σ(x) 放进 exact 向量；不写 MSIS 无条件唯一；不用未证的 ‖Δs‖≤2β；不把 relaxed 写成 exact；不把单次 s₂ exact 等同递归无 c̄ 累积；不做 Decider/LaZer。
