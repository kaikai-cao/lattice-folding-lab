# 20 · B2 联合提取器、真实提取流程与批量关系（LB-05T · LB-06 修订）

> LB-05T · 任务 A / D；**LB-06 修订（任务 A/B/C）**：按用户复核纠正"只对最终 c 分叉一次"的错误提取描述，忠实恢复 Theorem 5.3 的两次 challenge-matrix 执行 + 底层 E₁；分离 exact 余量 x_i 与 Eq.(54) 独立二值约束；处理 Protocol 7/8 不同范数界。日期：2026-11-20。
> 基线：`docs/19`（B2 联合关系 L1–L5、s/x 分离）、`docs/15`（无 c̄ 累积链边界）、`docs/21`（混合 MSIS / 三层 binding）。
> 本轮不比较 B1/B2、不改 B2 关系本身；修正提取流程、概率账本、变量映射、多实例 exact-norm。
>
> **结论先行（LB-06 修订要点）**：
> 1. **★修正**：Theorem 5.3 的提取**不是**"对最终挑战 c 分叉一次"。原文（PDF 印刷页 46）是**外层两次 challenge-matrix 执行**——第 1 轮用诚实 (R⁽ᵈ⁾,R⁽ᵉ⁾) 跑到第三轮调底层提取器 E₁，第 2 轮**回绕到第三轮**、用新鲜独立 (R′⁽ᵈ⁾,R′⁽ᵉ⁾) 再调一次 E₁；两次 opening 消息须相同（否则破坏 ABDLOP binding），消息相同⇒挑战矩阵与消息独立，再用新鲜挑战证 exact。期望时间为底层 E₁ 的 2 倍（Lemma 4.3）；**原文符号三处不同**（陈述页 `2T_{E_eval}`、证明正文"2 times E₁"、证明结论 `2T_{E′}`），不做等号替换（§1.5-A4）。底层 E₁ 自身是 Theorem 4.5 的交互提取器、时间 12T。详见 §1.4–1.5。
> 2. **联合提取器仍是 Theorem 5.3 的参数化实例、非新原语**：Fig10 的 (50)–(54) 由**一个**提取器一次恢复满足全部约束的共同 opening（PDF L6243–6264、L6597–6600）。B2 的 L1–L5 逐条落在模板内，s₂ 与 x 一样"追加进 Ajtai 槽"（L5734）。但**继承是有条件的**：须满足 Thm5.3 前提（§1.6）且参数可实例化（docs/22）；`B2-PROOF-PASS` 不是参数化通行证。
> 3. **★变量三分**（任务 B）：B2 主消息 s_A=(s₁,s₂)；exact-norm 内部二进制余量 x_i（表示 (β_i^(e))²−‖E_i s−v_i‖² 的分解）；Fig10 Eq.(54) 的**独立**二值约束 E_bin s−v_bin。原文把后两者拼进同一二值验证，但 statement 与参数计数上来源不同，**不得把 exact 余量 x_i 等同于 Eq.(54)**；B2 无额外二值约束时 k_bin 的设定见 §1.7。
> 4. **★Protocol 7/8 多实例**（任务 C）：N_e=(k+2)t 个盐块，LBF Remark 4.8 对 Step5/Step17 给**两个不同**上界（PDF/LBF 原文 sketch 未实例化）。**不得**压成统一 E_{s₂} 与统一 β；优先用 Fig10 的多 E_i / 多 β_i^(e) 分别承接，两组不同 β_i 同时满足整数提升条件须逐项核查（§2.5）。
> 5. **批量是现成能力但有边界**：Π_many 原生支持 N 条线性关系一次证明、无额外挑战（LBF L2820–2826）；但 exact-norm 层的统一批量是 B2 新设计，原文给两个界且未实例化（§2.5）。
>
> **来源与视觉复核**：LNP22 官方 PDF `C:/Users/dell/AppData/Local/Temp/lb02/lnp22_asia.pdf`（**本轮已对印刷页 19/45/46 做 PNG 渲染视觉复核**，见 `logs/2026-11-20-session-10.md`）、文本流 `C:/Users/dell/AppData/Local/Temp/pdf_check_lnp22/lnp22.txt`（`PDF L####`）；镜像 `content.md`（`LNP L####`）；LBF 镜像 `paper_mirror.txt`（`LBF L####`）。镜像字形（‖→}/p、≤→ď、上划线丢失）以官方文本流为准，正负号冲突处以 PDF 视觉为准。

---

## 0. 基线：B2 联合 statement（来自 docs/19 §2）

```
公开输入: t_A, t_B, t̂_A, t̂_B, A₁,A₂,B, Â_s,Â_x,Â_r,B̂, R₁,R_m, E_{s₂}, p, β
witness:   W = (s₁, s₂, m, r, x)        [σ(s_A) 由 s_A 决定，不单列]

(L1) R₁·s_A + R_m·m_A = [t_A;t_B]        R₁=[A₁ A₂; 0 B], R_m=[0; I_ℓ]
(L2) Â_s·s_A + Â_x·x + Â_r·r = t̂_A      （辅助承诺 Ajtai opening）
(L3) B̂·r + m_A = t̂_B                    （辅助承诺 BDLOP opening）
(L4) ⟨E_{s₂}·s_LNP, E_{s₂}·s_LNP⟩ + ⟨p,x⟩ = β² mod q,   s_LNP=(s_A,σ(s_A),m_A,σ(m_A))
(L5) ⟨x′,x′−1⃗⟩=0 mod q + Fig9 range     （x 二值 + 整数提升）
```
其中 `s_A=(s₁,s₂)` 为 Ajtai 消息（含追加的 x），`m_A=m` 为 BDLOP 消息，r 为新 randomness。

---

## 1. 任务 A：联合提取器构造

### 1.1 为什么"每个子协议各自知识可靠"不够

`[论文事实: PDF L6243–6264, L6597–6600]` LNP22 Fig10 的 soundness 结论形式是：
> "either [the extractor] breaks the binding of the commitment or recovers a valid opening (s̄₂, s̄₁, x̄_s, m̄, …) … satisfying Equations (50) to (54)."

`[推导]` 这是**单个**提取器、**单个** opening、同时满足全部约束。反观 B1（docs/18 §2.1）：原始 opening proof 提 (s̄₁, s̄₂)，辅助 exact proof 提 (s̄₂′, …)，两个证明各自知识可靠**不蕴含** s̄₂ = s̄₂′——这是"共享变量 ≠ 联合 PoK"（用户在 LB-05R 的核心质疑）。B2 若仍是两个协议并行，同样逃不掉该质疑。**因此 B2 必须落到一个 Fig10 实例内，用单一提取器一次性恢复 (s̄₁,s̄₂,m̄,r̄,x̄)。**

### 1.2 Fig10 模板的可联合性（原文依据）

`[论文事实: PDF L5613–5620]` §5.2 开宗明义：
> "a general protocol to prove various quadratic relations on s = (s₁, σ(s₁), m, σ(m)) … **we prove simultaneously** quadratic relations over R_q, quadratic relations over Z_q, approximate bound on the infinity norm, exact bound on the ℓ₂ norm and finally that a vector is binary. All the later statements are gathered in **this single protocol** …"

`[论文事实: PDF L5653–5684]` Fig10 的通用 statement 是五类约束：
```
(50) f_i(s)=0                      i∈[ρ]          R_q 上二次关系（线性是其特例）
(51) F_i(s)=0                      i∈[ρ_eval]     常数系数为零的 evaluation
(52) ‖D_i s − v_i‖_∞ ≤ β_i^(d)    i∈[υ_d]        近似 ℓ∞
(53) ‖E_i s − v_i‖   ≤ β_i^(e)    i∈[υ_e]        精确 ℓ₂
(54) E_bin s − v_bin ∈ {0,1}^{d k_bin}            二值向量
```
`[论文事实: PDF L6243–6264]` Theorem 5.3：**一个**提取器恢复**一个** opening `(s̄₂, s̄₁, x̄_s, m̄, ȳ⁽ᵈ⁾, ȳ⁽ᵉ⁾, b̄⁽ᵈ⁾, b̄⁽ᵉ⁾, c̄)` 同时满足 (50)–(54)。
`[论文事实: PDF L2835–2869, L3999–4042]` Lemma 4.3 / Theorem 4.5 同理：一个提取器恢复一个 witness 满足全部 batched 关系；N 个二次关系经 verifier 挑战 µ 随机线性组合压成一个（L2801–2806）。

`[推导]` **结论**：LNP22 的提取器天然"可联合"——它本就是为一个 statement 里的多个约束设计的，只是覆盖的是**固定模板** (50)–(54)，而非"任意可拆为线性+二次的 R(x,w)"的通用定理。B2 的 L1–L5 恰落在该模板内（§1.3），故直接继承 Theorem 5.3。

### 1.3 B2 → Fig10 逐分量映射（联合提取器存在性的核心论证）

`[推导]` 把 Fig10 模板参数化为 B2，只需把"追加进 Ajtai 消息槽的对象"从 x 扩展为 (s₂, x)：

| Fig10 角色 | 原文维度/来源 | B2 实例 | 合法性 |
|---|---|---|---|
| Ajtai 消息 s₁ | m₁（L5653） | s_A=(s₁,s₂)，基础维度 **M_base=m₁+m₂**（docs/22 §E1C，旧记号 m₁\* 同义） | 参数化扩展；x 已展示"追加进 Ajtai 槽"先例（L5734），s₂ 同法追加 |
| BDLOP 消息 m | ℓ | m_A=m | 原样 |
| randomness s₂ | m₂（L6179） | r（新盐），维度 m₂' | 角色换位：原 randomness 由 r 承担；r 是 fresh 短盐，满足采样界 |
| 二进制余量 x | υe（L5734） | x（υe=1） | 原样 |
| exact 向量 s | (s₁,σ(s₁),m,σ(m))∈R^{2(m₁+ℓ)} | s_LNP=(s_A,σ(s_A),m_A,σ(m_A))∈R^{2(m₁+m₂+ℓ)} | m₁→m₁+m₂ 参数化（用户已接受"通用接口支持"，参数实例化待核查） |
| (50) 二次函数 f_i | 任意公开 f_i | f(s_A,m_A)=R₁s_A+R_m m_A−[t_A;t_B]（L1） | 线性是二次特例；公开常量 −[t_A;t_B] 并入 f 的常数项 |

`[论文事实: LNP L5734]` 决定性原文：
> "the prover appends a commitment to the binary representation vector x … in the Ajtai part of the commitment to (s₁, m)."

`[推导]` 原文已展示"把需要 exact 证明的向量（x）追加进 Ajtai 消息槽、仍由同一提取器恢复"这一模式。B2 对 s₂ 做的是**同一件事**（把 s₂ 也放进 Ajtai 消息槽，使 `E_{s₂}s_LNP=s₂` 落在 (53) 的作用域内）。因此联合提取器 **= Theorem 5.3 在该参数化实例上的直接应用**：
```
联合提取器 E_B2 (rewindable black-box access to B2 prover):
  1. 运行 Fig10 参数化协议（L1–L5 作为 (50)/(53)/(54) 约束，s₁:=s_A, m:=m_A, s₂:=r）
  2. 对最后一个 Π⁽²⁾_eval 挑战 c 做 forking（PDF L10454–10493，[ACK21]），凑 3 个接受转录
  3. 解出共同 opening (s̄_A=(s̄₁,s̄₂), m̄_A, r̄, x̄, …) 满足 (50)–(54)
  4. 由 (L1) 得 A₁s̄₁+A₂s̄₂=t_A、Bs̄₂+m̄_A=t_B → (s̄₁,s̄₂,m̄_A) 是原始承诺 opening
```
`[推导]` **同一性来源**：(L1)–(L5) 的 witness 列表里 s₂ **只有一个变量符号**，提取器输出的 s̄₂ 同时进入 L1（原始 opening）、L4（exact 界）；不存在"两个 s₂ 事后比对"。这是结构性质，但仍需 binding 保证 s̄₂ 与诚实 opening 计算上一致（见 docs/21 §2.3 与 §3）。

### 1.4 ★真实提取流程：外层两次 challenge-matrix 执行 + 底层 E₁（LB-06 核心修正）

> **纠正旧稿**：旧稿 §1.4 写"固定 I₁–I₄、只对最终挑战 c 分叉、凑 3 个接受转录"——这是**错误**的。LNP22 Theorem 5.3 的 soundness 提取（PDF 印刷页 46, L6378–6437）是**外层两次执行 + 底层 E₁**，Fiat–Shamir 的多轮 RO 分叉（附录 B 的 E1–E4）是**另一套**用于非交互化的提取栈，二者不可混。

`[论文事实: PDF L6378–6437，印刷页 46 视觉复核]` Theorem 5.3 soundness 逐字复原：

```
记号：E = 本零知识证明(ZK)的提取器；E₁ = 底层 Π⁽²⁾_eval 的提取器(= Theorem 4.5 的交互式提取器)

外层提取流程 E（两次 challenge-matrix 执行）：
  第 1 次：
    (a) 运行 prover 到【第三轮】，用【诚实生成】的挑战矩阵 R⁽ᵈ⁾, R⁽ᵉ⁾；
    (b) 在其上调底层提取器 E₁；
    (c) 若 E₁ 未得到满足 (50)–(54) 的 valid opening (s̄₂,s̄₁,xs,m̄,ȳ⁽ᵈ⁾,ȳ⁽ᵉ⁾,b̄⁽ᵈ⁾,b̄⁽ᵉ⁾,c̄)，abort；否则继续。
  第 2 次：
    (d) 把 prover【回绕到第三轮】（同一前缀、同一 prover 随机带）；
    (e) 发送【新鲜、独立诚实生成】的 R′⁽ᵈ⁾, R′⁽ᵉ⁾；
    (f) 再调 E₁ 直到得到第二份 valid opening (s̄′₂,s̄′₁,xs′,m̄′,ȳ′⁽ᵈ⁾,ȳ′⁽ᵉ⁾,b̄′⁽ᵈ⁾,b̄′⁽ᵉ⁾,c̄′)。
  一致性判定（L6454–6456）：
    - 若两份 opening 的消息不同 → E 破坏 commitment binding（→ MSIS 解），走此分支结束；
    - 若消息相同 → 由消息固定，挑战矩阵 R⁽ᵈ⁾,R⁽ᵉ⁾ 与消息独立，走 witness 提取分支；
      随后用【新鲜挑战】证 exact-norm / range / 二值（下方概率账本）。
```

`[论文事实: PDF L6433–6437]` 时间/概率：
> "With this extraction strategy, the expected run time of E is **2 times** the expected run time of E₁ and E has the **same success probability** as E₁, see **Lemma 4.3** for justifications."

`[论文事实: PDF L2826–2829, L3152–3169 Lemma 4.3；L4250–4262, L4375–4386 Thm4.5]` Lemma 4.3 的核心期望恒等式 `E[X]=(1+1/ε)ε+1·(1−ε)=2`（两次调用子提取器）；Thm4.5 的 E₁ 自身是"同一 prover randomness、两次 fresh challenge Γ/Γ′"的交互提取器，期望时间 12T（`B_LNP=8η√(…)` 的 MSIS 归约在此层）。

**两个层级的严格区分（用户任务 A2 要求）**：

| 层级 | 对象 | 分叉/回绕的内容 | 时间 | 原文 |
|---|---|---|---|---|
| 底层 E₁（Theorem 4.5 提取器） | Fig8 的 ABDLOP opening proof | 两次 challenge 矩阵 Γ,Γ′（同一 prover randomness ρ_P）；内部再套 Lemma 4.3 的两次调用 | T_{E₁}=12T（P 单次 ≤ T） | PDF L3986–4054, L4250–4386 |
| 外层 E（Theorem 5.3 提取器） | Fig10 的 commit-and-prove（含 range/exact） | 回绕到**第三轮**、两次 fresh (R⁽ᵈ⁾,R⁽ᵉ⁾)/(R′⁽ᵈ⁾,R′⁽ᵉ⁾)，各调一次 E₁ | 陈述页 `2T_{E_eval}`；正文"2×E₁"；结论页 `2T_{E′}`（三处原文写法，不等同替换，§1.5-A4） | PDF L6264, L6378–6437, L6597–6600 |
| （另：FS 非交互提取栈 E1–E4，附录 B） | Fiat–Shamir 变换后的协议 | 对 RO 多轮分叉、构成 (1,1,1,3)-tree | 24+23Q queries（最内层 E1） | PDF L11413–11663 |

`[推导]` **旧稿"只对最终 c 分叉"实际描述的是第三行（FS 栈）的一部分，不是 Theorem 5.3 的交互式 soundness 提取**。B2 继承的是 Theorem 5.3（交互 rewindable black-box 模型）：外层两次 challenge-matrix 执行是"证明两个 opening 消息一致 ⇒ 挑战矩阵与消息独立"的关键；不能省略，也不能与 E₁ 内部的分叉合并成一步。

### 1.4b 提取协议调用顺序、挑战依赖（B2 继承的交互轮次）

`[论文事实: PDF L6064–6157]` Fig10 的交互阶段（B2 原样继承，作为外层两次执行的每一轮内部结构）：
```
阶段1  P→V: 承诺 (t⁽ᵈ⁾, t̄⁽ᵈ⁾, t⁽ᵉ⁾, t̄⁽ᵉ⁾)        （range/exact 的 mask 承诺）
阶段2  V→P: 挑战矩阵 R⁽ᵈ⁾, R⁽ᵉ⁾ ← Bin_{256×c}^1     （看到承诺后给；【回绕点=第三轮之前】）
阶段3  P→V: z⃗⁽ᵈ⁾, z⃗⁽ᵉ⁾（Rej₀ 通过才继续）          （依赖 R）
阶段4  P↔V: Π⁽²⁾_eval（自带 µ 批量挑战与最终挑战 c）  （最后运行；E₁ 在此提取 ABDLOP opening）
```
`[推导]` 外层":回绕到第三轮"指回到阶段 2 之前重新采样 R⁽ᵈ⁾,R⁽ᵉ⁾（阶段 1 的承诺与 prover 随机带保持不变），这正是"挑战矩阵与消息独立"的来源。L1（原始 opening 线性关系）在阶段 4 的 Π⁽²⁾_eval 内作为 (50) 类约束被验证；L4/L5（exact/二值）在阶段 1–3 的 mask+range 中处理，**全部在一个协议调用内**（B2 不是一个证明并行两个子协议）。

### 1.5 ★概率账本（原文恢复 + B2 替换 + 失败事件分解）

#### 1.5-A1/A2 · ε 阈值的四层记录与完整代数链（LB-06R 定点回修）

`[论文事实: PDF 印刷页 45/46 视觉 + 文本流 L6237–6242 / L6437–6452]` **四处必须分开记录，不得用"以证明页为准"一笔带过**：

| 层 | 原文位置 | 条件（逐字） | 性质 |
|---|---|---|---|
| ① 论文 Theorem 5.3 **陈述** | 印刷页 45（L6237–6242） | `ε ≥ 2/|C| − q^{−d/2} − q^{−λ} − 2^{−127}` | **减号**，含 `−2^{−127}`；论文原始陈述 |
| ② Soundness proof **实际写出** | 印刷页 46（L6437–6442） | `ε ≥ 2/|C| + q^{−d/2} + q^{−λ}` | **加号**，**无** `2^{−127}`、`2^{−128}` 裕量项 |
| ③ 证明随后写的下界 | 印刷页 46（L6447–6452） | `P_{E₁} ≥ ε − 2/|C| − q^{−d/2} − q^{−λ} ≥ 2^{−128}` | 声称结论；由②单独不能推出 |
| ④ B2 参数化采用 | 本文件 / docs/22 | `ε ≥ 2/|C| + q^{−d/2} + q^{−λ} + 2^{−128}` | **B2 显式附加的充分条件**，不是论文任一页原文 |

`[推导]` **逐步代数核对（用户 A2 要求的裕量链）**：

```
记 T := 2/|C| + q^{−d/2} + q^{−λ}。
(甲) 只用②：ε ≥ T ⇒ P_{E₁} ≥ ε − T ≥ 0。只能得到 0，不能得到 2^{−128}。
(乙) 用①：ε ≥ 2/|C| − q^{−d/2} − q^{−λ} − 2^{−127}
        ⇒ P_{E₁} ≥ ε − T ≥ −2q^{−d/2} − 2q^{−λ} − 2^{−127} < 0，
     与"成功概率非负"矛盾，①与③不可能同时为真。
(丙) 欲使③成立，必须额外要求 ε ≥ T + 2^{−128}（层④）：
        P_{E₁} ≥ ε − T ≥ (T + 2^{−128}) − T = 2^{−128}.   ∎
```

`[推导]` **诚实结论**：论文陈述页（减号）与证明页（加号）的 ε 阈值是**原文自身不一致**，且证明页②→③之间**缺少一个 `2^{−128}` 量级的裕量项**；视觉复核与文本流 OCR 一致，是原文内容而非转录错误。本轮**不替作者修补**：①/②/③/④ 四层并列保留，B2 只在层④的充分条件下调用定理，并明确声明"这是 B2 附加假设，不是论文已证条件"。`B2-PARAM-HOLD` 的阻断清单据此新增一项：**论文 ε 条件的内部不一致未获作者勘误或独立证明**（docs/22 §5、decisions/LB-06-decision.md）。

#### 1.5-A4 · 提取时间符号的三处原文（不做等号替换）

`[论文事实: 印刷页 45 / 46 / 47 视觉；文本流 L6264 / L6433–6437 / L6600]`：

| 位置 | 原文写法 | 说明 |
|---|---|---|
| Theorem 5.3 陈述（印刷页 45, L6264） | `in expected time 2T_{E_eval}` | 下标 `E_eval`；文本流写作 `2Teval`。原文未给 `T_{E_eval}` 单独定义 |
| Soundness proof 正文（印刷页 46, L6433–6437） | "expected run time of E is **2 times** the expected run time of E₁" | 相对叙述，没有出现 `2T_{E₁}` 这一符号；Lemma 4.3 给 `E[X]=2` |
| Soundness proof 结论（印刷页 47, L6597–6600） | `in time 2T_{E′}` | 视觉为 `E′`（E 撇，即 Theorem 4.5 提取器）；文本流 OCR 成 `2T_{E1}` |

`[推导]` `T_{E₁}`（Theorem 4.5 的 E₁，自身期望时间 12T，PDF L4250–4386）与 `T_{E_eval}` 的定义**未在原文中给出相等关系**；`2T_{E′}` 与陈述页 `2T_{E_eval}` 是三处不同写法。本轮**保留三种原文写法，不做等号替换**；B2 外层时间只写"两次调用底层 E₁，期望时间按 Lemma 4.3 为 2×T_{E₁}（E₁=Thm4.5 提取器）"，并把 `2T_{E_eval}` 记为定理陈述原符号、`2T_{E′}` 记为证明结论原符号。禁止在未证情况下写 `T_{E_eval}=T_{E₁}`。

#### 1.5-账本 · 各项来源与 B2 替换

`[论文事实: PDF L6437–6452, L6492–6600]` 各项来源与 B2 替换：

| 项 | 原文 | 来源 | B2 替换 |
|---|---|---|---|
| prover 接受概率阈值 | ①`ε ≥ 2/|C|−q^{−d/2}−q^{−λ}−2^{−127}` / ②`ε ≥ 2/|C|+q^{−d/2}+q^{−λ}` / ④B2 加 `+2^{−128}` | 承诺挑战空间 | |C| 不变；B2 采用④，保留①–③为原文记录（§1.5-A1/A2） |
| 底层提取器成功率 | `P_{E₁} ≥ ε−2/|C|−q^{−d/2}−q^{−λ} ≥ 2^{−128}`（需层④裕量才成立） | Lemma 4.3 两次调用 | 同上（E₁ 代 B2 的 Π⁽²⁾_eval 实例） |
| ∞-范数拒绝抽样失败 | `2^{−256}`（L6517），得 `‖s̄e⁽ᵈ⁾‖∞≤24s⁽ᵈ⁾` w.p. ≥1−2^{−256} | Lemma 2.7，Bin_{256×1}^{c⁽ᵈ⁾} | B2 用 B⁽ᵈ⁾ 类界，维度随 υ_d 变（docs/22） |
| exact ℓ₂ 拒绝抽样失败 | `2^{−128}`（L6549），得 `‖s̄e⁽ᵉ⁾‖≤B⁽ᵉ⁾` w.p. ≥1−2^{−128} | Lemma 2.9 + `B⁽ᵉ⁾<q/(41c⁽ᵉ⁾)` | B⁽ᵉ⁾ 按 M_Ajtai/ℓ′/c⁽ᵉ⁾ 重推（docs/22 §E1/E2；B⁽ᵈ⁾/B⁽ᵉ⁾ 定义已按视觉纠正） |
| 整数提升（exact）失败条件 | `2(max_i β_i^(e))²+(B⁽ᵉ⁾)²−1 < q`（L6221/L6585） | 无 mod-q 回绕 | β_i（两类盐块）与 B⁽ᵉ⁾ 代入（docs/22） |
| 整数提升（二值）失败条件 | `(B⁽ᵉ⁾)² + √(υe+k_bin)·d·B⁽ᵉ⁾ < q`（**印刷页 45 视觉：d 在根号外**；文本流 L6211/L6566 OCR 误把 d 写入根号） | 无回绕 ⇒ Lemma 5.2 | υe=(k+2)t、k_bin 代入；**不沿用旧 `√((υe+k_bin)d)` 写法**（docs/22 §E2） |
| 完成时 | `P_{E₁}(1−2^{−256})(1−2^{−128})`，陈述页时间 `2T_{E_eval}`、证明结论 `2T_{E′}` | 外层两次执行 | 同形式；三处时间符号三分见 §1.5-A4，不做等号替换 |

#### 1.5-A3 · 失败事件逐项分类（union bound 前）

`[推导]` 五类事件严格分开，**整数提升不写成概率误差**：

| 事件 | 含义 | 概率/界来源 | 是否概率误差 |
|---|---|---|---|
| `E_extract` | 底层 E₁ 未得到满足 (50)–(54) 的 valid opening | `P_{E₁}`；仅在层④充分条件下可下界 `2^{−128}` | 是（提取知识误差） |
| `E_outer` | 外层两次 challenge-matrix 执行的两份 opening **消息不同** | 触发"破坏 commitment binding"分支；由 binding 假设界定，**不是已知数值上界** | 是（绑定假设违反） |
| `E_bind` | 三层 binding 任一失败（原始 / 辅助 / 联合↔原始） | MSIS 假设层（docs/21 §2.4），非可量化概率 | 是（假设层） |
| `E_rej_d` / `E_rej_e` | 两次 rejection sampling 拒绝 | `2^{−256}` / `2^{−128}`（原文明确） | 是 |
| `E_lift_exact` / `E_lift_bin` | 整数提升发生 mod-q 回绕 | 由 C3 / C2 **参数条件**保证不发生 | **否**：参数条件，不进 union bound |

`[推导]` 原文**没有**给出单一 `δ_total`；B2 不得写无推导的 δ。尤其不得把"提取器输出两个不同 opening"直接写成某一已知概率上界：它只在绑定假设违反时发生，须由该假设归约界定。若需总误差，须在上表概率项上做有依据的 union bound，并把整数提升单列为参数条件。

### 1.5b soundness 继承的严格边界（不默认宣称）

`[推导]` "联合提取器由 Theorem 5.3 继承"依赖一个前提：**B2 的参数化实例满足 Fig10 soundness 证明的前提**。逐项核查：

| 前提 | Fig10 原文 | B2 实例 | 状态 |
|---|---|---|---|
| exact 向量是已承诺消息 | s=(s₁,σ(s₁),m,σ(m))，s₁ 是 Ajtai 消息 | s_A=(s₁,s₂) 是 Ajtai 消息，s_LNP 含其 σ 像 | ✓ 结构满足 |
| randomness 短采样 | s₂∈R^{m₂} 短（L6179） | r∈R^{m₂'} fresh 短盐 | ✓ 满足（r 是采样短盐） |
| 追加向量进 Ajtai 槽 | x 追加（L5734） | x 与 s₂ 都追加 | ✓ 同模式；s₂ 追加是扩展 `[参数实例化待核查]` |
| 扩展维度 m₁+m₂ 的接口兼容 | E_i∈R^{p_i×2(m₁+ℓ)}（L1681） | E_{s₂}∈R^{m₂×2(m₁+m₂+ℓ)} | `[参数实例化待核查]`：列数随 m₁→m₁+m₂ 自然扩展，Fig5/Fig8 多线性接口对扩展维度的实例化须在参数阶段验证 |
| Thm5.3 参数（q、B⁽ᵉ⁾、k_bin） | 按 m₁+ℓ 推 | 按 m₁+m₂+ℓ 须重推 | `[待核查]` |

`[推导]` **诚实判定**：结构性前提（消息槽 / randomness 短盐 / 追加模式）满足；**参数化前提**（扩展维度接口实例化、Thm5.3 参数重推）未完成。这属于"同一接口的新参数实例需完成参数验证"，不是"接口不兼容"或"新原语设计"——与用户在 LB-05S 把 E_{s₂} 定为"通用接口支持、参数实例化待核查"的口径一致。因此本轮论证联合提取器**存在性与结构**，不宣称参数层已闭合。

### 1.6 与三层 binding 的衔接

`[推导]` E_B2 输出的 s̄₂ 满足 (L1)：`A₁s̄₁+A₂s̄₂=t_A`。这给出"联合提取结果 ↔ 原始承诺 opening"的关联，但该关联是**计算绑定**（依赖原始承诺 MSIS），不是信息论相等。三层 binding（原始 LBF / 辅助 ABDLOP / 联合关联）的严格证明与 c̄-scaled 界见 `docs/21-b2-mixed-msis-bound.md` §2。

### 1.7 ★Figure 10 变量映射：三类二进制/消息对象的分离（任务 B）

`[论文事实: PDF L6313–6346（correctness）, L6556–6570（soundness Eq.54）, L5805–5839（Eq.61）]` Fig10 中至少出现**三个不同角色**的对象，旧稿把它们混记为"x"：

```
(1) 主消息 s_A=(s₁,s₂)（B2）／原文 (s₁,m) 的 Ajtai 部分
    → 进入 s_LNP=(s_A,σ(s_A),m_A,σ(m_A))，是 (50)(51)(52)(53) 的作用对象。
(2) exact-norm 内部二进制余量 x_i（每个 i∈[υe] 一个）
    → x⃗_i := ((β_i^(e))² − ‖E_i s−v_i‖²) 的二进制分解，support ≤ 2log β_i^(e) ≤ d（L6340）；
      进入 Eq.(53) 的 I_i(s,x) 第二实参、Eq.(61) 的 e^(e) 拼接；
      它【追加进 Ajtai 承诺】（L5734）但【不进入 s_LNP、无 σ(x) 配对】。
(3) Eq.(54) 的独立二值约束 E_bin s − v_bin ∈ {0,1}^{d·k_bin}（L5650/6567）
    → 这是【额外声明】的二值向量（如群签名中的比特承诺），与 (2) 来源不同。
      原文在 soundness 把 (2) 的 x⃗_i 与 (3) 拼进同一二值验证 x′₁（L6313–6324），
      但【statement 参数计数上二者分别记账】：k_bin 只由 (3) 决定，(2) 由 υe 与 β_i^(e) 决定。
```

`[推导]` **B2 的对应**：B2 需要的是 (2)（s₂ 的 exact 余量），**没有** (3) 这类额外二值秘密。故 B2 必须明确 `k_bin` 如何设定——**不能**把 exact 余量 x_i 当成 Eq.(54) 来满足、也不能据此把 k_bin 记成 υe 或 0 而不说明。两种处理（记为待 docs/22 决定）：
- (甲) 令 k_bin=0（无独立二值约束）——则 Eq.(54) 退化为平凡，但须确认 Thm5.3 对 k_bin=0 的参数式仍成立（`(B⁽ᵉ⁾)²+√(υe·d)·B⁽ᵉ⁾<q` 去掉 k_bin 项）；
- (乙) 若 Fig10 实现要求一个二值向量占位，须显式新增一个与 s₂ 无关的二值 witness，并计入消息维度。

`[推导]` 逐项映射表（用户任务 B2 要求，维度不重复计数）：

| LNP22 Fig10 | B2 对应对象 | 维度/来源 |
|---|---|---|
| Ajtai 主消息 s₁ | s_A=(s₁,s₂) | M_base=m₁+m₂（总 Ajtai 列 M_Ajtai=M_base+ν_x） |
| BDLOP 消息 m | m_A=m | ℓ |
| ABDLOP randomness s₂（**新盐**） | r | **m₂'**（不再沿用原 LBF 的 m₂） |
| exact-norm 余量 x_i | B2 内部二进制余量（(2)） | υe 个，每个 ≤2logβ_i^(e) bit |
| E_i | 对 s_LNP 的公开线性选择/映射矩阵 | E_i∈R_q^{p_i×2(m₁*+ℓ)} |
| β_i^(e) | 对应 exact 上界（两类盐块分别设，§2.5） | — |
| E_bin s−v_bin（(3)） | B2 **无**额外二值约束 → k_bin 设定见上 | k_bin=0 或显式新增 |
| k_bin | 独立二值约束维数参数 | 与 υe **分开计数** |

`[推导]` E_{s₂} selector 六问（用户任务 B3，须逐项确认表示一致性，否则不能宣称 ‖s₂‖₂≤β）：
1. **行列**：E_{s₂}∈R_q^{m₂×2(M_base+ℓ)}（m₂ 行选出 s₂ 的 m₂ 个 R_q 分量）；是通用 E_i 接口在 M_base=m₁+m₂ 下的参数化实例（用户 LB-05S 已接受此定位；p_i=m₂ 为 R_q 元素级，docs/22 §E1D）。
2. **选择对象**：它从 s_LNP 的 Ajtai 消息部分选出 s₂——是 **R_q 环元素**级选择（一次选一个 R_q 分量 s₂^{(j)}），不是逐系数整数向量选择。
3. **ℓ₂ 范数表示**：原文 exact 的 ‖E_i s−v_i‖ 是 **R_q 分量系数展开后的 ℓ₂**（§5.2 内积 ⟨·,·⟩ 按系数，L6356 "inner products are taken modulo q"、整数提升后按 ℤ 系数），非 CRT 表示。
4. **转换无损性**：`E_{s₂}s_LNP=s₂` 在 R_q 分量上精确成立、σ(s₂) 分量因 selector 只作用 Ajtai 原像部分而不引入额外项；故 ‖E_{s₂}s_LNP‖₂=‖s₂‖₂（系数 ℓ₂）**无损**——但须 docs/22 确认 L5613 `(s₁,m,σ(s₁),σ(m))` 与 L5653 `(s₁,σ(s₁),m,σ(m))` 的排列歧义不影响 selector 定位（已标 `[待核查]`）。
5. **是否需额外排列/automorphism**：若 selector 只取未变换的 s₂ 分量，无需额外 automorphism；若 s₂ 也需 σ 配对（R_F→自同构），则须按 component-wise（docs/12 §3.3.4）在 base ring 分别处理——B2 取前者，`[待核查]` 待参数阶段确认 E_{s₂} 的块位置。
6. **v_{s₂} 是否为零**：B2 目标是约束 s₂ 本身（‖s₂‖₂≤β），故取 v_{s₂}=0（纯选择器）；若改约束 E_{s₂}s−v（如 anchoring 的组合），v≠0 但那样约束的不是裸 s₂，不得宣称 ‖s₂‖≤β。

---

## 2. 任务 D：Protocol 7/8 批量关系

### 2.1 承诺计数与盐索引（原文核查）

`[论文事实: LBF L2883–2886]` Protocol 8 Step 5：单个 Π_many 调用覆盖 `N_c=(k+1)t` 个盐块（t 个输入 `C_j` + kt 个新 `C_{i,j}`）；逐个 fresh salt pair `s_{i,j}=(s₁,i,j, s₂,i,j)`（L2876–2877）。
`[论文事实: LBF L2752, L2775–2777]` Protocol 7 Step 17：t 个 mask 承诺 `C_{y,j}`，各一对 fresh salt `(s₁,y,j, s₂,y,j)`。
`[论文事实: LBF L2820–2826]` Remark 4.4：Step 1 的 (K+k)t 个、Step 5 的 (k+1)t 个、Step 17 的 t 个"can be collapsed into a single call to Π_many … vector-batching is free both in soundness and completeness"。
`[推导]` B2 的 `(k+2)t = (k+1)t + t` 计数正确（Step 5 的 (k+1)t + Step 17 的 t）。

### 2.2 Π_many 的拼接 witness 与公开矩阵

`[论文事实: LBF L1443, L1308–1316, L1612–1627]` Π_many 证明 `u = R₁s₁ + R_m m ∈ R_K^N`（full-ring identity，任意 N）。拼接实例：
```
witness:  s₁^cat=(s₁⁽¹⁾,…,s₁⁽ᴺᶜ⁾), s₂^cat=(s₂⁽¹⁾,…,s₂⁽ᴺᶜ⁾), m^cat=(m⁽¹⁾,…,m⁽ᴺᶜ⁾, g)
矩阵:    A₁^cat=blockdiag(A₁,…), A₂^cat=blockdiag(A₂,…), B^cat=blockdiag(B,…)
         R₁=0（anchoring 类）或按关系；R_m 是按关系的 block-row（非块对角）
```
`[论文事实: LBF L2885–2887]` Step 5 的 `R_m` 是 `t×N_c`，第 j 行为 `(1,−1,−b,…,−b^{k−1})` 落在第 j 块——跨块耦合 `C_j` 与 `{C_{i,j}}`。
`[推导]` B2 把 L1 批量化：`R₁^cat=[A₁^cat A₂^cat; 0 B^cat]`、`R_m^cat=[0; I_ℓ^cat]`，`u^cat=[{t_A⁽ᶦ⁾};{t_B⁽ᶦ⁾}]`——每块复现一个原始 opening 关系，N=(k+2)t 条，一次 Π_many 调用，无额外挑战、无可靠性代价（L2623–2625）。**这是原文现成接口，不需新协议。**

### 2.3 辅助承诺：一份覆盖整批，还是逐份？

`[论文事实: LBF L1455–1457, L1645–1655, L1701–1704]` Π_anc（anchoring 聚合）每次调用只在 m 末尾加**一个**垃圾槽 g（`ℓ→ℓ+1`），"no commitment is recomputed: the parties merely repackage openings they already hold"，"no fresh commitment is computed beyond the single garbage slot for g"。
`[推导]` 按原文 batched 接口，**一份**辅助承诺（g 槽）覆盖整批 N_c 个盐块，不是每个 s₂⁽ⁱ⁾ 各一份；这一份可推广到 (k+2)t 块（Definition 3.15 对任意 N_c 成立）。因此 B2 的辅助 ABDLOP 承诺 `t̂_A,t̂_B` 可按拼接 witness 构造，witness 为 `(s_A^cat, x^cat, r^cat, m^cat)`。

### 2.4 盐不相交性

`[论文事实: LBF L2757–2758, L3642–3643, L3648–3649, L3655]` `C_{y,0}`（ Ñ 个开盐承诺）的盐"disjoint from those of {C_{y,j}}"，且"never combined homomorphically with any other commitment"；它是唯一明文开盐的承诺。
`[推导]` 这是**结构/安全要求**（打开 C_{y,0} 会泄露共享盐、破坏 Step 17 PoK 的 hiding），不是分析便利。但对 B2 的 `(k+1)t + t` 两个**秘密盐**集合不构成障碍：它们按 (i,j)/j 独立采样、索引互异。障碍只在两种情形出现：(i) 把开盐的 `C_{y,0}` 塞进同一批；(ii) 为缩减 witness 跨集合复用盐（违背 LBF L1698 "independently sampled"）。**B2 不触碰这两者，盐不相交性满足。**

### 2.5 批量化的边界：哪些可向量化、哪些必须逐个 / 待核查

`[论文事实: LBF L3130–3139]` Remark 4.8 的 exact-norm sketch：作者给 Step 5 与 Step 17 的界**不同**——`kt(B̃−1)√(m₁+m₂)d` 与 `(B̃−1)t(m₁+m₂)d`——且"分别 append to Step 5 / Step 17"，并明确"which we do not instantiate"（L418–419）。
`[论文事实: LBF L1533–1535, L1851–1855, L1864–1867]` Π_many⁽¹⁾ 不原生支持直接写在 s₂ 上的关系；原文路线是 Lemma 3.10 替换 `Bs₂⁽ⁿ⁾=t_B⁽ⁿ⁾−m⁽ⁿ⁾` 转成消息关系；component-wise exact 的二次约束 `‖a‖²+‖b‖²≤β²` 可批量摊销。

`[推导]` 汇总（诚实区分）：

| 项目 | 可向量化？ | 依据 |
|---|---|---|
| (L1) 原始 opening 线性关系 ×(k+2)t | ✓ 单次 Π_many，免费 | LBF L2820–2826 |
| (L2)(L3) 辅助承诺 opening（拼接 witness） | ✓ 一份辅助承诺 + 拼接 salt | LBF L1612–1627, L1701–1704 |
| (L4) exact norm ×(k+2)t，统一 E_{s₂} | `[待核查]` | 原文 Step5/Step17 两个界不同、分别 append；Π_many⁽¹⁾ 不原生支持直接 s₂ 关系（L1533–1535）；统一选择矩阵覆盖全部 (k+2)t 是 B2 外推 |
| (L5) 二值余量 x | ✓ Fig10 (54) 原生批量 | PDF L5653–5684 |
| C_{y,0} 开盐承诺 | ✗ 不可并入 | LBF L3648–3649 "never combined homomorphically" |

`[推导]` **结论（旧）**：批量关系在**线性层与二值层**是原文现成能力；**exact-norm 层的统一批量**是 B2 相对 LBF 作者 sketch 的新设计，原文既未实例化、且给出了两个不同的界——这是进入参数阶段前须明确处理的 `[待核查]` 项（保留两处 append / 两个界，或证明统一界可行）。

### 2.5 ★多实例 exact-norm：Fig10 多 E_i 方案（任务 C，LB-06 新增）

`[论文事实: PDF L5648–5667]` Fig10 的 exact 模板**原生支持多个** `(E_i, v_i, β_i^(e))`：`∀i∈[υ_e], ‖E_i s−v_i‖≤β_i^(e)`（Eq.53），各 E_i 可有**独立**行数 p_i 与独立 β_i^(e)。这为"分别承接 Step5/Step17 的不同界"提供了原文接口。

`[推导]` **优先方案（多约束映射，用户 C1）**：设 υ_e=N_e=(k+2)t，每个盐块一个选择器：
```
E_i s − v_i = s₂^(i),   v_i = 0
β_i^(e) = { β_step5,   i ∈ I_step5 （Step5 的 (k+1)t 块）
          { β_step17,  i ∈ I_step17（Step17 的 t 块）
```
**★LB-06R 更新：LBF 官方 PDF 已可取得**（本地 `lbf.pdf`，印刷页 47 视觉复核，见 session-11），Remark 4.8 两处界逐字为：

```
Step 5  (Protocol 8):  √kt · (B̃−1) · √((m₁+m₂)d)
Step 17 (Protocol 7):  (B̃−1) · √(t(m₁+m₂)d)
```

旧稿镜像转录 `kt(B̃−1)√(m₁+m₂)d` / `(B̃−1)t(m₁+m₂)d` 的**根号覆盖与 t 的位置均有误**；以官方 PDF 视觉为准。`B̃` 的定义、两界是单块还是整批口径仍 `[待核查]`（本轮不启动参数定型）；原文明确 "which we do not instantiate"，故仍不得把该 sketch 当作已验证的实例化。两界不同⇒保留多 E_i 方案、用 max 满足 C3，不强行统一 β。

`[推导]` **可行性逐项核查（用户 C2）**：
- 多个 E_i ∈ Fig10 合法接口：✓（Eq.53 原生多实例）；
- 每个 E_i 输出维度 p_i：对纯选 s₂^(i)，p_i=m₂（选一个盐块的 m₂ 个 R_q 分量，R_q 元素级；**不是** m₂d 系数级）——原文 Fig10 输入 `c^(e)=d(k_bin+Σ(p_i+1))`（L6020–6027）已把 d 乘在最外层，p_i 必须按 R_q 元素数计；
- exact 余量 x_i 总维数：υ_e 个，每个 ≤2logβ_i^(e) bit，在 `2logβ_i^(e)≤d` 时各占 1 个 R_q 元素（ν_x=υ_e；docs/22 §E1C）；
- Ajtai 消息维度增加量：Ajtai 槽追加 (s₂^cat, x^cat)，增量 = (k+2)t·(m₂+υ_x) 个 R_q 元素（υ_x=每块余量环元素数）；
- exact challenge dimension c^(e)：与 υ_e、p_i 一起进入 B^(e) 与 Thm5.3 不等式（docs/22 代入）；
- rejection sampling α^(e) 增长：α^(e) 随 ‖e^(e)‖ 上界 B^(e) 变，B^(e) 随每个 x_i 的 2logβ_i^(e) 与拼接维度增长（docs/22）；
- Thm5.3 对 B^(e),q,β_i^(e) 限制：见 §1.5 概率账本三条不等式；
- 两组不同 β_i^(e) 同时整数提升：须 `2(max_i β_i^(e))²+(B^(e))²−1<q` 对 max(β_step5,β_step17) 成立——**用较大者即可同时满足**，故两组不同界在该条件上**可共存**（这是"不必强行压成统一 β"的关键论据）。

**★维度成本核对（LB-06R 闭合）**：原文 Fig10 输入参数（L6020–6027）逐字为 `c^(d)=d·Σ_{i=1}^{υ_e}k_i`、`c^(e)=d(k_bin+Σ_{i=1}^{υ_e}(p_i+1))`——用户任务给的系数展开式**就是原文定义**，不再是推定。B2 取 p_i=m₂、k_bin=0 ⇒ `c^(e)=d·υ_e·(m₂+1)`（docs/22 §E1D）。而 Thm5.3 的 C2（印刷页 45 **视觉**）为 `(B^(e))² + √(υ_e+k_bin)·d·B^(e) < q`，**`d` 在根号外**；文本流与旧稿写成 `√((υ_e+k_bin)d)` 是 OCR 误读。`c^(e)` 与 C2 的两个计数是**不同来源、不可互换**：`c^(e)` 数 E_i 输出与余量的系数总量（进入 C1 与 Lemma 2.9），C2 的 `υ_e+k_bin` 只数 exact 关系与独立二值约束的个数（进入整数提升，见 docs/22 §E1D/E2b）。不得把 `Σp_i` 直接代入 C2 的根号。

`[推导]` **若多约束方案不成立（用户 C3）**：退路是保留 Step5/Step17 **两组独立 exact-norm 调用**。代价与约束：
- 同一联合 witness：两组调用若共用 (s_A,m_A,r) 且都并入**同一个** Fig10 statement 的不同 (E_i,β_i) 块，仍可由一个提取器提取共同 witness（§1.2）——即"两次调用"指**同一 statement 内两组约束**，不是两个独立协议；
- 提取一致性：由单一提取器保证（非两个提取器事后比对）；
- 额外 challenge / 知识误差：若真拆成两个协议才有额外误差；同一 statement 内多 E_i 无额外 challenge（挑战矩阵 R⁽ᵉ⁾ 一次覆盖全部 E_i）；
- 辅助承诺重复：不重复（一份辅助承诺的拼接 witness 覆盖两批）；
- 盐不相交：保持（§2.4，两批 salt 索引互异）。

`[推导]` **方案比较（仅 A/B，不重开 B1/B2）**：
| 方案 | 不同 β 处理 | 主要风险 |
|---|---|---|
| 多 E_i 同一 statement（推荐先试） | 每个 E_i 带自己的 β_i^(e)，整数提升用 max | `Σp_i` vs `υ_e` 计数对账、B^(e) 增长（docs/22） |
| 两组独立 exact 调用拆两协议 | 各自 β，互不影响 | 回到"两个提取器 / 同一性未证"（B1 缺陷），**不采用** |
| 强行统一 E_{s₂}+统一 β | 压成单一 β | 违背 LBF 原文两界不同、未实例化——**禁止**（用户 C 明确） |

---

## 3. 边界与待核查（任务 A/D，LB-06R 更新）

- `[已修正 · LB-06]` 提取流程：旧稿"只对最终 c 分叉一次"错误，已改为外层两次 challenge-matrix 执行 + 底层 E₁（§1.4）；Fiat–Shamir 栈（附录 B）单列为另一层级。
- `[原文内部不一致 · 四层分开记录]` Thm5.3 陈述页 ε 用减号含 `−2^{−127}`、证明页用加号且**缺 `2^{−128}` 裕量**，②→③ 的推导不闭合；B2 显式采用层④充分条件 `ε≥T+2^{−128}`（§1.5-A1/A2）。**不再写"以证明页为准即解决"**。
- `[原文符号三分 · 不做等同]` 时间：陈述页 `2T_{E_eval}`、证明正文 "2×E₁"、证明结论 `2T_{E′}`（§1.5-A4）；未证 `T_{E_eval}=T_{E₁}`。
- `[已视觉确认 · LBF 官方 PDF]` β_step5/β_step17 精确表达式见 §2.5（印刷页 47）；`B̃` 定义与单块/整批口径仍待核查，原文标 "we do not instantiate"。
- `[已闭合 · LB-06R]` `c^(e)=d(k_bin+Σ(p_i+1))` 为原文 Fig10 输入（L6020–6027）；C2 的 `√(υ_e+k_bin)·d` 中 d 在根号外（印刷页 45 视觉）；两种计数分开（docs/22 §E1D/E2b）。L5613 vs L5653 的 σ 分量排列歧义（§1.7 问 4）仍待核查。
- `[参数实例化待核查]` E_{s₂} 的 2(m₁+m₂+ℓ) 扩展维度接口；Thm5.3 参数（q,B⁽ᵉ⁾,k_bin,c⁽ᵉ⁾）按新维度重推（docs/22）。
- `[待核查]` exact 余量 x_i（(2)）与 Eq.(54) 独立二值约束（(3)）的 k_bin 设定（§1.7；B2 取 k_bin=0 且不占 Ajtai 列，docs/22 §E1C.2）。
- `[未证 · 见 docs/21]` 三层 binding 严谨归约、混合 MSIS 差向量界、联合提取 s̄₂ 与诚实 opening 的计算绑定。
- `[边界]` 联合提取器 = Theorem 5.3 的**结构**继承；≠ 完整安全证明 / 已参数实例化 / 已实现；概率账本 ≠ 已达 128-bit；≠ 递归无 c̄ 累积（docs/15）。
- 不写"两个独立证明的 s₂ 自动同一"；不把"写在同一 statement"当"已证知识可靠"；不把 exact β 当无放大 MSIS 界；不做 Decider/LaZer。
