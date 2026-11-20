# Literature Map

> 本文件是阅读入口与竞争工作排查表，不是完整综述。每条"是/否/部分"必须有指定版本原文证据；只用摘要下结论的格子明确标注 `[摘要级]`。
> 本轮更新：LB-01 / 任务 F（2026-11-20）。核查日期：2026-11-20。
> 四层区分贯穿全文：**① 论文理论上提出 ② 论文完成安全证明 ③ 论文提供实现/数据 ④ 实现已被第三方复现**。表格单元格用上标标注层级；未达某层的不要外推。

---

## 1. 竞争工作比较表

图例：✅=有且已证明/实现；◑=部分/有限制/仅单步；❌=无或未声称；`?`=未充分核查。`[摘要级]`=只据官方 ePrint 摘要页，正文未逐节核。

| 工作（版本） | 格基安全 | 零知识 | Folding | Decider | 递归组合 | 实现 |
| -- | ---- | --- | ------- | ------- | ---- | -- |
| **NovaBlindFold** — HyperNova §7, ePrint 2023/573（Kothapalli–Setty; Vega ePrint 2025/2094 为其实现路线） | ❌ 离散对数（非 PQ） | ✅ blinding folding（HVZK 式）；[摘要级 + LBF §1 转述] | ✅ Nova folding + blindfold | ◑ 需 Spartan 外包验证（LBF 对 NovaBlindFold 的读法） | ✅ Nova IVC 语境；[摘要级] | ✅ Vega: 92ms prove/23ms verify/108kB（1920B credential）；[摘要级] |
| **SuperNeo** — ePrint 2026/242（Nguyen–Setty, CRYPTO 2026, 2026-09-04 末版） | ✅ Module-SIS / 小域；[摘要级 + LBF §2.4] | ❌ 明确 non-blinding；LBF Abstract/§3.1（p.1/20） | ✅ CCS folding，sum-check 单调用；pay-per-bit | ◑ 有 `Π_DEC`（**decomposition reduction**，非 Decider）；LBF Prop 2.26 | ✅ IVC/PCD 声称；[摘要级] | ◑ 论文有 evaluation；[摘要级]，未复现 |
| **LatticeFold** — ePrint 2024/257（Boneh–Chen, 2025-12-15 末版） | ✅ Module-SIS；[摘要级] | ❌ 摘要无 ZK/blinding；LBF Abstract 将其列为 randomizing only | ✅ R1CS/CCS，sumcheck 范数控制 | ? 未针对"承诺求值声明 Decider" | ✅ recursive SNARK + PCD（摘要明确） | ◑ 论文 evaluation "as performant as HyperNova"；[摘要级] |
| **LatticeFold+** — ePrint 2025/247（Boneh–Chen, CRYPTO 2025） | ✅ 格基（摘要继承 LatticeFold）；[摘要级] | ❌ 摘要无 ZK；LBF 列为 randomizing only | ✅  rangeproof 改进、double commitment、prover 5–10× 快 | ? | ✅ succinct proof systems 语境 | ◑ 有实现/性能声称；[摘要级] |
| **Verifiable Bootstrapping from Lattice-based Folding** — ePrint 2026/1127（Deo–Thibault, 2026-06-25） | ✅ 格基 IVC；[摘要级] | ❌ 摘要无 ZK；只讲 FHE bootstrapping 正确性 | ✅ 首个 lattice-based IVC from folding | ◑ 算术化 folding verifier（近 Decider 但目标是 IVC verifier） | ✅ IVC + ROM 下 knowledge-soundness 论证 | ✅ **explicitly construct and benchmark**；[摘要级]，第三方复现 `?` |
| **NovaBlindFold 工具链 / Jolt BlindFold** — 文档与 a16z 博客（2026） | ❌ | ✅ ZK folding（Nova 型） | ✅ | ◑ Spartan/outer 验证 | ✅ | ✅ 已集成（Vega/Jolt）；[二手/文档级，非论文] |
| **LaBRADOR ZK Toolkit** — ePrint 2026/1289（Biasioli–Bolboceanu–Lyubashevsky–Merino-Gallardo–Osadnik–Seiler–Steuer, CCS 2026, 2026-11-03 末版） | ✅ Module-SIS/LWE；[摘要级] | ✅ 真 ZK（集成 LNP22 线性大小 ZK，摘要明确） | ❌ 非 folding（通用简洁 ZK） | ✅ 通用：可对任意陈述（含算术化 ABDLOP 验证）出证明 | ◑ 工具级支持，非 folding 递归 | ✅ 已实现并 benchmark，扩展 LaZer；<100KB；[摘要级] |
| **LaZer / LaBRADOR 实现** — github.com/lazer-crypto/{lazer,labrador} | ✅ | ✅ | ❌ | ◑ 同上 | — | `[待核查]` 仓库当前 commit/构建未本轮实测（只核链接与 Toolkit 摘要对其扩展的陈述） |
| **LatticeBlindFold** — ePrint 2026/1857（Dall'Ava, 2026-09-01, v1） | ✅ Module-SIS/LWE/E-MLWE；§2.6 | ✅ **blinding，但仅 K=1、单步、blinded layout、unpadded、交互**；Thm 4.13 p.48 | ✅ 单次 step；Π_LBF = Π′DEC∘Π′RLC∘Π′R1CS | ❌ **明确缺口**，给出两条路但未实例化；§4.3.3/§5 | ❌ 明确不声称；Protocol 13 仅 blueprint | ❌ 论文未给实现；§4.3.3.1 只有 analytic size estimate（≈8.2/5.5MB），§5 列为 future work |

---

## 2. 四层区分逐项说明（防"论文提出"当"已实现"）

1. **理论上提出**：LatticeBlindFold 提出 ABDLOP 承诺版 commit-and-prove + Libra masking 的格基 folding；Decider 只是被点名"需要"，**没有提出具体 Decider 构造**。
2. **完成安全证明**：LBF Theorem 4.13 给出 RoK + blinding（有严格条件）✅；FS 下 round-by-round KS **未证**（§5 item (3)）；`K>1` blinding 未证。
3. **提供实现/数据**：LBF **没有**可运行实现；只有 §4.3.3.1 的分析式大小估算与 §4.3.4 参数估计（δ、ε、bit security）。参照工作 Vega、LaBRADOR Toolkit、Verifiable Bootstrapping 有 benchmark（均摘要级证据）。
4. **实现已经能够复现**：本仓库尚未对任何第三方实现做本地复现；`[待核查]`。

---

## 3. 竞争工作排除结论（针对候选问题："盲化承诺求值声明的可组合 ZK Decider"）

`[论文事实 + 推导]`，证据逐条：

- **NovaBlindFold / Vega / Jolt BlindFold**：✅ 已实现 ZK folding，但基于离散对数、非后量子（LBF §1）。**排除**（不满足格基安全维度）；其"用 random instance + Spartan 外包"的 Decider 思路可作为对照参考，但不能直接迁移到 ABDLOP 承诺。
- **SuperNeo / LatticeFold / LatticeFold+**：格基 folding 的强基线，但 LBF Abstract 明确它们 only randomizing, not blinding；且它们的 recursion/PCD 面向**承诺实例**，不产出 LBF 式 ABDLOP committed evaluation claims。**排除**为"盲化承诺声明 Decider"的直接解；它们是上游协议而非竞争者。
- **Verifiable Bootstrapping from Lattice-based Folding (2026/1127)**：✅ 有实现与 benchmark，且**算术化了 folding verifier**——与"把验证步骤放进 R1CS"的 succinct Decider 路线最接近。但它做的是 FHE bootstrapping 的 IVC 正确性，**摘要无零知识/盲化**，且没有 ABDLOP 承诺求值声明这一输出形态。**部分排除**：它证明"算术化格 folding verifier 可实现"，但不覆盖 LBF 的 ZK + 承诺声明接口；其 benchmark 数据（更小证明、prover/verifier 代价陡增）可作为成本参考。
- **LaBRADOR ZK Toolkit (2026/1289) / LaZer**：✅ 通用简洁格 ZK、有实现、<100KB 证明、**可证明任意陈述**，理论上可用来证明算术化后的 ABDLOP 验证。**未排除**：它是**潜在后端**而非现成 Decider；LBF §4.3.3/§5 明确指出障碍是 exact-ℓ₂ 范数证书、非简洁承诺宽度与安全模型拼接。不能把"有通用 ZK 工具"等同于"Decider 问题已解决"。
- **LatticeBlindFold 自身**：明确把 Decider 留空（"we instantiate neither, and record the gap as such"），故其候选问题**未被自身覆盖**。

**结论**：截至 2026-11-20，在已核工作范围内，**"针对 LatticeBlindFold 输出的 k 个 committed evaluation claims 的简洁、知识可靠、保持 ZK 的 Decider（并连带递归接口）"没有现成实现或论文级完整构造**。最接近的两条边界是 (a) 2026/1127 的 folding-verifier 算术化（无 ZK/无承诺声明接口），(b) 2026/1289 的通用格 ZK 工具（需自行算术化 + 范数证书）。这两条必须作为下一阶段的直接对照，不能回避。

`[待核查]` 可能对结论构成威胁但未逐字核正文的条目：Cyclo [GLLO26]、PikkuFold [Osa26]、Hachi [NOZ26]、Greyhound [NS24]、CFW26、KLSS23、以及截至本日的新预印本。本轮只在 LBF 引用中见其名。若下一阶段要主张研究空白，须再核这些工作。

---

## 4. 原始入口（书目）

- SuperNeo, IACR ePrint 2026/242: <https://eprint.iacr.org/2026/242>
- LatticeBlindFold, IACR ePrint 2026/1857: <https://eprint.iacr.org/2026/1857>
- NovaBlindFold（HyperNova §7）, ePrint 2023/573: <https://eprint.iacr.org/2023/573>
- Vega（NovaBlindFold 实现路线）, ePrint 2025/2094: <https://eprint.iacr.org/2025/2094>
- LatticeFold, ePrint 2024/257: <https://eprint.iacr.org/2024/257>；LatticeFold+, ePrint 2025/247: <https://eprint.iacr.org/2025/247>
- Verifiable Bootstrapping from Lattice-based Folding, ePrint 2026/1127: <https://eprint.iacr.org/2026/1127>
- LaBRADOR ZK Toolkit, ePrint 2026/1289: <https://eprint.iacr.org/2026/1289>
- BDLOP, ePrint 2016/997: <https://eprint.iacr.org/2016/997>；ABDLOP/LNP22, ePrint 2022/284: <https://eprint.iacr.org/2022/284>
- LaZer: <https://github.com/lazer-crypto/lazer>；LaBRADOR: <https://github.com/lazer-crypto/labrador>
- Nova: ePrint 2021/370: <https://eprint.iacr.org/2021/370>

> **引用勘误（重要）**：本任务包原文把 NovaBlindFold 写成 ePrint **2025/1210**。经核查，2025/1210 是 *A Generalized Approach to Root-based Attacks against PLWE*（Blanco Chacón et al.），**不是 NovaBlindFold**。正确的原始入口是 HyperNova (ePrint 2023/573) §7 "NovaBlindFold" 与 Vega (ePrint 2025/2094)；LBF 自己引用为 `[KS23, KS25]`。已在日志中记录修正。

---

## 5. 记录规则

每次引用论文时，补充：版本日期、章节/页码、原文定义或定理编号、自己的解释，以及适用条件。仅凭摘要或博客不得标记为"已解决/未解决"；表格中凡 `[摘要级]` 的格子都需要下一阶段回正文确认后才能升级为结论。
