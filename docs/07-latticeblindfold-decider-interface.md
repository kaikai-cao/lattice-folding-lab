# LatticeBlindFold 最终声明与 Decider 接口提取

> 状态：LB-01 / 任务 E 完成。**本文件不设计新 Decider**，只从 LBF 的最终输出反向整理接口与缺口，供下一阶段使用。
> 主来源：`[LBF]` = Luca Dall'Ava, *LatticeBlindFold: A Lattice-Based Analogue of NovaBlindFold*, ePrint 2026/1857, 2026-09-01；关键位置：Abstract (p.1)、§1.3 (p.5–7)、Definition 3.21/3.25 (p.33/35)、Protocol 12 (p.45–46)、§4.2.1 (p.46–47)、§4.3.3 (p.51–53)、§5 (p.59)、§4.5 (p.58–59)。
> 对照来源：`[NS26]` SuperNeo ePrint 2026/242（其 `Π_DEC` = decomposition reduction）；`[LKP22]/[LNP22]` LaBRADOR / ePrint 2022/284；`[LBF]` §4.3.3 与 §5 对两个 Decider 路线的原话。
> 标签：`[论文事实]` / `[实现事实]` / `[推导]` / `[研究假设]` / `[待核查]`。

---

## 0. 先精确界定"Decider 缺口"

`[论文事实: LBF Abstract, p.1]`
> "the LatticeBlindFold step is a single interactive step, taking its input uncommitted and outputting k committed evaluation claims together with the ABDLOP openings certifying them. Turning it into a deployable wrapper requires a decider for those claims, whether by having a downstream verifier consume them directly or by arithmetizing the ABDLOP verification; we do not construct one here, and neither recursive composition nor the instance-in/instance-out folding interface is claimed."

`[论文事实: LBF §4.3.3, p.52]`
> "Π_LBF terminates with k pairs in CE_com(b,L,B̃,Commit,T,K)^k and with the transcripts of N_PoK = 5+(K+k+1)t ABDLOP proofs of knowledge; a verifier convinced by them is convinced of the original R1CS statement, but only after checking them. Read as NovaBlindFold is read, this leaves a decider to be supplied, and there are two ways to supply it. The direct one hands the openings to the downstream verifier unchanged and a linear scan of them. The succinct one arithmetizes the ABDLOP verification equations tA = A₁s₁ + A₂s₂, tB = Bs₂ + m together with the masked-opening norm checks, and proves them inside a further R1CS instance; that circuit is Θ(N_c(m₁+m₂)d) ring operations and the norm checks are its awkward part, being the same exact-ℓ₂ machinery Remark 4.8 needs. **We instantiate neither, and record the gap as such.**"

`[论文事实: LBF §5 item (2), p.59]`
> "A decider for the output claims. As recorded in §4.3.3, Π_LBF stops at k committed evaluation claims plus their ABDLOP openings, and a deployable zero-knowledge wrapper needs something that checks them succinctly. The natural candidate is to arithmetize the ABDLOP verification, since its linear part is already R1CS-shaped over R_F and the componentwise instantiation of §3.3 keeps it over the base ring; the obstruction is the norm checks, which want the exact ℓ₂ certificate of [LNP22, §5.2] rather than the relaxed bounds a single invocation gets away with. Solving it would also unblock the recursive branch of Protocol 13, the two needing the same certificate (Remark 4.8), and we regard it as the main missing piece between this paper and a deployable implementation."

**一句话**：缺口不是"某个求值声明还没被证明"，而是**缺乏一个简洁组件来验证那 k 个已被承诺、并附 ABDLOP 转录的求值声明**；其技术障碍是范数检查需要 exact-ℓ₂ 证书（单次调用只给 relaxed）。

---

## 1. 公开输入（Verifier / Decider 可见）

`[论文事实: Definition 3.21, p.33; Definition 3.25, p.35; Protocol 12 Output, p.45–46]` `[推导]` 逐 clause 整理：

| 符号 | 含义 | 来源 |
|---|---|---|
| `pp`（含 `A₁,A₂,B` 等公钥矩阵）、结构 `s` | 公共参数与结构 | §2.1 / Definition 2.2 |
| `λ, q, F, K, R_F, R_K, Φ=X^d+1, d, m, n_F, n_{F,in}, u, t, b, B=b^k, C, T` | 全局参数 | Definition 2.2, p.10 |
| `{c'_i ∈ C}_{i∈[k]}` | 折叠输出的 compact Ajtai 承诺 | Protocol 12 Output |
| `{x'_i ∈ F^{n_{F,in}}}_{i∈[k]}` | 折叠输出的公开输入 | 同上 |
| `r' ∈ K^{log₂m}` | 最终 evaluation point（公开） | 同上 |
| `{C'_{i,j} = Commit(y'_{i,j}, s'_{i,j}) ∈ R_F^{κ_com}}_{i∈[k], j∈[t]}` | **k·t 个 committed evaluation hints**（核心输出声明） | 同上 |
| `{Commit(y'_{i,j})}` 的 BDLOP 分量 `Bs'₂+m`（已隐含在承诺中） | 用于 salt-substitution 检查 | Lemma 3.10, p.25 |
| ABDLOP PoK 转录 `N_PoK=5+(K+k+1)t` 份（Protocol 6 Steps 7,12,15,18；Protocol 7 Steps 1,17；Protocol 8 Step 5 等） | 认证上述承诺关系的 argument | §4.3.3, p.52 |
| 各挑战 `α⃗, γ⃗^(1..3), δ₀,δ₁, ζ, r⃗', {µ_ℓ}, ρ⃗`；`cF,cN,cE,u⋆`（V 派生）；`W_max` 与接受/拒绝模式 | 转录中的公开量 | Protocol 6/7/8 |

`[推导]` Decider 至少能拿到上面全部"公开 + 转录"信息；简洁 Decider 的目标是把这些转录**压缩**成对 `{c'_i, x'_i, r', C'_{i,j}}` 的一个短证明，而不是逐个验证 N_PoK 份 PoK。

---

## 2. 秘密见证（Prover / 模拟器持有）

`[论文事实: Definition 3.21/3.25, p.33/35; Protocol 12, p.45]`

| 符号 | 含义 | 约束 |
|---|---|---|
| `{z'_i ∈ F^{n_F}}_{i∈[k]}` | 折叠后的 witness 向量 | `‖z'_i‖∞ < b`；重组 `z=Σ_i b^{i−1}z'_i` 满足 `‖z‖∞ ≤ τ_{λ,ξ}·s`（Definition 3.25） |
| `{y'_{i,j} ∈ R_K}_{i∈[k],j∈[t]}` | evaluation hints | `y'_{i,j} = M̄_j ẑ'_i(r')` |
| `{s'_{i,j} = (s'_{1,i,j}, s'_{2,i,j}) ∈ R_F^{m₁}×R_F^{m₂}}` | ABDLOP 承诺盐 | `‖s'_{1,i,j}‖∞, ‖s'_{2,i,j}‖∞ < B̃`（=2 三元） |
| `w_circ`、`e`（blinding block） | 原始 R1CS witness + 后采盲化块 | `e←χ_b^{n_{R,bl}}`，`z₁=[x₁,w_circ,e]` |
| 各 PoK / mask / RLC 内部随机 | 模拟所需的辅助 opening | 不公开 |

---

## 3. 需要验证的关系（拆为独立等式）

`[论文事实: Definition 3.21, p.33; §3.5 式 (3.13), p.32; Remark 4.8, p.47; §4.3.3, p.52]` `[推导]` 每一项按"公开变量 / 秘密变量 / 依赖承诺 / 依赖安全性质"标注。

| # | 等式 | 公开变量 | 秘密变量 | 依赖承诺 | 依赖性质 |
|---|---|---|---|---|---|
| R1 | `c'_i = L(z'_i)` | `c'_i`, `pp`(L) | `z'_i` | compact Ajtai `c'_i` | Ajtai relaxed binding（MSIS）；**不是** hiding（靠 blinding block） |
| R2 | `x'_i = L_in(z'_i)` | `x'_i` | `z'_i` | — | 投影同态 |
| R3 | `‖z'_i‖∞ < b`，且重组 `‖Σ_i b^{i−1}z'_i‖∞ ≤ τ_{λ,ξ}s` | `b,τ,s,k` | `z'_i` | — | 范数检查；统计尾界（Lemma 3.19/§3.6）；Definition 3.25 |
| R4 | `y'_{i,j} = M̄_j ẑ'_i(r')` | `M̄_j, r'` | `y'_{i,j}, z'_i` | — | Sum-Check reduction（对正确 `r'` 由 Π′R1CS 保证） |
| R5 | `C'_{i,j} = Commit(y'_{i,j}, s'_{1,i,j}, s'_{2,i,j})` | `C'_{i,j}`, `A₁,A₂,B` | `y'_{i,j}, s'_{1,i,j}, s'_{2,i,j}` | ABDLOP `C'` | hiding（MLWE）；binding（MSIS） |
| R6 | `tB'_{i,j} = B s'_{2,i,j} + y'_{i,j}`（R5 的 BDLOP 分量） | `tB'_{i,j}`（公开承诺分量） | `s'₂, y'` | ABDLOP | salt-substitution（Lemma 3.10） |
| R7 | 最终 `h − ζ p(r⃗') = Q(r⃗')` 在承诺层成立 | `h, ζ, r⃗', cF,cN,cE, u⋆, {C'}` | mask `p`/`p(r⃗')`, 所有盐 | mask 承诺 `Commit(coeffs,s_P)` + hint 承诺 | ABDLOP ZKPoK/HVZK；`p(r⃗')` 由式 (3.13) 作公开线性泛函，不打开 |
| R8 | ABDLOP 验证：`tA=A₁s₁+A₂s₂, tB=Bs₂+m`（对所有需要的承诺） | `tA,tB`, 矩阵 | `s₁,s₂,m` | 全部 ABDLOP 承诺 | MSIS binding + MLWE hiding；**范数检查是难点** |
| R9 | 附带的 PoK 转录（`N_PoK` 份）均被验证通过 | 转录与挑战 | 各 opening/随机 | — | ABDLOP PoK knowledge soundness（`ε^(1)_ABDLOP` 等） |

`[推导]` **R8 中的范数检查**是 Decider 的关键：论文 §4.3.3/§5 明说，linear 部分 `tA/tB` 已是 `R_F` 上的 R1CS 形状，component-wise 实例化（§3.3）让它留在基环；但范数检查需要 `[LNP22, §5.2]` 的 exact-ℓ₂ 证书——而 Π′DEC 的 relaxed 界（`β^rlx`，Definition 3.22）对**单次调用**够用，对递归/Decider 不够（Remark 4.8）。

**最终输出关系的准确定义（写可复核版）**：
```
Public:  pp, s, {c'_i, x'_i}_{i∈[k]}, r'∈K^{log₂m},
         {C'_{i,j}=Commit(y'_{i,j}, s'_{i,j}) ∈ R_F^{κ_com}}_{i∈[k],j∈[t]},
         (+ ABDLOP PoK transcript T_pok, challenges, W_max, derived cF/cN/cE/u⋆)
Witness: {z'_i∈F^{n_F}, {y'_{i,j}∈R_K}_{j∈[t]}, {s'_{i,j}=(s'_{1,i,j},s'_{2,i,j})}}_{i∈[k]}
Relation CE_com(b,L,B̃,Commit,T,K)^k:  ∀i∈[k]:
   c'_i = L(z'_i) ∧ x'_i = L_in(z'_i) ∧ ‖z'_i‖∞<b
   ∧ ‖s'_{i,j}‖∞<B̃ ∧ y'_{i,j}=M̄_j ẑ'_i(r') ∧ C'_{i,j}=Commit(y'_{i,j},s'_{i,j})  ∀j∈[t]
   ∧ (Definition 3.25) ‖Σ_i b^{i−1} z'_i‖∞ ≤ τ_{λ,ξ}·s
```
`[推导]` 这是 Decider 要"简洁验证"的对象；它是**承诺求值关系**，不是原始 R1CS 关系，也不是 NovaBlindFold 意义下已折叠好的单个 instance。

---

## 4. Decider 缺口：逐问精确回答

### 4.1 原论文目前已经完成了什么？

`[论文事实: Theorem 4.13, p.48]` Π_LBF 是 reduction of knowledge，完备性误差 `ε^c ≤ 9·2^{−λ}`（batched），knowledge-soundness 误差 `ε_LBF`（Prop 4.17）；在 `K=1`、blinded layout、unpadded relation、单步条件下是 blinding（computational ZK）。§3.3 component-wise ABDLOP、§3.2 常数项 PoK 工具、§3.4 masking、§3.6 rejection sampling 均已给出并证明。

### 4.2 哪些求值声明已经可以验证？

`[论文事实: Protocol 6 Step 18 锚定 PoK; Protocol 7 Step 21; Protocol 8 Step 4–5]` 在一次 Π_LBF 执行内，通过 ABDLOP ZKPoK 与同态检查：
- 掩码 Sum-Check 的最终评价关系（R7：`h−ζp(r⃗')=Q(r⃗')` 在承诺层）；
- RLC 折叠承诺一致性（`Commit(y_j)=Σρ_i Commit(y_{i,j})+C_{y,j}`）；
- Π′DEC 分解一致性（`y_j−Σ b^{i−1}y_{i,j}=0`）与 `c=Σ b^{i−1}c_i`。
`[推导]` 这些都由相应 PoK/检查**在协议运行时**验证；验证者"only after checking them"才相信原 R1CS 声明（§4.3.3）。即**单步内部的求值声明有验证路径**，只是路径冗长（N_PoK 份 PoK）。

### 4.3 哪些声明尚未得到最终验证？

`[论文事实: §4.3.3/§5]` 尚未被**简洁地**验证的是：**输出的 k 个 committed evaluation claims 本身**（R1–R9 组成的 CE_com 元组）——它们在协议结束时以"承诺 + 认证转录"形式交付，但没有一个组件把它们压缩成单个短的可验证声明。"a verifier convinced by them is convinced of the original R1CS statement, but only after checking them" = 若不做 linear scan / arithmetization，这些 claim 的"最终验证"没有被提供。

### 4.4 缺少的是验证算法、知识证明，还是递归组合接口？

`[推导]`，基于原文：
- **不是缺少证明这些声明的知识证明**：ABDLOP PoK 转录已经认证了它们；
- **缺少的是 (a) 简洁验证算法**（把 N_PoK 份 PoK/承诺检查压成可高效验证/可算术化的形式）+ **(b) 递归组合接口**：Protocol 13 的递归分支、instance-in/instance-out folding interface 与 Theorem 4.13 的 exact-ℓ₂ 证书是同一个缺口（§5 item(2)、Remark 4.8）。作者原话："Solving it would also unblock the recursive branch of Protocol 13"。
- 因此准确表述：**缺"简洁 Decider（含范数/exact-ℓ₂ 算术化）"，连带缺递归组合接口**；"缺少验证算法"只在"简洁算法"意义下成立。

### 4.5 为什么 SuperNeo 的 `Π_DEC` 不能直接解决这个问题？

`[论文事实: §2.4.2 Proposition 2.26, p.17; Protocol 8, p.43–44; Remark 4.8, p.47]` `[推导]`
- SuperNeo 的 `Π_DEC`（decomposition reduction）把范数 `B=b^k` 的声明分解为 `k` 个范数 `b` 的声明，使 CCS 声明可反复折叠；它是**协议内部的 reduction**，不是验证最终声明的 Decider。
- LBF 的 Π′DEC（Protocol 8）已经是 Π_DEC 的"带盐"版本：分解 witness 但**fresh 重采盐**、用 `Π_many^{(1)}` 在消息层证明分解恒等式，盐界为 relaxed（Definition 3.22）。
- `[论文事实: Remark 4.8]` 关键差异：Π′DEC 步 5 只认证 relaxed 意义下的盐（`‖c̄ s̄_j‖₂≤β^rlx`），提取器得到的是乘挑战差后的界，**不是** `‖s_j‖∞<B_fold`；对**单次调用**这正够用（诚实 prover 的输出 witness 范数是 RoK 定义的假设），但递归分支需要把输出作为下一轮输入，此时 relaxed 界不足，需 exact-ℓ₂ 证书。
- `[推导]` 所以 `Π_DEC` 解决的是"范数分解"，而 Decider 要解决的是"简洁验证已承诺的求值声明（含精确范数）"——两者目标不同；把 SuperNeo 的 Π_DEC 当成 Decider 属于概念混淆（`docs/01-superneo-reading-notes.md` 的防混淆条目仍然有效）。

### 4.6 能否利用 LaBRADOR 通用零知识证明工具构造候选 Decider？

`[研究假设 + 论文事实]`
- LaBRADOR（Beullens–Seiler, CRYPTO 2023, ePrint 2022/1341）与其 ZK Toolkit（ePrint 2026/1289, ACM CCS 2026）提供基于 Module-SIS 的简洁 ZK 证明；Toolkit 的官方摘要确认：把 `[LNP22, CRYPTO 2022]` 的线性大小 ZK 证明集成进 LaBRADOR，并扩展 LaZer 库，为任意大陈述输出 <100KB 级证明，已实现并 benchmark。
- `[论文事实: LBF §3.5, p.31–32]` LBF 作者明确考虑过 multilinear PCS（Hachi `[NOZ26]`）与 Greyhound（NS24）类 split-PCS，理由是"被承诺对象本身已经是对数大小，简洁性无关"，所以**没用 PCS 而用 ABDLOP**——这是对 folding 内部 mask 的理由，不直接排除外部 LaBRADOR 工具。
- `[论文事实: LBF §4.3.3/§5]` 作者给出的自然候选是**算术化 ABDLOP 验证**（其线性部分已 R1CS-shaped，component-wise 使其留在基环 `R_F`，正好可喂给模块格 ZK 系统），障碍是范数检查需 exact-ℓ₂ 证书。
- `[研究假设]` 因此**可以**把 LaBRADOR/LaZer ZK 工具视为候选 Decider 后端（对 R8 的 `tA=A₁s₁+A₂s₂, tB=Bs₂+m` 及范数约束做简洁 ZK 证明）；但这尚属接口匹配的推测，需要解决：(i) exact-ℓ₂ 范数证书（LNP22 §5.2）；(ii) ABDLOP 的非简洁承诺宽度（d=128 下 `κ_com=27`、单次证明约 23 KB/承诺）；(iii) 与 LBF 挑战/盐体系的安全模型拼接。本阶段**不**声称已构造或可行。

### 4.7 直接调用现有工具会造成什么证明大小、时间及安全模型问题？

`[论文事实: LBF §4.3.3.1, p.52–53; §4.3.4 Table 2, p.54; §4.5, p.58–59; Remark 4.26, p.59]` `[推导]`

| 维度 | 具体问题 | 原文依据 |
|---|---|---|
| **证明大小** | 单次 folding 已 ≈8.2 MB (d=128)/≈5.5 MB (d=64)，其中 masked openings 4.57/3.01 MB、输出 ABDLOP 承诺 1.98/1.19 MB；Decider 若直接逐项算术化这些承诺（`κ_com=27`、每次约 23 KB），证明规模与 folding 转录同阶，无法获得"简洁 wrapper" | §4.3.3.1 |
| **时间/电路规模** | 算术化电路约 `Θ(N_c(m₁+m₂)d)` 环运算；范数检查（exact-ℓ₂）是"awkward part"，且与递归所需证书同源 | §4.3.3 |
| **安全模型** | LBF 全部结果是**交互式**（honest-but-curious public-coin V*、blinding 定义含 abort）。直接接非交互工具需 Fiat–Shamir：`K=F_{q²}` 在 `q=2⁶⁴−59` 下任何密码学 Q 都不够，部署需 `K=F_{q⁴}`；round-by-round knowledge soundness **未证**（§5 item(3)），generic multi-round bound 在 log₂m=21 + N_PoK≈8 下为 vacuous；simulator 需 ROM 逐 attempt program hash（Remark B.10） | §4.5 / §5(3) / Remark B.10 |
| **grinding** | FS 下 `ε_cw^FS = Q(K+k)/|C|`：d=128 仍 ≈2^{−171}，d=64 ≈2^{−43}（致命）；d=64 参数集本就仅 ≈116 bits，非安全实例化 | Remark 4.26 / Remark 4.19 |
| **范数/承诺语义** | ABDLOP 消息任意范数 + 三元盐 vs LaBRADOR 工具的 ℓ₂/CRT 假设：需桥接 exact-ℓ₂ 与 relaxed bound；`β^rlx` 是唯一随 `N_c`（从而 k,t,ℓ）增长的界（Remark 4.22） | §3.3.4 / Remark 4.22 |

`[推导]` 结论：把现有工具**黑盒**套在 LBF 输出上，最可能得到的是"正确但巨大、且只在 ROM/FS 假设下成立"的 Decider；这恰恰是作者把 Decider 列为开放问题的原因。下一阶段若设计 Decider，必须显式处理 exact-ℓ₂ 证书与交互→非交互的安全模型迁移，不能只做接口拼装。

---

## 5. 接口边界与禁令（为下一阶段立规）

- `[论文事实]` Π_LBF 的输出是 `CE_com(...)^k` 元组 + PoK 转录；任何 Decider 必须针对这一具体关系，不要自行把输出改写为"单个已折叠实例"（论文明确不声称 instance-in/instance-out folding interface）。
- `[论文事实]` `K=1` 是 blinding 的前提；Decider 若依赖 blinding，须保留 `K=1`。
- `[论文事实]` `ε^{LBF-blind}≈2^{−112}` 是具体非零量；不得写成"完美零知识/误差 0"。
- `[论文事实]` Decider 缺口与 SuperNeo `Π_DEC`、与"知识证明是否已存在"是三个不同问题；不要混为一谈。
- `[研究假设]` LaBRADOR 候选仅为待验证方向；本阶段未证明其可行性、大小或安全模型兼容性。
- `[论文事实（LB-02 更新）]` `[LNP22, §5.2]` exact-ℓ₂ 证书已回原文核查，结论与兼容性分类见 `docs/08-exact-l2-certificate-mapping.md`；`[NS24]` Greyhound、`[NOZ26]` Hachi、`[CFW26]` 与 LaBRADOR Toolkit 的针对性排查见 `docs/10-recent-competition-update.md`。
- `[待核查]` `[KLSS23]` Hint-MLWE 仍只经 LBF 引用接触；若后续采用必须回原文。
