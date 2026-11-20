# LNP22 exact-ℓ₂ 证书与 LatticeBlindFold 的逐变量映射

> 状态：LB-02 / 任务 A 完成。本文件只做可行性审查，**不声称发明新的 exact-ℓ₂ 证书，也不构造新 Decider**。
> 主来源：`[LNP22]` = V. Lyubashevsky, N. K. Nguyen, M. Plançon, *Lattice-Based Zero-Knowledge Proofs and Applications: Shorter, Simpler, and More General*，full version of CRYPTO 2022，ePrint 2022/284（2022-03-07 received，2022-08-14 last revision）；§5.2（PDF p.41–47），Figure 8–10，Lemma 5.2，Equation (50)–(69)，Theorem 5.3，§6.1 证明尺寸公式（PDF p.48–50）。
> 对照来源：`[LBF]` = L. Dall'Ava, *LatticeBlindFold*，ePrint 2026/1857，§2.5.2、§3.2.1.1、§3.3.4、§3.5、§4.3.3、Remark 4.8、Remark 4.22、§4.5、§5；LB-01 已复原于 `docs/03`–`docs/07`。
> 来源限制：`[论文事实]` 指向 ePrint 正文的章节/页码/公式编号；正文 PDF 因 eprint.iacr.org 的 Cloudflare 限制使用公开镜像 `eprint.iacr.asia/2022/284.pdf` 获取，并与 `[LBF]` 对 `[LNP22]` 的原文转述交叉核对。正式投稿前仍应以 eprint.iacr.org 最终 PDF 再核对排版符号。
> 标签：`[论文事实]` / `[实现事实]` / `[推导]` / `[研究假设]` / `[待核查]`。

---

## 0. 结论先行

`[论文事实 + 推导]`

1. **LNP22 §5.2 确实已经有紧的 exact-ℓ₂ 证明**，不能把“发明 exact-ℓ₂ 证书”列为 LB-02 或后续研究贡献。它把内积写成环上多项式乘积的常数项，用二进制余量表示 `β²−‖e‖²`，再用近似 ℓ∞ 范围证明把 mod q 等式提升到整数，最终给出 `‖E_i s−v_i‖₂≤β_i^{(e)}` 的 tight bound（LNP22 §5.2，Eq. (53)(59)(60)，Theorem 5.3）。
2. **它不能被直接套到 LBF 上当成现成 Decider**。核心原因不是 LNP22 证书不存在，而是：
   - LBF 的承诺把消息放在 BDLOP 槽、两个小向量都作为盐；LNP22 的 exact norm machinery 主要证明承诺部分 `s=(s₁,m)` 及其自同构表示，而 LBF 递归缺口还必须精确认证 BDLOP randomness `s₂`（LBF Remark 4.8 原话：`s₂ (untouched by [LNP22]'s norm machinery, which targets the committed part (s₁,m))`）。
   - LBF 使用 `K=F_{q²}` 的 component-wise ABDLOP；LNP22 的 automorphism 恒等式依赖 `R_q=Z_q[X]/(X^d+1)` 上的 `σ(X)=X^{−1}`。对 `x=a+bY∈R_K`，LBF 的范数是 `‖a‖²+‖b‖²`，而 K 层自同构会给出 `‖a‖²+ν‖b‖²`；`ν≠1` 时不能直接套 K 层恒等式（LBF §3.3.4；LB-01 `docs/05` C4.4）。**LB-03 修订**：这不代表 R_K 上无法做 exact-ℓ₂——LBF §3.3.4 已给出正确翻译：对 a、b 分别在 base-ring 用 `σ⁻¹(a)a=‖a‖²` 证明，再联合约束 `‖a‖²+‖b‖²≤β²`，无需新协议机制。
   - Decider 要验证的是 `CE_com^k` 的 k 个承诺求值声明 + `N_PoK` 份 ABDLOP 转录；exact-ℓ₂ 只覆盖其中范数子句，不覆盖求值、承诺同态、盐替换、知识可靠性拼接与递归接口。
3. 因此兼容性分类为：**需要参数或格式调整，且部分子问题需要新的协议构造；不是“可直接使用”，也不是“数学上不兼容”。**

---

## 1. 为什么普通 ℓ∞ 证明不够，exact-ℓ₂ 在证明什么

### 1.1 ℓ∞ 与 ℓ₂ 的目标差异

`[论文事实: LNP22 Abstract, p.1; §1.1–1.2, p.2–3]`

传统代数格 ZK 通常证明 `‖s‖∞` 小：把 witness 系数的 CRT 表示承诺为一个多项式，再证明 `(m−1)m(m+1)=0`。LNP22 指出两条限制：

- CRT embedding 与特定环结构绑定，并给 soundness 带来额外约束；
- 很多格原语的 trapdoor sampling 与噪声天然给出 **tight ℓ₂ bound**，用 `‖s‖∞` 再乘 `√N` 会引入不必要松弛。

`[推导]` 对 LBF 而言，这个差异被进一步放大：LBF 的 relaxed ABDLOP PoK 只给提取盐一个随挑战差放大的界 `‖c̄ s̄_j‖₂≤β^rlx`，单次调用够用，但递归时每轮放大因子会累积（LBF Remark 4.8）。这里需要的不是“某个更大的 ℓ∞ 界”，而是可跨轮保持的精确界。

### 1.2 exact-ℓ₂ 陈述

`[论文事实: LNP22 §5.2, p.41, Eq. (50)–(54)]`

设 `R_q=Z_q[X]/(X^d+1)`，`s=(s₁,σ(s₁),m,σ(m))∈R_q^{2m₁}×R_q^{2ℓ}`，其中 `(s₁,m)` 是 ABDLOP 承诺的消息，`σ` 是环自同构。Figure 10 同时证明：

| 类型 | 公式 | 含义 |
|---|---|---|
| Rq 上二次关系 | `f_i(s)=0`, i∈[ρ] （50） | 一般二次约束 |
| 常数项二次关系 | `F_i(s)=0`, i∈[ρ_eval] （51） | 只证明乘积/和的常数项 |
| 近似 ℓ∞ | `‖D_i s−u_i‖∞≤β_i^{(d)}`, i∈[υ_d] （52） | 比真实界略松的 ℓ∞ 界 |
| **exact ℓ₂** | `‖E_i s−v_i‖₂≤β_i^{(e)}`, i∈[υ_e] （53） | 本任务核心 |
| binary | `E_bin s−v_bin∈{0,1}^{d k_bin}` （54） | 二进制约束 |

`[论文事实: LNP22 §5.2, p.42]` `β_i^{(e)}` 是**被证明的紧上界**；协议不泄漏真实范数，只证明其不超过 `β_i^{(e)}`。

---

## 2. exact-ℓ₂ 的完整推导链

### 2.1 第一步：内积 → 多项式乘积常数项

`[论文事实: LNP22 Abstract, p.1; §1.3, p.3; §5.2, p.42, Eq. (66)]`

LNP22 的核心观察：两个向量 `r,s` 的内积 `⟨r,s⟩` 可以做成两个（或多个）以 `r,s` 为输入的多项式乘积的某个系数；在 `R_q=Z_q[X]/(X^d+1)` 中，通过自同构 `σ(X)=X^{−1}`，该系数可取为常数项。Figure 8 的 `Π_eval` 能零知识地证明“承诺消息上的二次函数常数项为 0”，因此可证明：

```
⟨E_i s−v_i, E_i s−v_i⟩ mod q = c
```

其中 `c` 是公开常数或由公开量表示的值。`[推导]` 这一步仍只发生在 `Z_q` 上，不能直接推出整数范数界，因为 mod q 可能 wraparound。

### 2.2 第二步：用二进制余量编码非负差

`[论文事实: LNP22 §5.2, p.42, Lemma 5.2 与证明]`

Lemma 5.2：

```
x ∈ Z^n,  ⟨x, x−1_n⟩ = 0  ⇒  x ∈ {0,1}^n.
```

证明逐项成立：`x_j(x_j−1)≥0` 对所有整数 `x_j` 成立，内积为 0 当且仅当每项为 0。

LNP22 用该引理证明两类 binary：

- exact-ℓ₂ 的余量向量 `x_i`；
- 式 (54) 中的 `E_bin s−v_bin`。

两者拼接为 `x′ = x ‖ (E_bin s−v_bin)`，并同时证明：

```
⟨x′, x′−1_{(υ_e+k_bin)d}⟩ = 0 mod q        （58 的 mod q 部分）
‖x′‖ ≤ B                                   （Figure 10 的近似 ℓ∞ 检查）
```

若 `B²+√((υ_e+k_bin)d)·B < q`，则 mod q 等式无 wraparound，按 Lemma 5.2 得 `x′` 在整数上 binary。

### 2.3 第三步：余量的二进制分解与 Eq. (59)

`[论文事实: LNP22 §5.2, p.42–43, Eq. (59); Proof of Theorem 5.3, p.45–46]`

对每个 exact 范数约束，prover 取

```
r_i = (β_i^{(e)})² − ‖E_i s−v_i‖₂² ≥ 0.
```

将 `r_i` 写成二进制向量 `x_i`，长度至多 `2 log₂ β_i^{(e)} ≤ d`；令 `p_i` 为对应 2 的幂次向量，则

```
⟨p_i, x_i⟩ = (β_i^{(e)})² − ⟨E_i s−v_i, E_i s−v_i⟩.
```

因此得到 Eq. (59)：

```
⟨E_i s−v_i, E_i s−v_i⟩ + ⟨p_i, x_i⟩ = (β_i^{(e)})²  mod q.
```

`[推导]` 若 `x_i` 是 binary 且等式在整数上成立，则右侧与平方范数之差是非负整数，故 `‖E_i s−v_i‖₂² ≤ (β_i^{(e)})²`，即式 (53)。注意这里证明的是 `≤β_i^{(e)}`，不需要、也不打开真实范数。

### 2.4 第四步：从 mod q 提升到整数

`[论文事实: LNP22 §5.2, p.42–43; Theorem 5.3, p.44–46; Figure 9 近似范围证明]`

提升依赖两组条件：

1. **binary 判定不 wraparound**：`B²+√((υ_e+k_bin)d)·B < q`；
2. **Eq. (59) 不 wraparound**：`2(max_i β_i^{(e)})² + (B^{(e)})² − 1 < q`；
3. **挑战矩阵 Lemma 2.9 条件**：`B^{(e)} < q^{1/(4c^{(e)})}`；
4. `t≥1.64` 时尾部概率 `≤2^{−128}`。

Theorem 5.3 原文条件（OCR 符号整理）：
```
B^{(d)} := 2⁸·√(337·γ^{(d)}·α^{(d)}),
B^{(e)} := 2·√(256/26)·t·γ^{(e)}·√(337·α^{(e)})   [以原 PDF 排版为准，见 §6 注]
B^{(e)} < q^{1/(4c^{(e)})},
(B^{(e)})² + √((υ_e+k_bin)d)·B^{(e)} < q,
2(max_i β_i^{(e)})² + (B^{(e)})² − 1 < q.
```
`[待核查]` `B^{(e)}` 的常数因子来自 PDF 文本提取，符号存在 detached glyph；使用具体参数前必须回 PDF 页面视觉核对。这不影响本文的结构性结论。

### 2.5 第五步：近似 ℓ∞ 范围证明的作用

`[论文事实: LNP22 Figure 9, p.40–41; §5.2, p.42, Eq. (61)(64)(65)]`

Figure 9 的 approximate range proof 不是最终要证明的范数界，而是用来证明：

- `e^{(d)} = (D_i s−u_i)_i` 与 `e^{(e)} = (E_i s−v_i)_i` 的中间计算在 mod q 下没有 wraparound；
- 其 ℓ∞ 界足够小，使后续从常数项/内积关系推断整数关系时成立。

它给出的是 `β_i^{(d)}`、`α^{(e)}`、`B^{(e)}` 这类“比真实值松”的界；紧的 `β_i^{(e)}` 由二进制余量 + integer lift 得到。`[推导]` 因此不能把 Figure 9 单独称为 exact-ℓ₂ 证明。

---

## 3. LNP22 §5.2 的变量、承诺与协议对象

### 3.1 变量表

`[论文事实: LNP22 §5.2, p.41–44, Figure 10]`

| 符号 | 定义 / 域 | 公开/秘密 | 作用 |
|---|---|---|---|
| `R_q` | `Z_q[X]/(X^d+1)`，`q≡5 mod 8`，`d` 2 的幂 | 公开 | 基础环；自同构 `σ(X)=X^{−1}` |
| `s₁` | `R_q^{m₁}`，Ajtai 部分消息/短向量 | 秘密 | 与 `m` 一起构成承诺消息；参与 exact 关系 |
| `m` | `R_q^{ℓ}`，BDLOP 部分消息 | 秘密 | 可任意范数的消息；LBF 中对应 evaluation hint `y` |
| `σ(s₁),σ(m)` | 自同构表示 | 由秘密导出 | 使内积可作为多项式乘积常数项 |
| `s` | `(s₁,σ(s₁),m,σ(m))` | 秘密 | 所有式 (50)–(54) 的自变量 |
| `s₂` | `R_q^{m₂}`，小范数承诺 randomness | 秘密 | ABDLOP 第二盐；Figure 10 中由 `B^{pd},B^{pe}` 的 opening 间接证明 |
| `D_i,u_i,β_i^{(d)}` | `D_i∈R_q^{k_i×2(m₁+ℓ)}`，`u_i∈R_q^{k_i}` | 公开 | 近似 ℓ∞ 关系 (52) |
| `E_i,v_i,β_i^{(e)}` | `E_i∈R_q^{p_i×2(m₁+ℓ)}`，`v_i∈R_q^{p_i}` | 公开 | exact ℓ₂ 关系 (53) |
| `E_bin,v_bin,k_bin` | `E_bin∈R_q^{k_bin×2(m₁+ℓ)}` | 公开 | binary relation (54) |
| `x_i` | `(β_i^{(e)})²−‖E_i s−v_i‖₂²` 的二进制分解 | 秘密 | 证明非负差 |
| `x′` | `x‖(E_bin s−v_bin)` | 秘密 | binary proof 的拼接向量 |
| `b^{(d)},b^{(e)}` | `±1` sign | 秘密 | 两侧近似范围证明的 mask sign |
| `R^{(d)},R^{(e)}` | 二值挑战矩阵 | 公开 | 由 V 在承诺后采样 |
| `z^{(d)},z^{(e)}` | `b R e + y` 的 masked opening | 公开 | rejection sampling + 范围检查 |

### 3.2 Figure 10 的协议骨架

`[论文事实: LNP22 Figure 10, p.43–44]`

1. Prover 采样 `b^{(d)},b^{(e)}∈{±1}`、高斯 mask `y^{(d)},y^{(e)}`，形成辅助承诺 `t^{(d)},t^{(e)},t̄^{(d)},t̄^{(e)}`。
2. Verifier 采样二值挑战矩阵 `R^{(d)},R^{(e)}`。
3. Prover 计算 `z^{(d)}=b^{(d)}R^{(d)}e^{(d)}+y^{(d)}`、`z^{(e)}=b^{(e)}R^{(e)}e^{(e)}+y^{(e)}`，经 `Rej0` 后发送。
4. Prover/Verifier 运行一次 `Π_eval(s*,σ,φ,Ψ)`，其中
   `s*=(s₂,(s₁,x),(m,y^{(d)},y^{(e)},b^{(d)},b^{(e)}))`，
   `φ,Ψ` 由 Eq. (68)(69) 打包，包含 `f_i,g^{(d)},g^{(e)},F_i,G,H_j^{(d)},H_j^{(e)},I_i,J_j^{(d)},J_j^{(e)}`。
5. Verifier 接受当且仅当 `Π_eval` 通过、两组 masked opening 范数检查通过。

`[推导]` 重要结构事实：exact-ℓ₂ 不是一个独立 append 的黑盒；它与二次关系、binary proof、近似范围 proof 共用一次 `Π_eval` 和同一承诺结构。因此“加一个 exact norm 组件”在成本上不是简单加法。

---

## 4. 成本结构（不编造具体数值）

### 4.1 新增/修改对象

`[论文事实: LNP22 §5.2, p.42–44; §5.4, p.47]`

| 开销项 | 是否新增 | 说明 |
|---|---|---|
| 二进制余量承诺 `x` | 是（但可嵌入现有承诺） | Appendix/footnote 14：可append 到 `(s₁,m)` 的 Ajtai part；若不能提前承诺，则放 BDLOP part |
| `x′=x‖(E_bin s−v_bin)` | 逻辑向量 | 进入 challenge 维度 `c^{(e)}=d(k_bin+Σ_i(p_i+1))` |
| sign `b^{(d)},b^{(e)}` | 是 | §5.3 可打包成一个 sign 承诺以省空间 |
| 两组近似范围 proof 承诺 | 是 | `t^{(d)},t̄^{(d)},t^{(e)},t̄^{(e)}`；若 `υ_d=0` 可省略，见 §5.4 |
| 两组 masked opening | 是 | `z^{(d)},z^{(e)}`，各 256 个坐标的压缩编码 |
| 一次 `Π_eval` | 复用/扩展 | 所有二次函数与常数项检查合并到同一 evaluate proof |
| rejection sampling | 两组 | 成功概率含 `exp(−1/(2γ²))` 因子；诚实证明者非完美完备性 |

### 4.2 原文给出的 proof size 公式

`[论文事实: LNP22 §6.1, p.48–50]` 全文非交互证明（FS 后、含 Huffman/Dilithium-G 压缩与优化）的完整形式约为（bits）：

```
n·d·(⌈log q⌉−D) + 2.25·n·d
+ (ℓ + 512/d + λ + 2)·d·⌈log q⌉
+ ⌈log(2κ+1)⌉·d
+ (m₁+υ_e)·d·(2.57+⌈log s₁⌉)
+ m₂·d·(2.57+⌈log s₂⌉)
+ 256·(2.57+⌈log s^{(e)}⌉)
+ 256·(2.57+⌈log s^{(d)}⌉).
```

若 `υ_d=0`（不证明近似 ℓ∞ 部分），§5.4/§6.1 给出省略 `t^{(d)},t̄^{(d)},z^{(d)}` 的版本：

```
n·d·(⌈log q⌉−D) + 2.25·n·d
+ (ℓ + 256/d + λ + 2)·d·⌈log q⌉
+ ⌈log(2κ+1)⌉·d
+ (m₁+υ_e)·d·(2.57+⌈log s₁⌉)
+ m₂·d·(2.57+⌈log s₂⌉)
+ 256·(2.57+⌈log s^{(e)}⌉).
```

`[推导]` 这些公式是 LNP22 自身应用的证明尺寸，不是 LBF Decider 的尺寸。不能直接把 LBF 的 `d=128, κ_com=27, m₁=15, m₂=53` 代入得到 Decider 大小，因为：
- LBF 还需要证明 `k` 个 committed evaluation claims、盐替换、PoK 转录等；
- LBF 的 `s₂` 需要额外的 anchoring；
- 上述公式的 `n,ℓ,υ_e,k_bin,D` 属于 LNP22 应用实例化，不是 LBF 输出关系。

### 4.3 待估算项

`[待估算/待核查]` LNP22 §5.2 没有给“每个 exact-ℓ₂ 约束的独立乘法约束数/Proof Size”拆分表；以下必须按具体 LBF 实例化另算，不能凭空填数：

- 每个 exact 约束对应的 `I_i` 函数数量与 `p_i` 长度；
- `(m₁+υ_e)` 中 `υ_e` 随 LBF 盐块数 `N_c`、块数 `k,t` 的增长；
- 对 component-wise `a+bY` 分别证明所需的 base-ring 约束数是否翻倍；
- LNP22 的 `Π_eval` 与 LBF 的 `Π_many^{(1)}`/ABDLOP PoK 合并后总 round 数与 soundness error。

---

## 5. 与 LatticeBlindFold 的逐变量兼容性

### 5.1 关键符号对照（不能直接按下标对齐）

`[论文事实: LBF §2.5.2, p.18; §3.3, p.27–30; LNP22 §5.2, p.41–44]` `[推导]`

| LNP22 符号 | LBF 中的对应/近似对象 | 是否可直接映射 | 说明 |
|---|---|---|---|
| `m`（BDLOP 消息，任意范数） | evaluation hint `y'_{i,j}` / mask message | 部分 | LBF 消息放 BDLOP 槽，语义一致；但 LBF 在 `R_K` 上按 component-wise 展开 |
| `s₁`（Ajtai 消息/短向量） | LBF 盐 `s₁`（也被 LBF 称 salt） | 形式相似，语义不同 | LNP22 的 exact machinery 针对 `(s₁,m)`；LBF 需要两个盐都受控 |
| `s₂`（承诺 randomness） | LBF 盐 `s₂` | **不能直接用；但有组合路径** | LNP22 exact 对象向量 `s=(s₁,σ(s₁),m,σ(m))` 不含 s₂，s₂ 仅有 relaxed 界 `‖c̄s₂‖₂≤β_rlx`（Fig10 caption (ii)）；LBF Remark 4.8 sketch 了经 §3.2.1.1 anchoring（`Bs₂=t_B−m`）触及 s₂ 的路径，但未实例化。详见 LB-03 `docs/11`/`docs/12` |
| `σ(s₁),σ(m)` | LBF base-ring automorphism | 条件兼容 | 仅对 `R_F=Z_q[X]/(X^d+1)` 成立；`R_K` 层不能直接用 |
| `E_i s−v_i` | 对盐/witness 的范数检查残差 | 需重建 | LBF 盐界是 `ℓ∞<B̃=2`，需转换为 ℓ₂ 界并指定 `E_i,v_i,β_i` |
| `x_i` | `β²−‖E_i s−v_i‖²` 的二进制余量 | 可嵌入但需提前承诺 | 若不能与 `(s₁,m)` 同时承诺，需放 BDLOP 分槽 |
| `E_bin s−v_bin` | 额外 binary 约束 | 视具体构造 | LBF 的 ternary 盐本身可用 binary 证明，但尚未与 Decider 关系合并 |

### 5.2 八个必须回答的兼容性问题

#### A4.1 ABDLOP 消息结构是否一致？

`[论文事实 + 推导]` **代数形式一致，具体实例化不一致。** LNP22 Figure 10 支持 `(tA,tB)=(A₁s₁+A₂s₂, Bs₂+m)`；LBF 式 (2.5) 同一形状。但 LBF 明确说 LNP22 自己的实例化（Figs. 11/13/15）取 `ℓ=0`、把消息放 Ajtai 部分，而 LBF 取 `ℓ≥1`、把 evaluation hint 放 BDLOP 部分（LBF §2.5.2；LB-01 `docs/05` C1.5）。因此这不是“照抄 instantiation”，而是把 Figure 10 的一般协议重新实例化到 LBF 的承诺布局。

**分类：需要参数/格式调整。**

#### A4.2 LBF 两个随机盐能否直接映射到 LNP22 的承诺消息？

`[论文事实: LBF Remark 4.8, p.47]` **不能直接用；但并非无构造。** LBF 的 exact 缺口有两个位置：Π′DEC Step 5 的输出盐、Protocol 7 Step 17 的 mask 盐。原文明确说 LNP22 machinery targets `(s₁,m)`、s₂ untouched，**但紧接着给出组合方案**：exact proof (§5.2 + §3.3.4 R_K 翻译) "reaches the BDLOP randomness s₂ ... through the anchoring instantiation of §3.2.1.1"，并给出两个 append 界与位置（Remark 4.8 末段）。语气是虚拟式 "One would append it"，且作者在 §1(6)/§4.3.3/§5(2) 一致声明 "we do not instantiate"。因此正确表述是：**组合路径已 sketch，缺的是实例化与安全证明，不是从零发明 anchoring 或 exact 范数机制。**

**分类（LB-03 修订）：需要参数/格式调整 + 把已有 sketch 装配为完整协议并证明无 c̄ 累积；比 LB-02 原判"需要全新协议构造"更乐观，但未达"可直接使用"。** 详见 `docs/11` §0/§3.1 与 `docs/12` §1–§2。

#### A4.3 component-wise commitment 能否满足 LNP22 要求？

`[论文事实: LBF §3.3.4, p.29; LBF §3.2.1.1]` `[推导]` 可以，但必须在 **base ring `R_F`** 上实例化：把 `x=a+bY∈R_K` 拆成 `(a,b)∈R_F²`，分别用 `σ_F` 证明范数，不能把 LNP22 的 `σ_K(x)·x` 恒等式直接移到 K 层。原因是 `‖x‖²=‖a‖²+‖b‖²`，而 K 层自同构给出 `‖a‖²+ν‖b‖²`。这会使 exact proof 的对象数量与约束数量按 component 展开。

**分类：需要格式调整，且需重新推导 soundness。**

#### A4.4 域、环、模数与多项式次数是否满足 LNP22 条件？

`[论文事实: LNP22 §1.3, p.3; §5.2, p.41; LBF §2.1]` 基础层：`R_F=Z_q[X]/(X^d+1)`，`q≡5 mod 8`，`d` 为 2 的幂；LBF `q=2⁶⁴−59≡5 mod 8`，`d∈{64,128}`，**基础条件表面兼容**。但 LBF 的 Sum-Check/evaluation 在 `K=F_{q²}`，且 LNP22 的 `2β²+B²−1<q`、`B^{(e)}<q^{1/(4c^{(e)})}` 等条件必须在 component-wise 展开后的 `c^{(e)}` 下重新验算。LBF q 足够大是可能的，但本阶段没有给出完整数值验算。

**分类：基础参数兼容，展开后的安全条件待核查。**

#### A4.5 ℓ₂ 与 ℓ∞ 如何转换？

`[论文事实: LBF §2.5.2, p.18; §3.3.4, p.29]` LBF 为统一记法把盐采样为 `‖s‖∞<B̃=2`；LNP22 原生 `ℓ₂`。转换用 `‖x‖₂≤√(|x|)‖x‖∞`，`|x|=m_l·d`。这会把 exact-ℓ₂ bound `β` 与 `B̃√((m₁+m₂)d)` 关联，并损失 `√维度` 因子。对 Decider 来说，若目标是匹配 LBF 输出关系中的 `ℓ∞<B̃`，必须在提取侧证明该转换后仍无递归放大。

**分类：可转换，但不是紧等价。**

#### A4.6 是否需要增加额外承诺？

`[论文事实: LNP22 footnote 14, p.42]` 需要承诺 `x`，但可以 append 到已有 `(s₁,m)` 的 Ajtai part；若 `x` 不能提前确定，则放 BDLOP part。LBF 中还要为两组 approximate range proof 增加辅助承诺/开证明。即使共享承诺矩阵，消息维度从 `m₁+ℓ` 增至 `m₁+υ_e+ℓ`，binding 界与 extended-MLWE 维度都要重算。

**分类：需要，且影响参数。**

#### A4.7 二进制分解向量能否包含在原有承诺结构中？

`[论文事实 + 推导]` 可以，前提是 `(s₁,m,x)` 同时承诺；这与 LBF 生成 ABDLOP 承诺的时点相容，因为盐与余量都由 prover 在承诺前确定。但如果把 exact proof 应用于从提取器获得的递归 witness，则必须保证 `x` 与提取出的盐一致；binding 提供唯一性，但需要把 `x` 也放进被绑定消息。若不能提前承诺，LNP22 给出的退路是 BDLOP 分槽。

**分类：格式可行，需修改承诺消息维度。**

#### A4.8 对盐做精确范数证明是否改变 binding/hiding？

`[论文事实: LNP22 Theorem 5.3, p.44–46; LBF Remark 4.8]` `[推导]`
- binding：LNP22 的 soundness “要么破 MSIS，要么提取到满足式 (50)–(54) 的 opening”；把 `x` append 到 Ajtai part 后，MSIS 界含 `m₁+υ_e`，必须重算。
- hiding：commit-and-prove simulatability 依赖 ABDLOP hiding + rejection sampling + `Π_eval` simulator，具体假定 Extended-MLWE。LBF 另有 E-MLWE 假设；两者拼接不是自动成立。
- LBF 特有风险：若只对 `s₁` 加 exact proof 而 `s₂` 仍走 relaxed path，递归放大未消除；若对 `s₂` 也加 anchoring，则需证明 anchoring 不泄漏 salt。

**分类：需重做安全拼接，不可直接引用 LNP22 Theorem 5.3。**

### 5.3 最终分类

`[推导]`

| 候选分类 | 结论 | 理由 |
|---|---|---|
| 可直接使用 | ❌ | LNP22 exact 对象向量不含 `s₂`、不覆盖 LBF 输出求值关系、`R_K` component-wise 需按 §3.3.4 翻译 |
| 需要参数或格式调整 | ✅ | ABDLOP 槽位、消息维度、`ℓ∞→ℓ₂` 转换、q/β/challenge 条件均需重设 |
| 需要新的协议构造 | ◑ **收窄** | LB-03 修订：`s₂` anchoring（§3.2.1.1 Lemma 3.10）与 R_K exact 翻译（§3.3.4）**均已存在且被作者 sketch 组合**（Remark 4.8），故不是"从零发明"；真正缺的是把 sketch **实例化**成每隔轮协议 + 证明"无 c̄ 累积"+ 与 `CE_com^k` Decider 的安全拼接。详见 `docs/11`/`docs/12`。 |
| 不兼容 | ❌ | 基础环、ABDLOP 线性形式、binary/inner-product machinery 可复用 |

---

## 6. 对后续 Decider 决策的直接含义

`[推导]`

1. **不要把 LNP22 §5.2 写成新贡献**：它已经给出 exact-ℓ₂ 与 tight bound。后续如果要写贡献，只能在“嵌入 LBF 特定承诺结构 / 覆盖 `s₂` / 与 Decider 和递归接口拼接 / 降低 component-wise 开销”上找。
2. **LNP22 是必要组件，不是 Decider**：它解决范数子句；Decider 还需处理 `CE_com^k` 中 `c'=L(z')`、`x'=L_in(z')`、`y'=M̄_j z'(r')`、ABDLOP opening、盐替换、所有 PoK 转录与零知识模拟。
3. **成本不能只按“多一个 norm proof”估计**：exact proof 与 approximate range proof、`Π_eval` 共用承诺与挑战，消息维度增加，component-wise 展开可能翻倍；必须作为整体重算。
4. **下一步决策应问的是：是否存在一个可接受的工程构造，把 LNP22 + anchoring + LaBRADOR/LaZer 后端拼成 Decider，且证明大小不至于回到 5–8 MB 转录规模。** 这是任务 B 的问题，本文件不预断。

---

## 7. 本文件明确的待核查项

- `[待核查]` LNP22 `B^{(e)}` 常数的精确排版；需视觉核对 PDF p.44 Theorem 5.3。
- `[待核查]` LNP22 Figure 8/9 的具体 soundness/completeness error 在本任务中只按 §5.2 结构引用，未逐项复算。
- `[待核查]` LBF Remark 4.8 给出的两个 exact bound 常数与根号位置；PDF 文本提取有 glyph 丢失，必须用视觉核对方确认。
- `[待估算]` component-wise 展开后的 `υ_e, c^{(e)}, m₁+υ_e` 数值；必须绑定到具体 LBF 盐块数 `N_c=(k+1)t` 与 `m₁,m₂,d` 参数后才能给 proof size。
- `[待核查]` LNP22 的 FS 安全模型与 LBF §4.5 的 ROM/QROM、round-by-round knowledge soundness 缺口如何拼接；属于任务 B/D。
