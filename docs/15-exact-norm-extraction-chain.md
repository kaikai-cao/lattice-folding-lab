# 15 · Exact-Norm 提取链与无 c̄ 累积判定

> LB-04 · 任务 D/E。日期：2026-11-20。
> 依赖：`docs/14`（s₂→LNP22 映射：PC=I 不成立、anchoring 仅标量、LBF 相反承诺约定）。
> 一手来源：LBF 镜像 `paper_mirror.txt`（行号 `LBF L####`）、LNP22 提取 `md_lnp22_asia/content.md`（行号 `LNP L####`）；镜像来源限制见 `docs/14` 开头。

---

## 1. 任务 D：两个 fresh salt 的证明目标

### 1.1 位置一：Protocol 8 Step 5（输出盐）

`[论文事实: LBF L2876, L2883–2893]` Protocol 8（分解归约 Π′DEC）Step 2 采样 fresh salt pair `s_{l,i,j}=(s_{1,i,j},s_{2,i,j})` 满足 `‖s_{l,i,j}‖∞ < B̃=2`，Step 5 对 `N_c=(k+1)t` 个承诺串接运行**单个** Π_many，`u=0, R₁=0`，`R_m` 为 t×N_c 块行矩阵，certify 消息恒等式：

```
y_j − Σ_{i∈[k]} b^{i−1} y_{i,j} = 0   for all j∈[t]
```

`[论文事实]` L2891–2893：`The message identity is exact by Lemma 3.6(3); the salt bounds are the relaxed ones of item (2), which is all one invocation of ΠLBF needs. Cf. Remark 4.8.` 即：**消息侧 exact，盐侧 relaxed**。

### 1.2 位置二：Protocol 7 Step 17（mask 盐）

`[论文事实: LBF L2775–2777]` Protocol 7（Π′RLC）Step 17：对每个 j∈[t]，对承诺 `y_{y,j} ∈ R_K` 运行 Π_many PoK（同 Π_many((s₂,s₁,m),f)）。mask 盐 `s_{l,y,j}` 随 `C_{y,j}=Commit(y_{y,j}, s_{y,j})` 承诺（LBF L2752、L3134）。

`[论文事实: LBF L3133–3135]` Remark 4.8 指定 exact 证书应 append 到：
- Protocol 8 Step 5，bound `k t(B̃−1)√((m₁+m₂)d)`；
- Protocol 7 Step 17 的 PoK，bound `(B̃−1)t√((m₁+m₂)d)`（"whose mask salts are subject to the same objection"）。

### 1.3 两个位置的证明目标骨架

`[推导]` 按任务包要求列出（凡 docs/14 判定不成立处标"受阻"）：

| 项 | Protocol 8 Step 5（输出盐） | Protocol 7 Step 17（mask 盐） |
|---|---|---|
| LNP22 exact 对象 | 需为 fresh salt s₂ 建消息槽承诺后作用（docs/14 §3.1）；**当前位置 Π_many 的对象是消息 (s₁,m)，不含 s₂ 本体** | 同左，对象是 mask 承诺消息 y_{y,j} |
| 公开矩阵/向量 E,v | `E_i, v_i, β_i^{(e)}` **未给出**——docs/14 证明无法从公开承诺构造恢复 s₂ 的 E；只能对新建消息承诺设 E（需额外结构） | 同左 |
| 范数界 | `‖s_{l,i,j}‖∞ < B̃=2`（采样，诚实）；relaxed `‖c̄s̄‖₂≤β_rlx`（提取）；exact 界 β 见 Remark 4.8 append bound，但**未实例化** | `‖s_{l,y,j}‖∞<B̃`，同上 |
| 二进制余量 x / integer lift | 若走 LNP22 Fig10：Eq.58 `⟨x',x'−1⟩=0`、Eq.59 `⟨E_is−v_i,E_is−v_i⟩+⟨p_i,x_i⟩=β²`、Eq.60 lift；但需先把 s₂ 变成 Fig10 的 s 分量 → **受阻** | 同左 |
| 提取对象 | Lemma 3.6 提取 `(s̄₁,s̄₂,c̄)`；消息恒等式 exact by (3)，盐 relaxed by (2) | Π_many 提取同结构 |
| 对应回 ABDLOP opening | `m̄=t_B−Bs̄₂`（Lemma 3.10）；s₂ 仅 binding 层，锚定消息侧 | 同结构，mask 承诺 opening |

`[推导]` **结论 D**：两个位置的现有 PoK 都是"**消息恒等式 exact + 盐 relaxed**"（LBF L2891–2893）。Remark 4.8 要求在盐侧追加 exact 证书，但 docs/14 已证明：**在现有承诺布局下无法构造以 s₂ 本体为对象的 E,v**（PC=I 不存在、anchoring 仅标量、LBF 消息在 BDLOP 槽）。因此这两个位置的 exact-norm 证明目标**只能写成"待定义"骨架**：需先新增消息槽承诺把 s₂ 提升为消息，才能套用 LNP22 Fig10 的 E/v/β/x/lift 机制。本文不写占位公式。

---

## 2. 任务 E：无 c̄ 累积提取链

### 2.1 LBF 声称的提取链（Remark 4.8）

`[论文事实: LBF L3135–3139]` 作者给出的理想链：
```
exact-ℓ₂ 追加 → 提取 salt 满足界无 c̄ 因子
              → binding of Commit 识别第 r 轮认证 opening 与第 r+1 轮提取 opening
              → nothing would accumulate
```

### 2.2 三问逐答

**问题 1：提取结果是否确实是同一个 s₂，而非仅具有相同线性像的另一个向量？**

`[推导]` **当前无法保证。**
- Lemma 3.6 提取 `(s̄₁,s̄₂,c̄)`，在 MSIS 下 `(s̄₁,s̄₂)` 唯一（LBF L1319），但这是**单个承诺内部**的唯一性（由 `A₁s̄₁+A₂s̄₂=t_A` 的 binding）。
- 跨承诺/跨轮识别需要 anchoring：Lemma 3.16 由 `ct(Σwₙm̄_{ι(n)})−u=0` 把 `σ,u★` 绑定到"同一 (m⁽ⁿ⁾,s₂⁽ⁿ⁾) underlying the commitments opened earlier"（LBF L2708–2714）。
- 但如 docs/14 §2.4 证明，anchoring 是**标量常数项泛函** `ct(ΣwₙBs₂)`，其核维数巨大（`m₂−(n+ℓ)` 量级）。因此 anchoring 只能保证"提取 s̄₂ 与该标量泛函一致"，**不能保证与完整原 s₂ 相同**——存在多个 s₂ 具有相同 `ct(ΣwₙBs₂)` 却范数迥异。
- 结论：**只能证明"同线性像"，不能证明"同向量"**。这是用户最担心的问题，且当前无法满足。

**问题 2：能否去掉 relaxed proof 中的 c̄ 因子？**

`[论文事实]` 在**消息侧**可以：Lemma 3.6(3) 的消息恒等式 `R₁s̄₁+R_m(t_B−Bs̄₂)=u` 对 s̄ 本身成立、无 c̄（LBF L2155–2157 "items (1) and (3) hold for s̄ itself"）。
`[推导]` 在**盐侧**：`‖c̄s̄₂‖₂≤β_rlx` 带 c̄，且 `c̄⁻¹` 不一定短（LBF L2158–2159），无法除掉得到 `‖s̄₂‖`。要去掉 c̄ 必须对 s₂ 本体建立 exact-ℓ₂（LNP22 Fig10 式 53/59），而这需要先解决 docs/14 的映射障碍（把 s₂ 变成消息）。**当前不能去掉**：salts 仍走 relaxed path。

**问题 3：相邻轮 binding 是否足以识别同一 opening、阻止范数逐轮放大？**

`[论文事实]` 单次调用中 binding 足够：Remark 4.8 说 relaxed 只影响 MSIS bound、blinding 不受影响（LBF L3124）；两 relaxed opening 给 `MSIS_{2β_rlx}` 解（LBF L2187–2191）。
`[推导]` 递归中**不足**：
- 每轮的 witness 来自上一轮提取器（LBF L3125–3127），其类型已从 tight `CE_com(B_fold)` 降级到 relaxed `CE_rlx_com(β_rlx)`（LBF L2859，Definition 3.22）；
- binding 保证"同一承诺的两个 opening 给出 MSIS 解"，但**不保证提取盐的范数不放大**——`‖c̄s‖≤β_rlx` 中的 c̄ 在下一轮再次累加（LBF L3127–3129）；
- 要截断放大链，需要每轮提取都带无 c̄ 的 exact 界（即问题 2 成立），而问题 1、2 当前都未满足。
- **结论**：相邻轮 binding 只能识别"同一承诺 opening"，**不足以阻止范数放大**；递归严格界未闭合。

### 2.3 β 链定性（保持示意性，不作已证明定理）

`[论文事实]` 论文只给定性陈述与单次接口因子：
- `β_rlx = 2s₂√(2N_c m₂ d)`（式 3.14，LBF L2168）；
- 接口处 `β_rlx⁽³⁾ = 2T₁(C)β_rlx`（式 3.15，LBF L2208），d=128 时 `2T₁(C)=29.6`（LBF L3694）；
- 每轮贡献 c̄（Lemma 3.6(2)）+ (ρᵢ−ρ'ᵢ)（Lemma 2.19），支撑 O(1) 轮（LBF L3127–3129）。

`[推导]` **示意性（非已证明递推定理）**：若把 relaxed 提取对象每轮复用，则量级上 `β_{r+1} ≈ 2T₁(C)·β_r ≈ 29.6·β_r`（d=128，约 +4.9 bit/轮），数轮逼近 q≈2⁶⁴ 上限。**必须强调**：论文只证明了"单次接口放大 2T₁(C)"与"O(1) 轮定性"，**没有逐轮提取证明**该几何递推；在问题 1/2/3 未闭合前，这个链只能是放大风险的示意，不能写成已证明的严格递推定理。若 exact-ℓ₂ 证书能实例化，则理论截断点仍是"提取 salt 无 c̄ + binding 识别同一 opening"（LBF L3135–3137），但该前提当前不成立。

### 2.4 提取链的总判定

```
accepting transcript
   → extracted opening (s̄₁,s̄₂,c̄)            [Lemma 3.6 ✓, 但带 c̄]
   → exact bound                              [✗ 受阻: docs/14 映射不成立, 盐侧无 exact]
   → next-round witness                       [✗ 类型降级为 relaxed, 范数逐轮放大]
```

**结论 E**：提取链在"extracted opening"之后断开——**无 c̄ 累积不成立**。仅能证明单轮的 relaxed 正确性，不能证明相邻轮绑定下的严格界。按任务要求，明确报告为**未闭合**，不写成递归已成立。

---

## 3. 本次修订落实

- `29.6^r` 链：全文标 `[推导]` 并明确"示意性、非已证明递推定理、论文只给定性与单次因子"，见 §2.3。
- toy demo 的 ℓ 说明不一致：已在 `experiments/s2_anchor_toy.py` 修正（见该文件或本轮 commit）。
