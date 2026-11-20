# D-LB-02 · Exact-L2 Certificate 与 Decider 可行性决策

> 日期：2026-11-20。任务包：LB-02。状态：**HOLD**。
> 依赖：`docs/08-exact-l2-certificate-mapping.md`、`docs/09-decider-backend-feasibility.md`、`docs/10-recent-competition-update.md`、LB-01 `docs/03`–`docs/07`。
> 本决策只判断研究方向与立项门槛，**不授权编写新 Decider 或创建实现仓库**。

---

## 1. 最终决策

**HOLD：数学上存在可行路径，但安全证明与成本存在尚未解决的阻断；不进入 GO-A 候选协议设计。**

`[推导]` 不是 NO-GO：目标没有被已有工作覆盖，且不存在已知数学矛盾。也不是 GO-A：现有组件尚未构成可验证的简洁 Decider，且无法给出可接受成本的证据。

---

## 2. 七个核心问题的回答

### 问题 1：LNP22 exact-ℓ₂ 证书是否能够直接用于 LatticeBlindFold？

**不能直接用于。**

`[论文事实 + 推导]` LNP22 §5.2 确实给出紧 exact-ℓ₂ 证明，但它主要证明承诺消息 `s=(s₁,σ(s₁),m,σ(m))` 的范数/二次关系；LBF 递归与 Decider 缺口还需要两个小盐、特别是 BDLOP randomness `s₂` 的精确界。LBF Remark 4.8 明确说 `s₂` 未被 LNP22 norm machinery 触及，需要 §3.2.1.1 anchoring。此外 LBF 的 `K=F_{q²}` component-wise 承诺不能直接使用 K 层 automorphism identity，必须回到 `R_F` 分别证明 `a,b` 分量的范数。

**分类**：需要参数/格式调整，且部分子问题需要新的协议构造。

### 问题 2：LaBRADOR/LaZer 是否能够构造一个可用的 Decider？

**目前不能称为“可用”。**

`[实现事实 + 推导]` 静态核查确认 lazer 有 `abdlop_*`、`lnp_prover_set_statement_l2` 等接口，labrador 有 `L2EXACT` 与 verify/commit；Toolkit 有 <125KB 级 ZK benchmark。但仓库没有 LBF `CE_com^k` 的 statement 编译器，也没有 `s₂` anchoring 或 LBF 递归组合接口；当前 i7-14700 无 AVX-512，未构建。把“通用格 ZK 可证明任意 NP”当成 Decider 已可用是错误的。

### 问题 3：如果能够构造，它究竟是简洁 Decider，还是仅仅把现有验证过程搬到另一个证明系统？

**当前证据只支持“可能搬移”，不支持“已简洁”。**

`[推导]` 直接路径必须把 `N_PoK=5+(K+k+1)t` 份 ABDLOP PoK、承诺同态、盐替换、求值关系与范数检查全部算术化。若只是把这些检查原样编码进 LaBRADOR，得到的是“外层证明包裹的线性扫描”，不是有实质简洁性的 Decider。只有同时满足以下条件才能称为简洁：
- 外层 statement 的大小与验证不随 `N_PoK` 线性增长；
- exact norm 在组件层面关闭盐放大，而不是重新引入 slack；
- 证明大小、prover/verifier time 显著优于 5–8 MB 直接转录基线。

目前三项均未证明。

### 问题 4：证明大小、验证成本和证明者开销是否能够接受？

**未知；不能接受 Toolkit 的数字外推。**

`[论文事实 + 推导]`
- LBF 直接转录：d=128 ≈8.2 MB、d=64 ≈5.5 MB；单位 ABDLOP commitment 23.05/14.38 KB。
- Toolkit 自有 benchmark：非 ZK 95–105 KB、ZK 115–125 KB（i7-11850H 单核），**不是 LBF 关系**。
- LNP22 exact proof size 有公式，但变量属于 LNP22 自身应用，未绑定到 LBF 的 `N_c,k,t,m₁,m₂,d`。
- 本阶段没有实际测量，也没有可接受的定量阈值；因此不能判断成本可用。

### 问题 5：CFW26 是否提供了更好的零知识 Sum-check 组合机制？

**是，提供更好的组合理论，但不解决 Decider。**

`[论文事实 + 推导]` CFW26 的强化 HVZK IOR 定义、fresh input/output、Lemma 2.5 组合定理、RBR knowledge soundness 与 `U_σ` mask 都可能改进 LBF mask 阶段。但限制明确：
- HVZK on fresh inputs 不等于 malicious-verifier ZK；
- uniformity 论证要求 mask 参数 σ 均匀，而 ABDLOP 承诺要求短盐；
- 输出是 folded oracle/linear constraint，不含 ABDLOP opening/salt/exact norm；
- LBF §4.5 的 Sum-Check+ABDLOP RBR KS 缺口不能自动由 CFW26 sumcheck IOR 补齐。

### 问题 6：Cyclo / PikkuFold 是否提供了更合适的 Folding 和范数管理基线？

**是，作为性能/上游基线；不是零知识 Decider。**

`[论文事实]` Cyclo 的 amortized norm-refreshing、extension commitment、partial range checks，以及 PikkuFold 的 layered random projections、fixed-weight challenge sampler、operator-norm rejection sampling 都值得作为 LBF 上游 folding/范数管理基线。PikkuFold 原文明确协议 not zero knowledge，5.7 KB 通信排除 fresh input commitments；Cyclo 未见 ZK/blinding 声称。二者均不提供 ABDLOP committed evaluation claims 的 Decider。

### 问题 7：是否存在一个仍然没有被已有工作解决、又能够实际完成的研究问题？

**存在，但需要先缩小为可验证的子问题。**

`[推导]` 未被覆盖的问题不是“发明 exact-ℓ₂ 证书”，而是：

> 能否把 LNP22 exact-ℓ₂ 证书以 component-wise、锚定 `s₂` 的方式嵌入 LBF 输出关系，并把 `CE_com^k` 编译成对格基简洁 ZK 后端友好、保持知识可靠性与零知识、且成本显著低于直接转录的关系？

这个问题具有研究价值，但目前缺少：
1. LBF 特定 relation compiler 的形式化定义；
2. `s₂` anchoring 与 exact salt bound 的完整协议；
3. LBF + LNP22 + 外层 ZK 的安全拼接证明；
4. 成本估算或原型数据。

在这些前提完成前，不授予 GO-A。

---

## 3. 为什么不选其他结论

| 结论 | 是否选择 | 理由 |
|---|---|---|
| GO-A | ❌ | 没有合理且已验证的 Decider 构造路线；关键阻断未关闭 |
| GO-B | ❌ | 尚未证明“可构造”；不能把未完成的编译假设当成构造 |
| **HOLD** | ✅ | 数学组件存在，安全与成本阻断明确，适合定向攻坚 |
| NO-GO | ❌ | 目标未被已有工作覆盖，也未发现内在矛盾 |

---

## 4. 解除 HOLD 的最小条件

后续若要升级为 GO-A，至少必须完成：

1. **精确定义 LBF relation compiler**：`CE_com^k + PoK transcript → 外层证明 statement` 的公开输入、秘密见证、等式与范数子句，且不丢 `c'/x'/r'/C'/salt` 任何语义。
2. **关闭 `s₂` 缺口**：给出 anchoring 的具体协议、bound、component-wise 展开与 soundness 论证；不能只引用 LBF Remark 4.8 的 sketch。
3. **给出完整安全拼接**：完备性、知识可靠性、ZK 模拟、FS/RBR/ROM-QROM 边界；HVZK 只能按 HVZK 声明。
4. **给出成本证据**：按固定 `k,t,N_c,m₁,m₂,d` 估算 proof size、prover/verifier time，并与 8.2/5.5 MB 直接转录基线比较。
5. **排除竞争覆盖**：尤其 CFW26 fresh-output 组合、LaBRADOR Toolkit 新接口与 PikkuFold/Cyclo 后续版本。

若这些条件无法满足，应转向“具体子问题优化”或 NO-GO，不得为维护方向默认 GO-A。

---

## 5. 对 RESEARCH_PLAN 的影响

本项目暂定主题保留，但研究问题已收窄：从“构造 Decider”改为“LBF 特定 exact-salt 证书与关系编译/安全拼接”。`RESEARCH_PLAN.md` 已加入 LB-02 更新说明；M2 的“候选构造”不应在 HOLD 解除前启动。
