# 组合持仓策略模块

本目录包含ths_trade项目中的各种交易策略实现，目前主要提供了组合持仓处理器。

## 组合持仓处理器 (CombinationHoldingProcessor)

`CombinationHoldingProcessor`是一个用于管理和调整证券账户与策略持仓之间差异的工具。它能够：

- 更新策略持仓数据
- 更新账户持仓数据
- 比较持仓差异，找出需要买入和卖出的标的
- 执行调仓操作

### 主要功能

1. **持仓差异分析**：比较账户实际持仓与策略目标持仓
2. **智能调仓**：根据持仓比例差异自动计算交易数量
3. **分批执行**：先卖出再买入，按价格排序优化买入顺序
4. **容错处理**：包含完善的错误处理和日志记录

### 使用方法

#### 基本使用

```python
from ths_trade.strategies import CombinationHoldingProcessor

# 创建处理器实例
processor = CombinationHoldingProcessor(
    strategy_name="your_strategy_name",  # 策略名称
    account_name="your_account_name"     # 账户名称
)

# 执行调仓
success = processor.operate_strategy_with_account()

if success:
    print("调仓成功")
else:
    print("调仓失败")
```

#### 完整示例

请参考`example_combination_strategy.py`文件，该文件提供了两个使用示例：
1. 基本的策略执行流程
2. 使用自定义数据运行策略

### 自定义和扩展

您可以通过以下方式自定义和扩展组合持仓处理器：

1. **自定义数据源**：重写`_update_strategy_holdings`方法以从您的数据来源获取策略持仓
2. **自定义交易执行**：根据需要修改`_execute_sell_operations`和`_execute_buy_operations`方法
3. **自定义排除列表**：修改`excluded_holdings`列表以排除特定股票

### 注意事项

1. 确保已正确配置ths_trade项目的依赖项
2. 在生产环境中使用前，请先在测试环境中验证功能
3. 交易执行涉及资金安全，请谨慎使用并做好风险控制
4. 默认情况下，当持仓比例差异小于10%时，不会触发交易，以避免频繁调整

## 依赖项

- pandas
- requests
- ths_trade（核心模块）

## 扩展计划

未来将添加更多策略实现，包括：
- 网格交易策略
- 均线交叉策略
- 动量策略
- 均值回归策略

欢迎贡献代码或提出建议！