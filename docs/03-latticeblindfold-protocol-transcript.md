# LatticeBlindFold Blind Folding 协议完整转录

> 状态：协议结构复原完成（LB-01 / 任务 A）。
> 主来源：Luca Dall'Ava, *LatticeBlindFold: A Lattice-Based Analogue of NovaBlindFold*, IACR ePrint **2026/1857**, 2026-09-01（单一版本 20260901:172842）。以下称 **[LBF]**。
> 引用格式：`[论文事实: LBF §x.y, p.N, Definition/Protocol/Theorem 编号]`。页码为论文印刷页码。
> 来源核验说明：ePrint 官方摘要页（<https://eprint.iacr.org/2026/1857>）确认标题、作者、日期、摘要与版本历史；PDF 受 Cloudflare 限制，正文用第三方公开镜像全文（与官方摘要逐段一致）核对，并与作者本人技术博客交叉验证公式。镜像获取路径与核验方法见 `logs/2026-11-20-session-02.md`。
> 标签：`[论文事实]` / `[实现事实]` / `[推导]` / `[研究假设]` / `[待核查]`。本文件不含新构造。

---

## 0. 一句话定位（先划定范围，避免外推）

`[论文事实: LBF Abstract, p.1; Theorem 4.13, p.48; §4.2.1, p.46–47]`

Π_LBF 是**单次交互式 step**：输入 **未承诺** 的 R1CS 实例（`CCS°(b)^K`，实际 `K=1`），输出 `k` 个 **committed evaluation claims**（`CE_com(b,L,B̃,Commit,T,K)^k`，每个 claim 带 ABDLOP 承诺 `{C'_{i,j}}`）以及认证这些承诺的 ABDLOP opening/argument。论文**不**声称：
- 完整 folding scheme（instance-in/instance-out 接口）；
- 递归组合；
- 非交互（Fiat–Shamir）安全性；
- `K>1` 时的 blinding。

上述四点均被作者明确列为未完成/限制，不能从"reduction of knowledge + blinding"外推。

---

## 1. 参与方、公共参数、Witness、输入关系

### 1.1 参与方

`[论文事实: LBF Protocol 6/7/8/12, p.36–46]`
两方：**Prover P** 与 **Verifier V**。V 是 honest-but-curious public-coin verifier `V*`（Definition 2.11, p.13）：给定其随机带 `ω`，所有挑战由固定 public map 从 `ω` 导出，因此模拟器可自采 `ω'` 提前复现挑战。这是 blinding 定义的建模前提，不能替换成恶意 verifier。

### 1.2 公共参数（Definition 2.2, p.10；§2.1, p.9–10）

`[论文事实]` 基础参数：`λ=120`（全文固定）；素域 `F=F_q`、低次扩域 `K`（工作集 `K=F_{q²}`）；分圆 `Φ=X^d+1`（`d` 为 2 的幂）；`R_F=F[X]/Φ`、`R_K=K[X]/Φ`；约束数 `m`、环向量长 `n_R`、域向量长 `n_F=d·n_R`（含盲化块）；输入长 `n_{F,in}/n_{R,in}`；多项式次数上界 `u`、结构矩阵数 `t`（R1CS 时 `f=Y₂Y₃−Y₁, u=2, t=3`）；折叠数 `K,k`；范数界 `b=2`、`B=b^k<q/2`。

Definition 2.2 追加固定四件对象：

| 对象 | 定义 | 作用 |
|---|---|---|
| 结构 `s` | §2.4.1，结构矩阵 `{M̄_j}_{j∈[t]}` + 次数 `u` 多项式 | 定义 CCS/R1CS 关系 |
| 强采样集 `C⊆R_F` | Definition 2.13, p.14；展开因子 `T`；`(K+k)T(b−1)<B`，`1/|C|=negl(λ)` | 折叠挑战 `ρ_i` 的采样域，控制范数爆炸 |
| 环承诺 `com=(Setup,Commit)` | Definition 2.27, p.17；同态、`(2B,C)`-relaxed binding；诱导 `L:=Commit(pp,·):R_F^{n_R}→C` | Ajtai 承诺；须在盲化块上 hiding（Lemma 3.3） |
| 投影 `L_in` | `R_F^{n_R}→R_F^{n_{R,in}}`，取前 `n_{R,in}` 列 | 抽取公开输入 |

`[论文事实: §2.1, p.9]` 其余：`κ,κ'=ℓ,κ_com=κ+κ'`（承诺秩/消息槽）；盐 `s=(s₁,s₂)∈R_F^{m₁}×R_F^{m₂}`；`β_ch`；`(ℓ,m₁,m₂)` 三元组；`cf/ct` 系数/常数项映射；`split_b`；`D_max=max{u+1,2b,2}=4`（本参数）；`M`（Rej1 重复率）、`W_max=⌈λ/log₂(M/(M−1))⌉`、`N_PoK`。

`[论文事实: Definition 3.1, p.20–21]` **Blinded layout**（blinding 成立的关键结构条件）：
1. `z=[x,w]`，`w` 尾部 `I_bl` 索引的 `n_{F,bl}` 坐标为 **blinding block `e`**，诚实 prover 从 `{v:‖v‖∞<b}` 均匀采样；
2. 固定索引 `ι₁≤n_{F,in}` 为常数 1 线 `z_{ι₁}=1`；
3. `i∈I_bl` 时 `(M̄₁)_{i,•}=(M̄₂)_{i,•}=δ_i`、`(M̄₃)_{i,•}=δ_{ι₁}` → 该行恒等式 `z_i·1−z_i=0`，对 `e` 无约束；
4. `i∉I_bl` 时 `(M̄_j)_{i,I_bl}=0` → 电路不读盲化列（但 `L` 在 `I_bl` 上有支撑，这正是 Lemma 3.3 要用）。

`[推导]` 条件 (3)(4) 保证：加盲化块不改变语言可满足性（Remark 3.2），但使 `c₁=L(z₁)=A_circ z_circ + A_bl e` 趋于均匀，从而掩盖 witness。

### 1.3 Prover 持有的 Witness

`[论文事实: Protocol 12, p.45; Definition 3.28, p.36; Protocol 11, p.44–45]`
- 真实 R1CS witness `w_circ`（`CCS°(b)` 的措施）；
- 由 `ι_bl`（式 3.19）在协议内**后采**的盲化块 `e←χ_b^{n_{R,bl}}`，`z₁=[x₁,w_circ,e]`，`c₁=L(z₁)`（协议消息，非输入）；
- `k` 个 prover 自采的盲化 accumulator 实例-见证对 `(u_i^{blind},w_i^{blind})_{i=K+1}^{K+k}`，含 Gaussian `z←D_s^{n_F}`（重启至 `‖z‖∞≤τ_{λ,ξ}s`）、`split_b`、评价提示 `y_{i,j}`、承诺盐 `s_{i,j}`（Protocol 11）；
- 每轮本地随机：mask 多项式系数 `{a_{i,j}}`、mask salt `s_P`、RLC mask `y←D_s^{n_F}` 及各承诺 fresh salt、各 ABDLOP PoK 的 mask/`γ⃗`/`c` 等内部随机。

### 1.4 输入关系

`[论文事实: Definition 4.6, p.46; Definition 3.28, p.36]`
输入 `R'=CCS°(b)^K`（未填充、无承诺），`K=1` 是 blinding 的前提条件。Definition 3.26 `CCS(b)^K={s;(x);w : ‖z‖∞<b ∧ f(M̄₁z,…,M̄_t z)∈ZS_log₂(m)}`；`ι_bl` 把它嵌入 `CCS(b,L)^K` 并公布 `c_i`。

### 1.5 使用的 Commitment（详见 `05`）

`[论文事实: §2.5, p.17–19]`
- **Compact Ajtai**（Definition 2.28）：`c=Az∈R_F^κ`，完美同态、**不 hiding**、B-binding/(B,C)-relaxed binding（MSIS）；用于输入 `c₁`、折叠实例 `c_i`。
- **BDLOP**（式 2.4）：`(t₁,t₂)=(A₁s₁, A₂s₁+y)`。
- **ABDLOP**（式 2.5）：`(tA,tB)=(A₁s₁+A₂s₂, Bs₂+y)`；消息放在 BDLOP 槽 `ℓ⁽ⁿ⁾≥1`；非简洁、计算 hiding（MLWE）、带 ZKPoK；`A₁∈R_F^{κ×m₁}, A₂∈R_F^{κ×m₂}, B∈R_F^{ℓ×m₂}`，`‖s₁‖∞<α`、`‖s₂‖∞<ν`（本文 `B̃=2` 三元盐，Remark 4.1(2), p.38）。

---

## 2. 完整协议转录表

`[论文事实: Protocol 6, p.36–38; Protocol 7, p.41–43; Protocol 8, p.43–44; Protocol 12, p.45–46]`
Π_LBF = `ι_bl` 前置 + `Π′DEC ∘ Π′RLC ∘ Π′R1CS`（**应用顺序** P6 → P7 → P8）。下表按实际时序展开；"派生"表示 V/P 本地计算、**不在信道上传输**。

| 顺序 | 参与方 | 消息或挑战 | 数学表达式 | 用途 |
|---|---|---|---|---|
| 0a | P（本地） | 盲化实例采样（Protocol 11） | `(u_i^{blind},w_i^{blind})_{i=K+1}^{K+k}←sample_{CE_com}^{blind}(pp,s)`；`z←D_s^{n_F}` 重启至 `‖z‖∞≤τ_{λ,ξ}s`，`split_b` | 提供与真实 witness 独立的随机 one-time pad（NovaBlindFold 式） |
| 0b | P（本地）→ 公布 | `ι_bl` 随机化（式 3.18/3.19） | `e←χ_b^{n_{R,bl}}`，`z₁=[x₁,w_circ,e]`，`c₁=L(z₁)` | 使输入 Ajtai 像 hiding（Lemma 3.3）；`e` 必须在协议内后采，否则攻击者可令 `e=0`（Lemma 3.3 后注, p.21） |
| 0c | V↔P | PoK on 输入承诺（P6 Step 1） | `Π_many^{(1)}` on `{Commit(y_{i,j},s_{i,j})}_{i∈[K+1,K+k],j∈[t]}` | 对携带进来的盲化承诺绑定 `y_{i,j}` |
| 1 | V→P | 第一批挑战（P6 Step 2） | `α⃗←K^{log₂m}`；`γ⃗^{(1)}←K^{K+k}`、`γ⃗^{(2)}←K^t`、`γ⃗^{(3)}←K^d`；`(δ₀,δ₁)←K²` | Sum-Check 点、三族独立批挑战（避免 union bound）、R1CS/范数/Eval 合并系数 |
| 2 | P（本地） | 复合多项式与和（P6 Step 3） | `F(X⃗)=Σ_{i≤K}γ_i^{(1)} f(M̄₁z_i,…,M̄_t z_i)`；`NC(X⃗)=Σ_{i≤K+k}γ_i^{(1)}∏_{j=−(b−1)}^{b−1}(z_i^{(e_i)}−j)`；`Eval(X⃗)=eq(X⃗,r⃗)Σ_{i>K,j,ℓ}γ_i^{(1)}γ_j^{(2)}γ_ℓ^{(3)}cf(M̄_j z_i)_ℓ`；`Q(X⃗)=eq(X⃗,α⃗)(F(X⃗)+δ₀NC(X⃗))+δ₁Eval(X⃗)`；`T=δ₁Σ_{i>K,j,ℓ}γ_i^{(1)}γ_j^{(2)}γ_ℓ^{(3)}cf(y_{i,j})_ℓ` | 把 R1CS、范数、携带评价声明压成一次 Sum-Check |
| 3 | P（本地）→V | **Polynomial Masking**（P6 Step 3–4） | `p(X⃗)=a₀+Σ_{i=1}^{ℓ}p_i(X_i)`，`p_i(X_i)=Σ_{j=1}^{d_i}a_{i,j}X_i^j`，`a_{i,j}` 均匀，`d_i=deg_{X_i}(Q)`；系数打包为 `⌈(1+D_max log₂m)/d⌉` 个 `coeffs∈R_K`，送 `Commit_ABDLOP(coeffs,s_P)` | Libra 风格隐藏 Sum-Check 轮消息；`P=Σ_{x⃗∈{0,1}^{log₂m}}p(x⃗)` 是承诺的公开线性函数 |
| 4 | V→P | blinding 挑战（P6 Step 5） | `ζ←K^×` | 在 `p` 被承诺后采样，使 `σ` 均匀、完美隐藏 `T` |
| 5 | P→V | 被隐藏的 claimed sum（P6 Step 6） | `σ:=ζ·P+T ∈ K` | `P` 均匀（因 `a₀` 均匀且 `2^{log₂m}` 可逆）⇒ `ζP+T` 在 `K` 上均匀，`T` perfect hidden（Remark 4.2(7), p.39） |
| 6 | V↔P | 锚定 PoK σ（P6 Step 7） | `Π_anc` on `N_c=1+kt` commitments，公开关系 `ct(ζR_m^{(Σ)}coeffs + δ₁Σ_{i,j}π_{i,j}y_{i,j} − σ)=0`，`π_{i,j}=Σ_ℓγ_i^{(1)}γ_j^{(2)}γ_ℓ^{(3)}τ_ℓ` | 在承诺层把 `σ` 绑定到 `p` 与 `y_{i,j}`，不打开任何值 |
| 7 | V↔P | 掩码 Sum-Check（P6 Step 8） | 对 `q=ζp+Q`、声明和 `ζP+T` 跑 SumCheck；`r⃗'←K^{log₂m}`；末轮 V 得公开 `h=(ζp+Q)(r⃗')` | 压缩约束检查；`p(r⃗')`、`Q(r⃗')` **从不形成 V 视图中的元素** |
| 8 | P→V | 新提示承诺（P6 Step 9–10） | `C'_{i,j}=Commit(y'_{i,j})`，`y'_{i,j}=M̄_j ẑ_i(r⃗')`；`ĉ_{i,j}=Commit(ŷ_{i,j})`，`ct(ŷ_{i,j})=ct(y'_{i,j})`、`cf(ŷ_{i,j})_ℓ=0 (ℓ≥2)` | 把明文提示换成承诺（commit-and-prove） |
| 9 | V→P | degree-0 批挑战（P6 Step 11） | `{µ_ℓ}_{ℓ=2}^d ← K^{d−1}`；`π_µ=Σ_{ℓ≥2}µ_ℓτ_ℓ` | 把 `d−1` 个零系数条件压为常数项关系 |
| 10 | V↔P | degree-0 + 二次关系 PoK（P6 Step 12–15） | `Π_many^{(ct)}`：`ct(π_µ·ŷ_{i,j})=0`、`ct(y'_{i,j}−ŷ_{i,j})=0`（错误 `2/|K|`）；`ĉ'_{i,sq}=Commit(ŷ_{i,1}²)`、`ĉ'_{i,cube}=Commit(ŷ_{i,1}³)`、`ĉ'_{i,prod}=Commit(ŷ_{i,2}ŷ_{i,3})`；`Π_ABDLOP,many^{(2)}` 证平方/立方/乘积 | 认证后续 `cF,cN` 所用的二次结构 |
| 11 | V（**派生**） | salt-offset 中间值（P6 Step 16） | `cF=Σ_{i≤K}γ_i^{(1)}ct(Commit(f(ŷ_{i,1},…))_2)`；`cN=Σ_{i≤K+k}γ_i^{(1)}ct(Commit(∏_{j=−(b−1)}^{b−1}(ŷ_{i,1}−j))_2)`；`cE=eq(r⃗',r⃗)Σ_{i>K,j,ℓ}γ_i^{(1)}γ_j^{(2)}γ_ℓ^{(3)}cf(Commit(y'_{i,j})_2)_ℓ`，其中 `Commit(·)_2=Bs₂+m` | 从 BDLOP 分量导出"评价值 + 未打开盐和"；不传输、不额外泄露 |
| 12 | V（**派生**） | 锚定目标（P6 Step 17） | `u⋆:=h−eq(r⃗',α⃗)(cF+δ₀cN)−δ₁cE` | 等于 `ζp(r⃗')−ct(B·s_{2,Q})` 型表达式；V 侧组装 |
| 13 | V↔P | 最终评价锚定 PoK（P6 Step 18） | `Π_anc` with weights `w_n`（含 `eq(r⃗',α⃗)γ_i^{(1)}`、`δ₀`、`δ₁eq(r⃗',r⃗)γ…`、`ζR_m` on `s_{P,2}`），公开 `u=Σ_n w_n(tB^{(n)})_{ι(n)}−u⋆`；由 Lemma 3.10（式 3.1′）化为 `ct(Σ_n w_n m^{(n)}_{ι(n)})−u=0` | 认证 `h−ζp(r⃗')=Q(r⃗')` 于承诺层，`p(r⃗')` 永不打开（这是与 Libra 原版的**关键区别**，Remark 4.2(8)） |
| 14 | V↔P | RLC 输入 PoK（P7 Step 1） | `Π_many^{(1)}` on `{y_{i,j}}_{i∈[K+k],j∈[t]}`（可批，Remark 4.4） | 绑定待折叠提示 |
| 15 | P（本地） | **RLC mask + Salt 承诺**（P7 Step 3–6） | `y←D_s^{n_F}`（**先于** `ρ⃗` 采样）；`c_y=L(y), x_y=L_in(y), y_{y,j}=M̄_j ŷ(r⃗)`；`C_{y,j}=Commit(y_{y,j},s_{1,y,j},s_{2,y,j})`；`C_{y,0}=Commit((c_y,x_y),s_{1,y,0},s_{2,y,0})`（`Ñ=⌈(κ+n_{R,in})/ℓ⌉` 个承诺的元组，Remark 4.21） | 用独立于 `v` 的高斯 mask 隐藏折叠结果；Ajtai 像不 hiding，故 `C_{y,0}` 用 ABDLOP 承诺并仅在接受时打开（Remark B.9） |
| 16 | P→V | mask 承诺（P7 Step 7） | 送 `C_{y,0}`、`{C_{y,j}}_{j∈[t]}` | pre-challenge 固定 mask |
| 17 | V→P | 折叠挑战（P7 Step 8，循环内每轮重采） | `w←w+1`；若 `w>W_max` 输出 ⊥ 并 halt；否则 `ρ₁,…,ρ_{K+k}←C` | 强采样集保证范数；`W_max` 为 verifier 可执行的最坏情况预算 |
| 18 | P（本地） | 折叠 + **Rejection Sampling**（P7 Step 9–11） | `v=Σ_i ρ_i z_i`；`z=v+y`；`Rej1(z,v,s)` 接受（接受率 `∈((1−2^{−λ})/M, 1/M]`） | 使 `z` 的条件分布与 `ρ×D_s^{n_F}` 统计距离 `≤2^{−λ}`，模拟器可复现（Lemma 3.20） |
| 19 | P→V / V | 打开 mask-block（P7 Step 12–14） | P 送 `(c_y,x_y),s_{1,y,0},s_{2,y,0}`；V 查 `C_{y,0}=Commit((c_y,x_y),·)` 且 `‖s_{l,y,0}‖∞<B̃`，`break`；拒绝则整块重采 | 绑定 mask 于挑战之前；拒绝轮只留 hiding commitments |
| 20 | V↔P | 折叠后 PoK（P7 Step 17） | `Π_many^{(1)}` on `y_{y,j}` | 供提取盐 |
| 21 | V / P | 折叠实例（P7 Step 18–20） | `c=Σ_iρ_i c_i + c_y`，`x=Σ_iρ_i x_i + x_y`；`s_{1,j}=Σ_iρ_i s_{1,i,j}+s_{1,y,j}`、`s_{2,j}` 同理；`y_j=Σ_iρ_i y_{i,j}+y_{y,j}`，送 `Commit(y_j)` | `mask y` 不被任何 `ρ_i` 缩放，只加法进入 |
| 22 | V | 同态检查（P7 Step 21） | `Commit(y_j) = Σ_{i∈[K+k]}ρ_i Commit(y_{i,j}) + C_{y,j}`，∀j∈[t] | ABDLOP 同态性（`B<B_com` ⇒ 盐界安全） |
| 23 | P（本地）→V | **分解 + 盐重采**（P8 Step 1–3） | `(z₁,…,z_k)←split_b(z)`；`c_i=L(z_i)`、`y_{i,j}=M̄_j ẑ_i(r⃗)`；每 `(i,j)` **fresh** `s_{i,j}=(s_{1,i,j},s_{2,i,j})`（`‖s_l‖∞<B̃`），`C_{i,j}=Commit(y_{i,j},s_{i,j})`；送 `{(c_i,{C_{i,j}})}` | 范数从 `B=b^k` 降回 `b`；盐重采样而非分解，避免约 17 个高位盐为零导致承诺退化（Remark 4.5, p.44） |
| 24 | V | 分解检查（P8 Step 4–5） | `(x₁,…,x_k)←split_b(x)`；`c=Σ_{i∈[k]}b^{i−1}c_i`；单个 `Π_many^{(1)}` on `N_c=(k+1)t` 盐块，`u=0`、`R₁=0`、`R_m` 第 j 行 `(1,−1,−b,…,−b^{k−1})`，证 `y_j−Σ_i b^{i−1}y_{i,j}=0` | 用消息层恒等式认证分解，盐界为 relaxed（Remark 4.8） |
| 25 | V | 接受与输出（P8 Step 6；Protocol 12 Step 3） | 接受 iff P8 步 4、5 均接受；返回 `(s; c'_i,x'_i,r',{Commit(y'_{i,j},s'_{i,j})};{y'_{i,j}},z'_i)_{i∈[k]}` | 输出 `CE_com(b,L,B̃,Commit,T,K)^k` |

> **挑战生成顺序（全部由 V 采样）**：`α⃗, γ⃗^{(1)},γ⃗^{(2)},γ⃗^{(3)}, (δ₀,δ₁)`（步 1）→ `ζ∈K^×`（步 4，在 `p` 承诺后）→ `r⃗'`（步 7 SumCheck 内）→ `{µ_ℓ}_{ℓ=2}^d`（步 9）→ `ρ₁..ρ_{K+k} ← C`（步 17，每个 Rej1 轮重采）。ABDLOP PoK 内部挑战（`γ⃗∈K^N`、`c̄` 差）由各自子协议生成。`[论文事实: 同上各 Protocol Step]`

---

## 3. 最终公开声明与"V 实际看到什么"

`[论文事实: §4.1.1.1, p.39–40]`

- **传输给 V**：Sum-Check 轮多项式及 `h=(ζp+Q)(r⃗')`；`σ=ζP+T`；所有 ABDLOP/Ajtai 承诺；所有挑战；`C_{y,0}` 接受时的打开 `(c_y,x_y,s_{1,y,0},s_{2,y,0})`。
- **V 派生、不传输**：`cF,cN,cE`（步 11）、`u⋆`（步 12）——是所传输承诺的确定性函数，不额外泄露。
- **从不揭示**：mask `p` 及 `p(r⃗')`；`Q(r⃗')`、`F(r⃗')`、`NC(r⃗')`、`Eval(r⃗')`；每个 `y'_{i,j}`/`ŷ_{i,j}` 及其平方/立方/乘积；所有承诺盐。由 fresh salt 下 MLWE hiding 及模拟器替换（§4.1.1.1；Theorem 4.13 证明 hybrid H1）。

`[论文事实: Definition 3.25, p.35]` 输出关系 `CE_com(b,L,B̃,Commit,T,K)^k` 是 `CE_com(b,L,B̃,Commit)^k` 的子集：把 `k` 个输出按 `z=Σ_{i∈[k]}b^{i−1}z_i` 重组后满足 `‖z‖∞ ≤ τ_{λ,ξ}·s`（`s=ξ(K+k)T(b−1)√n_F`）。这一条把 rejection sampling 的统计尾界写进了关系本身，是诚实输出与模拟器输出共同落入的集合。

**最终声明的准确形态**（`[推导]`，直译输出关系 `CE_com` 各 clause，Definition 3.21, p.33）：
公开：`{c'_i∈C, x'_i∈F^{n_{F,in}}, r'∈K^{log₂m}, {C'_{i,j}=Commit(y'_{i,j},s'_{i,j})∈R_F^{κ_com}}_{j∈[t]}}_{i∈[k]}`；
秘密：`{z'_i∈F^{n_F}, {y'_{i,j}∈R_K}_{j∈[t]}, {s'_{i,j}=(s'_{1,i,j},s'_{2,i,j})}}_{i∈[k]}`；
条件：`c'_i=L(z'_i)` ∧ `x'_i=L_in(z'_i)` ∧ `‖z'_i‖∞<b` ∧ `‖s'_{i,j}‖∞<B̃` ∧ `y'_{i,j}=M̄_j ẑ'_i(r')` ∧ `C'_{i,j}=Commit(y'_{i,j},s'_{i,j})` ∧（Definition 3.25 的重组范数条件）。

---

## 4. 安全性结论与其精确条件（不可外推）

`[论文事实: Theorem 4.13, p.48; Theorem A(2)–(3), p.6]`

1. Π_LBF（Protocol 12）是 **reduction of knowledge**：完备性误差 `ε_LBF^c ≤ [7+(K+k+1)t]·2^{−λ}`（unbatched；§4.1.2.1 batched 默认 `9·2^{−λ}`），knowledge-soundness 误差见 Proposition 4.17。
2. **Blinding（=本设定下的 honest-verifier ZK）仅当**：`K=1`、结构满足 blinded layout、限制到 `CE_com(...,T,K)^k`、并把 `ι_bl` 预复合到未填充输入 `R'=CCS°(b)^K`。此时存在仅输入 `(pp,s,x₁)` 的 EPT 模拟器 `S'`，区分优势 `ε^{LBF-blind}=N_PoK^{zk}ε^{zk}_ABDLOP + (W_max+2)t·ε_hide + W_max·ε_hide,0 + O(W_max 2^{−λ}) + ε_{L-hide}`，`N_PoK^{zk}=4+2t`（式 4.6, p.48）。默认 regime (1) 下 `ε_{L-hide}≤2^{−128}` 为统计项。
3. **不成立的推论**：`K>1` 的 blinding 未证；单次 step ≠ folding scheme；交互 ≠ 非交互（§4.5 需 `K=F_{q⁴}`，round-by-round KS 未证）；blinding ≠ knowledge soundness；`ε^{LBF-blind}` 不是零而是具体小量（在这些参数下约 `2^{−112}`，Remark 4.23, p.56–57）。

`[推导]` 类型归类：整体 blinding 是 **computational ZK**（含 Extended-MLWE/MLWE 优势项）；其中 masking 转录本身是 **perfect**（§4.1.1.1 "the masking is perfect"，模拟器零代价），`ε_L-hide` 在 regime (1) 是 **statistical**；不能笼统写成 perfect ZK 或 statistical ZK。

---

## 5. 六个核心问题的直接回答（任务包 §一）

1. **SuperNeo 原始 Folding 泄漏什么？** `[论文事实: §3.1, p.20; 作者博客 2026-06-19]` (a) 输入 `c₁=L(z₁)` 是 witness 的确定 Ajtai 像（Ajtai 不 hiding，Remark 2.29）；(b) Sum-Check 轮多项式泄露部分求值；(c) 明文评价提示 `y'_{i,j}=M̄_j z_i(r⃗')` 是 witness 在随机点的线性函数。诚实但好奇的 verifier 跨轮累积可恢复结构信息。
2. **Polynomial Masking 如何改变 Sum-check？** `[论文事实: §3.4, p.30–31; Protocol 6 Step 3–8, p.37]` 加私有 `p(X⃗)=a₀+Σ_i p_i(X_i)`（与 `Q` 同 partial degrees），承诺 `p` 后取 `ζ`，对 `ζp+Q` 跑 Sum-Check，声明和 `σ=ζP+T`。**决定性差别**：最终在承诺层认证 `h−ζp(r⃗')=Q(r⃗')`，`p(r⃗')` 永不打开，故不重演 Libra 原版 `f(r⃗)=h−ρg(r⃗)` 的残余泄漏（Remark 3.18(1) / CFW26）。详见 `04`。
3. **ABDLOP 如何隐藏 Evaluation Hints？** `[论文事实: Protocol 6 Step 9–18; Lemma 3.10, p.25]` 每个 `y'_{i,j}` 连同 fresh 盐 `s'_{i,j}` 被承诺；验证者从 BDLOP 分量 `Bs₂+m` 派生 `cF,cN,cE,u⋆`，通过 salt-substitution 化为承诺消息上的常数项线性关系，用 ABDLOP ZKPoK 认证；所有 `ct/cf` 评价以公开线性泛函方式实现（Lemma 3.12/3.13）。详见 `05`。
4. **Rejection Sampling 解决什么？** `[论文事实: §3.6, p.32–33; Protocol 7 Step 3–14]` 折叠 `z=v+y` 中 `v` 依赖 verifier 挑战 `ρ⃗`，故 `v` 的分布依赖真实 witness；高斯 `y` 在 `ρ⃗` 前独立采样，Rej1 使条件分布 `(v,z)` 与 `ρ×D_s^{n_F}` 统计距离 `≤2^{−λ}`，从而使**包括被拒轮在内的整个视图**可模拟（Remark 2.12 / B.9）。代价：`k=Θ(log n_F)`。详见 `06`。
5. **最终输出哪些承诺求值声明？** 见上文 §3：`k` 个 `CE_com` claim，每个含 `C'_{i,j}=Commit(y'_{i,j},s'_{i,j})` 与公开 `r'`、承诺 `c'_i`，并附 ABDLOP PoK 转录（`N_PoK=5+(K+k+1)t`，p.51）。**输出的是承诺 + 认证转录，不是已验证的最终声明**。
6. **"缺少 Decider" 的准确含义？** `[论文事实: §4.3.3, p.52; §5 item (2), p.59]` Π_LBF 停在"k 个承诺评价声明 + ABDLOP openings/PoK 转录"；把它变成可部署 wrapper 需要某组件**简洁地检查这些声明**。作者给两条路：(i) 直接把 openings 交下游 verifier 线性扫描；(ii) 算术化 ABDLOP 验证方程 `tA=A₁s₁+A₂s₂, tB=Bs₂+m` 及 masked-opening 范数检查，放进更深的 R1CS（约 `Θ(N_c(m₁+m₂)d)` 环运算），"we instantiate neither, and record the gap as such"。障碍是范数检查需要 `[LNP22, §5.2]` 的 exact-ℓ₂ 证书，而单次调用只得到 relaxed bound。详见 `07`。

---

## 6. 与本仓库已有笔记的关系

- `docs/01-superneo-reading-notes.md` 中"Π_DEC = decomposition reduction"的防混淆条目**继续有效**：本文 Π′DEC（Protocol 8, p.43）确为 decomposition reduction，与"Decider"是两件事。
- `docs/02-latticeblindfold-reading-notes.md` 的待核查清单已在本文件与 `04`–`07` 中逐项回答；该文件仅做状态更新，不改动既有正确表述。
- 教学实验 `experiments/hint_leakage_demo.py` 与本文件的数学结论无关；不得把它当成对 LatticeBlindFold 的攻击示例。
