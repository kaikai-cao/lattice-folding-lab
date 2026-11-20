# Experiments

本目录只存放可复现实验代码和测试。

## 当前实验

`hint_leakage_demo.py`：在有限域 F7 上构造二维线性映射，演示当公开线性 Hint 足够且矩阵可逆时，接收方可以恢复原向量。

它用于说明“线性求值不天然等于隐私保护”，不是 LatticeBlindFold 的真实攻击，也没有模拟 Sum-check、Ajtai、ABDLOP 或协议安全参数。

运行：

```bash
python -m unittest discover -s experiments -v
python experiments/hint_leakage_demo.py
```
