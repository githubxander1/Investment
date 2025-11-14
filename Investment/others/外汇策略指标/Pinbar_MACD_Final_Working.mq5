//+------------------------------------------------------------------+
//|                                 Pinbar_MACD_Final_Working.mq5 |
//+------------------------------------------------------------------+
#property copyright ""
#property link      ""
#property version   "1.00"

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

// 输入参数
input int                PinbarSize       = 2;        // Pinbar大小倍数 (降低默认值以增加信号)
input bool               UseMacdDivergence = true;    // 使用MACD背离
input int                FastEMA         = 12;       // 快线周期
input int                SlowEMA         = 26;       // 慢线周期
input int                SignalSMA       = 9;        // 信号线周期
input int                DivergenceLookback = 20;    // 背离检测回溯周期

// 全局变量
double UpBuffer[];               // 多头信号
double DownBuffer[];             // 空头信号

//+------------------------------------------------------------------+
int OnInit()
{
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA);
    SetIndexBuffer(1, DownBuffer, INDICATOR_DATA);
    
    PlotIndexSetInteger(0, PLOT_ARROW, 233);
    PlotIndexSetInteger(1, PLOT_ARROW, 234);
    
    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    // 清理资源
}

//+------------------------------------------------------------------+
bool IsPinbar(const int index, const double &high[], const double &low[], const double &open[], const double &close[])
{
    // 计算蜡烛图各部分大小
    double body = MathAbs(close[index] - open[index]);
    double upper_wick = high[index] - MathMax(open[index], close[index]);
    double lower_wick = MathMin(open[index], close[index]) - low[index];
    
    // 判断是否为Pinbar
    if(body == 0)
        return(false);
    
    if(upper_wick >= PinbarSize * body || lower_wick >= PinbarSize * body)
        return(true);
    
    return(false);
}

//+------------------------------------------------------------------+
// 底背离检测（多头信号）
bool IsBullishDivergence(const int current, const int lookback, const double &low[], const double &macd_values[])
{
    // 确保索引有效
    if(current <= lookback || lookback < 10)
        return(false);
    
    // 找到最近的低点
    int lowest_idx = current;
    double lowest_price = low[current];
    
    for(int i = current-1; i >= current-lookback; i--)
    {
        if(low[i] < lowest_price)
        {
            lowest_price = low[i];
            lowest_idx = i;
        }
    }
    
    // 如果当前就是最低点，检查MACD是否背离
    if(lowest_idx == current)
    {
        // 找到MACD的最低点 - 初始化变量
        int macd_lowest_idx = current;
        double macd_lowest_value = macd_values[current];
        
        for(int i = current-1; i >= current-lookback; i--)
        {
            if(macd_values[i] < macd_lowest_value)
            {
                macd_lowest_value = macd_values[i];
                macd_lowest_idx = i;
            }
        }
        
        // 底背离：价格创新低，但MACD的最低点出现在之前
        // 更明确的条件：MACD当前值大于前一个低点的MACD值
        if(macd_lowest_idx < current && macd_values[current] > macd_values[macd_lowest_idx])
        {
            return(true);
        }
    }
    
    return(false);
}

// 顶背离检测（空头信号）
bool IsBearishDivergence(const int current, const int lookback, const double &high[], const double &macd_values[])
{
    // 确保索引有效
    if(current <= lookback || lookback < 10)
        return(false);
    
    // 找到最近的高点
    int highest_idx = current;
    double highest_price = high[current];
    
    for(int i = current-1; i >= current-lookback; i--)
    {
        if(high[i] > highest_price)
        {
            highest_price = high[i];
            highest_idx = i;
        }
    }
    
    // 如果当前就是最高点，检查MACD是否背离
    if(highest_idx == current)
    {
        // 找到MACD的最高点 - 初始化变量
        int macd_highest_idx = current;
        double macd_highest_value = macd_values[current];
        
        for(int i = current-1; i >= current-lookback; i--)
        {
            if(macd_values[i] > macd_highest_value)
            {
                macd_highest_value = macd_values[i];
                macd_highest_idx = i;
            }
        }
        
        // 顶背离：价格创新高，但MACD的最高点出现在之前
        // 更明确的条件：MACD当前值小于前一个高点的MACD值
        if(macd_highest_idx < current && macd_values[current] < macd_values[macd_highest_idx])
        {
            return(true);
        }
    }
    
    return(false);
}

//+------------------------------------------------------------------+
int OnCalculate(const int rates_total, const int prev_calculated,
                const datetime &time[], const double &open[],
                const double &high[], const double &low[],
                const double &close[], const long &tick_volume[],
                const long &volume[], const int &spread[])
{
    // 初始化缓冲区
    ArrayInitialize(UpBuffer, EMPTY_VALUE);
    ArrayInitialize(DownBuffer, EMPTY_VALUE);
    
    // 计算起始位置
    int start = prev_calculated - 1;
    if(start < 0)
        start = 0;
    
    // 获取MACD数据
    int macd_handle = iMACD(Symbol(), Period(), FastEMA, SlowEMA, SignalSMA, PRICE_CLOSE);
    
    if(macd_handle != INVALID_HANDLE)
    {
        // 计算需要的数据量
        int bars_needed = rates_total;
        if(bars_needed > BARS_MAX)
            bars_needed = BARS_MAX;
        
        // 创建MACD值数组
        double macd_main[];
        ArrayResize(macd_main, bars_needed);
        
        // 复制MACD数据
        CopyBuffer(macd_handle, 0, 0, bars_needed, macd_main);
        
        // 分析每根K线
        for(int i = start; i < rates_total && i < ArraySize(macd_main); i++)
        {
            // 检测Pinbar
            if(IsPinbar(i, high, low, open, close))
            {
                // 如果不使用MACD背离，直接显示信号
                if(!UseMacdDivergence)
                {
                    if(close[i] > open[i])
                        UpBuffer[i] = low[i];
                    else
                        DownBuffer[i] = high[i];
                }
                else
                {
                    // 检测MACD底背离（多头信号）
                    if(i >= DivergenceLookback && IsBullishDivergence(i, DivergenceLookback, low, macd_main))
                    {
                        UpBuffer[i] = low[i];
                    }
                    // 检测MACD顶背离（空头信号）
                    if(i >= DivergenceLookback && IsBearishDivergence(i, DivergenceLookback, high, macd_main))
                    {
                        DownBuffer[i] = high[i];
                    }
                }
            }
        }
        
        // 释放MACD句柄
        IndicatorRelease(macd_handle);
    }
    
    return(rates_total);
}
//+------------------------------------------------------------------+
