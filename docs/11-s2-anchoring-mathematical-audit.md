# 11 · LatticeBlindFold 的 s₂ Anchoring 数学审计

> LB-03 · 任务 A。日期：2026-11-20。
> 目标：复原 LBF 已有的 s₂ anchoring 构造，判定它究竟证明了什么、缺少哪个数学环节。
> 一手来源：`C:/Users/dell/AppData/Local/Temp/lbf/paper_mirror.txt`（LatticeBlindFold ePrint 2026/1857 全文镜像，5114 行；镜像来源与核验方法见 `logs/2026-11-20-session-02.md`）。行号 `L####` 均指该文件。`C:/Users/dell/AppData/Local/Temp/lb02/md_lnp22_asia/content.md` 为 LNP22 正文提取，行号记 `LNP L####`。
> 镜像排版注：Unicode 下标/根号有丢失（`βrlx`=β_rlx；`2 s2 2Nc m2 d`=2·s₂·√(2N_c m₂ d)）；本文按上下文恢复，不改变量语义。

---

## 0. 结论先行（供任务 B/C 直接引用）

`[论文事实 + 推导]`

1. **anchoring 不是范数证明。** LBF §3.2.1.1 的 anchoring 本质是 **salt/message substitution**：用承诺等式 `B s₂⁽ⁿ⁾ = t_B⁽ⁿ⁾ − m⁽ⁿ⁾` 代入，把关于 `s₂` 聚合的常数项条件 (3.1) 改写成只关于**已承诺消息 m** 与**公开 t_B** 的关系（Lemma 3.10，L1537–1554）。Π_anc 最终 certify 的是 `ct(Σₙ wₙ m̄_{ι(n)}) − u = 0`（Lemma 3.16，L1662），**从不对 s₂ 本身给出范数上界**。
2. **s₂ 在现有协议里只在 binding 层出现。** 提取器确实返回 `(s̄₁, s̄₂, m̄⁽ⁿ⁾)`，但 `s̄₂` 仅用于 `m̄⁽ⁿ⁾ := t_B⁽ⁿ⁾ − B s̄₂` 与 `A₁s̄₁ + A₂s̄₂ = t_A`（Lemma 3.16 证明，L1670–1681）；其范数界是 **relaxed**：`‖c̄ s̄₂‖₂ ≤ β_rlx`（Definition 3.22，L2160–2168），含挑战差 c̄，不是 `‖s₂‖∞ < B̃` 的紧界。
3. **作者已 sketch 如何用 anchoring 让 exact-ℓ₂ 触及 s₂，但明确未实例化。** Remark 4.8（L3130–3139）逐字说 exact-ℓ₂ proof（LNP22 §5.2，R_K 翻译见 §3.3.4）"**reaches the BDLOP randomness s₂ (untouched by [LNP22]'s norm machinery, which targets the committed part (s₁, m)) through the anchoring instantiation of §3.2.1.1**"，并给出两个 append 界与位置；但语气是虚拟式 "One would append it"，且 §1 贡献(6)（L418–419）、§4.3.3（L3466）、§5(2)（L3896–3897）一致声明 "we do not instantiate"。
4. 因此用户指出的修正成立：**不能说 s₂ anchoring「完全没有构造」**——已有"把 s₂ 线性像绑定到承诺消息"的 anchoring，且已有"用 anchoring 触及 s₂ 的 exact-ℓ₂ 组合 sketch"；**也不能说它已经足够**——该 sketch 未实例化，且未证明提取出的 s₂ 携带可支撑递归的严格范数界。

---

## 1. 原始 ABDLOP 关系（A1）

### 1.1 承诺公式

`[论文事实]` LBF §2.5.2，L1095–1107，式 (2.4)(2.5)：

```
BDLOP:   (t₁, t₂)ᵀ = [[A₁, 0], [A₂, y]] · s₁ + (0, m)ᵀ                  (2.4)
ABDLOP:  (t_A, t_B)ᵀ = [[A₁, A₂], [0, B]] · (s₁, s₂)ᵀ + (0, m)ᵀ        (2.5)
         ⟹  t_A = A₁ s₁ + A₂ s₂   (mod q)
             t_B = B s₂ + m       (mod q)
```

系数映射（Lemma 2.31，L1111–1122）：把环元视作域向量经 `cf` 识别后，`cf(t_A) = cf(A₁s₁) + cf(A₂s₂)`、`cf(t_B) = cf(B s₂) + cf(y)`；对第 ℓ 个系数 `(cf(t_B))_ℓ = (cf(B s₂))_ℓ + (cf(y))_ℓ`，ℓ=1 时 `cf(·)₁ = ct(·)`（常数项）。

### 1.2 变量表（严格区分 s₁ 与 s₂ 的安全角色）

| 符号 | 所属环/维度 | 公开/秘密 | 采样分布与范数 | 在承诺中的位置 | 安全角色 |
|---|---|---|---|---|---|
| `s₁` | `R_F^{m₁}` | 秘密 | 短向量，`‖s₁‖∞ < α`（L1095–1097） | Ajtai 槽（t_A 的 A₁ 项） | **承诺的"消息/短秘密"主槽**；LNP22 exact-ℓ₂ 的证明对象在此 |
| `s₂` | `R_F^{m₂}` | 秘密 | `s₂ ← χ^{m₂}`，χ 为 `{c:‖c‖∞≤ν}` 上均匀（L1097–1099, L1143–1146） | BDLOP 槽（t_A 的 A₂ 项 + t_B 的 B 项） | **承诺随机性/salt**；提供 hiding（Extended-MLWE），LNP22 只给 relaxed 界 |
| `m` | `R_F^{ℓ}` | 秘密（消息） | 任意范数消息（LBF §3.3 / LNP22 §2） | t_B 的消息项 | 被承诺消息；与 s₁ 一起是 exact-ℓ₂ 对象 |
| `A₁` | `R_q^{n×m₁}` | 公开 | 均匀 | — | Ajtai 矩阵 |
| `A₂` | `R_q^{n×m₂}` | 公开 | 均匀 | — | 跨槽矩阵 |
| `B` | `R_q^{ℓ×m₂}` | 公开 | 均匀 | — | BDLOP 矩阵；anchoring 的关键矩阵 |
| `t_A, t_B` | `R_q^{n}, R_q^{ℓ}` | 公开 | 由承诺产生 | — | 承诺分量 |

`[论文事实]` 范数约定：除非下标注明，`‖·‖` 指 ℓ∞ 范数，按系数扩展到环元素向量（L1138–1139）。ABDLOP 原生在 `q ≡ 5 (mod 8)` 上（L1108）。
`[推导]` **关键区分**：s₁ 与 s₂ 虽同为"短"向量，但角色不同——s₁ 是被证明范数的 committed message 主槽，s₂ 是提供 hiding 的 randomness。不能因符号下标相近就推断二者在 LNP22 中有相同安全角色；下文所有"exact-ℓ₂ 覆盖 s₁"均**不自动**延伸至 s₂。

### 1.3 ZKPoK 证明对象（Lemma 3.6 / 3.7）

`[论文事实]` Lemma 3.6（L1308–1326，引 LNP22 Lemma 3.1）：协议 `Π_many((s₂,s₁,m),(f₁..f_N))` 是 `(s̄₁, s̄₂, c̄) ∈ R_q^{m₁} × R_q^{m₂} × C̄` 的 proof of knowledge，满足：

1. `A₁ s̄₁ + A₂ s̄₂ = t_A`；
2. `‖s̄_i · c̄‖ ≤ 2 s_i √(2 m_i d)`，`i=1,2` ← **relaxed 范数界，含挑战差 c̄**；
3. `R₁ s̄₁ + R_m (t_B − B s̄₂) = u`。

在 `MSIS_{n, m₁+m₂, B}` 难（B 见 L1318）时 `(s̄₁,s̄₂)` 唯一。模拟器 `S_ABDLOP` 在 Extended-MLWE 下不需 s₁,s₂,m 即可模拟（L1321–1326）。
`[论文事实]` Lemma 3.7（L1411）与 L1406：LBF 实例化取 `k=1, σ=id`（无自同构提升），只需 certify 全环恒等式（如 `m_sq,i − y_{i,1}·y_{i,1}=0`）。

`[推导]` **注意**：Π_many 的输入元组写作 `(s₂,s₁,m)`，提取器返回 s̄₂，**但这只是 opening 知识提取**：结论 (2) 对 s₂ 给的是 relaxed 界，且 (3) 中 s₂ 只以 `t_B − B s̄₂ = m̄` 形式进入消息关系。这与"对 s₂ 做 exact-ℓ₂ 范数证明"是两回事。

---

## 2. LBF anchoring 完整复原（A2）

### 2.1 待锚定的两个量

`[论文事实]` §3.2.1.1 开头（L1510–1514）：Protocol 6 中需把两个量绑定到 V 视图中的承诺，防止作弊证明者提供任意域值：
- **claimed sum** `σ := ζP + T`（Step 7）：直接是 committed messages `coeffs` 与 `{y_{i,j}}` 的常数项关系，**只需 Protocol 4 在承诺串接上即可**（L1515–1517），无需 s₂。
- **verifier target** `u★ := h − eq(r′,α)·(c_F + δ₀ c_N) − δ₁ c_E`（Step 18）：具有 (3.1) 的形状，是 anchoring 的真正对象。

### 2.2 关系 (3.1) 与 Lemma 3.10（salt/message substitution）

`[论文事实]` 式 (3.1)（L1518–1529）：

```
u★  ?=  ct( Σ_{n=1}^{N_c} w_n · (B s₂⁽ⁿ⁾)_{ι(n)} )        (3.1)
```
其中 `w_n ∈ R_K` 是打包旋转 π_{i,j}（Lemma 3.12）乘挑战积（如 γᵢ⁽¹⁾, ζδ₁, eq(r′,α)），`ι(n) ∈ [ℓ]` 指示 B 的第几行；`w_n, ι(n)` 公开。

`[论文事实]` **Lemma 3.10（L1537–1554）**：设 `{(t_A⁽ⁿ⁾, t_B⁽ⁿ⁾)}` 是共享公开矩阵 `(A₁,A₂,B)` 的 ABDLOP 承诺，每个 BDLOP 部分非空（`t_B⁽ⁿ⁾ = B s₂⁽ⁿ⁾ + m⁽ⁿ⁾`）。则对任意公开 `w_n ∈ R_K, ι(n) ∈ [ℓ]`，式 (3.1) 成立 **当且仅当**

```
ct( Σ_{n=1}^{N_c} w_n · m⁽ⁿ⁾_{ι(n)} ) − u = 0,
其中  u := Σ_{n=1}^{N_c} w_n · (t_B⁽ⁿ⁾)_{ι(n)} − u★ · 1 ∈ R_K,
且 u 可由 V 仅用已传输承诺与公开权重算出。
```

证明（L1550–1552）：代入 `B s₂⁽ⁿ⁾_{ι(n)} = t_B⁽ⁿ⁾_{ι(n)} − m⁽ⁿ⁾_{ι(n)}`，用 `ct` 的 K-线性即得。

`[论文事实]` Remark 3.11（L1555–1561）：V 在 Protocol 6 Step 16 已做此动作——`c_F, c_N, c_E` 由 BDLOP 分量 `Commit(·)₂ = B s₂ + m` 派生并记录为 `c_F = F(r⃗′) + ct(B·s₂,F)`。**每个 salt 聚合对 V 可见的形式恰是"(公开 BDLOP 分量) − (已承诺消息)"，这正是 Lemma 3.10 利用的形式。** 假设 `ℓ⁽ⁿ⁾ ≥ 1` 是必要的：若某块 `ℓ⁽ⁿ⁾=0`，其 `B s₂` 在转录中不出现，u 不可计算。

`[推导]` **这是本任务最重要的判定**：anchoring 的方向是 **消去 s₂**（用承诺等式替换掉 `B s₂`），把"含 s₂ 的线性像条件"化为"含消息 m 的常数项条件"，从而能被 Π_many（证明 (s₁,m) 关系）认证。**它绑定的是 s₂ 的线性像 B s₂ 与承诺消息 m 之间的一致性，不是 s₂ 的范数。**

### 2.3 串接实例与 Π_anc（Lemma 3.16）

`[论文事实]` §3.2.1.3（L1608–1655）：对 `N_c` 个已有承诺，定义串接见证 `s₁^cat=(s₁⁽¹⁾,…,s₁⁽ᴺᶜ⁾)`、`s₂^cat=(s₂⁽¹⁾,…,s₂⁽ᴺᶜ⁾)`、`m^cat=(m⁽¹⁾,…,m⁽ᴺᶜ⁾, g)`（g 为 Protocol 4 的 garbage），矩阵 `A_i^cat=blockdiag(A_i,…,A_i)`、`B^cat=blockdiag(B,…,B)`，并定义

```
f^anc(s₁^cat, m^cat) := R_m m^cat − u ∈ R_K,   R₁ := 0,
R_m := w₁ e_{ι(1)}ᵀ | … | w_{N_c} e_{ι(N_c)}ᵀ .
```

Π_anc 即以 `N=1` 执行 Protocol 4 认证 `ct(f^anc)=0`，拒绝采样宽度 `s₁^cat = γ₁ η α √(N_c m₁ d)`、`s₂^cat = γ₂ η ν √(N_c m₂ d)`（L1638–1640）。**不重算承诺，只是重新打包已有 opening**（L1645–1653）。

`[论文事实]` **Lemma 3.16（L1657–1699）**：在 `B^anc := 8η√((s₁^cat·√(2N_c m₁ d))² + (s₂^cat·√(2N_c m₂ d))²)` 的 `MSIS_{n,m₁+m₂,B^anc}` 难假设下，Π_anc 完备，且是如下 opening 的 proof of knowledge：

```
提取 (s̄₁⁽ⁿ⁾, s̄₂⁽ⁿ⁾, m̄⁽ⁿ⁾)_{n∈[N_c]}，满足
   ct( Σₙ wₙ m̄⁽ⁿ⁾_{ι(n)} − u ) = 0      （= 在提取的 salt 上的式 (3.1)，经 Lemma 3.10）
```

zk 与 soundness：soundness error 比 Lemma 3.6 多 Lemma 3.8 的加性 `1/|K|`；HVZK 由 Lemma 3.8 + S_ABDLOP 组合，在 Extended-MLWE 下，逐块 hybrid，**损失因子 N_c，不引入新假设**（L1664–1699）。成本：一次 Π_many（长度 N_c·m₁, N_c·m₂）+ 一次 N=1 包裹，`O(N_c(m₁+m₂)d)` 域运算，无新承诺（除 g 的单一 garbage 槽）（L1701–1705）。

**提取器证明逐字（L1670–1681）**：Lemma 3.8 归约到 Lemma 3.6 在 Protocol 4 Step 5 的提取器，返回 `(s̄₁^cat, s̄₂^cat, c̄)` 满足 `A₁s̄₁^cat + A₂s̄₂^cat = t_A^cat` 与 `R₁s̄₁^cat + R_m(t_B^cat − B^cat s̄₂^cat) = u`。因 `R₁=0`，即 `Σₙ wₙ(t_B⁽ⁿ⁾ − B s̄₂⁽ⁿ⁾)_{ι(n)} = u`，于是定义 `m̄⁽ⁿ⁾ := t_B⁽ⁿ⁾ − B s̄₂⁽ⁿ⁾`，**这就是所断言的关于提取消息的关系，再经 Lemma 3.10 即为提取 salt 上的式 (3.1)**。

### 2.4 关系图（每条边标真实代数关系）

```
      s₁ ∈ R_F^{m₁}              s₂ ∈ R_F^{m₂}, m ∈ R_F^{ℓ}
   (‖s₁‖∞<α, 短)              (s₂←χ^{m₂}, ‖s₂‖∞<ν; m 任意范数)
        \                              /
   A₁ s₁ + A₂ s₂ = t_A        B s₂ + m = t_B      [ABDLOP 承诺, 式(2.5)]
        \                              /
         +----------- Commitment ----------------+
                      (t_A, t_B) 公开
                          |
        Lemma 3.10 代入: B s₂⁽ⁿ⁾_{ι(n)} = t_B⁽ⁿ⁾_{ι(n)} − m⁽ⁿ⁾_{ι(n)}
                          v
        u = Σₙ wₙ (t_B⁽ⁿ⁾)_{ι(n)} − u★·1   (V 可算, 公开)
                          |
        Π_anc: ct( Σₙ wₙ m̄⁽ⁿ⁾_{ι(n)} − u ) = 0   [Lemma 3.16, 提取消息上的关系]
                          |
        提取器 (s̄₁,s̄₂,m̄): m̄⁽ⁿ⁾ := t_B⁽ⁿ⁾ − B s̄₂⁽ⁿ⁾, A₁s̄₁ + A₂s̄₂ = t_A
                          |
        公共验证关系: 式(3.1) 在提取 salt 上成立 ⟺ 承诺消息满足常数项等式
        ★ s̄₂ 的界 = relaxed ‖c̄ s̄₂‖₂ ≤ β_rlx (Lemma 3.6(2))，无 exact 界 ★
```

`[推导]` 图中从 s₂ 出发只有两条边：一条进 `A₁s₁+A₂s₂=t_A`（binding），一条进 `Bs₂+m=t_B`（随后被 Lemma 3.10 消去换成 m）。**没有任何一条边给出 `‖s₂‖ ≤ β` 的 exact 约束。** 这就是"anchoring 提供承诺关系与秘密随机量的联系，但不等于范数证明"的图证据。

---

## 3. 现有证明的边界（A3）

| 类别 | 内容 | 证据 |
|---|---|---|
| **已经验证的关系** | `A₁s̄₁+A₂s̄₂=t_A`；`ct(Σₙ wₙ m̄_{ι(n)})−u=0`（⟺ 提取 salt 上的式 3.1）；`R_m m^cat − u` 的常数项为 0 | Lemma 3.16, L1660–1662 |
| **已经提取的秘密信息** | `(s̄₁⁽ⁿ⁾, s̄₂⁽ⁿ⁾, m̄⁽ⁿ⁾)`；其中 `m̄⁽ⁿ⁾ := t_B⁽ⁿ⁾ − B s̄₂⁽ⁿ⁾` | Lemma 3.16 证明, L1670–1681 |
| **已证明的范数界** | 仅 **relaxed**：`‖c̄ s̄_i‖₂ ≤ 2s_i√(2m_i d)`（i=1,2）；对 s₂ 无 exact-ℓ₂ 界 | Lemma 3.6(2), L1315；Def 3.22, L2160–2168 |
| **仅依赖诚实证明者的条件** | 单次调用中输出见证是诚实证明者的，其范数属 RoK 定义的成员假设；关心对象 z₁ 由 NC⃗(X) 在同轮精确界定（**no salt involved**）；其余 relaxed 对象只是证明者自采的 blinding 实例 | Remark 4.8, L3116–3124 |
| **尚未得到安全保证的条件** | 递归第 r 轮提取出的 salt 的**严格范数界**：现有只有 relaxed，含 c̄ 与 (ρᵢ−ρ'ᵢ)，每轮复合，只支撑 O(1) 轮 | Remark 4.8, L3125–3129 |

### 3.1 为什么"能帮助触及 s₂"却"没关闭递归严格界"

`[论文事实]` Remark 4.8 完整陈述（L3125–3139）：
- 迭代时第 r 轮见证由第 r+1 轮提取器产生，其 salt 界**必须被证明而非假设**，而 `R₂` 成员只在最后一轮才能 discharge 范数条款；
- relaxation 复合：每轮贡献一个 `c̄`（Lemma 3.6(2)）与一个 `(ρᵢ−ρ'ᵢ)`（Lemma 2.19 逐坐标求逆），支撑轮数 `O(1)` 且很小；
- "To fold without such a bound, the fresh salts must be certified exactly. The device is the exact ℓ₂-norm proof of [LNP22, §5.2], whose translation to R_K is the content of §3.3.4, and which reaches the BDLOP randomness s₂ (untouched by [LNP22]'s norm machinery, which targets the committed part (s₁, m)) through the anchoring instantiation of §3.2.1.1."（L3130–3133）
- 作者给出 append 位置与界：Protocol 8 Step 5 处界 `k t (B̃−1)√(m₁+m₂)d`；Protocol 7 Step 17 处界 `(B̃−1)t√(m₁+m₂)d`（L3133–3135）；并称若如此，提取 salt 满足界**无 c̄ 因子**，binding 识别第 r 轮认证 opening 与第 r+1 轮提取的 opening，"nothing would accumulate"（L3135–3137）。

`[推导]` 精确回答用户问题：
- **"能帮助触及 s₂"**：指 anchoring 提供了把 s₂ 的线性像 `B s₂` 写成"公开 t_B − 已承诺消息 m"的通道，使 exact-ℓ₂ 证明系统（其原生只能对承诺消息 (s₁,m) 证明）可以**把 s₂ 纳入可证明关系**。这是真实存在的构造 sketch（§3.2.1.1 + Remark 4.8），不是空想。
- **"没关闭递归严格界"**：因为（a）该 sketch 用虚拟式 "One would append it"，作者明确 "we do not instantiate"；（b）即使 sketch 成立，它要求把 exact-ℓ₂ 证书**追加到每一轮的提取点**，而现有协议只在 relaxed 关系 `CE_rlx_com`/`β_rlx` 下工作；（c）缺少把"§3.3.4 的 R_K exact-ℓ₂ 翻译"装配成"每隔轮对 fresh salt 输出无 c̄ 紧界"的具体协议与安全证明。因此关闭的是"能否 principle 够得着 s₂"，未关闭的是"递归中每轮提取盐的紧界如何装配并证明不累积"。

### 3.2 relaxed bound 与 β 链（供任务 E）

`[论文事实]` Definition 3.22（L2160–2168）：`CE_rlx_com(b,L,β,Commit)` 把盐条款 `‖s_j‖∞ < B̃` 换成 `∃ c̄ ∈ C̄\{0}: ‖c̄ s_j‖₂ ≤ β`；(3.14) `β_rlx := 2 s₂ √(2N_c m₂ d)`。Remark 3.23（L2178–2186）：`CE_com(B,L,B_fold) ⊆ CE_rlx_com(B,L,β_rlx)` 当 `β_rlx ≥ 2T(C)B_fold√(m₁+m₂)d`；"tight 记录诚实执行产生，relaxed 记录提取认证"。Binding 未削弱：两个 relaxed opening 仍给出 `MSIS_{κ,m₁+m₂,2β_rlx}` 解（L2187–2191）。Definition 3.24（L2202–2208）：接口处再放大 `β_rlx⁽³⁾ := 2T₁(C) β_rlx`，`T₁(C)=max_{c̄∈C̄\{0\}}‖c̄‖₁`。B_fold（Lemma B.1, L4237–4243）：`B_fold = (K+k)T(C)(B̃−1) + B̃`，B̃=2。
`[推导]` 递归累积式（本文推导，论文只给定性 + 单次因子）：若每轮把 relaxed 提取对象作为下一轮 witness，则 `β_{r+1} ≈ 2T₁(C)·β_r`（接口处因子每轮复现）；d=128 时 `2T₁(C)=29.6`（L3694），约每轮 +4.9 bit，迅速逼近 `q≈2^64` 的 MSIS/绑定上限——这是 O(1) 轮的量化依据。若按 Remark 4.8 实例化 exact-ℓ₂ 证书，则链截断为 `β_{r+1}=β_r`，但该实例化缺失。详细见 `docs/12` 任务 E。

---

## 4. 本任务对 LB-02 的修正记录

1. **修正"component-wise 不能做 exact-ℓ₂"的措辞**：LB-02 说"K=F_{q²} component-wise 不能套 K 层 automorphism identity"——这只说对了一半。§3.3.4（L1841–1855）明确：直接套 `σ̂_K(x)·x` 会证到错误量 `‖a‖²+ν‖b‖²`（因 ν≠1），**但正确做法是**对 a、b 分别用 base-ring 自同构 `σ⁻¹(a)·a = ‖a‖²`、`σ⁻¹(b)·b = ‖b‖²`，再联合约束 `‖a‖²+‖b‖² ≤ β²`，"provable by the same machinery as any other exact-norm statement in [LNP22, §5.2] with no adaptation beyond summing the two independent square-norm terms"。故 **R_K 上的 exact-ℓ₂ 翻译是存在且正确的**，LB-02 的"需新协议构造"过强，应改为"翻译已给出，但未装配进 LBF 协议每轮"。
2. **修正"s₂ 完全未触及"的措辞**：见本文结论第 3 点与 §3.1。anchoring + exact-ℓ₂ 触及 s₂ 的 sketch 已存在，只是未实例化。

---

## 5. 待核查

- `[待核查]` LBF 镜像为第三方全文镜像；Remark 4.8 与 Lemma 3.10/3.16 的公式编号已与正文自洽引用交叉核验，但正式 PDF 页码（LBF v1, §3/§4）未逐页核对（ePrint PDF 受 Cloudflare 阻挡）。
- `[待核查]` 若进入实现，需确认 LNP22 §5.2 exact-ℓ₂ 追加到 Protocol 8 Step 5 / Protocol 7 Step 17 后，与 Π′DEC 的 relaxed 输入接口（Definition 3.24 的 `β_rlx⁽³⁾`）如何对接——本文只确认组件存在，未验证接口兼容。
