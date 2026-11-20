# LB-02 竞争工作针对性排查

> 状态：LB-02 / 任务 C + 任务 E 完成。本文只更新 LB-01 `docs/00-literature-map.md` 中 `[待核查]` 的竞争项，不重复完整综述。
> 来源：`eprint.iacr.asia` 公开 PDF 镜像全文（eprint.iacr.org 受 Cloudflare 阻挡），官方 ePrint 入口用于书目；工程仓库以固定 commit 做静态核查，未构建。
> 标签：`[论文事实]` / `[实现事实]` / `[推导]` / `[研究假设]` / `[待核查]`。

---

## 0. 一句话结论

`[推导]` 截至本次核查，**没有一项竞争工作直接解决 LatticeBlindFold 输出的 `CE_com^k` 简洁、知识可靠、保持 ZK 的 Decider**。但已有四类工作分别覆盖了周边关键组件：

| 工作 | 覆盖的周边组件 | 未覆盖的目标 |
|---|---|---|
| Cyclo / PikkuFold | 高效 folding、norm refresh、range proof、challenge sampling | ZK folding、ABDLOP Decider |
| Hachi / Greyhound | 扩域/环上多项式求值承诺 | 通用多变量 LBF mask、ABDLOP opening/salt/norm |
| CFW26 | 可组合 HVZK sum-check IOR、RBR knowledge soundness | ABDLOP committed evaluation claims Decider |
| LaBRADOR ZK Toolkit / LaZer | 通用格基简洁 ZK、exact-norm 相关接口 | LBF 关系编译、`s₂` anchoring、递归 Decider 接口 |

---

## 1. Cyclo（ePrint 2026/359）

### 1.1 核心机制

`[论文事实: Cyclo §1–2.2, §5, Appendix C.2]` Cyclo 提出 **amortized norm-refreshing folding**：

- 不对 accumulated relation 的 witness 做分解/range-check，只对 input relation 做；
- 用 **extension commitment** 降低输入 witness 范数，再接基于 Sum-Check 的简单 range check；
- `Π_ext` 被作者称为 Cyclo 最昂贵部分，原文给出 `a'·m·ℓ` 级 ring multiplication，其中 `ℓ` 由分解界决定（PDF 文本提取的 `ℓ` 表达式有 glyph 丢失，见 §5；本文件不硬写常数）；
- 论文 Table 1 给出 folding proof **31.4 / 31.8 / 32.9 KB**（mφ=2²⁵/2²⁷/2²⁹）；Table 2 对比 LatticeFold+ 的 100 KB vs 31.8 KB，rank 13 vs 9、q≈2⁵⁰ vs 2¹²⁸、φ=128 vs 64；
- Appendix C.2 给出 extension commitment 与 LatticeFold+ double commitment 的 benchmark：特定设置下 **36.7 s vs 129.4 s**（约 3.53×）；该比较**只计承诺计算、未计分解与 Sum-Check**，单线程 Intel HEXL AVX-512，作者承认对 LatticeFold+ “unfair advantage”。

### 1.2 与 LBF 的关系

`[推导]`

- **可以借鉴**：LBF Π′DEC 当前 fresh 重采盐并只给 relaxed bound；Cyclo 的“只对输入做范数管理/分解”思想可能减少 folding 内部成本，但 LBF 的缺口恰在递归时累积的盐界，Cyclo 不直接提供 exact salt certificate。
- **不能外推**：Cyclo 是格基 folding/norm-management 技术；全文未见零知识/blinding 声称，不能称为零知识 folding，也没有 ABDLOP Decider。
- **兼容性待核查**：Cyclo 的 extension commitment 是否可与 LBF 的 ABDLOP 承诺与 component-wise `R_K` 兼容，本文未证明。

**分类：上游 folding/norm-management 基线；不是目标 Decider。**

---

## 2. PikkuFold（ePrint 2026/1809）

### 2.1 核心机制与数据

`[论文事实: PikkuFold §1 contributions, §3.1 Lemma 9, §5.2 Definition 31, §6 benchmarks]`

- **Layered random projections**：Lemma 9 给出降低范数/通信的随机投影性质；
- **Fixed Hamming weight challenge sampler**：先从精确固定 Hamming weight 分布采样，再按 multiplication operator norm 拒绝，阈值暴露 challenge norm 与采样时间 tradeoff；
- **Operator-Norm Rejection Sampling**：§5.2 Definition 31，用 operator norm 控制挑战扩张；
- 通信口径：folding messages **excluding fresh input commitments** 约 5.62/5.72/5.83 KB（φ=64/128/256 类参数）；比较表中 PikkuFold 5.72 KB vs Cyclo 31.8 KB、SALSAA 62.25 KB；
- Prover 时间仍为百毫秒至数秒量级，verifier 约 3.87–9.80 ms（具体硬件/参数见原文表）；实现基于 RoKoko 后端、单次 Fiat–Shamir 与 50-bit modulus，作者明确其表 7 仅为 indicative，与 Cyclo/LatticeFold+ 不同 folded relation，不能当公平横比。

### 2.2 关键限制

`[论文事实: PikkuFold §1, p.9 附近]` 原文明确：

> "the presented protocol is not zero knowledge, and hiding the witness throughout sumcheck without losing its communication and prover efficiency requires additional techniques, for example those developed in Libra."

`[推导]`

- 5.7 KB 是**单步 folding 额外通信，排除 fresh input commitments**，不是 ZK Decider 证明大小，也不包含 LBF 的 `N_PoK` ABDLOP opening。
- 固定 Hamming weight + operator-norm rejection 可被视为 LBF challenge sampling 的优化基线，但 LBF 现有强采样集/盐界与 PikkuFold 的 operator-norm 界不同，不能替换。
- 作者自己把 ZK 与 arithmetic hash 留给未来工作；没有 ABDLOP committed evaluation claim Decider。

**分类：强性能基线；不是零知识 folding；不能自动解决 Decider。**

---

## 3. Hachi（ePrint 2026/156）

`[论文事实: Hachi Abstract/§1/§3/§4]` Hachi 是 **extension field 上的高效格基 multilinear PCS**：

- 使用 ring switching、trace map、inner/outer Ajtai commitment；
- 把 `F_{q^k}` 上的 multilinear evaluation claim 转成 `R_q` 上的关系；
- 证明大小 `poly(ℓ,λ)`、verifier `Õ(√2^ℓ λ)` 级别；ℓ=30 实例给出具体数据；
- §3 的讨论“generalizes LNP22”指 inner-product 在子域上的关系转写到 `R_q` 的 trace map，**不是**给出 LBF 所需的 exact salt norm certificate；
- 论文 Table 2 在 ℓ=30、|F|=2⁶⁴ 下给 proof ≈55.1 KB、prover ≈270 s、verifier ≈227 ms；作者说明 prover 只有第一轮 Rust 实现，数值不应外推为部署成本。

`[推导]`

- LBF 的 mask 是布尔多变量多项式 `p=a₀+Σp_i(X_i)`，且承诺对象是 `R_K` 中的 component-wise ABDLOP，不是 Hachi 定义的 `ℓ`-variate multilinear polynomial over extension fields。
- 不能把 Hachi 称为“通用多变量 PCS”，也不能用它直接替代 LBF polynomial masking 或 ABDLOP commitment。
- 它可能作为未来某些 `R_K` evaluation subclaim 的组件，但当前与目标 Decider 无直接接口。

**分类：PCS 组件；与目标关系不兼容于直接替换。**

---

## 4. Greyhound（ePrint 2024/1293）

`[论文事实: Greyhound, CRYPTO 2024, LBF §3.5 引用]` Greyhound 是格基多项式承诺与求值验证技术，强调快速 verifier 与较小证明。论文 ℓ=30 基准给 proof 25–33 KB、verifier 0.8–1.6 ms；hiding 变体只需 +0.75 KB，但这是 PCS 层 hiding，不是对 LBF 完整 relation 的 ZK。

`[推导]`

- 能覆盖“承诺多项式在某点的求值”子问题，但 LBF 输出还包含 `c'=L(z')`、`x'=L_in(z')`、ABDLOP opening、盐界、PoK 转录与 blinding；
- LBF 作者已说明 folding 内部被承诺对象很小，使用简洁 PCS 不划算；
- 在 Decider 中外层使用 PCS 仍需定义 `CE_com^k → PCS statement` 的编译，这本身未解决。

**分类：求值承诺性能基线；不是 Decider。**

---

## 5. CFW26（ePrint 2026/391）

### 5.1 已解决的部分

`[论文事实: CFW26 §2.3–2.5, §6]`

- 强化 HVZK IOR 定义，显式模拟后续查询，从而可组合（Lemma 2.5，误差 `ζ₁+ζ₂`）；
- `fresh input` / `fresh output` 概念保证编码 randomness 在组合后仍可用；
- `U_σ` mask polynomial 与编码 spare coordinates 隐藏 sumcheck messages，避免全量 mask 的 2× overhead；
- Construction 6.4 / Theorem 6.3：`k+1` rounds、`k d_s+1` 个 M 元素直接通信、verifier `O(k d_s)`；对有限环/模成立；
- Lemma 6.5：HVZK on fresh inputs，误差约 `2^k ζ_C`；Lemma 6.6：RBR knowledge soundness。

### 5.2 与 LBF 的实质差异

`[论文事实 + 推导]`

| 问题 | CFW26 是否解决 |
|---|---|
| 直接替代 LBF polynomial masking | ◑ 理论同类，但 LBF 在 `R_K` component-wise ABDLOP 上，CFW 要求编码有 spare coordinates 且 mask 参数 σ 均匀 |
| 改善模拟器 | ◑ 提供更强的可组合 HVZK 定义；但不是 malicious-verifier ZK |
| 改善 round-by-round KS | ◑ sumcheck IOR 本身有 RBR；LBF 的 Sum-Check+ABDLOP 拼接仍未证 |
| 与 ABDLOP commitment 组合 | `?` 需把 LBF 短盐承诺改造成 CFW 所需的 ZK encoding/fresh output；冲突点：CFW uniformity 论证要 σ 均匀，ABDLOP 盐须短 |
| 解决 Decider | ❌ 输出仍是 folded oracle/linear constraint，不含 ABDLOP opening/salt/exact norm |

**分类：重要的组合理论组件；不是 ABDLOP Decider。**

---

## 6. LaBRADOR ZK Toolkit（ePrint 2026/1289）与 LaZer / LaBRADOR 实现

### 6.1 论文层

`[论文事实: Toolkit Abstract/§1/§3.3/§4]`

- 首次具体实现 LNP22 linear-size ZK 与 LaBRADOR 的组合：LaBRADOS 多轮压缩 + LNP-Lite + LaBRADOR；
- benchmark 使用 Intel Core i7-11850H 单核，ring `d=512` 输入转到 proof ring `d=256`；
- proof size：非 ZK 约 95–105 KB，ZK 启用约 **115–125 KB**，差约 20 KB；
- LNP-Lite 的 knowledge-sound extraction 仍有 norm slack `c≈79.59`（Theorem 1），不是 exact ℓ₂；
- 论文理论上给出 IVC blueprint，但明确说当前 lattice-based 实践中尚未实用，hash arithmetic 是主要障碍。

### 6.2 工程静态核查

`[实现事实: 固定 commit]`

| 仓库 | commit | 已见接口/事实 | 限制 |
|---|---|---|---|
| `lazer-crypto/lazer` | `b958e247a2fdb9593b3c25c9603c6c5305c19420` | `src/abdlop.c` 中 `abdlop_keygen/commit/prove/verify`；`src/lnp.c` 中 `lnp_prover_set_statement_l2/bin/arp`；README 要求 Linux amd64、AVX-512、AES、gcc≥13.2、Sage≥10.2 | 当前 i7-14700 无 AVX-512，未构建 |
| `lazer-crypto/labrador` | `c1ae0e612d5accd9e7d9d1c264951c1afe949c83` | `normtype` 含 `L2EXACT/L2APPROX/BIN/NONORM`；有 `commit()`/`verify()`；`data.h` LOGQ=38、N=256；`lnp.h` q=2^38−107 | 未见 LBF `CE_com^k` statement/adapter；不支持当前硬件构建验证 |
| `osdnk/cyclo` | `31158a781c16a967c714c7fbde31ae1558e23118` | `CyclotomicRing<MOD_Q,N>`；README 参数 q≈2^50、φ=128；HEXL bindings；未提 zero-knowledge | 仅性能基线，不能作为 ZK Decider |

### 6.3 与 LBF 的关系

`[推导]`

- LaBRADOR Toolkit 是**最现实的候选后端**：它有可复用 exact-norm 相关接口与简洁 ZK 实现；
- 但 LNP-Lite 的 slack `≈79.59` 与 LBF 递归所需 exact salt bound 不同；直接调用会把 relaxed problem 搬入外层，而不是关闭缺口；
- 其 benchmark <125 KB 对应论文自己的用例，不能写成“LBF Decider <125 KB”；
- 未见批量验证/递归组合对 `CE_com^k` 的现成接口。

**分类：技术后端候选；不是现成 Decider。**

---

## 7. Verifiable Bootstrapping from Lattice-based Folding（ePrint 2026/1127）

`[论文事实: 摘要 + LB-01 文献地图]` 它算术化 folding verifier 并给 benchmark，是“验证器算术化可行”的最近证据；摘要无 ZK，输出不是 ABDLOP committed evaluation claims。

**分类：成本与工程参考；不覆盖目标。**

---

## 8. 最终竞争结论

`[推导]`

1. **已经解决我们的一部分问题**：CFW26 的组合 HVZK sumcheck；LNP22/Toolkit 的 exact/近似范数 ZK 工具；Cyclo/PikkuFold 的 folding 与 range/challenge 优化；Hachi/Greyhound 的求值承诺。
2. **可以作为技术组件**：LaBRADOR/LaZer（外层简洁 ZK）、CFW26（sumcheck 层）、Cyclo/PikkuFold（上游 folding 基线）。
3. **只能作为性能基线**：PikkuFold 5.7 KB、Cyclo extension commitment 36.7 s、Toolkit 115–125 KB、2026/1127 verifier arithmetic benchmark。
4. **与目标关系不兼容于直接替换**：Hachi multilinear PCS、Greyhound PCS、SuperNeo Π_DEC、PikkuFold non-ZK folding。
5. **仍未解决**：针对 `CE_com^k` 的简洁、知识可靠、保持 ZK 且可递归组合的 Decider。最接近的仍是“LNP22 exact norm + anchoring + LaBRADOR 外层”，但其构造与安全拼接尚未完成。

---

## 9. 待核查

- `[待核查]` CFW26 的 fresh output 是否可通过修改 LBF mask 生成满足；短 σ 与 uniformity 的冲突目前只有结构性判断。
- `[待核查]` Cyclo extension commitment 与 ABDLOP component-wise commitment 的组合接口。
- `[待核查]` PikkuFold operator-norm rejection 是否能在不破坏 LBF 强采样集 binding/soundness 的前提下替换 challenge sampler。
- `[待核查]` LaBRADOR Toolkit 是否已有可复用的批量证明/递归状态接口；静态核查只覆盖可见源码与 README。
- `[待核查]` 所有 PDF 正文符号仍需以 eprint.iacr.org 最终版视觉核对；本轮使用公开镜像。
