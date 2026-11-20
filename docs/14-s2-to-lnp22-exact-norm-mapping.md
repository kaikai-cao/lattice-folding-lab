# 14 · 从 ABDLOP s₂ 到 LNP22 Exact-Norm Statement 的映射分析

> LB-04 · 任务 A/B/C。日期：2026-11-20。
> 核心问题：能否把 LBF 的 `s₂` 写成 LNP22 exact-ℓ₂ 可直接处理的、已承诺消息向量的线性函数 `s₂ = E x − v`？用户提出的候选路线是找公开 `P` 使 `PC=I`，`C=[A₂;B]`。
> **结论先行：候选路线 `PC=I` 在维度与 hiding 两个层面都不成立；真实可行的替代是 LNP22 的标准做法——用单独的 ABDLOP 把目标向量放进消息槽再证 exact norm。但这一步在 LBF 中尚未实例化，且"新承诺的 s₂"与"原承诺的 s₂"是否同一仍是未闭合缺口。**
>
> 来源标注：ePrint 官方 PDF `eprint.iacr.org/2022/284.pdf` 本轮仍被 Cloudflare 阻挡（WebFetch 仅返回 "Just a moment..."），本机缺 `fitz`、截图渲染命令被安全策略拦截。故本文所有原文引用来自 **ePrint 镜像 PDF** `C:/Users/dell/AppData/Local/Temp/lb02/lnp22_asia.pdf` 经 `workbuddy-pdf` 提取的 `md_lnp22_asia/content.md`（3453 行，行号记 `LNP L####`），以及 LBF 全文镜像 `C:/Users/dell/AppData/Local/Temp/lbf/paper_mirror.txt`（行号记 `LBF L####`）。**镜像不是已核验的官方 PDF 版本**；关键数值用多处独立参数表交叉验证，但不冒充官方 PDF 逐页核对。

---

## 1. 任务 A：原文复核（维度定义）

### 1.1 ABDLOP 承诺的精确维度

`[论文事实: LNP22 Fig.4, LNP L495; LBF §2.5.2, LBF L1082–1087]`

```
A₁ ∈ R_q^{n×m₁}      (LBF 记 n 为 κ)
A₂ ∈ R_q^{n×m₂}
B  ∈ R_q^{ℓ×m₂}
s₁ ∈ R_q^{m₁},  m ∈ R_q^{ℓ},  s₂ ∈ R_q^{m₂}
(t_A, t_B) = (A₁s₁ + A₂s₂,  Bs₂ + m) ∈ R_q^{n+ℓ}
```

LBF 把行数记为 `κ`（Ajtai 承诺矩阵行数），`ℓ = κ′` 为要承诺的无限制环元素个数（LBF L1082–1087）。为与用户候选式一致，下文用 `n ≡ κ`。

### 1.2 候选矩阵 C 与 J 的维度

用户候选式：`x=[s₁;m] ∈ R_q^{m₁+ℓ}`，`C=[A₂;B]`，`J=[A₁ 0; 0 I_ℓ]`，则

```
[t_A; t_B] − J x = [A₁s₁+A₂s₂ − A₁s₁ ;  Bs₂+m − m] = [A₂s₂ ; Bs₂] = C s₂   ✓   (代数恒等式成立)
```

`[论文事实 + 推导]` 代数恒等式本身正确（就是 ABDLOP 定义）。维度：

```
C = [A₂ ; B] ∈ R_q^{(n+ℓ)×m₂}        （行数 n+ℓ, 列数 m₂）
J = [A₁ 0 ; 0 I_ℓ] ∈ R_q^{(n+ℓ)×(m₁+ℓ)}
```

### 1.3 决定性事实：m₂ > n+ℓ

`[论文事实]` 三处独立证据表明 `m₂` 严格大于 `n+ℓ`：

1. **Extended-MLWE 参数**：LNP22 的 hiding/模拟依赖 `Extended-MLWE^{n+ℓ+·, m₂−n−ℓ−·}`（LNP L730、L1141、L1839；LBF L1326、L1665）。第二参数 `m₂−n−ℓ−(·)` 必须为正，否则问题无意义 → **`m₂ > n+ℓ`**。
2. **LNP22 具体参数表**（LNP L2015）：`n=9, ℓ=0, m₂=25`（group signature 外的实例化）；另一组（LNP L2100）`n=9, ℓ=0, m₂=29`；群签名（LNP L2266）`n=12, ℓ=0, m₂=41`。均 `m₂ ≫ n+ℓ`。
3. **LBF 具体参数表 Table 2**（LBF L3555–3572）：
   - d=128：`κcom = n+ℓ = 27`（L3561 `κ,κ′=ℓ,κcom = 11,16,27`，即 n=11,ℓ=16,κcom=27），`m₂=53`（L3562）。`53 > 27`。
   - d=64：`n+ℓ = 35`（n=19,ℓ=16），`m₂=83`。`83 > 35`。

`[推导]` 这不是参数巧合，而是 **hiding 的数学要求**：ABDLOP 的 hiding 来自 `(A₂;B)s₂` 与均匀不可区分（Extended-MLWE，LNP L474–478），只有当 `m₂ > n+ℓ`（s₂ 的自由度超过公开像的维度）时才可能；若 `m₂ ≤ n+ℓ`，`Cs₂` 一般唯一确定 s₂，hiding 立即失效。

---

## 2. 任务 B：PC=I 左逆存在性判定

### 2.1 域/环上左逆存在的必要条件

`[推导]` 对 `C ∈ R_q^{(n+ℓ)×m₂}`，存在 `P ∈ R_q^{m₂×(n+ℓ)}` 使 `PC = I_{m₂}` 的**必要条件**（无论 `R_q` 是域还是环）是：

- `C` 必须是**单射**（左可逆 ⇒ 作为 `R_q`-模同态 `R_q^{m₂} → R_q^{n+ℓ}` 是单射，因为 `PC=I` 给出左逆）；
- 在域上等价于满列秩 `rank(C)=m₂`，要求 `m₂ ≤ n+ℓ`；
- 在环 `R_q=Z_q[X]/(X^d+1)` 上更强：左逆存在要求 `C` 的列构成一个自由直和因子，特别是需要 `m₂ ≤ n+ℓ`（列数不超过行数；否则 `\bigwedge^{m₂}C` 无定义，因为需要 m₂ 行）。

### 2.2 判定：不存在

`[推导]` 由 §1.3，`m₂ > n+ℓ` 在所有相关参数下成立：

| 参数集 | n+ℓ (行数) | m₂ (列数) | C 形状 | 满列秩? | PC=I? |
|---|---|---|---|---|---|
| LBF d=128 | 27 | 53 | 27×53 宽矩阵 | 否（≤27<53） | **不存在** |
| LBF d=64 | 35 | 83 | 35×83 宽矩阵 | 否（≤35<83） | **不存在** |
| LNP group sig. | 12 | 41 | 12×41 宽矩阵 | 否 | **不存在** |
| LNP ver. enc. | 9 | 25 | 9×25 宽矩阵 | 否 | **不存在** |

**结论 B1**：`C=[A₂;B]` 是宽矩阵（列多于行），`ker(C)` 非平凡（维数 ≥ m₂−(n+ℓ)>0），`C` 不是单射，**不存在公开左逆 P 使 PC=I**。用户候选式 `PC=I ⇒ s₂ = P[t_A;t_B]−PJx = Ex−v` 的起点不成立。

### 2.3 这是 hiding 的直接后果，不是参数不幸

`[推导]` 更重要的结构性结论：**`PC=I` 不存在恰恰是 ABDLOP hiding 的必要条件**。若存在公开可算的 P 使 `s₂ = P[t_A;t_B] − PJx`，则任何持有公开承诺 `(t_A,t_B)` 与消息 x 的验证者都能线性解出随机盐 s₂——这直接摧毁 Extended-MLWE hiding（攻击者无需区分 `Cs₂` 与均匀：给定承诺即可反解）。因此"从承诺线性恢复完整 s₂"在 hiding 的承诺方案中**原则上不可能**，与具体矩阵无关。这也是 §B4 所问"是否存在基于 anchoring 的替代映射"的根本约束：**任何能从公开承诺恢复完整 s₂ 的映射都违反 hiding**。

### 2.4 部分线性像是否可行？

`[推导]` 若放弃"完整 s₂"，只恢复线性像 `L·s₂`（L 的行数 ≤ n+ℓ），则只要 `L` 的行落在 `C` 的行空间内就能从 `Cs₂ = [t_A;t_B]−Jx` 线性解出。典型例子：
- `A₂ s₂ = t_A − A₁s₁`：可解（A₂ 有 n 行，但 n<m₂，欠定，仍不可唯一恢复 s₂，只能恢复 n 维线性像）；
- anchoring 的 `ct(Σ wₙ (Bs₂)_{ι(n)})`：是 `Bs₂` 的**标量常数项加权和**（LBF L2701–2707），一个 K 元素。

`[论文事实: LBF L2701–2707]` anchoring call certifies `u★ = ζ·S_{2,p} = ct(Σₙ wₙ Bs₂⁽ⁿ⁾)`，经 Lemma 3.10 转为消息侧 `ct(Σwₙ m_{ι(n)})=ct(u)`。这是一个**标量线性泛函**，不是一个能恢复 m₂ 维 s₂ 的方程组。

**结论 B2**：即使退而求其次，anchoring 也只覆盖 `Bs₂` 的标量常数项聚合，**不足以恢复完整 s₂，更不足以给出 ‖s₂‖ 的 exact 界**。

### 2.5 R_K → R_F component-wise 展开后是否成立？

`[推导]` 不变。component-wise 展开（LBF §3.3.1，L1719–1743）把 `R_K` 元素 `a+bY` 映到 `(a,b)∈R_F²`，把 `C ∈ R_K^{(n+ℓ)×m₂}` 映到 `ψ(C) ∈ R_F^{2(n+ℓ)×2m₂}`（rank-doubling embedding，LBF 式 3.2）。展开后：
- 行数 `2(n+ℓ)`，列数 `2m₂`，仍是宽矩阵（`2m₂ > 2(n+ℓ)`）；
- `ker(ψ(C))` 仍非平凡（维数 ≥ 2(m₂−n−ℓ)）；
- `P'C'=I_{2m₂}` 同样不存在。
且 LBF §3.3.4（L1841–1855）明确：component-wise 的 exact-ℓ₂ 翻译只解决"**已知消息向量**的范数证明"（对 (a,b) 分别证 `‖a‖²/‖b‖²`），**不解决"从承诺恢复 s₂"**——后者是承诺结构问题，与域展开无关。

---

## 3. 任务 C：作者 sketch 与实际映射是否一致

### 3.1 LNP22 对 randomness 证 exact 范数的真实机制

`[论文事实: LBF §2.1, LBF L511–515]` **更关键：LBF 明确采用与 LNP22 相反的承诺布局约定。** 逐字：`Every ABDLOP commitment issued here carries its message in the BDLOP slot, i.e. ℓ⁽ⁿ⁾ ≥ 1 and t_B = Bs₂ + m⁽ⁿ⁾, never in the Ajtai slot s₁; both s₁ and s₂ are salts. We stress this because [LNP22]'s own instantiations … take ℓ = 0 and place the message in the Ajtai part instead.` 因此：
- LBF 中消息 m 固定在 BDLOP 槽，s₁、s₂ **都是盐**；
- LNP22 的标准 exact-ℓ₂ 配方（把目标向量放 Ajtai 消息槽，LNP L126）与 LBF 布局**直接冲突**；
- 要把 s₂ 变成可 exact-证明的消息，必须**改变 LBF 的核心承诺约定**（新增一个 ℓ≥1 把 s₂ 当 message 的承诺），这不是"调用现成接口"，而是新增承诺结构。LBF 全文未提出这一步（Explore-1 全文检索确认"未见"）。

`[论文事实]` 在此前提下，LNP22 从不直接对 ABDLOP 的 randomness 槽 s₂ 证 exact-ℓ₂。其两个关键应用都采用"**把目标向量放进消息槽额外承诺**"：

- **一般配方**（LNP L126）：`first commit to s as part of the s1 part of (5)` ——将要证范数的向量 s 放进 Ajtai 消息部分。
- **群签名**（LNP L185）：`the user commits to s1, s2, r, μ in the "Ajtai" part of the ABDLOP commitment (5). He then proves that the norms of s1, s2, r are small` ——这里 s₂（原本是 randomness 的符号）被**作为消息承诺到 Ajtai 槽**后再证范数。
- **可验证加密**（LNP L2081, Remark 6.2）：`since we commit to r and m using a separate ABDLOP commitment, we circumvent the relaxation factor by proving exact norms on r and m` ——**用单独的 ABDLOP 承诺 r、m 作为消息，从而绕开 relaxation factor c̄**。

`[推导]` 这三条铁证说明：LNP22 处理"对某随机向量证紧范数"的**唯一展示机制**是把它提升为消息（通常在额外承诺里），而非从 randomness 槽的承诺线性恢复。这与 §2.3 的结构性结论一致。

### 3.2 LBF Remark 4.8 sketch 的定位

`[论文事实: LBF L3130–3139]` 作者说 exact ℓ₂ proof "reaches the BDLOP randomness s₂ ... through the anchoring instantiation of §3.2.1.1"，并给两个 append bound：`k t(B̃−1)√((m₁+m₂)d)`（Protocol 8 Step 5）与 `(B̃−1)t√((m₁+m₂)d)`（Protocol 7 Step 17），称 "The extracted salts would then satisfy their bounds with no factor c̄, binding of Commit would identify the certified opening at round r with the one the extractor of round r+1 recovers, and nothing would accumulate."

`[推导]` 结合 §3.1 与 §3.1 的 LBF 相反约定，sketch 的**唯一原理可行**解释是：
1. 对 fresh salt `s_{l,i,j}`（prover 自己采样、知道它），**新增一个 ℓ≥1 的 ABDLOP 把 s₂ 作为消息承诺**（借鉴 LNP22 群签名/VE 做法，但违背 LBF"消息永在 BDLOP 槽、s₂ 永为盐"的约定），对这个新承诺用 §3.3.4 的 component-wise exact-ℓ₂ 证 `‖s₂‖₂≤β`，无 c̄；
2. 用 anchoring（Lemma 3.10 的标量约束）把这个新承诺的 s₂ 与原承诺 `Commit(y,s₁,s₂)` 中的 s₂ 关联——这是 sketch 中 "through anchoring" 的含义。

`[论文事实 + 推导]` 但 **Remark 4.8 的 "it" 的精确作用对象只能从 bound 反推**：append 的两处 bound 是 `kt(B̃−1)√((m₁+m₂)d)` 与 `(B̃−1)t√((m₁+m₂)d)`，维度因子是 `(m₁+m₂)`（消息+盐两槽），作用于 Protocol 8 Step 5 的 Π_many 与 Protocol 7 Step 17 的 Π_many——这两处都是**消息恒等式 + 盐的 relaxed 界**（L2892、L2775–2777）。原文从未写出一个以 "‖s₂‖₂ ≤ β" 为结论的定理，也从未说明新增消息槽承诺。故作者 sketch 的"it"最保守解读是：**对已承诺消息（含 s₂ 的标量锚定）追加 exact-ℓ₂ 检查**，而非建立完整的 ‖s₂‖₂ 紧界定理。用户要求的"sketch 与实际映射是否一致"的答案：**不一致**——sketch 只声称"reaches s₂"，但没有给出、也不足以给出完整 s₂ 的 exact 范数映射。

### 3.3 未闭合缺口（关键）

`[推导]` 但 §2.4 已证明：anchoring 只给 `Bs₂` 的**标量常数项聚合**绑定（`ct(ΣwₙBs₂)` 一个 K 元素），**不足以把 m₂ 维的新承诺 s₂ 与原承诺 s₂ 识别为同一向量**。要在两个承诺间识别同一 s₂，需要 m₂ 个线性无关约束（或足以确定 s₂ 的 binding 论证），而现有 anchoring 带宽不够。因此：

- **候选式 PC=I**：失败（维度 + hiding，§2.2/2.3）；
- **anchoring 替代映射**：只覆盖标量线性像，不足以绑定完整 s₂（§2.4）；
- **LNP22 标准做法（额外承诺消息槽）**：原理可行且是 LNP22 已展示的，但在 LBF 中**未实例化**，且与原承诺的 s₂ 一致性绑定缺 a m₂-维约束。

`[推导]` 所以用户警告的两点都成立：
- "不能因代数形式看起来吻合就认定 PC=I 路线与 anchoring instantiation 等价"——正确，二者不等价：PC=I 要恢复完整 s₂（不可能），anchoring 只给标量泛函。
- "不能把 Bs₂ 的范数界直接当 s₂ 的范数界"——正确：`ker(B)` 非平凡（B 是 ℓ×m₂，ℓ=16<m₂=53），`‖Bs₂‖≤β` 完全不约束 `ker(B)` 方向上的 s₂ 分量。

### 3.4 判定

**候选映射在数学上不成立（PC=I）；基于 anchoring 的部分映射只覆盖标量线性像；可行的替代（额外消息槽承诺）在 LBF 未实例化且缺完整 s₂ 一致性绑定。** 这对应 LB-04 决策 **C（目前无法建立所需映射，方案 B 退回 HOLD）**，但需注明：不是"路线被证伪"，而是"现有 LBF 组件不足以建立映射，需新增承诺结构"，故可视为 C 中带建设性的结论。详见 `decisions/LB-04-decision.md`。

---

## 4. 待核查

- `[待核查]` 官方 PDF 页面截图未能获取；维度结论来自镜像 PDF 提取文本，已用 4 处独立参数表交叉验证（§1.3）。若后续取得官方 PDF，应复核 LNP L495/L730/L2015 与 LBF L3561–3562。
- `[待核查]` LBF "通过 anchoring 触及 s₂"的作者意图，是否隐含了"对 s₂ 额外承诺到消息槽"这一步——Remark 4.8 未明说，本文按 LNP22 标准做法推测（`[推导]`）。Explore-1 正在核查 LBF 全文是否有更明确表述。
- `[待核查]` component-wise 展开下 `ψ(C)` 的左逆判定基于 rank-doubling embedding 的一般性质，未逐元素验算。
