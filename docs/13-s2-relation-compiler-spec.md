# 13 · s₂ Relation Compiler 初步接口规格（待定义版）

> LB-03 · 任务 F。日期：2026-11-20。
> 状态：**接口骨架 + 逐项"待定义"**，不是可运行编译器，不是 Decider 实现。
> 前提：`docs/12` §3 得出 `R_{s₂}(x,w)` 的关系规格，但方案 B 的装配/安全证明/成本**未闭合**（LB-03 决策为 B）。因此本文只定义输入输出与约束边界；凡未由 LB-03 一手证据确认者一律标 `[待定义]` 或 `[待核查]`，**不写占位公式假装完整**。
> 依赖：`docs/11`（anchoring 审计）、`docs/12`（三路线与 R_s₂）、LB-01 `docs/07`（CE_com^k 接口）。

---

## 0. 依赖图（按任务包要求；标注每层的确认状态）

```
LBF Public Statement                       [已确认: CE_com^k, docs/07]
        |
        v
ABDLOP Commitment Relation                 [已确认: 式(2.5), docs/11 §1]
   t_A=A₁s₁+A₂s₂, t_B=Bs₂+m
        |
        v
s₂ Anchoring                               [已确认: Lemma 3.10/3.16, docs/11 §2]
   m̄=t_B−Bs₂; ct(Σwₙm̄_{ι(n)})−u=0
        |
        v
Exact Norm Certificate                     [部分确认: 组件存在(Remark4.8 sketch + §3.3.4),
                                             装配与安全证明 待定义]
   ‖s₂‖₂≤β 无 c̄ 因子; 二进制余量 x_i; integer lift
        |
        v
Component-wise Constraints                 [已确认: §3.3.4 翻译, LB-02 已修订]
   ‖a‖²+‖b‖²≤β², a,b∈R_F
        |
        v
Outer ZK Statement                         [待定义: LaBRADOR/LaZer statement 编译未存在]
   R1CS/CCS 约束集合 + exact-norm 模块接口
```

`[推导]` 图中前三行与 component-wise 行均有 LB-03 一手证据；**Exact Norm Certificate 的"装配"与 Outer ZK Statement 两层无现成构造**，是本编译器规格必须诚实标记的核心缺口。

---

## 1. 上游输入是什么

`[论文事实 + 推导]` 编译器的上游输入是 LBF 单次 folding 的输出（LB-01 `docs/07`）：
- `k` 个 `CE_com(b,L,B̃,Commit,T,K)` 承诺求值声明（含 `{c'_i, x'_i, r', {C'_{i,j}}}`）；
- `N_PoK = 5 + (K+k+1)t` 份 ABDLOP PoK 转录（LBF L3458）；
- 每份承诺的 opening `(s₁⁽ⁿ⁾, s₂⁽ⁿ⁾, m⁽ⁿ⁾)` 及 anchoring 数据 `(wₙ, ι(n), u★)`。

`[待定义]` 上游到编译器的**精确序列化格式**（哪份转录对应哪个约束、公开/秘密分界）尚无现成规格，需按 `docs/07` 的 9 条等式逐条映射后确定。

## 2. 变量公开/秘密分界

| 变量 | 上游角色 | 编译后处理 | 依据 |
|---|---|---|---|
| `pp, A₁,A₂,B, t_A,t_B` | 公开 | 保持公开 | `docs/11` §1.2 |
| `wₙ, ι(n), u★, u` | 公开（V 可算 u） | 保持公开 | Lemma 3.10 |
| `c'_i, x'_i, r', C'_{i,j}` | 公开声明 | 保持公开 | `docs/07` |
| `s₁, s₂, m (=t_B−Bs₂)` | 秘密见证 | 转外层秘密见证 | ABDLOP opening |
| `m̄⁽ⁿ⁾, s̄₁⁽ⁿ⁾, s̄₂⁽ⁿ⁾` | 提取见证 | 转外层秘密见证 | Lemma 3.16 |
| 二进制余量 `x_i`、mask `y` | exact 证书辅助 | 转外层秘密见证 | LNP22 Eq.58/59 |
| `c̄`（relaxed 乘子） | 提取副产物 | `[待定义]` exact 路线应消除 c̄，故是否保留为见证取决于方案 B 是否实例化成功 |

`[推导]` 关键分界原则：凡 V 可仅由已公开承诺与挑战算出的（如 u），保持公开；凡涉及 salt/opening/余量的，转外层秘密见证。

## 3. 进入 R1CS/CCS 的等式

`[论文事实 + 推导]` 参照 LBF §4.3.3（L3462–3466）：简洁路线需把 ABDLOP verification equations 算术化。进入外层约束的等式集合：

1. `A₁ s₁ + A₂ s₂ = t_A`（commitment consistency，R_q 线性）；
2. `t_B = B s₂ + m`（BDLOP message，R_q 线性）；
3. `ct(Σₙ wₙ m̄_{ι(n)}) − u = 0`（anchoring，R_K 常数项线性 → component-wise 两条 R_F 线性）；
4. `m̄⁽ⁿ⁾ = t_B⁽ⁿ⁾ − B s̄₂⁽ⁿ⁾`（salt/message substitution）；
5. `c'_i = L(z'_i)`, `x'_i = L_in(z'_i)`, `y'_{i,j}=M̄_j z'(r')` 等求值声明（`docs/07` 9 条）；
6. `‖a‖²+‖b‖² ≤ β²` 的 exact 范数二次约束（component-wise）。

`[待定义]` 第 6 条如何与 LNP22 Fig10 的 exact-ℓ₂ machinery（Eq.58/59 + Fig9 + Thm5.3）拼接成 R1CS/CCS 约束——LBF 只说 norm checks 是 "awkward part"、"the same exact-ℓ₂ machinery Remark 4.8 needs"（L3465–3466），未给约束级规格。

## 4. 依赖 exact-norm 模块的约束

`[推导]` 需外层 ZK 后端提供以下 exact-norm 原语（对应 LNP22 §5.2）：
- **inner-product-as-constant-coefficient**：`⟨E_i s−v_i, E_i s−v_i⟩ mod q` 的常数项证明（Fig8 Π_eval）；
- **binary remainder**：`⟨x_i, x_i−1⟩=0`（Lemma 5.2）+ 小范数（Fig9）；
- **integer lift**：Eq.59 + Eq.60 把 mod q 提升到 Z（Thm 5.3 参数条件）；
- **component-wise base-ring**：`σ⁻¹(a)a=‖a‖²`、`σ⁻¹(b)b=‖b‖²`（§3.3.4）。

`[待核查]` LaZer 是否暴露这些原语的**可组合**接口：静态核查确认有 `lnp_prover_set_statement_l2`、`L2EXACT`、`abdlop_*`（LB-02 `docs/09`），但**从 LBF 的 CE_com^k 到这些接口的 statement 编译器不存在**；且 `set_statement_l2` 的向量/矩阵是否接受 component-wise 拆分后的 `(a,b)` 形式未验证。

## 5. 如何复用 LaBRADOR/LaZer 现有证明接口

`[实现事实 + 推导]` 可复用组件（LB-02 静态核查，commit lazer `b958e24`/labrador `c1ae0e6`）：
- ABDLOP：`abdlop_keygen/commit/prove/verify`（`src/abdlop.c`）；
- exact L2：`lnp_{prover,verifier}_set_statement_l2` + `L2EXACT`（`src/lnp.c`、`python/labrados.py`）；
- 批量验证：`ort_pack_verify`/`dch_pack_verify`（labrador 侧）。

`[待定义]` 复用路径的具体形式：
- 选择一：把第 3 节 1–5 条线性/求值约束编成 `Π_many`/Fig4-style 线性关系，`set_statement_l2` 承担第 6 条范数——但需验证两者 challenge set 与 soundness 兼容；
- 选择二：全部编入 LaBRADOR R1CS 外层，exact-norm 作为子证明——需处理子证明与外层的 Fiat–Shamir 拼接（ROM/QROM 边界 `[待核查]`）。
两种选择均未实测（本机无 AVX-512，见 LB-02），不能断言哪个可行。

## 6. 是否需要额外的承诺转换

`[论文事实 + 推导]` 视方案而定：
- 方案 B（推荐）：**不重算承诺**——Π_anc 只重新打包已有 opening（LBF L1645–1653），组件-wise exact 翻译也不新增承诺（除二进制余量 x 追加到 Ajtai 槽，LNP L1719）。故理论上只需"余量承诺"这一步转换。
- 方案 A（扩展证明对象）：需为 s₂ 增加 Ajtai 承诺槽，属非平凡转换（`docs/12` §2 方案 A）。
`[待核查]` 二进制余量 x 的追加承诺与现有 `CE_com^k` 承诺布局是否冲突（消息维度、garbage 槽），LBF 未给合成规格。

## 7. 关系依赖图（逐层状态）

见本文 §0。额外说明：

`[推导]` 编译器的**最小可用版本**应至少打通：LBF Public Statement → ABDLOP Relation → s₂ Anchoring → Component-wise Constraints 四层（均有 LB-03 一手证据）；Exact Norm Certificate 的"装配"与 Outer ZK Statement 两层在 LB-03 决策 B 下**保持待定义**，待后续阶段关闭 HOLD 条件后再补。本文件不以占位公式填补这两层。

---

## 8. 待定义清单（诚实边界汇总）

1. `[待定义]` 上游输入到编译器的精确序列化格式（§1）。
2. `[待定义]` exact-norm 证书（无 c̄ 紧界）装配到每隔轮协议的具体步骤与安全证明（§0、§4）。
3. `[待定义]` LBF CE_com^k → LaZer `set_statement_l2` / ABDLOP 接口的 statement 编译器（§4、§5）。
4. `[待定义]` Fiat–Shamir / RBR / ROM-QROM 下外层与 exact 子证明的安全拼接（§5）。
5. `[待核查]` LaZer `set_statement_l2` 对 component-wise `(a,b)` 拆分的支持（§4）。
6. `[待核查]` 二进制余量追加承诺与 CE_com^k 布局的兼容性、增量成本（§6）。
7. 本文件不构成 Decider 实现，不授权进入候选协议设计；遵守 LB-03 决策 B。
