# Polynomial Masking 深度核验

> 状态：LB-01 / 任务 B 完成。所有结论回到原文定义/公式/定理，页码为 LBF 印刷页码。
> 主来源：`[LBF]` = Luca Dall'Ava, *LatticeBlindFold: A Lattice-Based Analogue of NovaBlindFold*, ePrint 2026/1857, 2026-09-01。
> 基础来源：`[XZZ+19]` = Chiesa et al., *Libra: Succinct Zero-Knowledge Proofs with Optimal Prover Computation*（LBF 引作 Construction 1, §4.1 / Theorem 3）；`[CFW26]` = Chiesa, Fenzi, Weissenberg, *Zero-knowledge IOPPs for constrained interleaved codes*, ePrint 2026/391（LBF Remark 3.18(1) 引用）；`[Tha22]` = Thaler, *Proofs, Arguments, and Zero-Knowledge*, §13.3；`[LNP22]` = ePrint 2022/284。
> 本文件不提出新构造。标签：`[论文事实]` / `[推导]` / `[研究假设]` / `[待核查]`。

---

## B1. 原始多项式

### B1.1 原始 Sum-check 用的是哪个多项式

`[论文事实: LBF §2.4.2, p.16–17, 式 (2.3); Protocol 6 Step 3, p.37]`

回忆版（SuperNeo，式 2.3）：
```
Q(X⃗) := eq(X⃗, α⃗) · (F(X⃗) + γ^K · NC(X⃗)) + γ^{2K+k} · Eval(X⃗) ∈ K[X⃗]
```
实用版（LBF Protocol 6 Step 3，用三族独立批挑战）：
```
F(X⃗)     := Σ_{i=1}^{K} γ_i^{(1)} · f(M̄₁ z_i, …, M̄_t z_i)
NC(X⃗)    := Σ_{i=1}^{K+k} γ_i^{(1)} · ∏_{j=−(b−1)}^{b−1}(z_i^{(e_i)} − j)
Eval(X⃗)  := eq(X⃗, r⃗) · Σ_{i=K+1}^{K+k} Σ_{j=1}^{t} Σ_{ℓ=1}^{d} γ_i^{(1)} γ_j^{(2)} γ_ℓ^{(3)} · cf(M̄_j z_i)_ℓ
Q(X⃗)     := eq(X⃗, α⃗) · (F(X⃗) + δ₀ · NC(X⃗)) + δ₁ · Eval(X⃗)
```
其中 `z_i=[x_i,w_i]`（新实例）或 `z_i` 为携带的评价见证（盲化 accumulator），`M̄_j` 为结构矩阵，`f` 为 R1CS/CCS 多项式，`α⃗` 为 Sum-Check 随机点，`δ₀,δ₁`（回忆版为 `γ^K, γ^{2K+k}`）合并三项检查。

**component 来源** `[论文事实: §2.4.2, p.16–17]`：
- `F` 来自 `K` 个新 R1CS/CCS 实例约束；
- `NC` 来自 `K+k` 个 witness 的范数约束（检验 `‖z_i‖∞<b`）；
- `Eval` 来自 `k` 个携带的 evaluation claim（点 `r⃗`、提示 `y_{i,j}=M̄_j ẑ_i(r⃗)`）。

**claimed sum** `[论文事实: Protocol 6 Step 3, p.37]`：
```
T := δ₁ · Σ_{i=K+1}^{K+k} Σ_{j=1}^{t} Σ_{ℓ=1}^{d} γ_i^{(1)} γ_j^{(2)} γ_ℓ^{(3)} · cf(y_{i,j})_ℓ
```
`[推导]` 这正是把 `Eval` 中未知的 `cf(M̄_j z_i)_ℓ` 用 verifier 已知的提示 `y_{i,j}` 替换后得到的和，`Σ_{x⃗∈{0,1}^{log₂m}}Q(x⃗)=T` 成立当且仅当三类检查都过（Schwartz–Zippel 意义，错误项见 `ε_SZ`）。

### B1.2 变量数、次数、partial degrees

`[论文事实: §2.1, p.9; Protocol 6 Step 3, p.37; §4.5, p.58]`

- **变量数**：`ℓ = log₂(m)`。参数集 `m=n_F=2²¹` ⇒ `ℓ=21` 个变量（Sum-Check 21 轮）。
- **所在域**：`Q ∈ K[X⃗]`，即变量在扩域 `K=F_{q²}`（交互版），系数经由 `cf` 落到 `R_F`/`R_K`。
- **单变量次数上界**：`D_max := max{u+1, 2b, 2}`，本文 `u=2,b=2` ⇒ `D_max=4`（`[论文事实: §2.1, p.9]`）。
- **partial degrees**：`d_i := deg_{X_i}(Q(X⃗))`，逐变量取（不一定都等于 `D_max`）；mask 的 partial degree 精确取 `d_i`（B2）。
- **总次数**：`[待核查]` 论文没有单独给 `deg Q` 的总次数上界表达式；只给 `D_max` 与 partial degrees。R1CS 情形各变量最多 4 次，`eq(X⃗,α⃗)` 为多线性，`f` 乘积带来度数；不要自行写"总次数 O(u)"。

---

## B2. 掩码多项式

### B2.1 生成方式与系数来源

`[论文事实: LBF Protocol 6 Step 3–4, p.37; §3.4, p.30–31; §3.5, p.32]`

```
p(X⃗) := a₀ + Σ_{i=1}^{ℓ} p_i(X_i),
p_i(X_i) := Σ_{j=1}^{d_i} a_{i,j} X_i^j,
d_i := deg_{X_i}(Q(X⃗)),
a₀, a_{i,j} ← K 均匀随机（prover 私有）。
```
- **系数来源**：prover 本地均匀采样 `K` 中元素；共 `1 + Σ_{i=1}^{ℓ} d_i ≤ 1 + D_max·ℓ` 个。参数集 `ℓ=21, D_max=4` ⇒ 85 个元素（p.32）。
- **承诺**：把系数打包成 `⌈(1+D_max·log₂ m)/d⌉` 个 `coeffs ∈ R_K`（d=64 时为 2 个，d=128 时为 1 个），用 `Commit_ABDLOP(coeffs, s_P)` 在 `ζ` 采样**之前**承诺（Protocol 6 Step 4；§3.5 需求 (1)）。
- **P 的计算**：`P := Σ_{x⃗∈{0,1}^{ℓ}} p(x⃗) = 2^ℓ a₀ + 2^{ℓ−1}Σ_{i,j}a_{i,j}`（`[推导]`，由 §4.1.1.1 p.40 的均匀性论证读出）；`P` 是 `coeffs` 的公开线性函数（§3.5），V 不必知道 `p` 即可从承诺验证 `σ`（Step 7  anchoring）。

### B2.2 次数限制

`[论文事实: Protocol 6 Step 3, p.37; §3.4 "note that here we only require that the degrees of the g_i's correspond to the partial degrees of f", p.30]`
- **要求逐变量 partial degrees 对齐**：`deg_{X_i}(p)=deg_{X_i}(Q)=d_i`，不多不少（多了会改变 Sum-Check 一致性类的维度，模拟器无法"零代价"采样；少了则 `ζp+Q` 的度数与 `Q` 不同、掩码不充分）。
- **形式限制**：`p` 是 **单变量分量之和**（additive separable），不是任意多变量多项式；这正是 Libra [XZZ+19, Construction 1] 的结构，好处是系数只 `1+Σd_i` 个、承诺小。
- `[推导]` 该形式足够，因为被隐藏的是每轮一元消息 `h_i(X_i)=Σ_{x⃗_{>i}}q(…,X_i,…)`；`p` 的单变量分量对每个 `h_i` 只贡献一个同次数的一元多项式，从而把 `h_i` 打成均匀。

### B2.3 布尔点上的性质

`[论文事实: §3.4, p.30–31; Protocol 6 Step 8, p.37]`
- `p` 在 `{0,1}^ℓ` 上的和 `P` 是公开可承诺推导的（`P=Σ_{x⃗}p(x⃗)`），Sum-Check 在 `q:=ζp+Q` 上运行，声明和 `σ:=ζP+T`，且在布尔点上 `Σ q(x⃗)=ζP+T` 成立（线性）。
- **`p` 不要求在布尔点上取特定值**（不同于 §3.4 中 "mask final evaluation" 的 `m_i(X)=X_i(1−X_i)` 技巧——那是 Thaler/ GKR 路线，LBF 只在背景介绍里引用，正文实际采用"完全不打开 `p(r⃗')`"的路线；见 B3/B4 与 `Remark 4.2(8)`）。
- `[推导]` 因 `q` 是由 `p` 与 `Q` 相加得到，Sum-Check 逐轮消息 `h_i(X_i)=ζ·(p 的对应一元分量)+Q 的对应一元分量`；由于 `p` 均匀且 prover 私有，`h_i` 在其一致性仿射空间内均匀（§4.1.1.1 的三角双射论证）。

### B2.4 最终随机点上的求值处理 —— 与 Libra 的决定性差别

`[论文事实: Remark 3.18(1), p.31; Remark 4.2(8), p.39; §4.1.1.1, p.39–40]`

- **Libra 原版 [XZZ+19]**：V 打开 PCS commitment 得 `g(r⃗)`，计算 `v_f = h_ℓ(r_ℓ) − ρ·g(r⃗)` 并与 `f(r⃗)` 比较 → **`f(r⃗)` 被恢复，构成残余泄漏**（[CFW26]，LBF Remark 3.18(1) 逐字："the Libra masking protocol is not completely zero-knowledge … as it reveals the evaluation of f at ⃗r (from the opening of g at ⃗r)"）。
- **LBF 的处理**：**不打开 `p`**，也不让 V 形成 `Q(r⃗')`。Sum-Check 末轮只公开 `h := h_{log₂m}(r'_{log₂m}) = (ζp+Q)(r⃗')`。随后 V 计算
  ```
  u⋆ := h − eq(r⃗',α⃗)·(cF + δ₀·cN) − δ₁·cE
  ```
  由 Lemma 3.10（salt/message substitution）把 `u⋆` 化为承诺消息上的常数项线性关系，用锚定 `Π_anc` 证明：
  ```
  h − ζ·p(r⃗') = Q(r⃗')        （在承诺层认证，p(r⃗') 从不作为域元素出现）
  ```
  `p(r⃗')` 由式 (3.13) `p(r⃗')=⟨coeffs,(1,r'_i,r'_i²,r'_i³,r'_i⁴)_{i∈[ℓ]}⟩` 表示为承诺系数的**公开线性泛函**（packaged rotation, Lemma 3.12），在 PoK 内部消化。
- `[推导]` 这是"把 [XZZ+19] 的 PCS 打开步骤替换成 commit-and-prove（ABDLOP ZKPoK）"的直接后果：丧失简洁性（mask 只有 85 个系数，无需 PCS，§3.5）换取 `f(r⃗)` 不再泄漏。

---

## B3. 零知识性质

### B3.1 真实转录分布、模拟器、模拟器可得信息

`[论文事实: §4.1.1.1, p.39–40; Theorem 4.13, p.48; Protocol 19, p.72–74]`

**真实转录**（V 视图）：Sum-Check 轮多项式与 `h=(ζp+Q)(r⃗')`；`σ=ζP+T`；全部承诺；全部 V 挑战；`C_{y,0}` 接受时打开；接受/拒绝模式（含拒绝轮留下的 hiding commitments）。

**模拟器 `S'`（Theorem 4.13）**：输入仅 `(pp, s, x₁)`——**不含** witness `z₁`、不含盲化块 `e`、不含承诺 `c₁`。它自采 `ω'` 导出所有挑战（含每个 rejection attempt 的 `ρ⃗^{(τ)}`），自采盲化 accumulator 对；构造 **fake witness** `ŵ₁←{w:‖w‖∞<b}`、`ẑ₁=[x₁,ŵ₁]`（"never claimed to be an opening of c₁"）；Sum-Check 转录**直接采样**（在一致性仿射空间均匀抽 round polynomials，读 `h`）；σ 均匀采样；所有 ABDLOP ZKPoK 用其 HVZK 模拟器；折叠循环中对拒绝轮发送 `Commit(0,·)`，对接受轮用 slack variable `c_y = L(z) − ρ₁c₁ − Σρ_{K+i}c_i^{blind}`（只有模拟器能做到，因为 ρ⃗ 由它自选；见 Remark B.7/B.8）。

**模拟器可得公开信息**：`pp`、结构 `s`、公开输入 `x₁`（以及自身采样的随机带），**不得**得到 `w_circ`、`e`、`c₁`。

### B3.2 原论文零知识定理与具体条件

`[论文事实: Theorem 4.13, p.48; Definition 2.11 (Blinding Folding Interactive Reduction), p.13; Theorem A(2)–(3), p.6]`

**条件（缺一不可）**：
1. `K = 1`（只折叠一个真实 R1CS 实例 + `k` 个模拟实例）；
2. 结构满足 blinded layout（Definition 3.1）；
3. 限制输出关系为 `CE_com(b,L,B̃,Commit,T,K)^k ⊂ CE_com(...)^k`（Definition 3.25）；
4. 把 `ι_bl` 预复合，输入取未填充 `R'=CCS°(b)^K`，`e` 由 prover 在协议内后采；
5. verifier 为 honest-but-curious public-coin `V*`；
6. 单次 step（非完整 folding scheme）；交互设定。

**结论**：存在 EPT 模拟器，区分优势 `ε^{LBF-blind}`（式 4.6）：
```
N_PoK^{zk} ε^{zk}_ABDLOP + (W_max+2)t·ε_hide + W_max·ε_hide,0 + O(W_max·2^{−λ}) + ε_{L-hide}
N_PoK^{zk} = 4+2t,  ε_hide,0 = Ñ ε_hide,  ε_{L-hide} ≤ 2^{−128}（默认 regime (1)）
```
`[论文事实: Remark 4.23, p.56–57]` 在这些参数（λ=120, t=3, W_max≤2⁸）下 `O(W_max·2^{−λ})≈2^{−112}` 主导，故实际 `ε^{LBF-blind}≈2^{−112}`，**不是** 2^{−120}。

### B3.3 Perfect / Statistical / Computational 的严格区分

`[论文事实: §4.1.1.1, p.40; Remark 3.18(3), p.31; Remark 3.4, p.21; Appendix B.4, p.74–77]` `[推导]`

| 组件 | 类型 | 依据 |
|---|---|---|
| Masking（Sum-Check 转录 + `h` + `σ`） | **Perfect**：`p` 均匀时在一致性类上均匀，与 `Q` 独立，模拟器零代价 | §4.1.1.1 "the masking is perfect"；Remark 3.18(3)；Remark 4.2(7) |
| `ε_L-hide`（输入 `c₁` 的隐藏） | **Statistical**（regime (1)，`≤2^{−128}`，对无界区分者）；**Computational**（regime (2)，DKS∞） | Lemma 3.3, p.20–21 |
| `ε_hide, ε_hide,0`（ABDLOP 承诺） | **Computational**（MLWE） | §2.5.2 / Remark 2.36 |
| `ε^{zk}_ABDLOP`（PoK 模拟器） | **Computational**（Extended-MLWE） | Lemma 3.6 / Appendix B.4 |
| `O(W_max 2^{−λ})`（拒绝尾/abort 模式） | Statistical（高斯尾） | Lemma 3.19 / Remark 2.12 |
| **整体 Π_LBF blinding** | **Computational ZK**（包含上述 perfect/statistical 组件，但总优势由计算项主导） | Theorem 4.13 证明 (B.2)："computationally indistinguishable from the real blinding execution" |

`[推导]` **不可**写成"perfect ZK"或"statistical ZK"：虽然 masking 本身是 perfect，但折叠与承诺层的模拟依赖 MLWE/Extended-MLWE。也不可把 "blinding" 与 "knowledge soundness" 混为一谈（前者是 witness 隐私，后者是可靠性）。

---

## B4. 关键问题：mask 单独够不够？

`[论文事实 + 推导]` **不够。** 证据链：

1. `[论文事实: Remark 3.18(1), p.31]` [XZZ+19]/Libra 式 masking 在 PCS 打开 mask 求值时泄漏 `f(r⃗)`；[CFW26] 明确记录这一点。论文逐字："we must hide this value"。
2. `[论文事实: Remark 4.2(8), p.39]` LBF 之所以不同，是因为 "we reveal neither ... the final check takes place entirely at the level of the commitments, so `p(r⃗')` is never opened and `Q(r⃗')` never formed as a field element in V's view"（摘要同样陈述）。
3. `[论文事实: §3.5, p.32]` 绑 `p`、全程藏 `p`、证明 `p(r⃗')` 与所承诺 `p` 一致——三需求缺一不可；论文用 ABDLOP（非 PCS）一次性满足。
4. `[论文事实: Lemma 3.3 后注, p.21; Remark 3.27, p.35]` 即使 masking 完美，**输入 Ajtai 承诺 `c₁` 仍可能泄漏**；必须在 blinded layout + unpadded relation 上让 prover 后采 `e`。layout 本身不够。
5. `[论文事实: §3.6, p.32; Remark B.9, p.76–77]` RLC 折叠结果 `z=v+y` 的分布依赖 witness；必须有 rejection sampling，且被拒轮的 Ajtai 像必须 ABDLOP-承诺（Ajtai 不 hiding）。masking 对此无能为力。
6. `[论文事实: Theorem 4.13 条件, p.48]` blinding 还要求 `K=1`、blinded layout、unpadded input、单步；masking 只解决 Sum-Check 轮消息这一环。

`[推导]` 结论：Polynomial Masking 是 **必要但不充分** 的机制。完整的 ZK/ blinding 需要四件独立随机化协同：
```
(① blinding block e 隐藏输入 Ajtai 像)
+ (② Libra-style mask p 隐藏 Sum-Check 轮消息)
+ (③ ABDLOP commit-and-prove 藏提示与 mask 求值、替代 PCS 打开)
+ (④ rejection sampling 使折叠输出（含盐）可模拟)
```
任何把"用了随机多项式"直接等同于"协议零知识"的说法都是错误的；这也是本任务包强调的核查点。

---

## B5. [待核查] 与边界

- `[待核查]` 本文提供的第三方全文镜像中 §3.4 的 "Protocol 5 zkSumCheck" 为 **[XZZ+19] 的回忆/转述**，不是 LBF 自己的协议；LBF 自己的版本在 Protocol 6 Steps 3–18（p.37–38）与 §4.1.1.1（p.39–40）。引用时不可混用两套符号（`g/ρ` vs `p/ζ`，`v_f` vs `u⋆`）。
- `[待核查]` [CFW26] 的正式定理编号与页码需回 ePrint 2026/391 原文核对；本文只按 LBF Remark 3.18(1) 的引用陈述，未读 CFW26 正文。
- `[待核查]` Fiat–Shamir 版需要 `K=F_{q⁴}`、round-by-round knowledge soundness 未证（§4.5, p.58–59）：本文所有 masking 的 ZK 结论仅对交互式协议成立，非交互转换不由本文覆盖。
- 不要把 `p_i(X_i)` 的 partial-degree 对齐误写成"p 是 multilinear"；它是逐变量次数 ≤ `d_i`（本文 ≤4）的 separable 多项式。
