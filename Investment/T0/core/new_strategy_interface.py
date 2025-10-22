from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Tuple
import pandas as pd
from datetime import datetime

class NewStrategyInterface(ABC):
    """
    新策略接口类，为T+0交易系统提供统一的策略接口
    """
    
    def __init__(self, strategy_name: str):
        self.strategy_name = strategy_name
    
    @abstractmethod
    def analyze(self, stock_code: str, trade_date: Optional[str] = None) -> Optional[Tuple[pd.DataFrame, Dict[str, List[Tuple[datetime, float]]]]]:
        """
        分析股票数据并生成交易信号
        
        Args:
            stock_code: 股票代码
            trade_date: 交易日期
            
        Returns:
            (数据框, 信号字典) 或 None
        """
        pass
    
    @abstractmethod
    def plot(self, stock_code: str, trade_date: Optional[str] = None) -> Optional[str]:
        """
        绘制策略图表
        
        Args:
            stock_code: 股票代码
            trade_date: 交易日期
            
        Returns:
            图表保存路径或None
        """
        pass

# 具体策略实现
class PriceMADeviationStrategy(NewStrategyInterface):
    """
    价格均线偏离策略
    """
    
    def __init__(self):
        super().__init__("PriceMA Deviation")
    
    def analyze(self, stock_code: str, trade_date: Optional[str] = None) -> Optional[Tuple[pd.DataFrame, Dict[str, List[Tuple[datetime, float]]]]]:
        try:
            from Investment.T0.indicators.price_ma_deviation import analyze_price_ma_deviation
            return analyze_price_ma_deviation(stock_code, trade_date)
        except Exception as e:
            print(f"价格均线偏离策略分析失败: {e}")
            return None
    
    def plot(self, stock_code: str, trade_date: Optional[str] = None) -> Optional[str]:
        try:
            from Investment.T0.indicators.price_ma_deviation import plot_tdx_intraday
            return plot_tdx_intraday(stock_code, trade_date)
        except Exception as e:
            print(f"价格均线偏离策略绘图失败: {e}")
            return None

class VolatilityStrategy(NewStrategyInterface):
    """
    波动率策略
    """
    
    def __init__(self):
        super().__init__("Volatility")
    
    def analyze(self, stock_code: str, trade_date: Optional[str] = None) -> Optional[Tuple[pd.DataFrame, Dict[str, List[Tuple[datetime, float]]]]]:
        try:
            from Investment.T0.indicators.volatility_strategy import analyze_volatility_strategy
            return analyze_volatility_strategy(stock_code, trade_date)
        except Exception as e:
            print(f"波动率策略分析失败: {e}")
            return None
    
    def plot(self, stock_code: str, trade_date: Optional[str] = None) -> Optional[str]:
        try:
            from Investment.T0.indicators.volatility_strategy import plot_volatility_strategy
            return plot_volatility_strategy(stock_code, trade_date)
        except Exception as e:
            print(f"波动率策略绘图失败: {e}")
            return None

class MomentumReversalStrategy(NewStrategyInterface):
    """
    动量反转策略
    """
    
    def __init__(self):
        super().__init__("Momentum Reversal")
    
    def analyze(self, stock_code: str, trade_date: Optional[str] = None) -> Optional[Tuple[pd.DataFrame, Dict[str, List[Tuple[datetime, float]]]]]:
        try:
            from Investment.T0.indicators.momentum_reversal import analyze_momentum_reversal
            return analyze_momentum_reversal(stock_code, trade_date)
        except Exception as e:
            print(f"动量反转策略分析失败: {e}")
            return None
    
    def plot(self, stock_code: str, trade_date: Optional[str] = None) -> Optional[str]:
        try:
            from Investment.T0.indicators.momentum_reversal import plot_momentum_reversal
            return plot_momentum_reversal(stock_code, trade_date)
        except Exception as e:
            print(f"动量反转策略绘图失败: {e}")
            return None

# 策略工厂
class StrategyFactory:
    """
    策略工厂类，用于创建策略实例
    """
    
    @staticmethod
    def create_strategy(strategy_type: str) -> Optional[NewStrategyInterface]:
        """
        创建策略实例
        
        Args:
            strategy_type: 策略类型
            
        Returns:
            策略实例或None
        """
        strategies = {
            "price_ma_deviation": PriceMADeviationStrategy,
            "volatility": VolatilityStrategy,
            "momentum_reversal": MomentumReversalStrategy
        }
        
        strategy_class = strategies.get(strategy_type.lower())
        if strategy_class:
            return strategy_class()
        return None
    
    @staticmethod
    def get_available_strategies() -> List[str]:
        """
        获取可用的策略列表
        
        Returns:
            策略名称列表
        """
        return ["price_ma_deviation", "volatility", "momentum_reversal"]