# BDLOP / ABDLOP Commitment 数学结构复原

> 状态：LB-01 / 任务 C 完成。这是本阶段最重要的技术核验之一。
> 主来源：`[LBF]` = Luca Dall'Ava, *LatticeBlindFold*, ePrint 2026/1857, 2026-09-01, §2.5/§2.5.2 (p.17–19)、§3.2 (p.21–27)、§3.3 (p.27–30)。
> 基础来源（已回查官方 ePrint 摘要页以核实书目与定位）：
> - `[BDL+16]` = Baum, Damgård, Lyubashevsky, Oechsner, Peikert, *More Efficient Commitments from Structured Lattice Assumptions*, ePrint **2016/997**（2016-10-20 received；2018-06-21 last revision；SCN 2018）。LBF 参考文献条目 p.61。
> - `[LNP22]` = Lyubashevsky, Nguyen, Plançon, *Lattice-Based Zero-Knowledge Proofs and Applications: Shorter, Simpler, and More General*, ePrint **2022/284**（2022-03-07 received；2022-08-14 last revision；CRYPTO 2022）。LBF 参考文献条目 p.61。
>
> **归属声明（重要）**：下面的 BDLOP/ABDLOP 公式均首先按 **[LBF] 对原文 recall 的形式** 记录（论文明确说 "we briefly recall here the form of such commitments"，p.18 L1080–1081；"we do not report them in full and simply recall the main results we need"，p.21 L1297–1299）。基础论文的书目、主题与安全模型已回官方摘要核实；公式编号 `(2.4)(2.5)` 属 **[LBF]** 的编号，**不是** [BDL+16]/[LNP22] 原文的编号。`[待核查]` 标注原文编号处见 §7。

---

## C1. 公式、矩阵、消息、盐、维度

### C1.1 Ajtai 承诺（对照基线）

`[论文事实: LBF Definition 2.28, p.18; Remark 2.29, p.18]`

- 矩阵 `A ←$ R_F^{κ×m}`；消息 `z∈R_F^m`；承诺 `c := A·z ∈ R_F^κ`。
- **完美同态**：`Commit(pp,z₁+αz₂)=Commit(pp,z₁)+α·Commit(pp,z₂)`。
- **不 hiding**（Remark 2.29）；binding 依 MSIS^{∞,κ,q}_{m,2B}，(B,C)-relaxed binding 依 MSIS^{∞,κ,q}_{m,4TB}（Proposition 2.30）。
- 简洁：`c∈R_F^κ`，`κ` 与消息长 `m` 无关——这是 SuperNeo 保持 folding 简洁的关键，也是它不能被 ABDLOP 全量替代的原因。

### C1.2 BDLOP 承诺

`[论文事实: LBF 式 (2.4), p.18]`

```
( t₁ )     ( A₁   0 )            ( 0 )
(    )  =  (         ) · s₁  +      (   )   (mod q)  =: Commit_BDLOP(m)
( t₂ )     ( A₂   y )            ( n )
```
即：`t₁ = A₁ s₁`，`t₂ = A₂ s₁ + m`（此处 `y`/`n` 为原文分块占位符；按上下文 `t₂=A₂s₁+message`）。

`[论文事实: [BDL+16] 官方摘要]` 该方案是结构化格假设上的加性同态承诺 + opening ZKPoK；可配置为 statistical binding 或 statistical hiding，最高效时两者都只 computational；相比前人方案证明约缩小 4 倍、承诺约缩小 6 倍。

### C1.3 ABDLOP 承诺（LBF 实际使用）

`[论文事实: LBF 式 (2.5), p.18]`

```
( tA )     ( A₁   A₂ ) ( s₁ )   ( 0 )
(    )  =  (          )·(    ) + (   )   (mod q)  =: Commit_ABDLOP(m)
( tB )     ( 0    B  ) ( s₂ )   ( y )
```
即：
```
tA = A₁ s₁ + A₂ s₂ ∈ R_F^κ        （Ajtai 部分）
tB = B s₂ + y      ∈ R_F^ℓ        （BDLOP 部分，消息在此）
```

| 对象 | 环/维度 | 约束 | 注释 |
|---|---|---|---|
| `A₁` | `R_F^{κ×m₁}` | 均匀随机 | Ajtai 主矩阵 |
| `A₂` | `R_F^{κ×m₂}` | 均匀随机 | ABDLOP 新增，绑定第二盐 |
| `B` | `R_F^{ℓ×m₂}` | 均匀随机 | ABDLOP 新增，承载消息槽 |
| `ℓ = κ'` | `ℓ = 待承诺的（无范数限制）环元素个数` | 本文 ≥1（standing convention） | BDLOP 秩 = 消息槽数 |
| `y` | `R_F^ℓ` | **无小范数限制** | 消息放 BDLOP 槽，与 [LNP22] 原生实例化相反（见 C1.5） |
| `s₁` | `R_F^{m₁}` | `‖s₁‖∞ < α` | 盐（短） |
| `s₂` | `R_F^{m₂}` | `‖s₂‖∞ < ν` | 盐（短）；本文 `B̃=2` 三元盐 |
| `κ_com` | `κ + κ' = κ + ℓ` | — | 承诺 `(tA,tB)∈R_F^{κ_com}` 的环分量总数 |
| ring | `R_F = F[X]/(X^d+1)`，`q` 素数 | LNP22 原生 `q≡5 mod 8`；本文 `q=2⁶⁴−59` | MSIS/MLWE/Extended-MLWE 假设 |

`[论文事实: §2.1, p.9; Remark 4.1(2), p.38]` 本文所有 ABDLOP 承诺把消息放在 **BDLOP 槽**（`ℓ^{(n)}≥1`，`tB^{(n)}=Bs₂^{(n)}+m^{(n)}`），两个分量 `s₁,s₂` 因此**都是盐**；`B̃=2`（三元）为具体承诺盐的系数界。

`[论文事实: LBF 式 (2.6)(2.7), Lemma 2.31, p.18]` 逐系数展开：
```
cf(Commit_ABDLOP(y)) = ( cf(tA) ; cf(tB) )
                     = ( cf(A₁s₁) + cf(A₂s₂) ; cf(Bs₂) + cf(y) ) mod q
```
对每个系数索引 ℓ 同理；`ℓ=1` 时 `cf(·)_1 = ct(·)`。`[推导]` 这是"承诺的每个系数是消息系数的公开线性函数 + 未打开的盐和"的形式化基础，直接支撑 Lemma 3.10 与 Sum-Check hint 在承诺层的检查。

### C1.4 ABDLOP 相对 BDLOP 的扩展

`[论文事实: §2.5.2, p.18]` BDLOP 只有一个短盐 `s₁`、一个消息 `m`；ABDLOP 增加第二短盐 `s₂`、矩阵 `A₂∈R_F^{κ×m₂}` 与 `B∈R_F^{ℓ×m₂}`，使第一块从 `A₁s₁` 变为 `A₁s₁+A₂s₂`，第二块从 `A₂s₁+m` 变为 `Bs₂+m`。作用（论文动机）：把 binding randomness 分成两个可独立控制范数的分量，并配套 ZKPoK；消息任意范数也可承诺。

### C1.5 与 [LNP22] 原文的已知偏离（必须记录，防二手推断）

`[论文事实: LBF 自身声明]`
1. **范数约定**：LBF 用 ℓ∞ 采样盐（与全文一致），LNP22 原文用 ℓ₂；LBF 说这最多放松 `√(m_l·d)` 因子（p.18 L1089–1095）。
2. **消息位置**：LBF 把消息放 BDLOP 槽 `ℓ≥1`，而 "[LNP22]'s own instantiations (Figs. 11, 13, 15) take ℓ=0 and place the message in the Ajtai part instead"（p.9 L511–515）。
3. **挑战域**：[LNP22] 在 `Z_q` 上 masking 错误 `1/q` 需重复 `⌈λ/log₂q⌉` 次；LBF 用 `K=F_{q²}` 一次到位，`1/|K|≈2^{−128}`（Remark 3.9, p.24）。
4. **符号重名**：`ℓ` 同时表示 Sum-Check 变量数/BDLOP 消息长/系数下标；`m` 既为约束数又为 ABDLOP 文献中的消息（Lemma 2.31 改名 `y`）；`κ` 在本文为 Ajtai 秩，在 [LNP22] 为挑战系数界（Notation 2.1, p.10）。

`[待核查]` 上述偏离是 LBF 自己明确写出的；[BDL+16]/[LNP22] 原文的**公式编号与维度表**未逐字核验（ePrint PDF 受 Cloudflare 限制，本阶段只核实了书目、版本、摘要主题）；引用原文编号前必须回两篇原文确认。

---

## C2. 安全性质

`[论文事实: LBF §2.5.2, p.18–19; Remark 2.36, p.19–20; [BDL+16]/[LNP22] 摘要]`

| 性质 | BDLOP/ABDLOP（论文回忆） | 依据/假设 |
|---|---|---|
| **Hiding** | ABDLOP 计算 hiding（MLWE，带 HVZK opening PoK）；BDLOP 类似 | Remark 2.36；LNP22 摘要（Module-LWE） |
| **Binding** | (B,C)-relaxed binding；差分须 ∈ C−C | Definition 2.27；MSIS |
| **Homomorphic** | 承诺映射是 `R_F`-模同态；逐系数 cf 保持线性（式 2.6/2.7） | §2.5.2；Lemma 2.31 |
| **Message Norm** | **无约束**（可承诺任意范数环向量）——这是相对 Ajtai 的关键优势 | §2.5.2 "without norm constraints"；§3.5 |
| **Randomness Norm** | 盐须小：`‖s₁‖∞<α`、`‖s₂‖∞<ν`（ℓ∞ 约定）；ABDLOP 机制内部用 ℓ₂，靠 `‖x‖₂≤|x|‖x‖∞` 转换（|x|=m_l·d） | §2.5.2；§3.3.4 |
| **安全假设** | Module-SIS（binding）、Module-LWE / Extended-MLWE（hiding + ZKPoK 模拟器）；E-MLWE 假设"几乎与 MLWE 同难" | Definition 2.32/2.33/2.34；Remark 2.36 |

`[论文事实: [BDL+16] 摘要]` 该文明确方案不限于 statistical binding，可配置 binding/hiding；最高效配置为两者皆 computational。
`[论文事实: [LNP22] 摘要]` 核心是直接证明短向量的 ℓ₂ 范数，不经过 ℓ∞  equivocation 或 CRT 转换；适合 `Z[X]/(Xⁿ+1)` 类环（自同构）；可黑盒插入多种隐私原语。

`[推导]` LBF 选择"任意范数消息 + 小范数盐 + 计算 hiding + 同态 + ZKPoK"的组合，正是为了同时满足：隐藏 mask/evaluation hints（任意范数）、在承诺层做线性检查（同态）、模拟折叠转录（hiding + ZKPoK），而输入 `c₁` 保持 Ajtai 简洁性。

---

## C3. 代数操作：`C₁ + ρ·C₂` 对应什么消息与盐

`[论文事实: Lemma 3.10 (Salt/message substitution), p.25; Remark 3.11, p.25; §4.1.2, p.41–42]`

设 `C₁=Commit(y₁,s₁)`、`C₂=Commit(y₂,s₂)`，共享公开矩阵 `(A₁,A₂,B)`，则 ABDLOP 同态性给出：
```
C₁ + ρ·C₂ = Commit(y₁ + ρ·y₂ , s₁ + ρ·s₂)
```
逐块验证：
```
tA₁+ρ tA₂ = A₁(s₁₁+ρ s₁₂) + A₂(s₂₁+ρ s₂₂)
tB₁+ρ tB₂ = B(s₂₁+ρ s₂₂) + (y₁+ρ y₂)
```
`[论文事实: Protocol 7 Step 20–21, p.42]` LBF 实际检查即此式（叠加 mask 项）：
```
Commit(y_j) = Σ_i ρ_i · Commit(y_{i,j}) + C_{y,j},
其中 y_j = Σ_i ρ_i y_{i,j} + y_{y,j},  s_j = Σ_i ρ_i s_{i,j} + s_{y,j}.
```
**适用条件（必须逐条核对）**：
1. **共享公开矩阵**：所有被组合的承诺使用相同 `(A₁,A₂,B)`；否则同态不成立。LBF 固定三元组 `(ℓ,m₁,m₂)` 支配全文（§2.1）。
2. **盐范数**：`s_j` 的范数须仍满足 relaxed-binding 可用界；`B<B_com`（p.42 Remark："Since B<B_com, we can deduce that also the randomness is suitably bounded"）。折叠盐 `B_fold=(K+k)T(C)(B̃−1)+B̃`（Remark 4.5），非任意大；LBF 在 Π′DEC 选择**重采样**盐而非分解，因为分解会让约 17 个高位盐为零使承诺退化（Remark 4.5, p.44）。
3. **ρ 来自强采样集**：`ρ∈C`（Definition 2.13）控制范数放大 `T(C)`；不能从全 `R_F` 采样。
4. **模数一致**：所有运算 `mod q`，同一分圆环 `R_F`。
5. **消息无范数限制**：`y_j` 可任意（含 Gaussian 折后），这正是 ABDLOP 相对 Ajtai 的必要性。

**V 视角的"盐替换"恒等式** `[论文事实: Lemma 3.10, p.25]`：若只需在承诺层验证某个公开线性泛函 `ct(Σ_n w_n (B s₂^{(n)})_{ι(n)}) = u⋆`（所有承诺 BDLOP 分量非空 `ℓ^{(n)}≥1`），则等价于
```
ct(Σ_n w_n m^{(n)}_{ι(n)}) − u = 0,
u := Σ_n w_n (tB^{(n)})_{ι(n)} − u⋆  ∈ R_K   （V 可仅凭传输承诺与公开 w_n 计算）
```
`[推导]` 代入 `Bs₂^{(n)}=tB^{(n)}−m^{(n)}` 即得；这解释 LBF 为何能在**不打开任何盐**的前提下检查 Sum-Check 的最终评价关系（Protocol 6 Step 18），且是 `C₁+ρC₂` 类线性操作在"证据"层的应用。

---

## C4. 接入 LatticeBlindFold 的具体用途

### C4.1 哪些 Evaluation Hints 被承诺

`[论文事实: Protocol 6 Step 9–10, p.37–38; Protocol 7 Step 5/20, p.42; Protocol 8 Step 2, p.44]`
- 新提示 `y'_{i,j} = M̄_j ẑ_i(r⃗')`，∀i∈[K+k], j∈[t]（Sum-Check 后）；
- 零次替代 `ŷ_{i,j}`（只保留常数项），及其平方/立方/乘积 `ŷ_{i,1}², ŷ_{i,1}³, ŷ_{i,2}ŷ_{i,3}`；
- RLC 输出提示 `y_j = Σ_i ρ_i y_{i,j} + y_{y,j}`（含 mask 贡献）；
- mask-block `(c_y,x_y)`（Protocol 7 Step 6，隐藏 mask 的 Ajtai 像）；
- Π′DEC 分解输出 `y_{i,j}`（fresh 盐重承诺）。
每个都 `C=Commit(y,s)`，盐 fresh 且 `‖s‖∞<B̃(=2)`。

### C4.2 为什么不能直接公开

`[论文事实: §1.1, p.4–5; Remark 2.29, p.18; §4.1.1.1, p.39–40]`
- `y'_{i,j}` 是 witness 在随机点的线性函数；跨 folding 轮累积会泄漏结构信息（作者博客：honest-but-curious verifier 可恢复 witness 结构）。
- `p(r⃗')`/`Q(r⃗')` 若公开即 Libra 残余泄漏（[CFW26]）；LBF 通过承诺层检查避免。
- An adversarial-but-honest verifier 的 `ρ⃗` 依赖视图；若 mask 的 Ajtai 像明文传输，条件于拒绝的分布依赖 witness（Remark B.9）。

### C4.3 为什么普通 Ajtai 承诺不能直接替代

`[论文事实: Remark 4.2(2)(3)(5)(8), p.39; §3.5, p.31–32; Remark 2.29, p.18]`（逐条，均可在原文定位）
1. **不 hiding**：Ajtai 无随机盐，是消息的确定映射；无法隐藏 mask/hint。
2. **不能承诺任意范数消息**：Ajtai binding 只在消息/盐小范数时成立；`p` 的系数折叠、salt aggregate 范数可能大。
3. **系数-环一致性**："we need a compatibility between the commitments of ring elements and the commitments of their associated coefficients"（Remark 4.2(2)）；ABDLOP 的 cf/ct 逐系数线性（Lemma 2.31）提供此兼容，Ajtai 不提供 ZK opening。
4. **ZKPoK**：ABDLOP 自带 randomness/message 与其线性/二次关系的 HVZK proof of knowledge；Ajtai 无。
5. **PCS 替代也不划算**：mask 只有 `1+D_max·ℓ=85` 个系数，"succinctness is irrelevant … we would pay ≈d² log m log q to compress something smaller than a single Sum-Check transcript"（§3.5）。
`[推导]` Ajtai 仍用于**必须简洁**的地方（输入 `c₁`、`c_i`、`c_y`），其信息泄漏由 blinding block/RLC mask 在 preimage 层补丁（§3.1/§3.6），形成"简洁 Ajtai + 非简洁 ABDLOP"的分工。

### C4.4 ABDLOP 如何参与后续 Folding

`[论文事实: Protocol 7 Step 21, p.42; Protocol 8 Step 5, p.44; §3.3, p.27–30]`
- RLC 用同态性折叠 `C_j`（式见 C3），并在承诺层公开检查；
- Π′DEC 对每个分解 `C_{i,j}` fresh 重承诺，用单个 batched `Π_many^{(1)}` 在 `N_c=(k+1)t` 盐块上证明 `y_j−Σ_i b^{i−1}y_{i,j}=0`（消息层恒等式，盐界 relaxed）；
- 因 ABDLOP 原生只在 `R_F` 安全，而 Sum-Check 在 `R_K`，LBF 用 §3.3 的 **component-wise instantiation**：`K=F[Y]/(Y²−ν)`，把 `x=a+bY∈R_K` 直接当 `(a,b)∈R_F²` 承诺，秩倍增嵌入 `ψ(a+bY)=[[a,νb],[b,a]]`（式 3.2），线性关系展开为式 (3.3) 两条 `R_F` 关系，二次关系展开为式 (3.11) 两条 `R_F` 二次关系；矩阵 `(A₁,A₂,B)` 真正均匀取自 `R_F`，安全只依赖标准 `R_F`-MLWE/MSIS。
- `[论文事实: §3.3.4, p.29]` 范数取 `‖a+bY‖²:=‖a‖²+‖b‖²`（`φ` 是等距）；**警告**：不能用 `σ_K(x)x` 的 K-level automorphism 恒等式直接证明该范数（会得到 `‖a‖²+ν‖b‖²`，ν 非剩余 ⇒ 错误量），须对 a、b 分别用 base-ring 自同构证明。

---

## C5. 参数数值（与 `06` 共用，此处只列承诺相关）

`[论文事实: §4.3.4, p.54, Table 2]` `q=2⁶⁴−59`，`n_F=2²¹`，`ξ≈20`，`λ=120`：

| 量 | d=64 | d=128 |
|---|---|---|
| `κ, κ'=ℓ, κ_com` | 19, 16, 35 | 11, 16, 27 |
| `m₁, m₂` | 15, 83 | 15, 53 |
| `Ñ`（mask-block 承诺元组数） | `⌈(19+n_{R,in})/16⌉` | `⌈(11+n_{R,in})/16⌉` |
| `B̃`（承诺盐系数界） | 2 | 2 |
| `β^rlx = 2s₂√(2N_cm₂d)` | log₂≈35.2 | log₂≈36.6 |
| δ_MSIS / δ_MLWE | 1.004419 / 1.004399 | 1.004491 / 1.004399 |
| 单位承诺大小 | 14.38 KB (ABDLOP), 13 KB (Ajtai) | 23.05 KB (ABDLOP), 15 KB (Ajtai) |

`[论文事实: Remark 4.19, p.54–55]` d=64 参数集约 116 bits，**不足 λ=120**，仅为 illustrative，不应视为安全实例化；d=128 约 121 bits。

---

## C6. 关键结论清单（可独立检查）

1. `[论文事实]` BDLOP：`(A₁s₁, A₂s₁+m)`；ABDLOP：`(A₁s₁+A₂s₂, Bs₂+m)`；消息任意范数，盐小范数（LBF 式 2.4/2.5, p.18）。
2. `[推导]` 同态：`Commit(y₁,s₁)+ρ·Commit(y₂,s₂)=Commit(y₁+ρy₂, s₁+ρs₂)`，条件为共享 `(A₁,A₂,B)`、`ρ∈C`、盐范数仍在 binding 界内、模数/环一致。
3. `[论文事实]` 盐替换：只要每个承诺 BDLOP 分量非空，`V` 可用公开 `tB` 分量把"环元素线性泛函的常数项"检查化为承诺消息上的关系，而**不需要任何盐**（Lemma 3.10）。
4. `[推导]` 为什么 Ajtai 不能替代：不 hiding、消息须小范数、缺 ZKPoK、缺系数-环兼容；其简洁性只在输入 `c₁` 等处保留，泄漏靠 preimage 随机化补丁。
5. `[论文事实]` R_K 上的使用必须 component-wise（§3.3），安全假设不超出 `R_F`-MSIS/MLWE/E-MLWE。
6. `[待核查]` 原始 [BDL+16]/[LNP22] 的公式编号与维度表未逐字核原文（见 §C1.5）；本文件的 `(2.4)(2.5)` 编号属 LBF。
