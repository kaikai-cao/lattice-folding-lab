# 16 · 路线 A：不新增承诺，直接对 ABDLOP randomness s₂ 证 exact-ℓ₂

> LB-05 · 任务 A / 任务 C（路线 A 部分）/ 任务 D（骨架）。日期：2026-11-20。
> 核心问题：能否**不新增承诺**、只扩展现有 ABDLOP proof，直接在 original randomness 位置证明 `‖s₂‖₂ ≤ β`，并让该界约束原始 opening？
> 结论先行：**不能。** LNP22 §5.2 的 exact-ℓ₂ 接口在三个层面拒绝"就地作用于 s₂"：(i) 它只作用于**已承诺消息** `s=(s₁,σ(s₁),m,σ(m))`，s₂ 在现有承诺中是 randomness、不在消息向量内；(ii) 它要求目标向量带**自同构 σ 配对**，而 s₂ 作为随机盐没有这个结构，强行套用会证明错误的量（component-wise 已明确避开 `‖a‖²+ν‖b‖²`）；(iii) 唯一能"不新增承诺"的机制是 anchoring 的标量替换，但它只保留 `Bs₂` 的常数项线性泛函，无法恢复 m₂ 维 s₂。故路线 A 需要改变承诺布局（把 s₂ 搬进消息槽），而那已不是"不新增承诺"。
> 一手来源：LNP22 镜像 `C:/Users/dell/AppData/Local/Temp/lb02/md_lnp22_asia/content.md`（`LNP L####`）；LBF 全文镜像 `C:/Users/dell/AppData/Local/Temp/lbf/paper_mirror.txt`（`LBF L####`）。镜像来源限制与字形瑕疵见 `docs/14` 开头；本阶段官方 PDF 仍被 Cloudflare 阻挡，所有引用为镜像提取文本，**非官方 PDF 逐页核对**。

---

## 0. 问题边界与记号

用户任务包路线 A 原文：*"不新增承诺，直接扩展现有 ABDLOP proof，直接证明 ‖s₂‖₂≤β。"* 本节严格按此边界，只评估**保持 LBF 现有承诺布局**（消息在 BDLOP 槽、`ℓ≥1`、s₁/s₂ 均为盐，LBF L508–515）的就地扩展。任何需要新增承诺或改变承诺矩阵的构造，归入 `docs/17`（路线 B）并明确不算路线 A 成立。

现有 ABDLOP opening（LBF L1082–1087 / LNP L495）：

```
A₁ ∈ R_q^{n×m₁},  A₂ ∈ R_q^{n×m₂},  B ∈ R_q^{ℓ×m₂}
t_A = A₁s₁ + A₂s₂
t_B = Bs₂ + m
s = (s₁, s₂) 盐,  m 消息（BDLOP 槽）
```

---

## 1. 任务 A 四问逐答

### 问题 1：能否在 original randomness 位置直接证明 `‖s₂‖₂ ≤ β`？

**判定：否（在现有承诺布局下）。**

`[论文事实: LNP L1679, L1690]` §5.2 exact-ℓ₂ 协议的输入被明确定义为"**承诺消息**的二次关系"：

> "we describe a general protocol to prove various quadratic relations on `s = (s₁, m, σ(s₁), σ(m))`, where `(s₁, m)` is **the message of an ABDLOP commitment** … among the relations … is an exact norm proof `‖s‖ ≤ β`, where β is tight."（LNP L1679）

> "includes the knowledge of a vector `s = (s₁, σ(s₁), m, σ(m)) ∈ R^{2m₁} × R^{2ℓ}` such that … `‖E_i s − v_i‖ ≤ β_i^{(eq)}`"（LNP L1690，Eq.53）

`[推导]` exact 向量 `s` 的四个分量全部来自**消息** `s₁`（Ajtai 消息）与 `m`（BDLOP 消息）及其 σ 像；**没有 s₂ 的位置**。而 LBF 中 s₂ 是 randomness：它进入 `t_A` 的 `A₂s₂` 项与 `t_B` 的 `Bs₂` 项，从不进入 `s=(s₁,m)`。Remark 4.8 原文确认这一点：

> "which reaches the BDLOP randomness s₂ (**untouched by [LNP22]'s norm machinery, which targets the committed part (s₁, m)**) through the anchoring instantiation of §3.2.1.1."（LBF L3131–3133）

因此"在 original randomness 位置直接证 `‖s₂‖₂≤β`"**不是**调用 §5.2 现成接口能做到的——该接口的被证对象不包含 randomness。

### 问题 2：能否用 LNP22 的内积/多项式乘积对隐藏的 s₂ 建立自内积证明？

**判定：原理上有二次工具，但因缺 σ 配对与缺承诺位置而无法就地应用；强行套用会证错量。**

`[论文事实: LNP L126, L130, L134]` LNP22 的自内积机制依赖两个条件：

1. **承诺位置**：目标 s 必须先作为消息承诺在 Ajtai 槽——"first commit to s as part of the s₁ part of (5) (i.e. in the 'Ajtai part' of the ABDLOP scheme)"（LNP L126）；伴随的二进制余数向量 b 也追加到 Ajtai 槽（LNP L1719）。
2. **σ 配对**：`‖s‖²` 是 `∑ᵢ sᵢ(X^{−1})·sᵢ(X)` 的常数项，验证者用 `σ(z)·z − σ(c)cβ²` 检验（LNP L130）；可靠性论证要求挑战 `c` 取自 σ 的不动集合 `S^σ_κ`（LNP L141, L451–455）。

`[论文事实: LNP L168]` 最关键——论文自己说明了**没有自同构时**的唯一出路：

> "If g is **not an automorphism**, then proving knowledge of `‖s‖² = ǧ(s)·s` would **require the prover to commit to both s and g(s), and then also prove the linear relationship between the commitments of s and g(s)**. Opening two commitments instead of one will increase the proof size …"（LNP L168）

`[推导]` 对 LBF 的 s₂：它是 `R_F^{m₂}` 中的随机盐，LBF 全文没有为 s₂ 构造 σ(s₂) 配对（s₂ 走 relaxed 路径，LBF L1315）。若强行把 K 级自同构恒等式套到 component-wise 的 `x=a+bY`，得到的是 `‖a‖²+ν‖b‖²`，而 LBF 要的是 `‖a‖²+‖b‖²`，二者因 ν 为非剩余而不同——LBF §3.3.4 明确警告"proves the wrong quantity and must be avoided"（LBF L1841–1847）。因此：

- 有 σ 配对的消息向量：`‖s‖²` 自内积证明可行（LNP 现成）；
- 无 σ 配对的 s₂：要么按 LNP L168 **新增第二个承诺**（→ 路线 B），要么无法就地建立 tight 自内积；
- 这两种都不满足路线 A"不新增承诺"的边界。

### 问题 3：现有 scalar anchoring 是否足以把 exact 界约束到原始 opening？

**判定：否。anchoring 是标量常数项替换，不是 s₂ 的恒等识别。**

`[论文事实: LBF L1537–1554, L1645–1652, L2701–2714]` anchoring 的技术核心是 Lemma 3.10 的替换 `Bs₂ = t_B − m`，把 s₂ 的常数系数条件改写为消息侧条件 `ct(Σₙ wₙ m^{ι(n)}) − u = 0`，再用 Π_many 证明。关键点：

> "**so no commitment is recomputed: the parties merely repackage openings they already hold**."（LBF L1645–1652）

`[推导]` 这意味着 anchoring：
- **不产生** s₂ 的新承诺，也不对 s₂ 本体施加约束；
- 只把 `Bs₂` 的**一个标量常数项加权和** `ct(Σₙ wₙ Bs₂^{(n)})` 转成 m 的线性条件（docs/14 §2.4）；
- 其核维数巨大（`≈ m₂ − (n+ℓ)` 量级），存在大量不同 s₂ 共享同一 `ct(ΣwₙBs₂)` 值却范数迥异。

即便我们成功对"anchoring 转换后的消息侧向量"证了 exact-ℓ₂，那个界约束的是 `ct(ΣwₙBs₂)` 相关的线性像，**不是**完整 s₂ 的 `‖s₂‖₂`。用户明确警告的"不能把 Bs₂ 的范数界当 s₂ 的界"在这里直接适用：`ker(B)` 非平凡（B 为 `ℓ×m₂`，`ℓ=16<m₂=53`），`‖Bs₂‖≤β` 完全不约束 `ker(B)` 方向的 s₂ 分量。

**结论**：scalar anchoring 不能把任何 exact 界"约束回"原始 opening 的 s₂。它只能证明 s₂ 的某个标量线性泛函与消息侧一致。

### 问题 4：是否需要新协议而非简单追加 Fig10？

**判定：是。需要结构性新构造，不是简单 append。**

`[论文事实: LBF L418–419, L3466, L3894–3897]` LBF 作者三处明确把 fresh salts 上的 exact-ℓ₂ 记为"sketched but not instantiated / the main missing piece"：

> "requires the exact ℓ₂-norm certificate on the fresh salts sketched there, **which we do not instantiate**."（LBF L418–419）

Remark 4.8 的 "one would append it" 是反事实设想，其 append bound（Step5 `kt(B̃−1)√((m₁+m₂)d)`、Step17 `(B̃−1)t√((m₁+m₂)d)`，LBF L3133–3135；镜像缺根号字形 [待核查]）本身也印证：它要 certify 的对象是 `(m₁+m₂)d` 维的**整个 opening 消息+盐**，而现有 Fig10 只覆盖 `2(m₁+ℓ)` 维的消息向量——**维度都对不上**，不可能"简单追加"。

`[推导]` 具体地，路线 A 若要成立，缺的不是"调用 append"，而是至少三件新东西：
1. **s₂ 的承诺位置**：必须让 s₂ 成为某个 exact-ℓ₂ statement 的被证消息分量（现无此位置）；
2. **s₂ 的 σ 配对或双承诺**：按 LNP L168，无自同构时需第二承诺 + 线性关系证明；
3. **二进制余数 + 整数提升**：`Eq.58/59/60` 的 wraparound 防护要为新对象重做，并满足定理 5.3 的 q/界条件（LNP L1823–1827）。

这三件都是**新承诺结构或新协议**，落入路线 B 范畴。故路线 A 作为"不新增承诺的直接扩展"**不成立**。

---

## 2. 任务 D：两处 fresh salt 在路线 A 下的骨架（均受阻）

`[论文事实: LBF L2883–2893, L2775–2777]` 两处现有 PoK 均为"消息恒等式 exact（Lemma 3.6(3)，无 c̄）+ 盐 relaxed（Lemma 3.6(2)，带 c̄）"：

| 位置 | 现有 witness | s₂ 的界 | 路线 A exact 目标 | 状态 |
|---|---|---|---|---|
| Protocol 8 Step 5（输出盐） | 输入/输出承诺 opening；fresh `s_{2,i,j}` 随 `C_{i,j}=Commit(y_{i,j},s_{i,j})` | relaxed `‖c̄s̄₂‖₂≤β_rlx` | `‖s_{2,i,j}‖₂≤β` 就地 | **受阻**：s₂ 不在 Fig10 消息向量；见 §1 问题 1–4 |
| Protocol 7 Step 17（mask 盐） | mask 承诺 `y_{y,j}` 的 opening；mask 盐 `s_{2,y,j}` | relaxed，同上（LBF L3134–3135） | `‖s_{2,y,j}‖₂≤β` 就地 | **受阻**：同上 |

`[推导]` Remark 4.8 要求 append 的 bound 维度是 `(m₁+m₂)d`（消息+盐），而 Fig10 exact 向量维度是 `2(m₁+ℓ)`，二者不等——这是"append 现有 Fig10"不足的代数证据。**在路线 A 边界内，两处 exact-norm 证明目标只能记为"受阻/待定义"，不写占位公式**（沿用 docs/15 §1.3 的处理）。

---

## 3. 路线 A 判定与安全成本（任务 C 部分）

| 判据 | 路线 A（不新增承诺就地扩展） |
|---|---|
| Binding（同 s₂） | 现有 binding 只钉住**单个承诺内部** opening（LBF L1318–1320）；anchoring 不产生跨承诺同一性（LBF L1645–1652）。路线 A 无跨承诺问题，但也**无法施加 s₂ 本体约束**。 |
| Hiding | 不涉及新增承诺，hiding 不变；但也无新增信息可用于证明。 |
| Exact norm 紧界 | **不可得**：s₂ 不在 exact 向量、无 σ 配对、component-wise 证错量。 |
| Component-wise（`R_K→R_F²`） | 只能对 committed (a,b) 证（LBF L1853）；对 randomness s₂ 无接口。 |
| 新增假设 | 无（因为无新增承诺）——但这也是"无新增能力"的另一面。 |
| 成本 | 无新增承诺成本；但**目标无法达成**，成本讨论无意义。 |

**路线 A 总判定：不成立（A = false）。** 在保持现有承诺布局、不新增承诺的边界下，无法把 ‖s₂‖₂≤β 的 exact 界约束到原始 opening 的 s₂。任何可行构造都必须改变承诺结构（把 s₂ 提升为承诺消息并为之配 σ 影子或第二承诺），这已超出路线 A 定义，交由路线 B（`docs/17`）评估。

---

## 4. 待核查与边界

- `[待核查]` 官方 PDF 逐页未核对；Remark 4.8 append bound 的根号字形缺失，按镜像原样 + `docs/15` 的合理还原 `√((m₁+m₂)d)` 标注，不作确定结论。
- `[推导]` 本文所有"不可行"判定均限定在**现有承诺布局 + 不新增承诺**边界内；不排除改变布局后的构造（见 docs/17、LB-04 决策 C 的建设性含义）。
- 本文不实现 Decider、不做 LaZer 集成、不把 relaxed 界写成 exact、不把 anchoring 当作范数证明、不把单次证明等同递归证明。
