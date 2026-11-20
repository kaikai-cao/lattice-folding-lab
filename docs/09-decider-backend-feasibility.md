# Decider 后端可行性与安全模型拼接审查

> 状态：LB-02 / 任务 B + 任务 D 完成。本文件比较三条候选路径，**不构造新 Decider，也不声称已实现。**
> 主来源：`[LBF]` ePrint 2026/1857，§4.3.3、§4.3.3.1、§4.5、§5、Remark 4.8/4.22/4.26；`[LNP22]` ePrint 2022/284，§5.2、Theorem 5.3、§6.1；`[LBR26]` LaBRADOR ZK Toolkit ePrint 2026/1289；`[LBR23]` LaBRADOR ePrint 2022/1341；`[CFW26]` ePrint 2026/391，§2.3–2.5、§6；`[GH24]` Greyhound ePrint 2024/1293；`[HNO26]` Hachi ePrint 2026/156；`[NS26]` SuperNeo ePrint 2026/242。
> 标签：`[论文事实]` / `[实现事实]` / `[推导]` / `[研究假设]` / `[待核查]`。成本数字必须附口径，不从渐近符号外推实际运行时间。

---

## 0. 决策对象

Decider 要验证的关系不是原始 R1CS，而是 LB-01 `docs/07` 定义的：

```
Public: pp, {c'_i,x'_i}_{i∈[k]}, r', {C'_{i,j}=Commit(y'_{i,j},s'_{i,j})}, PoK transcript
Witness: {z'_i, y'_{i,j}, s'_{i,j}}
Relation CE_com^k:
  c'_i=L(z'_i) ∧ x'_i=L_in(z'_i) ∧ ‖z'_i‖∞<b
  ∧ y'_{i,j}=M̄_j ẑ'_i(r') ∧ C'_{i,j}=Commit(y'_{i,j},s'_{i,j})
  ∧ ‖s'_{i,j}‖∞<B̃ ∧ ‖Σ_i b^{i−1}z'_i‖∞≤τ·s.
```

`[推导]` 任何“Decider”若只验证范数、只验证某个 PCS 求值，或只重放 PoK 转录，都没有覆盖完整关系。下面三条路径按“覆盖完整关系的能力”排序，而不是按实现难度排序。

---

## 1. 路径一：直接验证 ABDLOP Opening（线性扫描基线）

### 1.1 构造描述

`[论文事实: LBF §4.3.3, p.52]` 原文给出的 direct route：把 `N_PoK = 5+(K+k+1)t` 份 ABDLOP PoK 转录原样交给下游 verifier，逐份检查 `tA=A₁s₁+A₂s₂`、`tB=Bs₂+m`、masked opening 范数、盐替换与 challenged relation。

### 1.2 评估

| 维度 | 结论 |
|---|---|
| 数学兼容性 | `[论文事实]` 完备且 sound：同一单步协议内的 PoK 已认证输出；不需要新数学组件。 |
| 完备性 | `[论文事实]` 继承 Theorem 4.13；统计完备性误差 `≤9·2^{−λ}`（batched）。 |
| 知识可靠性 | `[论文事实]` 继承 ABDLOP PoK 的 KS 与 LBF RoK；**但 verifier 成本线性扫描**。 |
| 零知识 | `[论文事实]` 保持 LBF 单步 blinding/ZK 条件（`K=1`、blinded layout、unpadded）。 |
| 证明大小 | `[论文事实: §4.3.3.1]` 单次 folding 转录 d=128 ≈8.2 MB，d=64 ≈5.5 MB；其中 masked openings 4.57/3.01 MB，输出 ABDLOP 承诺 1.98/1.19 MB；单位 ABDLOP commitment 23.05/14.38 KB。 |
| Prover Time | `[推导]` 无额外外层 prover；只是原 transcript。 |
| Verifier Time | `[论文事实]` 电路/检查量为 `Θ(N_c(m₁+m₂)d)` 环运算；随 k、t 线性增长。 |
| 批量验证 | `[论文事实]` LBF 有 `Π_many^{(1)}` batched constant-coefficient proof，但输出转录整体仍需逐项检查。 |
| 递归组合 | `[推导]` 不提供简洁状态；实质是把 5–8 MB 转录交给下一层，不构成 NovaBlindFold 式 Decider。 |
| 实现可行性 | `[论文事实]` 组件级可实现；论文未给完整实现。 |

### 1.3 角色

`[推导]` 路径一是**正确性基线与成本上界**，不是候选研究贡献。它证明“关系已经可验证”，但不能满足“简洁、可递归”的目标。若后续最终结论为 HOLD/NO-GO，这一路径是必须诚实写出的 fallback。

---

## 2. 路径二：LNP22 exact-ℓ₂ + LaBRADOR / LaZer 外层证明

### 2.1 构造设想（仅接口级，不实现）

`[论文事实 + 研究假设]`

1. 算术化 ABDLOP 线性等式：`tA=A₁s₁+A₂s₂`、`tB=Bs₂+m`，以及 `CE_com^k` 的 `L/L_in/evaluation hint/承诺同态` 关系；LBF §4.3.3 说线性部分已是 `R_F` 上的 R1CS 形状。
2. 对范数子句嵌入 `LNP22 §5.2` 的 exact-ℓ₂ commit-and-prove；按 `docs/08` 的结论，必须用 §3.2.1.1 anchoring 才能触及 LBF 的 `s₂`，并在 `R_F` 上 component-wise 处理 `K=F_{q²}`。
3. 把上述约束交给外层格基简洁 ZK 证明系统（LaBRADOR/LaZer），目标是让 verifier 只检查一个短证明而不是 5–8 MB 转录。

### 2.2 必须区分的三个层次

`[论文事实: LBR23, LBR26, LaZer repo]`

| 层次 | 能力 | 不能外推为 |
|---|---|---|
| LaBRADOR 原始协议（2022/1341） | Module-SIS 上的简洁 ZK/R1CS 证明框架 | 自动包含 LBF 承诺、exact norm、递归接口 |
| LaBRADOR ZK Toolkit（2026/1289） | 集成 LNP22 线性大小 ZK，扩展 LaZer，给出 <100KB 级证明声称 | “任意陈述”包括具体 LBF 关系且成本仍 <100KB |
| LaZer 实际代码 | 暴露 `abdlop_keygen/commit/prove/verify`、`lnp_prover_set_statement_l2` 等接口；有 L2EXACT 类型 | 已有 `CE_com^k` Decider 或直接可调用的 LBF 适配器 |

`[实现事实: 静态核查]` LaZer 仓库当前 commit `b958e247a2fdb9593b3c25c9603c6c5305c19420`；LaBRADOR 仓库 `c1ae0e612d5accd9e7d9d1c264951c1afe949c83`。代码中可见 `normtype` 枚举的 `L2EXACT`、`commit()`、`verify()` 与 exact euclidean 参数痕迹；README 要求 Linux amd64/x86-64、AVX-512、AES、gcc≥13.2、Sage≥10.2。当前 i7-14700 无 AVX-512，**未构建验证**。

`[推导]` 因此“LaBRADOR 支持任意 NP，所以可直接用”是错误论证；必须证明 LBF 的具体承诺矩阵、盐界、challenge 域、component-wise 展开、安全模型都能被接口接受。

### 2.3 数学与工程阻断

`[论文事实: docs/08 结论; LBF §4.3.3/§5]`

1. **范数缺口仍未关闭**：LNP22 exact machinery 不覆盖 LBF 的 `s₂`；LBF 只 sketch 了 anchoring，没有实例化（Remark 4.8）。
2. **电路规模**：算术化电路约 `Θ(N_c(m₁+m₂)d)` 环运算；这是一个大电路，简洁外层证明的 prover 成本可能吞掉收益。
3. **证明大小不可从 Toolkit 摘要外推**：Toolkit 的 <100KB 是其应用实例化下的结果；LBF 的关系包含 `k·t` 个 hint 承诺和 `N_PoK` 份转录语义，未证明外层证明仍在该量级。
4. **函数调用不等于协议组合**：LaZer 的 `set_statement_l2` 期望自己的 statement/witness 布局；LBF 需先把 `CE_com^k` 编译成该布局，这一步本身是未完成的协议工作。
5. **批量/递归**：静态接口可见批量式证明痕迹，但没有证据表明存在对 LBF 输出状态可直接递归的组合接口。

### 2.4 成本判断（列明假设）

`[推导]` 设外层证明的 statement 已成功编译为 LaBRADOR 关系，且 exact norm 的 component-wise 展开已加入；则：

- **Verifier Time**：目标是 polylog/简洁，但只有在“外层证明确实对该大电路简洁”且 FS/RBR 安全成立时成立；当前为 `[研究假设]`。
- **Prover Time**：至少包含 (i) 算术化 `CE_com^k` 的 witness 展开，(ii) exact norm 的二进制分解与 rejections，(iii) 外层 ZK prover。没有实测，不给具体秒数。
- **Proof Size**：下界不是 0；需对 `N_c,m₁,m₂,d,υ_e,k_bin` 代入后估算。直接引用 <100KB 会混淆 Toolkit 自身陈述与 LBF 陈述。
- **Outer commitment count**：需把 `x_i`、`x′`、sign、approximate range proof 辅助承诺纳入；`docs/08` §4 给出 LNP22 原公式，但未绑定到 LBF。

### 2.5 路径二结论

`[推导]` **数学上可能，安全与成本均未建立；不能称为已构造的简洁 Decider。** 若后续继续，第一优先级不是“调 LaZer”，而是完成 LBF 特定 `CE_com^k → statement` 的编译器式定义，并证明 `s₂` anchoring 与 component-wise exact norm 的正确性。

---

## 3. 路径三：PCS / IOP 组合方案

### 3.1 Greyhound

`[论文事实: GH24]` Greyhound 是格基多项式承诺与求值验证技术，解决“承诺多项式在点的求值”相关子问题。

`[推导]` 它能覆盖 `y'_{i,j}=M̄_j ẑ'_i(r')` 中“求值声明”的某一层，但不验证：
- ABDLOP 承诺的 opening 与盐；
- `A₁s₁+A₂s₂`、`Bs₂+m` 的绑定关系；
- exact-ℓ₂ 盐界；
- LBF PoK 转录与知识可靠性。

`[论文事实: LBF §3.5, p.31–32]` LBF 作者已说明 folding 内部被承诺对象很小，用简洁 PCS 压缩“不划算”。这只解释内部 mask 不用 PCS，不直接排除外部 Decider 使用 PCS。

**分类：组件级相关，不是 Decider。**

### 3.2 Hachi

`[论文事实: HNO26]` Hachi 是扩域上的高效格基 multilinear polynomial commitment，使用 ring switching、trace map、inner/outer Ajtai commitment 等技术；它不是通用多变量 PCS。

`[推导]` LBF 的 Sum-Check 是布尔多变量、掩码多项式为 `a₀+Σp_i(X_i)`，component-wise 承诺在 `R_K`。Hachi 的 multilinear/extension-field 结构可能用于某类求值子声明，但不能直接替换 LBF 的 polynomial masking 承诺结构，也不能替代 ABDLOP Decider。

**分类：不能等同于通用多变量 PCS，不能直接解决 Decider。**

### 3.3 CFW26

`[论文事实: CFW26 §2.3 Lemma 2.5, §2.5, §6 Theorem 6.3/Lemma 6.5/Lemma 6.6]`

CFW26 给出：
- 强化的 IOR HVZK 定义（Definition 2.4），要求模拟器同时模拟后续对 implicit instance 的查询；
- 组合定理（Lemma 2.5）：误差按 `ζ₁+ζ₂` 累加，并要求输出对下一阶段是 fresh input；
- 零知识 sum-check reduction：用编码的 spare coordinates 保存 mask，mask polynomial `U_σ` 隐藏 sumcheck messages；
- Theorem 6.3：k+1 rounds、`k·d_s+1` 个 M 元素直接通信、verifier `O(k d_s)`；
- Lemma 6.5：HVZK on fresh inputs，误差约 `2^k ζ_C`；
- Lemma 6.6：round-by-round knowledge soundness。

`[推导]` 对 LBF 的影响：
1. **可能替代/改进的是 mask 阶段的组合性质**，尤其是“后续查询是否泄漏”的问题；LBF 的 Libra-style masking 与 CFW 的 spare-coordinate masking 属于同类但不同实例化。
2. **不能直接替代 ABDLOP Decider**：CFW 的输出仍是 folded oracle/linear constraint，不是 `CE_com^k` 的承诺 opening 与盐界。
3. **HVZK on fresh inputs ≠ malicious-verifier ZK**；`fresh output` 条件若不满足，组合定理不能用。
4. **挑战集条件**：CFW 要求有限非空 `C⊆Z(R)` 且满足相应 sampling/MCA 条件（中心、两两差可逆）；LBF 的强采样集/扩展环挑战需另行匹配。
5. **mask 分布存在实质冲突**：CFW Lemma 6.2 的 transcript-uniformity 论证要求 mask 参数 `σ` 在 `(R^p)^{k+1}` 上均匀，而 LBF 为 ABDLOP 承诺必须让 mask 系数为短范数；直接换成短 σ 会破坏 uniformity 论证。
6. **RBR KS 有帮助但不能自动补齐 LBF §4.5 的缺口**：LBF 明确说 Sum-Check+ABDLOP 的 round-by-round KS 未证，generic multi-round bound 在 `21+N_PoK` rounds 下 vacuous。CFW 的 RBR relaxation 是 list-decoding/proximity，LBF 的 relaxation 是范数与坐标反演，二者拼接仍需新证明。

**分类：重要的组合理论工具；不是 Decider。**

### 3.4 Verifiable Bootstrapping from Lattice-based Folding

`[论文事实: 2026/1127 摘要 + LB-01 文献地图]` 它算术化了 folding verifier 并给 IVC benchmark，是“验证器算术化可行”的性能参考；摘要无 ZK，输出关系不是 LBF 的 ABDLOP committed evaluation claims。

**分类：性能/工程基线，不是目标问题的解。**

### 3.5 路径三结论

`[推导]` PCS/IOP 各自解决不同层次：Greyhound/Hachi 解决部分求值承诺，CFW 解决可组合 HVZK sumcheck IOR，LaBRADOR 解决通用简洁 ZK。**它们不是可互换的同一个组件。** 一个完整 Decider 仍需定义层间接口、状态 freshness、承诺兼容、范数证书与安全拼接。

---

## 4. 三路径统一比较

`[推导]` 评级说明：✅=已有/可严格继承；◑=部分或条件成立；❌=无或无研究价值；`?`=需新证明/实测。

| 指标 | 路径一：直接验证 ABDLOP Opening | 路径二：LNP22 + LaBRADOR/LaZer | 路径三：PCS/IOP 组合 |
|---|---|---|---|
| 数学兼容性 | ✅ 同协议内直接成立 | ◑ 基础兼容，`s₂`/扩展环/槽位需改写 | ◑ 只覆盖求值或 sumcheck 子层 |
| 完备性 | ✅ Theorem 4.13 | `?` 需 LNP22+LBF+外层拼接后重证 | `?` CFW 有其自身条件；LBF 拼接未证 |
| 知识可靠性 | ✅ 继承 ABDLOP PoK（线性验证） | `?` 需 binding + LNP extraction + 外层 KS + 拼接 | ◑ CFW 有 RBR KS；ABDLOP Decider 未覆盖 |
| 零知识 | ✅ 保持 LBF 单步条件 | `?` E-MLWE + rejection + 外层 ZK 需组合证明 | ◑ CFW 是 HVZK on fresh inputs，非全局 ZK |
| Proof Size | ❌ 8.2/5.5 MB 转录 | `?` Toolkit <100KB 不能外推；需按 LBF 关系估算 | `?` 无完整 Decider 证明大小 |
| Prover Time | ✅ 无额外 prover | `?` 至少含大电路算术化 + exact norm + 外层 prover | `?` 组件级有界，整体未定义 |
| Verifier Time | ❌ `Θ(N_c(m₁+m₂)d)` | ◑ 目标简洁，但未证 | `?` 取决于最终组合 |
| 递归组合 | ❌ 无简洁状态 | `?` exact norm 是必要非充分；接口未定义 | ◑ CFW fresh-output/RBR 有帮助，非 Decider |
| 实现可行性 | ◑ 组件有、论文无完整实现 | ◑ 仓库有 API；无 LBF 适配；AVX-512 限制 | ◑ 组件各在，不在同一关系上 |

**排序结论**：路径一是基线；路径二是唯一可能达成“简洁 Decider”的路线，但阻断最多；路径三是工具箱，不可替代路径二，只能辅助其中求值/sumcheck 子层。

---

## 5. 安全模型兼容性检查表

### 5.1 各组件实际提供的性质

`[论文事实]`

| 组件 | ZK 类型 | Soundness 类型 | 交互模型 | 组合条件 |
|---|---|---|---|---|
| LBF 单步 | blinding；`ε≈2^{−112}` 非零；`K=1`、blinded/unpadded | RoK + ABDLOP PoK KS | public-coin interactive，honest-but-curious V* 语义 | 单步；递归未证 |
| ABDLOP PoK | computational hiding + ZKPoK simulator | MSIS-based binding/KS | interactive | 需共享矩阵、盐界、扩展 MLWE |
| LNP22 §5.2 | commit-and-prove simulatability；rejection sampling | rewindable black-box extraction；tight ℓ₂ | interactive | 参数条件 Theorem 5.3；`s₂` 未覆盖 |
| LaBRADOR / Toolkit | 格基 ZK；Toolkit 集成 LNP ZK | Module-SIS / R1CS KS | 通常 FS 后非交互 | ROM 下安全描述；QROM/递归需另证 |
| CFW26 sumcheck IOR | HVZK on fresh inputs，误差 `2^kζ_C` | round-by-round KS | IOR / oracle 模型 | fresh input + fresh output；强采样集 |
| SuperNeo Π_DEC | non-blinding | RoK decomposition reduction | interactive | 非 Decider |

### 5.2 必须区分的边界

`[论文事实 + 推导]`

1. **Perfect / Statistical / Computational ZK**：LBF 的 blinding 是统计意义且误差非零；不能写成完美 ZK。LNP22 的 simulatability 依赖 Extended-MLWE，属于 computational。
2. **HVZK / Malicious-verifier ZK**：CFW26 只给 HVZK on fresh inputs；LBF 内部 ABDLOP 转录的模拟依赖 message-omitting simulator + rejection sampling，不是对任意外部组合自动成立。
3. **Soundness / Knowledge Soundness**：Σ-protocol 式 soundness 不足以证明提取出 witness；Decider 目标要求 KS。
4. **Public-coin interactive / Non-interactive**：LBF 是交互式；FS 后需 ROM/QROM 与 RBR KS。LBF §4.5 明确说 Sum-Check+ABDLOP 的 RBR KS **未证**，generic multi-round bound 在 `log₂m=21 + N_PoK` 下 vacuous。
5. **单步 / 可组合 / 递归**：LBF 单步 blinding 与 RoK 不推出多轮递归；Relaxed bound 每轮累积（Remark 4.8）。exact-ℓ₂ 关闭盐放大，但仍需 Decider 状态、freshness 与 RBR 安全。
6. **ROM / QROM**：Toolkit/LaZer 的 FS 安全描述不能自动迁移到 LBF；本阶段未找到 LBF 特定 QROM 证明，`[待核查]`。

### 5.3 拼接条件清单

`[推导]` 若后续坚持路径二，必须逐项证明：

- [ ] LBF 输出 `CE_com^k` 可无歧义编译为外层证明的 statement，且公开输入不包含秘密盐；
- [ ] exact norm 同时覆盖 witness 与两组盐，特别是 `s₂` 的 anchoring；
- [ ] component-wise base-ring 分解后，自同构/范数恒等式仍然正确；
- [ ] ABDLOP binding、LNP extraction 与外层 KS 的 soundness error 可合并，不能简单相加后忽略挑战相关性；
- [ ] ZK 模拟器的 view 包含后续 verifier/decider 查询；若只能 HVZK，必须证明 fresh-input/fresh-output；
- [ ] FS 转换的 RBR KS 与 grinding 界成立；d=64 参数集已知不足，不能作为安全实例化；
- [ ] 递归状态包含精确范数与承诺 opening 的唯一性，不能依赖“诚实 prover 的输出范数”假设。

---

## 6. 本阶段判断

`[推导]`

- **路径一**已经给出“可验证但巨大”的基线，无法满足简洁/递归目标。
- **路径二**是唯一在数学上可能达到简洁 Decider 的路线，但当前缺少三项关键证明：LBF 特定关系编译、`s₂` exact anchoring、安全模型拼接；成本也未实测。
- **路径三**提供可替换的 sumcheck masking 与部分 PCS 组件，但不解决 ABDLOP opening、盐与完整 Decider 关系。
- 因此技术状态是 **HOLD 条件成立**：不是 NO-GO（没有数学矛盾或已覆盖证据），也不是 GO-A（没有已验证构造）。最终决策见 `decisions/LB-02-decision.md`。

---

## 7. 待核查 / 待估算

- `[待核查]` LaBRADOR Toolkit 对具体 `CE_com^k` 关系的 statement 编译方式、批量接口与 FS 安全模型细节。
- `[待核查]` CFW26 spare-coordinate mask 与 LBF Libra-style mask 的形式化等价/差异；fresh-output 是否成立。
- `[待估算]` exact norm component-wise 展开后的 proof size、prover/verifier 时间；需固定 `N_c,k,t,m₁,m₂,d` 后按 `docs/08` §4 公式计算。
- `[待核查]` 2026/1127 的具体 benchmark 与是否可被改造成 ZK；本文件只作为性能基线。
- `[待核查]` QROM 下 LaBRADOR/LaZer + LBF 拼接的安全论证是否存在。
