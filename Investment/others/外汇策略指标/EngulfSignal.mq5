//+------------------------------------------------------------------+
//|                        EngulfSignal.mq5                          |
//+------------------------------------------------------------------+
#property copyright ""
#property link      ""
#property version   "1.00"
#property strict

// 修复可能的编译错误 - 确保所有必要的头文件都被包含

#property indicator_chart_window
#property indicator_buffers 2
#property indicator_plots   2

#property indicator_type1   DRAW_ARROW
#property indicator_color1  clrRed
#property indicator_width1  1
#property indicator_label1  "买入信号"

#property indicator_type2   DRAW_ARROW
#property indicator_color2  clrGreen
#property indicator_width2  1
#property indicator_label2  "卖出信号"

// 全局变量
double BuySignalBuffer[];
double SellSignalBuffer[];

//+------------------------------------------------------------------+
//| 指标初始化函数                                                  |
//+------------------------------------------------------------------+
int OnInit()
{
   // 设置指标缓冲区
   SetIndexBuffer(0, BuySignalBuffer, INDICATOR_DATA);
   SetIndexBuffer(1, SellSignalBuffer, INDICATOR_DATA);
   PlotIndexSetInteger(0, PLOT_ARROW, 233); // 设置买入箭头样式（向上箭头）
   PlotIndexSetInteger(1, PLOT_ARROW, 234); // 设置卖出箭头样式（向下箭头）
   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| 指标去初始化函数                                                |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
}

//+------------------------------------------------------------------+
//| 指标主函数                                                      |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total, const int prev_calculated,
                const datetime &time[], const double &open[],
                const double &high[], const double &low[],
                const double &close[], const long &tick_volume[],
                const long &volume[], const int &spread[])
{
   // 检查数据是否足够
   if(rates_total < 2) return(0);
   
   // 计算信号
   int start = prev_calculated - 1;
   if(start < 1) start = 1;
   
   for(int i = start; i < rates_total; i++)
   {
      BuySignalBuffer[i] = EMPTY_VALUE;
      SellSignalBuffer[i] = EMPTY_VALUE;
      
      // 买入信号：收盘价高于开盘价（阳线）
      if(close[i] > open[i])
      {
         BuySignalBuffer[i] = low[i] - 0.0001; // 在K线下方显示买入信号
      }
      // 卖出信号：收盘价低于开盘价（阴线）
      else if(close[i] < open[i])
      {
         SellSignalBuffer[i] = high[i] + 0.0001; // 在K线上方显示卖出信号
      }
   }
   
   return(rates_total);
}
//+------------------------------------------------------------------+