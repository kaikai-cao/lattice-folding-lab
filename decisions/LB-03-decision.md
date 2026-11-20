# D-LB-03 · s₂ Anchoring 与 Exact-Norm 组合决策

> 日期：2026-11-20。任务包：LB-03。状态：**决策 B（需要一个明确的局部扩展；不进入完整 Decider）**。
> 依赖：`docs/11-s2-anchoring-mathematical-audit.md`、`docs/12-s2-exact-norm-construction-options.md`、`docs/13-s2-relation-compiler-spec.md`、`experiments/s2_anchor_toy.py`、LB-02 `docs/08`/`09`。
> LB-02 的 HOLD **维持**；本阶段不解除、不授权编写新 Decider、不建实现仓库。

---

## 1. 最终决策

**B：现有组件方向正确，但需要一个明确的局部扩展——把 LBF 的 exact-ℓ₂ sketch 实例化为每隔轮协议并证明"无 c̄ 累积"；给出最小数学缺口与候选构造，不直接开始完整 Decider。**

`[推导]` 排除项：
- **非 A**：作者只 sketch（"One would append it" + "we do not instantiate"），没有完整映射、安全证明与成本证据，不满足 A 的"给出完整映射、证明条件和成本"。
- **非 C/D**：anchoring（§3.2.1.1 Lemma 3.10）、R_K exact 翻译（§3.3.4）、组合 sketch（Remark 4.8）**都真实存在**，不是"路线不适合"或"不可接受的数学障碍"。
- **非维持纯 HOLD 无增量**：本阶段把"s₂ 缺口"从模糊陈述收敛为**三个明确的局部任务**（见 §4），较 LB-02 有实质进展。

---

## 2. 核心结论（对应任务包七问）

### 原有 anchoring 的准确数学定义
`[论文事实]` §3.2.1.1 的 anchoring 是 **salt/message substitution**：用 `Bs₂⁽ⁿ⁾ = t_B⁽ⁿ⁾ − m⁽ⁿ⁾` 代入，把式 (3.1) `u★ ?= ct(Σₙ wₙ (Bs₂⁽ⁿ⁾)_{ι(n)})` 化为 `ct(Σₙ wₙ m̄⁽ⁿ⁾_{ι(n)}) − u = 0`（Lemma 3.10，L1537–1554）。Π_anc（Lemma 3.16）提取 `(s̄₁,s̄₂,m̄⁽ⁿ⁾)` 但 certify 的是消息 m 的关系，**从不对 s₂ 给 exact 范数界**。详见 `docs/11` §2。

### LNP22 exact-norm 的实际覆盖范围（消除歧义）
`[论文事实]` Figure 10 的 exact 对象向量是 `s=(s₁,σ(s₁),m,σ(m)) ∈ R_q^{2(m₁+ℓ)}`，`E_i` 不含 s₂ 列；s₂ 作为 randomness 仅出现在 opening relation 与 **relaxed** 界 `‖s_i c̄‖ ≤ 2s_i√(2m_i d)`（i=1,2）。故"Fig10 涉及 s₂ ≠ 已有可复用 exact-norm 证书"**表述准确**，须精确化为"relaxed 覆盖、exact 不覆盖"。见 `docs/12` §1。

### 三条候选路线比较
方案 A（扩展证明对象到 s₂）：可行但改承诺布局、代价大；方案 B（anchoring + 就地追加 exact，LBF sketch）：**最小缺口、作者方向**；方案 C（component-wise base-ring）：LBF §3.3.4 已给出且正确，是 A/B 在 R_K 上的必备细节而非独立解法。统一比较见 `docs/12` §2.4。

### s₂ 目标关系
`[推导]` 已提取 `R_{s₂}(x,w)=1` 规格：公开输入（pp/A₁A₂B/t_A t_B/wₙ/ι/u★/β/挑战）、秘密见证（s₂/s₁/m/m̄/余量 x/mask）、五类约束（Commitment Consistency / Anchoring Equation / Exact Norm Constraint / Binary Remainder / Integer Lift）。**能转成 LNP22 可证明关系**（分两步：s₂ 组件作为 exact 对象 + anchoring 嵌入公共关系），但"能证明"≠"已装配支撑递归"。见 `docs/12` §3。

### 是否得到可行的 exact-norm 证明
**部分**：组件层面可行（Lemma 3.10 + §3.3.4 + Remark 4.8 sketch），协议层面未闭合（未实例化、无 c̄ 累积未证、成本未知）。

### 递归安全性质
`[论文事实+推导]` 现有 relaxed 界下每轮乘 `2T₁(C)`（d=128 时 =29.6，约 +4.9 bit/轮），β 几何增长逼近 q≈2⁶⁴，只支撑 O(1) 轮；exact 证书理论上把链截断为 `β_{r+1}=β_r`（Remark 4.8 L3135–3137），但该实例化缺失。**单次正确 ≠ 递归成立**。见 `docs/12` §4 E5。

### LaBRADOR 接口能否承载
`[实现事实+推导]` 有 `lnp_*_set_statement_l2`/`L2EXACT`/`abdlop_*`/批量验证等组件，但无 CE_com^k→statement 编译器；component-wise 支持与 FS 拼接 `[待核查/待定义]`。见 `docs/13` §5。

---

## 3. LB-02 表述修正（用户指定）

1. **"s₂ anchoring 完全没有构造"→ 修正**：已有 salt/message substitution 构造（Lemma 3.10/3.16），提供"承诺关系与秘密随机量的联系"；尚待验证的是该联系是否足以支撑 exact-ℓ₂ 与递归严格界。
2. **"component-wise 不能做 exact-ℓ₂"→ 修正**：§3.3.4 已给出正确翻译（base-ring 分别证 `‖a‖²`/`‖b‖²`，联合 `‖a‖²+‖b‖²≤β²`）；不能套 K 层恒等式 ≠ 不能做。
3. **docs/08 Figure 10 歧义已消**：明确 s₂ 在 Fig10 是 randomness + relaxed 界，exact 对象向量不含 s₂；已就地修订 `docs/08` 的变量映射表、A4.2、最终分类。

---

## 4. 解除决策 B 的最小条件（下一阶段局部攻坚）

按优先级，均为**局部机制**，不是完整 Decider：
1. **实例化 exact-ℓ₂ 追加**：把 Remark 4.8 的 "One would append it" 落成协议——明确在 Protocol 8 Step 5 与 Protocol 7 Step 17 追加 exact 证明的具体消息、承诺与验证等式（bound 已由原文给出：`k t(B̃−1)√((m₁+m₂)d)` 与 `(B̃−1)t√((m₁+m₂)d)`）。
2. **证明无 c̄ 累积**：形式化"提取 salt 满足无 c̄ 紧界 + binding 识别相邻轮 opening → 链不累积"（Remark 4.8 L3135–3137 的论证需补全为定理）。
3. **component-wise + exact 联合参数验算**：在 LBF 具体参数（q=2⁶⁴−59, d∈{64,128}, N_c=(k+1)t）下验算 Thm5.3 条件与增量成本，对比 8.2/5.5 MB 直接转录基线。
4. **statement 编译器原型**：CE_com^k → LaZer `set_statement_l2`/ABDLOP 接口的映射（docs/13 §4/§5 的待定义项）。
5. **安全拼接**：完备/知识可靠/ZK 模拟 + FS/RBR/ROM-QROM 边界；HVZK 只按 HVZK 声明。

---

## 5. 明确不做的边界

- 不把 LNP22 §5.2 称为新贡献；不把 anchoring 等同范数证明；不把 relaxed 改写成 exact；不把单次证明等同递归。
- 不编写新 Decider、不建实现仓库、不改 F7 教学实验、不改 LBF 原始协议转录、不改 SuperNeo 笔记。
- toy 实验 `experiments/s2_anchor_toy.py` 仅验证 Lemma 3.10 代数恒等式，不证明 Module-SIS/exact-ℓ₂/ZK（脚本与测试已显式声明）。

---

## 6. 下一步建议

进入"关闭决策 B 的最小条件"的下一任务包：以**条件 1+2（实例化 exact 追加 + 无 c̄ 累积定理）**为核心，这是 s₂ 问题的最小组装缺口；条件 3–5 视其结论再排。`RESEARCH_PLAN.md` 已相应收窄（本次仅在研究方向确实需要处更新）。
