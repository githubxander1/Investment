import os
import sys
from typing import Dict, List, Optional, Tuple, Any, Protocol
import pandas as pd
from datetime import datetime

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class IndicatorProtocol(Protocol):
    """指标模块协议，定义所有指标模块必须实现的接口"""
    
    def analyze(self, stock_code: str, trade_date: Optional[str] = None) -> Optional[pd.DataFrame]:
        """分析股票数据并返回结果"""
        ...
    
    def detect_signals(self, df: pd.DataFrame) -> Dict[str, List[datetime]]:
        """从分析结果中检测交易信号"""
        ...
    
    def plot(self, stock_code: str, trade_date: Optional[str] = None) -> Optional[str]:
        """绘制分析图表并返回保存路径"""
        ...
    
    def get_name(self) -> str:
        """获取指标名称"""
        ...

class ResistanceSupportIndicator:
    """阻力支撑指标适配器"""
    
    def __init__(self):
        # 延迟导入以避免循环依赖
        from indicators.resistance_support_indicators import (
            analyze_resistance_support, 
            detect_trading_signals as detect_rs_signals,
            plot_tdx_intraday as plot_rs
        )
        self.analyze_func = analyze_resistance_support
        self.detect_signals_func = detect_rs_signals
        self.plot_func = plot_rs
    
    def analyze(self, stock_code: str, trade_date: Optional[str] = None) -> Optional[pd.DataFrame]:
        """分析阻力支撑指标"""
        return self.analyze_func(stock_code, trade_date)
    
    def detect_signals(self, df: pd.DataFrame) -> Dict[str, List[datetime]]:
        """检测阻力支撑交易信号"""
        return self.detect_signals_func(df)
    
    def plot(self, stock_code: str, trade_date: Optional[str] = None) -> Optional[str]:
        """绘制阻力支撑图表"""
        # 注意：原始函数可能返回DataFrame而不是路径，需要适配
        result = self.plot_func(stock_code, trade_date)
        # 尝试从结果中获取图表路径
        if isinstance(result, str):
            return result
        # 假设图表已经保存在默认位置
        if trade_date is None:
            from datetime import datetime, timedelta
            yesterday = datetime.now() - timedelta(days=1)
            trade_date = yesterday.strftime('%Y-%m-%d')
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'output', 'charts',
            f"{stock_code}_{trade_date}_阻力支撑指标.png"
        )
    
    def get_name(self) -> str:
        """获取指标名称"""
        return "阻力支撑指标"

class VolumePriceIndicator:
    """量价指标适配器"""
    
    def __init__(self):
        # 延迟导入以避免循环依赖
        from indicators.volume_price_indicators import (
            analyze_volume_price,
            plot_indicators as plot_vp,
            detect_signals as detect_vp_signals
        )
        self.analyze_func = analyze_volume_price
        self.plot_func = plot_vp
        self.detect_signals_func = detect_vp_signals
    
    def analyze(self, stock_code: str, trade_date: Optional[str] = None) -> Optional[pd.DataFrame]:
        """分析量价指标"""
        return self.analyze_func(stock_code, trade_date)
    
    def detect_signals(self, df: pd.DataFrame) -> Dict[str, List[datetime]]:
        """检测量价交易信号"""
        # 调用原始函数进行信号检测
        df = self.detect_signals_func(df)
        
        # 整理信号格式
        signals = {
            'buy_signals': df[df['买入信号']].index.tolist() if '买入信号' in df.columns else [],
            'sell_signals': df[df['卖出信号']].index.tolist() if '卖出信号' in df.columns else [],
            'fund_signals': df[df['主力资金流入']].index.tolist() if '主力资金流入' in df.columns else []
        }
        return signals
    
    def plot(self, stock_code: str, trade_date: Optional[str] = None) -> Optional[str]:
        """绘制量价指标图表"""
        # 先进行分析以获取必要的数据
        df = self.analyze(stock_code, trade_date)
        if df is None:
            return None
        
        # 提取绘图所需的额外参数
        buy_ratio = df.get('买比例', 0).iloc[-1] if '买比例' in df.columns and not df.empty else 0
        sell_ratio = df.get('卖比例', 0).iloc[-1] if '卖比例' in df.columns and not df.empty else 0
        diff_ratio = df.get('差比例', 0).iloc[-1] if '差比例' in df.columns and not df.empty else 0
        
        # 调用绘图函数
        self.plot_func(df, stock_code, trade_date, buy_ratio, sell_ratio, diff_ratio)
        
        # 返回图表保存路径
        if trade_date is None:
            from datetime import datetime, timedelta
            yesterday = datetime.now() - timedelta(days=1)
            trade_date = yesterday.strftime('%Y-%m-%d')
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'output', 'charts',
            f"{stock_code}_{trade_date}_量价指标.png"
        )
    
    def get_name(self) -> str:
        """获取指标名称"""
        return "量价指标"

class ExtendedIndicator:
    """扩展指标适配器"""
    
    def __init__(self):
        # 延迟导入以避免循环依赖
        from indicators.extended_indicators import (
            analyze_extended_indicators,
            plot_tdx_intraday as plot_ext,
            detect_trading_signals as detect_ext_signals
        )
        self.analyze_func = analyze_extended_indicators
        self.plot_func = plot_ext
        self.detect_signals_func = detect_ext_signals
    
    def analyze(self, stock_code: str, trade_date: Optional[str] = None) -> Optional[pd.DataFrame]:
        """分析扩展指标"""
        return self.analyze_func(stock_code, trade_date)
    
    def detect_signals(self, df: pd.DataFrame) -> Dict[str, List[datetime]]:
        """检测扩展指标交易信号"""
        # 调用原始函数进行信号检测
        return self.detect_signals_func(df)
    
    def plot(self, stock_code: str, trade_date: Optional[str] = None) -> Optional[str]:
        """绘制扩展指标图表"""
        return self.plot_func(stock_code, trade_date)
    
    def get_name(self) -> str:
        """获取指标名称"""
        return "扩展指标"

class IndicatorFactory:
    """指标工厂类，负责创建不同类型的指标实例"""
    
    @staticmethod
    def create_indicator(indicator_type: str) -> Optional[IndicatorProtocol]:
        """
        创建指定类型的指标实例
        
        Args:
            indicator_type: 指标类型，支持 'resistance_support', 'volume_price', 'extended'
        
        Returns:
            指标实例，如果类型不支持则返回None
        """
        if indicator_type == 'resistance_support':
            return ResistanceSupportIndicator()
        elif indicator_type == 'volume_price':
            return VolumePriceIndicator()
        elif indicator_type == 'extended':
            return ExtendedIndicator()
        else:
            print(f"不支持的指标类型: {indicator_type}")
            return None

class IndicatorManager:
    """指标管理器，管理所有可用的指标"""
    
    def __init__(self):
        self.indicators = {
            'resistance_support': ResistanceSupportIndicator(),
            'volume_price': VolumePriceIndicator(),
            'extended': ExtendedIndicator()
        }
        self.current_indicator: Optional[IndicatorProtocol] = None
    
    def set_indicator(self, indicator_type: str) -> bool:
        """
        设置当前使用的指标
        
        Args:
            indicator_type: 指标类型
        
        Returns:
            是否设置成功
        """
        if indicator_type in self.indicators:
            self.current_indicator = self.indicators[indicator_type]
            print(f"已切换到指标: {self.current_indicator.get_name()}")
            return True
        else:
            print(f"未知的指标类型: {indicator_type}")
            return False
    
    def get_indicator(self, indicator_type: str) -> Optional[IndicatorProtocol]:
        """
        获取指定类型的指标实例
        
        Args:
            indicator_type: 指标类型
        
        Returns:
            指标实例，如果不存在则返回None
        """
        return self.indicators.get(indicator_type)
    
    def get_available_indicators(self) -> Dict[str, str]:
        """
        获取所有可用的指标类型
        
        Returns:
            指标类型与名称的映射字典
        """
        return {key: indicator.get_name() for key, indicator in self.indicators.items()}
    
    def analyze(self, stock_code: str, trade_date: Optional[str] = None) -> Optional[pd.DataFrame]:
        """
        使用当前指标分析股票
        
        Args:
            stock_code: 股票代码
            trade_date: 交易日期
        
        Returns:
            分析结果DataFrame
        """
        if self.current_indicator is None:
            print("请先设置指标")
            return None
        return self.current_indicator.analyze(stock_code, trade_date)
    
    def detect_signals(self, df: pd.DataFrame) -> Dict[str, List[datetime]]:
        """
        使用当前指标检测交易信号
        
        Args:
            df: 分析结果DataFrame
        
        Returns:
            交易信号字典
        """
        if self.current_indicator is None:
            print("请先设置指标")
            return {}
        return self.current_indicator.detect_signals(df)
    
    def plot(self, stock_code: str, trade_date: Optional[str] = None) -> Optional[str]:
        """
        使用当前指标绘制图表
        
        Args:
            stock_code: 股票代码
            trade_date: 交易日期
        
        Returns:
            图表保存路径
        """
        if self.current_indicator is None:
            print("请先设置指标")
            return None
        return self.current_indicator.plot(stock_code, trade_date)

# 单例模式的指标管理器实例
global_indicator_manager = IndicatorManager()

def get_indicator_manager() -> IndicatorManager:
    """
    获取全局指标管理器实例
    
    Returns:
        指标管理器实例
    """
    return global_indicator_manager

# 辅助函数
def analyze_stock_with_indicator(
    stock_code: str, 
    indicator_type: str, 
    trade_date: Optional[str] = None
) -> Optional[pd.DataFrame]:
    """
    使用指定指标分析股票
    
    Args:
        stock_code: 股票代码
        indicator_type: 指标类型
        trade_date: 交易日期
    
    Returns:
        分析结果DataFrame
    """
    indicator = IndicatorFactory.create_indicator(indicator_type)
    if indicator:
        return indicator.analyze(stock_code, trade_date)
    return None

def plot_stock_with_indicator(
    stock_code: str, 
    indicator_type: str, 
    trade_date: Optional[str] = None
) -> Optional[str]:
    """
    使用指定指标绘制股票图表
    
    Args:
        stock_code: 股票代码
        indicator_type: 指标类型
        trade_date: 交易日期
    
    Returns:
        图表保存路径
    """
    indicator = IndicatorFactory.create_indicator(indicator_type)
    if indicator:
        return indicator.plot(stock_code, trade_date)
    return None

if __name__ == "__main__":
    # 示例使用
    manager = get_indicator_manager()
    
    # 设置使用阻力支撑指标
    manager.set_indicator('resistance_support')
    
    # 分析股票
    stock_code = '000333'
    df = manager.analyze(stock_code)
    
    if df is not None:
        # 检测信号
        signals = manager.detect_signals(df)
        print(f"检测到的信号: {signals}")
        
        # 绘制图表
        chart_path = manager.plot(stock_code)
        if chart_path:
            print(f"图表已保存至: {chart_path}")
    
    # 切换到量价指标
    print("\n切换到量价指标")
    manager.set_indicator('volume_price')
    df = manager.analyze(stock_code)
    
    # 查看可用指标
    print("\n可用指标:")
    for key, name in manager.get_available_indicators().items():
        print(f"  {key}: {name}")