//+------------------------------------------------------------------+
//|                                      Pinbar_MACD_Fixed.mq5        |
//|                        Copyright © 2024, All rights reserved      |
//|                          修复版：优化Pinbar识别和MACD背离检测逻辑     |
//|                              目的：提高信号显示率                   |
//+------------------------------------------------------------------+
#property copyright ""
#property link      ""
#property version   "1.01"

#property indicator_chart_window
#property indicator_buffers 2
#property indicator_plots   2

#property indicator_type1   DRAW_ARROW
#property indicator_color1  clrGreen
#property indicator_width1  1
#property indicator_type2   DRAW_ARROW
#property indicator_color2  clrRed
#property indicator_width2  1

// 常量定义
#define BARS_MAX 10000  // 最大条形图数量

// 信号模式枚举
enum SignalMode
{
    MODE_COMBINED = 0,  // 组合模式：同时满足Pinbar和MACD背离
    MODE_PINBAR_ONLY = 1,  // 仅Pinbar信号
    MODE_DIVERGENCE_ONLY = 2,  // 仅MACD背离信号
    MODE_EITHER = 3  // 任一模式：满足Pinbar或MACD背离任一条件
};

// 输入参数
input int                pinbarSize        = 1.5;      // 降低默认值以增加信号
input int                fastEMA          = 12;       // 快线周期
input int                slowEMA          = 26;       // 慢线周期
input int                signalSMA        = 9;        // 信号线周期
input int                divergenceLookback = 20;     // 背离检测回溯周期
input bool               debugMode        = true;     // 调试模式开关
input int                localBottomWindow = 3;       // 局部低点/高点检测窗口
input SignalMode         signalMode       = MODE_EITHER;   // 信号模式选择 (默认使用任一模式以提高信号显示率)

// 全局变量
double upBuffer[];               // 多头信号
double downBuffer[];             // 空头信号

//+------------------------------------------------------------------+
//| 初始化函数 - 添加详细调试信息                                     |
//+------------------------------------------------------------------+
int OnInit()
{
    SetIndexBuffer(0, upBuffer, INDICATOR_DATA);
    SetIndexBuffer(1, downBuffer, INDICATOR_DATA);
    
    PlotIndexSetInteger(0, PLOT_ARROW, 233);
    PlotIndexSetInteger(1, PLOT_ARROW, 234);
    
    // 输出详细的初始化信息
    if(debugMode)
    {
        Print("======= Pinbar_MACD Fixed 初始化信息 =======");
        Print("信号模式: ", signalMode);
        Print("Pinbar大小阈值: ", pinbarSize);
        Print("MACD参数: 快线=", fastEMA, ", 慢线=", slowEMA, ", 信号线=", signalSMA);
        Print("背离检测回溯期: ", divergenceLookback);
        Print("局部低点/高点检测窗口: ", localBottomWindow);
        Print("========================================");
    }
    
    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| 反初始化函数                                                     |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    // 清理资源
}

//+------------------------------------------------------------------+
//| 检测Pinbar形态函数 - 大幅放宽识别条件                             |
//+------------------------------------------------------------------+
bool isPinbar(const int index, const double &high[], const double &low[], const double &open[], const double &close[])
{
    // 计算蜡烛图各部分大小
    double body      = MathAbs(close[index] - open[index]);
    double upperWick = high[index] - MathMax(open[index], close[index]);
    double lowerWick = MathMin(open[index], close[index]) - low[index];
    double range     = high[index] - low[index]; // 蜡烛图总范围
    
    // 大幅降低识别阈值，使更多蜡烛图能被识别为Pinbar
    bool isPinbarValue = false;
    
    // 处理十字星形态 - 极低阈值
    if(body == 0 || body < range * 0.1)  // 极短实体也视为十字星
    {
        // 只要有一端影线明显即可
        isPinbarValue = (upperWick >= range * 0.3 || lowerWick >= range * 0.3);
        if(isPinbarValue && debugMode)
            Print("十字星Pinbar detected at bar ", index, ", upperWick=", upperWick, ", lowerWick=", lowerWick, ", range=", range);
    }
    else
    {
        // 常规Pinbar判断 - 极低阈值要求
        isPinbarValue = (upperWick >= body * 0.5 || lowerWick >= body * 0.5);
        
        // 额外条件1：影线至少占总体范围的30%
        if(!isPinbarValue)
        {
            isPinbarValue = (upperWick / range >= 0.3 || lowerWick / range >= 0.3);
        }
        
        // 额外条件2：判断是否为锤形或倒锤形
        if(!isPinbarValue)
        {
            // 锤形：下影线较长，实体在上半部分
            if(body < range * 0.5 && lowerWick > upperWick * 1.5)
            {
                isPinbarValue = true;
            }
            // 倒锤形：上影线较长，实体在下半部分
            else if(body < range * 0.5 && upperWick > lowerWick * 1.5)
            {
                isPinbarValue = true;
            }
        }
    }
    
    // 记录识别的Pinbar信息
    if(isPinbarValue && debugMode)
        Print("Pinbar detected at bar ", index, 
              ", body=", body, ", range=", range, 
              ", upperWick=", upperWick, ", lowerWick=", lowerWick, 
              ", body/range=", body/range, 
              ", upperWick/body=", (body > 0) ? (upperWick/body) : -1, 
              ", lowerWick/body=", (body > 0) ? (lowerWick/body) : -1);
    
    return(isPinbarValue);
}

//+------------------------------------------------------------------+
//| 检查是否是局部低点                                               |
//+------------------------------------------------------------------+
bool isLocalBottom(const int index, const int window, const double &low[])
{
    for(int i = 1; i <= window; i++)
    {
        // 检查左侧
        if(index - i >= 0 && low[index - i] < low[index])
            return false;
        // 检查右侧
        if(index + i < ArraySize(low) && low[index + i] < low[index])
            return false;
    }
    return true;
}

//+------------------------------------------------------------------+
//| 检查是否是局部高点                                               |
//+------------------------------------------------------------------+
bool isLocalTop(const int index, const int window, const double &high[])
{
    for(int i = 1; i <= window; i++)
    {
        // 检查左侧
        if(index - i >= 0 && high[index - i] > high[index])
            return false;
        // 检查右侧
        if(index + i < ArraySize(high) && high[index + i] > high[index])
            return false;
    }
    return true;
}

//+------------------------------------------------------------------+
//| 优化版底背离检测（多头信号） - 大幅降低识别阈值                  |
//+------------------------------------------------------------------+
bool isBullishDivergence(const int currentBar, const int lookbackPeriod, const double &low[], const double &macdValues[])
{
    // 极度简化的背离检测 - 寻找价格新低但MACD没有新低的情况
    
    // 检查最近几根K线
    for(int i = currentBar - 3; i >= 0 && i >= currentBar - lookbackPeriod; i--)
    {
        // 极低阈值条件：价格创新低，且MACD有回升趋势
        bool priceLower = (low[currentBar] < low[i]);
        bool macdNotLower = (macdValues[currentBar] > macdValues[i]);
        
        // 简化条件：只要价格创新低且MACD没有创新低，就认为是背离
        if(priceLower && macdNotLower)
        {
            if(debugMode)
                Print("Bullish divergence detected at bar ", currentBar, ", comparison bar ", i,
                      ", price lower: ", priceLower, ", macd higher: ", macdNotLower,
                      ", price diff: ", low[i] - low[currentBar], ", macd diff: ", macdValues[currentBar] - macdValues[i]);
            return(true);
        }
    }
    
    // 额外检测：最近MACD是否有回升趋势（即使没有严格的价格新低）
    if(currentBar >= 3)
    {
        bool macdRising = (macdValues[currentBar] > macdValues[currentBar-1]) && 
                         (macdValues[currentBar-1] > macdValues[currentBar-2]);
        bool priceNearLow = (low[currentBar] <= Lowest(low, 10, currentBar));
        
        if(macdRising && priceNearLow)
        {
            if(debugMode)
                Print("Bullish trend divergence detected at bar ", currentBar, ", macd rising: ", macdRising, ", price near low: ", priceNearLow);
            return(true);
        }
    }
    
    return(false);
}

//+------------------------------------------------------------------+
//| 优化版顶背离检测（空头信号） - 大幅降低识别阈值                  |
//+------------------------------------------------------------------+
bool isBearishDivergence(const int currentBar, const int lookbackPeriod, const double &high[], const double &macdValues[])
{
    // 极度简化的背离检测 - 寻找价格新高但MACD没有新高的情况
    
    // 检查最近几根K线
    for(int i = currentBar - 3; i >= 0 && i >= currentBar - lookbackPeriod; i--)
    {
        // 极低阈值条件：价格创新高，且MACD有下降趋势
        bool priceHigher = (high[currentBar] > high[i]);
        bool macdNotHigher = (macdValues[currentBar] < macdValues[i]);
        
        // 简化条件：只要价格创新高且MACD没有创新高，就认为是背离
        if(priceHigher && macdNotHigher)
        {
            if(debugMode)
                Print("Bearish divergence detected at bar ", currentBar, ", comparison bar ", i,
                      ", price higher: ", priceHigher, ", macd lower: ", macdNotHigher,
                      ", price diff: ", high[currentBar] - high[i], ", macd diff: ", macdValues[i] - macdValues[currentBar]);
            return(true);
        }
    }
    
    // 额外检测：最近MACD是否有下降趋势（即使没有严格的价格新高）
    if(currentBar >= 3)
    {
        bool macdFalling = (macdValues[currentBar] < macdValues[currentBar-1]) && 
                          (macdValues[currentBar-1] < macdValues[currentBar-2]);
        bool priceNearHigh = (high[currentBar] >= Highest(high, 10, currentBar));
        
        if(macdFalling && priceNearHigh)
        {
            if(debugMode)
                Print("Bearish trend divergence detected at bar ", currentBar, ", macd falling: ", macdFalling, ", price near high: ", priceNearHigh);
            return(true);
        }
    }
    
    return(false);
}

//+------------------------------------------------------------------+
//| 指标计算函数 - 支持多种信号模式                                  |
//+------------------------------------------------------------------+
int OnCalculate(const int ratesTotal, const int prevCalculated,
                const datetime &time[], const double &open[],
                const double &high[], const double &low[],
                const double &close[], const long &tickVolume[],
                const long &volume[], const int &spread[])
{
    // 初始化缓冲区
    ArrayInitialize(upBuffer, EMPTY_VALUE);
    ArrayInitialize(downBuffer, EMPTY_VALUE);
    
    // 计算起始位置
    int startPos = prevCalculated - 1;
    if(startPos < 0)
        startPos = 0;
    
    // 添加调试信息
    if(debugMode)
    {
        if(prevCalculated == 0)
            Print("首次计算，可用K线总数: ", ratesTotal, ", 起始K线索引: ", startPos);
        else
            Print("增量计算，起始K线索引: ", startPos);
    }
    
    // 获取MACD数据
    int macdHandle = iMACD(Symbol(), Period(), fastEMA, slowEMA, signalSMA, PRICE_CLOSE);
    
    if(macdHandle != INVALID_HANDLE)
    {
        // 确保获取足够的数据
    int barsNeeded = MathMax(divergenceLookback + 10, ratesTotal);  // 确保有足够的历史数据
    if(barsNeeded > BARS_MAX)
        barsNeeded = BARS_MAX;
    
    // 添加数据数量检查
    if(ratesTotal < 10)
    {
        if(debugMode)
            Print("数据不足，当前K线数量: ", ratesTotal, "，需要至少10根K线");
        return(0);
    }
        
        // 创建MACD值数组
        double macdMain[];
        ArrayResize(macdMain, barsNeeded);
        
        // 复制MACD数据 - 从0索引开始复制足够的数据
        int copiedBars = CopyBuffer(macdHandle, 0, 0, barsNeeded, macdMain);
        if(debugMode)
            Print("Copied ", copiedBars, " bars of MACD data");
        
        // 分析每根K线 - 修复索引范围检查
        for(int i = startPos; i < ratesTotal; i++)
        {
            // 确保MACD数据足够
            if(i >= ArraySize(macdMain))
            {
                if(debugMode)
                    Print("MACD数据不足，索引: ", i, "，MACD数组大小: ", ArraySize(macdMain));
                continue;
            }
            
            // 确保MACD数据足够
            if(i >= ArraySize(macdMain))
                continue;
            
            // 根据选择的信号模式判断信号
            bool pinbarFound = isPinbar(i, high, low, open, close);
            bool bullishDivergenceFound = false;
            bool bearishDivergenceFound = false;
            
            // 只有在需要时才计算背离
            if(signalMode != MODE_PINBAR_ONLY && i >= 10)
            {
                bullishDivergenceFound = isBullishDivergence(i, divergenceLookback, low, macdMain);
                bearishDivergenceFound = isBearishDivergence(i, divergenceLookback, high, macdMain);
            }
            
            // 根据信号模式计算信号
            bool bullishSignal = false;
            bool bearishSignal = false;
            
            switch(signalMode)
            {
                case MODE_COMBINED:
                    // 组合模式：同时满足Pinbar和MACD背离
                    bullishSignal = pinbarFound && bullishDivergenceFound;
                    bearishSignal = pinbarFound && bearishDivergenceFound;
                    break;
                case MODE_PINBAR_ONLY:
                    // 仅Pinbar信号
                    // 根据Pinbar形态进一步判断是看涨还是看跌
                    if(pinbarFound)
                    {
                        double body = MathAbs(close[i] - open[i]);
                        double upperWick = high[i] - MathMax(open[i], close[i]);
                        double lowerWick = MathMin(open[i], close[i]) - low[i];
                        
                        // 下影线长于上影线，倾向于看涨
                        bullishSignal = (lowerWick > upperWick);
                        // 上影线长于下影线，倾向于看跌
                        bearishSignal = (upperWick > lowerWick);
                    }
                    break;
                case MODE_DIVERGENCE_ONLY:
                    // 仅MACD背离信号
                    bullishSignal = bullishDivergenceFound;
                    bearishSignal = bearishDivergenceFound;
                    break;
                case MODE_EITHER:
                default:
                    // 任一模式：满足任一条件
                    bullishSignal = pinbarFound || bullishDivergenceFound;
                    bearishSignal = pinbarFound || bearishDivergenceFound;
                    
                    // 但对于任一模式，我们需要避免同一点位同时出现看涨和看跌信号
                    if(bullishSignal && bearishSignal)
                    {
                        // 如果同时满足，根据强度判断
                        double bullishStrength = (pinbarFound ? 1 : 0) + (bullishDivergenceFound ? 1 : 0);
                        double bearishStrength = (pinbarFound ? 1 : 0) + (bearishDivergenceFound ? 1 : 0);
                        
                        if(bullishStrength >= bearishStrength)
                            bearishSignal = false;
                        else
                            bullishSignal = false;
                    }
                    break;
            }
            
            // 设置信号
            if(bullishSignal)
            {
                upBuffer[i] = low[i];
                if(debugMode)
                    Print("Bullish signal at bar ", i, " (Signal mode: ", signalMode, ")");
            }
            if(bearishSignal)
            {
                downBuffer[i] = high[i];
                if(debugMode)
                    Print("Bearish signal at bar ", i, " (Signal mode: ", signalMode, ")");
            }
            
            // 记录信号检测情况
            if(debugMode)
            {
                Print("Bar ", i, ", Pinbar: ", pinbarFound, ", 看涨背离: ", bullishDivergenceFound, ", 看跌背离: ", bearishDivergenceFound);
                Print("Bar ", i, ", 信号模式: ", signalMode, ", 看涨信号: ", bullishSignal, ", 看跌信号: ", bearishSignal);
            }
        }
        
        // 释放MACD句柄
        IndicatorRelease(macdHandle);
    }
    else if(debugMode)
    {
        Print("Failed to get MACD indicator handle");
    }
    
    return(ratesTotal);
}
//+------------------------------------------------------------------+
