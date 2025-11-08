//+------------------------------------------------------------------+
//|                                                   ExpWPRBB_增强版.mq5 |
//|                                  Copyright 2025, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property strict

//+------------------------------------------------------------------+
//| 包含文件                                                         |
//+------------------------------------------------------------------+
#include <Trade\Trade.mqh>
#include <Arrays\ArrayLong.mqh>

//+------------------------------------------------------------------+
//| 枚举类型                                                         |
//+------------------------------------------------------------------+
//--- 信号类型
enum ENUM_SIGNAL_TYPE
  {
   SIGNAL_TYPE_NONE,                                                 // 无信号
   SIGNAL_TYPE_LONG,                                                 // 买入信号
   SIGNAL_TYPE_SHORT,                                                // 卖出信号
  };

//--- 指标类型
enum ENUM_MY_INDICATOR
  {
   MY_IND_WPR,                                                       // WPR指标
   MY_IND_BANDS,                                                     // 布林带指标
  };

//--- 结构体
struct SData
  {
   CArrayLong  list_tickets;                                         // 持仓订单列表
   double      total_volume;                                         // 总持仓量
  };

struct SDataPositions
  {
   SData       Buy;                                                  // 买入持仓数据
   SData       Sell;                                                 // 卖出持仓数据
  } Data;

//+------------------------------------------------------------------+
//| 宏定义                                                           |
//+------------------------------------------------------------------+
#define  DATA_COUNT        3                                         // 从指标获取的数据数量
#define  ENV_ATTEMPTS      3                                         // 等待环境更新的尝试次数
#define  ENV_WAIT_ATTEMPT  1000                                      // 每次等待时间（毫秒）
#define  SPREAD_MLTP       3                                         // 点差倍数

//+------------------------------------------------------------------+
//| 输入参数                                                         |
//+------------------------------------------------------------------+
//--- WPR参数
input int                  InpPeriodWPR      =  32;                  // WPR计算周期
input double               InpOverboughtWPR  = -20;                  // WPR超买水平
input double               InpOversoldWPR    = -80;                  // WPR超卖水平
//--- BB参数
input int                  InpPeriodBB       =  58;                  // BB计算周期
input double               InpDeviationBB    =  2.0;                 // BB标准差
input int                  InpShiftBB        =  0;                   // BB偏移
input ENUM_APPLIED_PRICE   InpPriceBB        =  PRICE_CLOSE;         // BB应用价格
//--- ATR参数
input int                  InpPeriodATR      =  64;                  // ATR计算周期
//--- 交易参数
input bool                 InpSignalsOnly    =  true;                // 仅显示信号，不自动交易
input double               InpVolume         =  0.1;                 // 交易手数
input ulong                InpDeviation      =  10;                  // 滑点（点数）
input ulong                InpMagic          =  123456;              // 魔术数字
input int                  InpStopLoss       =  -1;                  // 止损（点数），0-无，-1-半布林带宽度
input int                  InpTakeProfit     =  -1;                  // 止盈（点数），0-无，-1-ATR值
input double               InpSLMltp         =  2.6;                 // 止损倍数（当SL==-1时）
input double               InpTPMltp         =  1.3;                 // 止盈倍数（当TP==-1时）
//--- 日志参数
input bool                 InpLogSignals     =  true;                // 记录信号日志
input bool                 InpLogTrades      =  true;                // 记录交易日志
input bool                 InpLogErrors      =  true;                // 记录错误日志

//+------------------------------------------------------------------+
//| 全局变量                                                         |
//+------------------------------------------------------------------+
CTrade   trade;                                                      // 交易对象
int      handle_wpr;                                                 // WPR指标句柄
int      handle_bb;                                                  // BB指标句柄
int      handle_atr;                                                 // ATR指标句柄
double   wpr[DATA_COUNT]={};                                         // WPR值数组
double   bb0[DATA_COUNT]={};                                         // BB值数组，缓冲区0（上轨）
double   bb1[DATA_COUNT]={};                                         // BB值数组，缓冲区1（下轨）
double   bb2[DATA_COUNT]={};                                         // BB值数组，缓冲区2（中轨）
double   atr[DATA_COUNT]={};                                         // ATR值数组
MqlRates prc[DATA_COUNT]={};                                         // 价格和时间数组

int      period_wpr;                                                 // WPR计算周期
double   overbought_wpr;                                             // WPR超买水平
double   oversold_wpr;                                               // WPR超卖水平

int      period_bb;                                                  // BB计算周期
double   deviation_bb;                                               // BB标准差
int      shift_bb;                                                   // BB偏移

int      period_atr;                                                 // ATR计算周期

double   lot;                                                        // 交易手数
string   program_name;                                               // 程序名称
int      prev_total;                                                 // 上一次持仓数量
bool     netto;                                                      // 净值账户标志

//+------------------------------------------------------------------+
//| 初始化函数                                                       |
//+------------------------------------------------------------------+
int OnInit()
  {
   //--- 检查账户类型
   netto=false;
   if(AccountInfoInteger(ACCOUNT_MARGIN_MODE)!=ACCOUNT_MARGIN_MODE_RETAIL_HEDGING)
     {
      Print("警告：该EA专为对冲账户设计，在净值账户上可能无法正常工作");
      netto=true;
     }

   //--- 设置和校正指标输入参数
   //--- WPR
   period_wpr=(InpPeriodWPR<1 ? 14 : InpPeriodWPR);
   overbought_wpr=(InpOverboughtWPR<-99  ? -99  : InpOverboughtWPR> 0   ?  0  : InpOverboughtWPR);
   oversold_wpr  =(InpOversoldWPR  <-100 ? -100 : InpOversoldWPR  >-1   ? -1  : InpOversoldWPR);
   if(overbought_wpr<=oversold_wpr)
      overbought_wpr+=1;
   //--- BB
   period_bb=(InpPeriodBB<2 ? 20 : InpPeriodBB);
   deviation_bb=InpDeviationBB;
   shift_bb=InpShiftBB;
   //--- ATR
   period_atr=(InpPeriodATR<1 ? 14 : InpPeriodATR);

   //--- 初始化指标值数组
   ArrayInitialize(wpr,EMPTY_VALUE);
   ArrayInitialize(bb0,EMPTY_VALUE);
   ArrayInitialize(bb1,EMPTY_VALUE);
   ArrayInitialize(bb2,EMPTY_VALUE);
   ZeroMemory(prc);

   //--- 创建指标句柄
   //--- WPR
   handle_wpr=iWPR(Symbol(),PERIOD_CURRENT,period_wpr);
   if(handle_wpr==INVALID_HANDLE)
     {
      LogError("创建WPR指标失败，周期: ", period_wpr);
      return INIT_FAILED;
     }
   //--- BB
   handle_bb=iBands(Symbol(),PERIOD_CURRENT,period_bb,shift_bb,deviation_bb,InpPriceBB);
   if(handle_bb==INVALID_HANDLE)
     {
      LogError("创建布林带指标失败，参数: 周期=", period_bb, ", 偏移=", shift_bb, ", 标准差=", DoubleToString(deviation_bb, 3));
      return INIT_FAILED;
     }
   //--- ATR
   handle_atr=iATR(Symbol(),PERIOD_CURRENT,period_atr);
   if(handle_atr==INVALID_HANDLE)
     {
      LogError("创建ATR指标失败，周期: ", period_atr);
      return INIT_FAILED;
     }

   //--- 设置程序名称和持仓数量
   program_name=MQLInfoString(MQL_PROGRAM_NAME);
   prev_total=0;

   //--- 设置交易参数
   trade.SetTypeFilling(GetTypeFilling());
   trade.SetExpertMagicNumber(InpMagic);
   trade.SetDeviationInPoints(InpDeviation);
   lot=CorrectLots(InpVolume);

   //--- 初始化成功
   LogInfo("ExpWPRBB增强版初始化成功");
   return(INIT_SUCCEEDED);
  }

//+------------------------------------------------------------------+
//| 反初始化函数                                                     |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   LogInfo("ExpWPRBB增强版已停止运行");
  }

//+------------------------------------------------------------------+
//| 每 tick 执行函数                                                 |
//+------------------------------------------------------------------+
void OnTick()
  {
   //--- 获取指标和价格数据
   if(!CopyIndicatorsData() || !CopyPricesData())
      return;

   //--- 更新持仓列表
   int positions_total=PositionsTotal();
   if(prev_total!=positions_total)
     {
      if(!FillingListTickets(Symbol(),InpMagic))
         return;
      prev_total=positions_total;
     }

   //--- 获取指标信号
   ENUM_SIGNAL_TYPE signal_wpr=SignalWPR();
   ENUM_SIGNAL_TYPE signal_bb=SignalBB();
   //--- 综合信号（两个指标信号一致时才生成）
   ENUM_SIGNAL_TYPE signal=(signal_wpr==signal_bb ? signal_wpr : SIGNAL_TYPE_NONE);

   //--- 记录信号日志
   if(InpLogSignals && signal!=SIGNAL_TYPE_NONE)
     {
      string signal_text = (signal==SIGNAL_TYPE_LONG) ? "买入" : "卖出";
      string wpr_text = (signal_wpr==SIGNAL_TYPE_LONG) ? "买入" : (signal_wpr==SIGNAL_TYPE_SHORT) ? "卖出" : "无";
      string bb_text = (signal_bb==SIGNAL_TYPE_LONG) ? "买入" : (signal_bb==SIGNAL_TYPE_SHORT) ? "卖出" : "无";
      LogInfo("信号生成 - 综合信号: ", signal_text, ", WPR信号: ", wpr_text, ", 布林带信号: ", bb_text);
     }

   //--- 仅显示信号模式
   if(InpSignalsOnly)
     {
      SetArrow(MY_IND_WPR,signal_wpr,false);
      SetArrow(MY_IND_BANDS,signal_bb,true);
      return;
     }

   //--- 执行交易
   TradeProcess(signal);
  }

//+------------------------------------------------------------------+
//| 获取价格数据                                                     |
//+------------------------------------------------------------------+
bool CopyPricesData(void)
  {
   ResetLastError();
   if(CopyRates(Symbol(),PERIOD_CURRENT,0,DATA_COUNT,prc)!=DATA_COUNT)
     {
      LogError("获取价格数据失败，错误代码: ", GetLastError());
      return false;
     }
   return true;
  }

//+------------------------------------------------------------------+
//| 获取WPR指标数据                                                  |
//+------------------------------------------------------------------+
bool CopyWPRData(void)
  {
   ResetLastError();
   if(CopyBuffer(handle_wpr,0,0,DATA_COUNT,wpr)!=DATA_COUNT)
     {
      LogError("获取WPR数据失败，错误代码: ", GetLastError());
      return false;
     }
   return true;
  }

//+------------------------------------------------------------------+
//| 获取布林带指标数据                                               |
//+------------------------------------------------------------------+
bool CopyBBData(void)
  {
   ResetLastError();
   if(CopyBuffer(handle_bb,UPPER_BAND,0,DATA_COUNT,bb0)!=DATA_COUNT)
     {
      LogError("获取布林带上轨数据失败，错误代码: ", GetLastError());
      return false;
     }
   if(CopyBuffer(handle_bb,LOWER_BAND,0,DATA_COUNT,bb1)!=DATA_COUNT)
     {
      LogError("获取布林带下轨数据失败，错误代码: ", GetLastError());
      return false;
     }
   if(CopyBuffer(handle_bb,BASE_LINE,0,DATA_COUNT,bb2)!=DATA_COUNT)
     {
      LogError("获取布林带中轨数据失败，错误代码: ", GetLastError());
      return false;
     }
   return true;
  }

//+------------------------------------------------------------------+
//| 获取ATR指标数据                                                  |
//+------------------------------------------------------------------+
bool CopyATRData(void)
  {
   ResetLastError();
   if(CopyBuffer(handle_atr,0,0,DATA_COUNT,atr)!=DATA_COUNT)
     {
      LogError("获取ATR数据失败，错误代码: ", GetLastError());
      return false;
     }
   return true;
  }

//+------------------------------------------------------------------+
//| 获取所有指标数据                                                 |
//+------------------------------------------------------------------+
bool CopyIndicatorsData(void)
  {
   bool res=CopyWPRData(); // 获取WPR数据结果
   res &=CopyBBData();     // 获取BB数据结果
   res &=CopyATRData();    // 获取ATR数据结果
   return res;
  }

//+------------------------------------------------------------------+
//| 获取指定索引的开盘价                                             |
//+------------------------------------------------------------------+
double PriceOpen(const int index)
  {
   return(index<0 || index>DATA_COUNT-1 ? 0 : prc[DATA_COUNT-index-1].open);
  }

//+------------------------------------------------------------------+
//| 获取指定索引的最高价                                             |
//+------------------------------------------------------------------+
double PriceHigh(const int index)
  {
   return(index<0 || index>DATA_COUNT-1 ? 0 : prc[DATA_COUNT-index-1].high);
  }

//+------------------------------------------------------------------+
//| 获取指定索引的最低价                                             |
//+------------------------------------------------------------------+
double PriceLow(const int index)
  {
   return(index<0 || index>DATA_COUNT-1 ? 0 : prc[DATA_COUNT-index-1].low);
  }

//+------------------------------------------------------------------+
//| 获取指定索引的收盘价                                             |
//+------------------------------------------------------------------+
double PriceClose(const int index)
  {
   return(index<0 || index>DATA_COUNT-1 ? 0 : prc[DATA_COUNT-index-1].close);
  }

//+------------------------------------------------------------------+
//| 获取指定索引的时间                                               |
//+------------------------------------------------------------------+
datetime Time(const int index)
  {
   return(index<0 || index>DATA_COUNT-1 ? 0 : prc[DATA_COUNT-index-1].time);
  }

//+------------------------------------------------------------------+
//| 获取指定索引的WPR值                                              |
//+------------------------------------------------------------------+
double WPR(const int index)
  {
   return(index<0 || index>DATA_COUNT-1 ? EMPTY_VALUE : wpr[DATA_COUNT-index-1]);
  }

//+------------------------------------------------------------------+
//| 获取指定索引的布林带上轨值                                       |
//+------------------------------------------------------------------+
double BBUpper(const int index)
  {
   return(index<0 || index>DATA_COUNT-1 ? EMPTY_VALUE : bb0[DATA_COUNT-index-1]);
  }

//+------------------------------------------------------------------+
//| 获取指定索引的布林带下轨值                                       |
//+------------------------------------------------------------------+
double BBLower(const int index)
  {
   return(index<0 || index>DATA_COUNT-1 ? EMPTY_VALUE : bb1[DATA_COUNT-index-1]);
  }

//+------------------------------------------------------------------+
//| 获取指定索引的布林带中轨值                                       |
//+------------------------------------------------------------------+
double BBMiddle(const int index)
  {
   return(index<0 || index>DATA_COUNT-1 ? EMPTY_VALUE : bb2[DATA_COUNT-index-1]);
  }

//+------------------------------------------------------------------+
//| 获取布林带半宽度（点数）                                         |
//+------------------------------------------------------------------+
int HalfSizeBB(const int index)
  {
   double up=BBUpper(index);
   double dn=BBLower(index);
   if(up==EMPTY_VALUE || dn==EMPTY_VALUE)
      return 0;
   return (int)round(((up-dn)/2.0)/Point());
  }

//+------------------------------------------------------------------+
//| 获取指定索引的ATR值                                              |
//+------------------------------------------------------------------+
double ATR(const int index)
  {
   return(index<0 || index>DATA_COUNT-1 ? EMPTY_VALUE : atr[DATA_COUNT-index-1]);
  }

//+------------------------------------------------------------------+
//| WPR信号生成                                                      |
//+------------------------------------------------------------------+
ENUM_SIGNAL_TYPE SignalWPR(void)
  {
   //--- 获取WPR值
   double wpr0=WPR(1);
   double wpr1=WPR(2);
   //--- 数据不完整，无信号
   if(wpr0==EMPTY_VALUE || wpr1==EMPTY_VALUE)
      return SIGNAL_TYPE_NONE;

   //--- 买入信号：WPR从下向上突破超卖区
   if(wpr0>wpr1 && wpr1<=oversold_wpr)
      return SIGNAL_TYPE_LONG;
   //--- 卖出信号：WPR从上向下跌破超买区
   if(wpr0<wpr1 && wpr1>=overbought_wpr)
      return SIGNAL_TYPE_SHORT;
   //--- 无信号
   return SIGNAL_TYPE_NONE;
  }

//+------------------------------------------------------------------+
//| 布林带信号生成                                                   |
//+------------------------------------------------------------------+
ENUM_SIGNAL_TYPE SignalBB(void)
  {
   //--- 获取布林带和价格数据
   double bbup=BBUpper(0);
   double bbdn=BBLower(0);
   double bbmd=BBMiddle(0);
   double price=PriceOpen(0);
   //--- 数据不完整，无信号
   if(bbup==EMPTY_VALUE || bbdn==EMPTY_VALUE || bbmd==EMPTY_VALUE || price==0)
      return SIGNAL_TYPE_NONE;

   //--- 计算上下轨与中轨的中间值
   double upper=(bbup+bbmd)*0.5;
   double lower=(bbdn+bbmd)*0.5;

   //--- 买入信号：价格低于下轨与中轨的中间值
   if(price<lower)
      return SIGNAL_TYPE_LONG;
   //--- 卖出信号：价格高于上轨与中轨的中间值
   if(price>upper)
      return SIGNAL_TYPE_SHORT;
   //--- 无信号
   return SIGNAL_TYPE_NONE;
  }

//+------------------------------------------------------------------+
//| 在图表上绘制信号箭头                                             |
//+------------------------------------------------------------------+
void SetArrow(const ENUM_MY_INDICATOR indicator,const ENUM_SIGNAL_TYPE signal,bool chart_redraw)
  {
   //--- 无信号或指标类型错误，直接返回
   if(signal==SIGNAL_TYPE_NONE || (indicator!=MY_IND_WPR && indicator!=MY_IND_BANDS))
      return;

   //--- 获取当前K线时间
   datetime time=Time(0);
   if(time==0)
      return;

   ENUM_OBJECT obj_type;   // 对象类型
   double      price=0;    // 箭头价格位置
   //--- 根据指标类型设置价格和箭头类型
   switch(indicator)
     {
      //--- WPR信号
      case MY_IND_WPR :
        price=PriceOpen(0);
        obj_type=(signal==SIGNAL_TYPE_LONG ? OBJ_ARROW_BUY : OBJ_ARROW_SELL);
        break;

      //--- 布林带信号
      default:
        obj_type=OBJ_ARROW;
        price=(signal==SIGNAL_TYPE_LONG ? BBLower(0) : BBUpper(0));
        break;
     }
   //--- 时间或价格获取失败，返回
   if(price==0)
      return;

   //--- 创建对象名称
   string ind=(indicator==MY_IND_WPR ? "_WPR" : "_BB");
   string sig=(signal==SIGNAL_TYPE_LONG ? "_Long_signal_" : "_Short_signal_");
   string name=program_name+ind+sig+TimeToString(time);
   //--- 对象已存在，返回
   if(ObjectFind(0,name)==0)
      return;

   //--- 创建对象
   if(!ObjectCreate(0,name,obj_type,0,time,price))
      return;

   //--- 设置箭头颜色
   ObjectSetInteger(0,name,OBJPROP_COLOR,(signal==SIGNAL_TYPE_LONG ? clrBlue : clrRed));
   //--- 设置线条样式
   ObjectSetInteger(0,name,OBJPROP_STYLE,STYLE_SOLID);
   //--- 设置线条宽度
   ObjectSetInteger(0,name,OBJPROP_WIDTH,0);

   //--- 设置布林带信号箭头代码
   if(indicator==MY_IND_BANDS)
      ObjectSetInteger(0,name,OBJPROP_ARROWCODE,159);

   //--- 设置显示层级
   ObjectSetInteger(0,name,OBJPROP_BACK,false);
   //--- 禁止鼠标选择和移动
   ObjectSetInteger(0,name,OBJPROP_SELECTABLE,false);
   ObjectSetInteger(0,name,OBJPROP_SELECTED,false);
   //--- 隐藏对象名称
   ObjectSetInteger(0,name,OBJPROP_HIDDEN,true);

   //--- 重绘图表
   if(chart_redraw)
      ChartRedraw();
  }

//+------------------------------------------------------------------+
//| 获取订单执行类型                                                 |
//+------------------------------------------------------------------+
ENUM_ORDER_TYPE_FILLING GetTypeFilling(const ENUM_ORDER_TYPE_FILLING type=ORDER_FILLING_RETURN)
  {
   const ENUM_SYMBOL_TRADE_EXECUTION exe_mode=(ENUM_SYMBOL_TRADE_EXECUTION)::SymbolInfoInteger(Symbol(),SYMBOL_TRADE_EXEMODE);
   const int filling_mode=(int)::SymbolInfoInteger(Symbol(),SYMBOL_FILLING_MODE);

   return((filling_mode==0 || (type>=ORDER_FILLING_RETURN) || ((filling_mode &(type+1))!=type+1)) ?
          (((exe_mode==SYMBOL_TRADE_EXECUTION_EXCHANGE) || (exe_mode==SYMBOL_TRADE_EXECUTION_INSTANT)) ?
          ORDER_FILLING_RETURN :((filling_mode==SYMBOL_FILLING_IOC) ? ORDER_FILLING_IOC : ORDER_FILLING_FOK)) : type);
  }

//+------------------------------------------------------------------+
//| 校正交易手数                                                     |
//+------------------------------------------------------------------+
double CorrectLots(const double lots,const bool to_min_correct=true)
  {
   double min=SymbolInfoDouble(Symbol(),SYMBOL_VOLUME_MIN);
   double max=SymbolInfoDouble(Symbol(),SYMBOL_VOLUME_MAX);
   double step=SymbolInfoDouble(Symbol(),SYMBOL_VOLUME_STEP);
   return(to_min_correct ? VolumeRoundToSmaller(lots,min,max,step) : VolumeRoundToCorrect(lots,min,max,step));
  }

//+------------------------------------------------------------------+
//| 四舍五入到合适的手数                                             |
//+------------------------------------------------------------------+
double VolumeRoundToCorrect(const double volume,const double min,const double max,const double step)
  {
   return(step==0 ? min : fmin(fmax(round(volume/step)*step,min),max));
  }

//+------------------------------------------------------------------+
//| 向下取整到合适的手数                                             |
//+------------------------------------------------------------------+
double VolumeRoundToSmaller(const double volume,const double min,const double max,const double step)
  {
   return(step==0 ? min : fmin(fmax(floor(volume/step)*step,min),max));
  }

//+------------------------------------------------------------------+
//| 检查账户持仓限制                                                 |
//+------------------------------------------------------------------+
bool CheckLotForLimitAccount(const ENUM_POSITION_TYPE position_type,const double volume)
  {
   double lots_limit=SymbolInfoDouble(Symbol(),SYMBOL_VOLUME_LIMIT);
   if(lots_limit==0)
      return true;
   double total_volume=(position_type==POSITION_TYPE_BUY ? Data.Buy.total_volume : Data.Sell.total_volume);
   return(total_volume+volume<=lots_limit);
  }

//+------------------------------------------------------------------+
//| 校正止损价格                                                     |
//+------------------------------------------------------------------+
double CorrectStopLoss(const ENUM_POSITION_TYPE position_type,const int stop_loss)
  {
   if(stop_loss==0)
      return 0;
   double pt=Point();
   double price=(position_type==POSITION_TYPE_BUY ? SymbolInfoDouble(Symbol(),SYMBOL_ASK) : SymbolInfoDouble(Symbol(),SYMBOL_BID));
   int lv=StopLevel(), dg=Digits();
   return(position_type==POSITION_TYPE_BUY   ?  NormalizeDouble(fmin(price-lv*pt,price-stop_loss*pt),dg) :
                                                NormalizeDouble(fmax(price+lv*pt,price+stop_loss*pt),dg));
  }

//+------------------------------------------------------------------+
//| 校正止盈价格                                                     |
//+------------------------------------------------------------------+
double CorrectTakeProfit(const ENUM_POSITION_TYPE position_type,const int take_profit)
  {
   if(take_profit==0)
      return 0;
   double pt=Point();
   double price=(position_type==POSITION_TYPE_BUY ? SymbolInfoDouble(Symbol(),SYMBOL_ASK) : SymbolInfoDouble(Symbol(),SYMBOL_BID));
   int lv=StopLevel(), dg=Digits();
   return(position_type==POSITION_TYPE_BUY   ?  NormalizeDouble(fmax(price+lv*pt,price+take_profit*pt),dg) :
                                                NormalizeDouble(fmin(price-lv*pt,price-take_profit*pt),dg));
  }

//+------------------------------------------------------------------+
//| 获取止损水平                                                     |
//+------------------------------------------------------------------+
int StopLevel(void)
  {
   int sp=(int)SymbolInfoInteger(Symbol(),SYMBOL_SPREAD);
   int lv=(int)SymbolInfoInteger(Symbol(),SYMBOL_TRADE_STOPS_LEVEL);
   return(lv==0 ? sp*SPREAD_MLTP : lv);
  }

//+------------------------------------------------------------------+
//| 检查交易环境是否确定                                             |
//+------------------------------------------------------------------+
bool IsUncertainStateEnv(const string symbol_name,const ulong magic_number)
  {
   //--- 在策略测试器中环境始终确定
   if(MQLInfoInteger(MQL_TESTER))
      return false;
   //--- 遍历所有订单
   int total=OrdersTotal();
   for(int i=total-1; i>=0; i--)
     {
      //--- 选择订单
      if(OrderGetTicket(i)==0)
         continue;
      //--- 魔术数字不匹配，跳过
      if(OrderGetInteger(ORDER_MAGIC)!=magic_number)
         continue;
      //--- 订单类型不是买入或卖出，跳过
      ENUM_ORDER_TYPE type=(ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE);
      if(type!=ORDER_TYPE_BUY && type!=ORDER_TYPE_SELL)
         continue;
      //--- 如果订单没有对应的持仓ID且符号匹配，说明环境不确定
      if(!OrderGetInteger(ORDER_POSITION_ID) && OrderGetString(ORDER_SYMBOL)==symbol_name)
         return true;
     }
   //--- 环境正常
   return false;
  }

//+------------------------------------------------------------------+
//| 检查交易环境状态                                                 |
//+------------------------------------------------------------------+
bool CheckUncertainStateEnv(const string symbol_name,const ulong magic_number,const int attempts,const int wait)
  {
   //--- 环境正常，返回true
   if(!IsUncertainStateEnv(symbol_name,magic_number))
      return true;
   //--- 多次尝试等待环境稳定
   int n=0;
   while(!IsStopped() && n<attempts && IsUncertainStateEnv(symbol_name,magic_number))
     {
      n++;
      Sleep(wait);
     }
   //--- 等待后环境仍然不确定
   if(n>=attempts && IsUncertainStateEnv(symbol_name,magic_number))
     {
      LogError("交易环境不确定，请稍后重试");
      return false;
     }
   //--- 环境正常
   return true;
  }

//+------------------------------------------------------------------+
//| 填充持仓列表                                                     |
//+------------------------------------------------------------------+
bool FillingListTickets(const string symbol_name,const ulong magic_number)
  {
   //--- 检查环境状态
   if(!CheckUncertainStateEnv(symbol_name,magic_number,ENV_ATTEMPTS,ENV_WAIT_ATTEMPT))
      return false;

   //--- 清空列表并初始化变量
   Data.Buy.list_tickets.Clear();
   Data.Sell.list_tickets.Clear();
   Data.Buy.total_volume=0;
   Data.Sell.total_volume=0;

   //--- 遍历所有持仓
   int total=PositionsTotal();
   for(int i=total-1; i>WRONG_VALUE; i--)
     {
      //--- 选择持仓
      ulong ticket=PositionGetTicket(i);
      if(ticket==0)
         continue;
      //--- 魔术数字或交易品种不匹配，跳过
      if(PositionGetInteger(POSITION_MAGIC)!=InpMagic || PositionGetString(POSITION_SYMBOL)!=symbol_name)
         continue;
      //--- 获取持仓类型和手数
      ENUM_POSITION_TYPE type=(ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);
      double volume=PositionGetDouble(POSITION_VOLUME);
      //--- 根据持仓类型添加到相应列表
      if(type==POSITION_TYPE_BUY)
        {
         Data.Buy.list_tickets.Add(ticket);
         Data.Buy.total_volume+=volume;
        }
      //--- POSITION_TYPE_SELL
      else
        {
         Data.Sell.list_tickets.Add(ticket);
         Data.Sell.total_volume+=volume;
        }
     }
   //--- 成功
   return true;
  }

//+------------------------------------------------------------------+
//| 获取买入持仓数量                                                 |
//+------------------------------------------------------------------+
int TotalBuy(void)
  {
   return Data.Buy.list_tickets.Total();
  }

//+------------------------------------------------------------------+
//| 获取卖出持仓数量                                                 |
//+------------------------------------------------------------------+
int TotalSell(void)
  {
   return Data.Sell.list_tickets.Total();
  }

//+------------------------------------------------------------------+
//| 获取指定类型持仓的最新订单号                                     |
//+------------------------------------------------------------------+
ulong LastAddedTicket(const ENUM_POSITION_TYPE type)
  {
   return(type==POSITION_TYPE_BUY ? (TotalBuy()>0 ? Data.Buy.list_tickets.At(0) : 0) : (TotalSell()>0 ? Data.Sell.list_tickets.At(0) : 0));
  }

//+------------------------------------------------------------------+
//| 获取持仓K线索引                                                  |
//+------------------------------------------------------------------+
int PositionBar(const ulong ticket)
  {
   //--- 选择持仓
   ResetLastError();
   if(!PositionSelectByTicket(ticket))
     {
      LogError("选择持仓失败，订单号: ", ticket, "，错误代码: ", GetLastError());
      return -1;
     }
   //--- 获取持仓时间和交易品种
   datetime time=(datetime)PositionGetInteger(POSITION_TIME);
   string   symbol=PositionGetString(POSITION_SYMBOL);

   //--- 返回持仓时间对应的K线索引
   return iBarShift(symbol,PERIOD_CURRENT,time);
  }

//+------------------------------------------------------------------+
//| 检查当前K线是否已有指定类型持仓                                  |
//+------------------------------------------------------------------+
bool IsPresentPosOnCurrentBar(const ENUM_POSITION_TYPE type)
  {
   ulong ticket=LastAddedTicket(type);
   return(ticket>0 ? PositionBar(ticket)==0 : false);
  }

//+------------------------------------------------------------------+
//| 获取持仓的开仓价格                                               |
//+------------------------------------------------------------------+
double PositionPriceOpen(const ulong ticket)
  {
   //--- 检查订单号
   if(ticket==0)
      return 0;
   //--- 选择持仓
   ResetLastError();
   if(!PositionSelectByTicket(ticket))
     {
      LogError("选择持仓失败，订单号: ", ticket, "，错误代码: ", GetLastError());
      return 0;
     }
   //--- 返回开仓价格
   return PositionGetDouble(POSITION_PRICE_OPEN);
  }

//+------------------------------------------------------------------+
//| 平仓所有买入持仓                                                 |
//+------------------------------------------------------------------+
bool CloseBuy(void)
  {
   int total=TotalBuy();
   bool res=true;
   for(int i=total-1; i>=0; i--)
     {
      ulong ticket=Data.Buy.list_tickets.At(i);
      if(ticket==NULL)
         continue;
      if(!trade.PositionClose(ticket,InpDeviation))
         res=false;
     }
   return res;
  }

//+------------------------------------------------------------------+
//| 平仓所有卖出持仓                                                 |
//+------------------------------------------------------------------+
bool CloseSell(void)
  {
   int total=TotalSell();
   bool res=true;
   for(int i=total-1; i>=0; i--)
     {
      ulong ticket=Data.Sell.list_tickets.At(i);
      if(ticket==NULL)
         continue;
      if(!trade.PositionClose(ticket,InpDeviation))
         res=false;
     }
   return res;
  }

//+------------------------------------------------------------------+
//| 开仓交易                                                         |
//+------------------------------------------------------------------+
bool OpenPosition(const string symbol_name,const ENUM_POSITION_TYPE type,const double volume,const string comment)
  {
   //--- 计算止损止盈参数
   int    bb=int(HalfSizeBB(0)*InpSLMltp);
   double atrd=ATR(0);
   int    atrp=(atrd!=EMPTY_VALUE ? int(round(atrd*InpTPMltp/Point())) : 0);
   double sl=(InpStopLoss==0   ? 0 : (InpStopLoss<0 ? (bb!=0   ? CorrectStopLoss(type,bb)     : 0) : CorrectStopLoss(type,InpStopLoss)));
   double tp=(InpTakeProfit==0 ? 0 : (InpStopLoss<0 ? (atrp!=0 ? CorrectTakeProfit(type,atrp) : 0) : CorrectTakeProfit(type,InpTakeProfit)));

   //--- 净值账户移除止损止盈
   if(netto)
      sl=tp=0;

   //--- 获取当前价格
   MqlTick tick={};
   if(!SymbolInfoTick(symbol_name,tick))
     {
      LogError("无法获取当前价格");
      return false;
     }
   //--- 检查并获取规范化的交易手数
   double ll=trade.CheckVolume(symbol_name,volume,(type==POSITION_TYPE_BUY ? tick.ask : tick.bid),(ENUM_ORDER_TYPE)type);
   if(ll==0)
     {
      LogError("检查交易手数返回0，请检查交易品种设置");
      return false;
     }

   //--- 检查账户持仓限制
   if(!CheckLotForLimitAccount(type,ll))
     {
      LogError("超出账户持仓限制");
      return false;
     }

   //--- 检查交易环境状态
   if(!CheckUncertainStateEnv(symbol_name,InpMagic,ENV_ATTEMPTS,ENV_WAIT_ATTEMPT))
      return false;

   //--- 再次获取价格
   if(!SymbolInfoTick(symbol_name,tick))
     {
      LogError("无法获取当前价格");
      return false;
     }

   //--- 执行交易并返回结果
   bool result = (type==POSITION_TYPE_BUY ? trade.Buy(ll,symbol_name,tick.ask,sl,tp,comment) : trade.Sell(ll,symbol_name,tick.bid,sl,tp,comment));

   //--- 记录交易日志
   if(InpLogTrades)
     {
      string position_text = (type==POSITION_TYPE_BUY) ? "买入" : "卖出";
      LogInfo("开仓交易 - 类型: ", position_text, ", 手数: ", DoubleToString(ll, 2));
      LogInfo("价格: ", DoubleToString(type==POSITION_TYPE_BUY ? tick.ask : tick.bid, Digits()),
              ", 止损: ", (sl==0 ? "无" : DoubleToString(sl, Digits())),
              ", 止盈: ", (tp==0 ? "无" : DoubleToString(tp, Digits())));
     }

   return result;
  }

//+------------------------------------------------------------------+
//| 交易处理过程                                                     |
//+------------------------------------------------------------------+
void TradeProcess(const ENUM_SIGNAL_TYPE signal)
  {
   //--- 无信号，返回
   if(signal==SIGNAL_TYPE_NONE)
      return;

   //--- 买入信号处理
   if(signal==SIGNAL_TYPE_LONG)
     {
      //--- 当前K线无买入持仓
      if(!IsPresentPosOnCurrentBar(POSITION_TYPE_BUY))
        {
         //--- 获取最近买入持仓的开仓价格
         double price_last=PositionPriceOpen(LastAddedTicket(POSITION_TYPE_BUY));
         //--- 首次开仓或价格优于上次开仓价格
         if(price_last==0 || price_last>SymbolInfoDouble(Symbol(),SYMBOL_ASK))
           {
            //--- 开仓并更新持仓列表
            if(OpenPosition(Symbol(),POSITION_TYPE_BUY,lot,"WPR+BB策略买入"))
              {
               FillingListTickets(Symbol(),InpMagic);
               SetArrow(MY_IND_WPR,SIGNAL_TYPE_LONG,false);     // 显示WPR买入信号
               SetArrow(MY_IND_BANDS,SIGNAL_TYPE_LONG,true);    // 显示布林带买入信号
              }
           }
        }
     }

   //--- 卖出信号处理
   if(signal==SIGNAL_TYPE_SHORT)
     {
      //--- 当前K线无卖出持仓
      if(!IsPresentPosOnCurrentBar(POSITION_TYPE_SELL))
        {
         //--- 获取最近卖出持仓的开仓价格
         double price_last=PositionPriceOpen(LastAddedTicket(POSITION_TYPE_SELL));
         //--- 首次开仓或价格优于上次开仓价格
         if(price_last==0 || price_last<SymbolInfoDouble(Symbol(),SYMBOL_BID))
           {
            //--- 开仓并更新持仓列表
            if(OpenPosition(Symbol(),POSITION_TYPE_SELL,lot,"WPR+BB策略卖出"))
              {
               FillingListTickets(Symbol(),InpMagic);
               SetArrow(MY_IND_WPR,SIGNAL_TYPE_SHORT,false);    // 显示WPR卖出信号
               SetArrow(MY_IND_BANDS,SIGNAL_TYPE_SHORT,true);   // 显示布林带卖出信号
              }
           }
        }
     }
  }

//+------------------------------------------------------------------+
//| 日志记录函数                                                     |
//+------------------------------------------------------------------+
void LogInfo(string text)
  {
   if(InpLogSignals || InpLogTrades)
      Print("【信息】 ", text);
  }

void LogError(string text)
  {
   if(InpLogErrors)
      Print("【错误】 ", text);
  }

void LogInfo(string text, string val1)
  {
   if(InpLogSignals || InpLogTrades)
      Print("【信息】 ", text, val1);
  }

void LogError(string text, string val1)
  {
   if(InpLogErrors)
      Print("【错误】 ", text, val1);
  }

void LogInfo(string text, string val1, string val2)
  {
   if(InpLogSignals || InpLogTrades)
      Print("【信息】 ", text, val1, val2);
  }

void LogError(string text, string val1, string val2)
  {
   if(InpLogErrors)
      Print("【错误】 ", text, val1, val2);
  }

void LogInfo(string text, string val1, string val2, string val3)
  {
   if(InpLogSignals || InpLogTrades)
      Print("【信息】 ", text, val1, val2, val3);
  }

void LogError(string text, string val1, string val2, string val3)
  {
   if(InpLogErrors)
      Print("【错误】 ", text, val1, val2, val3);
  }

void LogInfo(string text, string val1, string val2, string val3, string val4)
  {
   if(InpLogSignals || InpLogTrades)
      Print("【信息】 ", text, val1, val2, val3, val4);
  }

void LogError(string text, string val1, string val2, string val3, string val4)
  {
   if(InpLogErrors)
      Print("【错误】 ", text, val1, val2, val3, val4);
  }

void LogInfo(string text, string val1, string val2, string val3, string val4, string val5)
  {
   if(InpLogSignals || InpLogTrades)
      Print("【信息】 ", text, val1, val2, val3, val4, val5);
  }

void LogError(string text, string val1, string val2, string val3, string val4, string val5)
  {
   if(InpLogErrors)
      Print("【错误】 ", text, val1, val2, val3, val4, val5);
  }

void LogInfo(string text, string val1, string val2, string val3, string val4, string val5, string val6)
  {
   if(InpLogSignals || InpLogTrades)
      Print("【信息】 ", text, val1, val2, val3, val4, val5, val6);
  }

void LogError(string text, string val1, string val2, string val3, string val4, string val5, string val6)
  {
   if(InpLogErrors)
      Print("【错误】 ", text, val1, val2, val3, val4, val5, val6);
  }

void LogInfo(string text, string val1, string val2, string val3, string val4, string val5, string val6, string val7)
  {
   if(InpLogSignals || InpLogTrades)
      Print("【信息】 ", text, val1, val2, val3, val4, val5, val6, val7);
  }

void LogError(string text, string val1, string val2, string val3, string val4, string val5, string val6, string val7)
  {
   if(InpLogErrors)
      Print("【错误】 ", text, val1, val2, val3, val4, val5, val6, val7);
  }

void LogInfo(string text, int val1)
  {
   if(InpLogSignals || InpLogTrades)
      Print("【信息】 ", text, IntegerToString(val1));
  }

void LogError(string text, int val1)
  {
   if(InpLogErrors)
      Print("【错误】 ", text, IntegerToString(val1));
  }

void LogInfo(string text, int val1, int val2)
  {
   if(InpLogSignals || InpLogTrades)
      Print("【信息】 ", text, IntegerToString(val1), ", ", IntegerToString(val2));
  }

void LogError(string text, int val1, int val2)
  {
   if(InpLogErrors)
      Print("【错误】 ", text, IntegerToString(val1), ", ", IntegerToString(val2));
  }

void LogInfo(string text, int val1, int val2, int val3)
  {
   if(InpLogSignals || InpLogTrades)
      Print("【信息】 ", text, IntegerToString(val1), ", ", IntegerToString(val2), ", ", IntegerToString(val3));
  }

void LogError(string text, int val1, int val2, int val3)
  {
   if(InpLogErrors)
      Print("【错误】 ", text, IntegerToString(val1), ", ", IntegerToString(val2), ", ", IntegerToString(val3));
  }

void LogInfo(string text, double val1)
  {
   if(InpLogSignals || InpLogTrades)
      Print("【信息】 ", text, DoubleToString(val1, Digits()));
  }

void LogError(string text, double val1)
  {
   if(InpLogErrors)
      Print("【错误】 ", text, DoubleToString(val1, Digits()));
  }

void LogInfo(string text, double val1, double val2)
  {
   if(InpLogSignals || InpLogTrades)
      Print("【信息】 ", text, DoubleToString(val1, Digits()), ", ", DoubleToString(val2, Digits()));
  }

void LogError(string text, double val1, double val2)
  {
   if(InpLogErrors)
      Print("【错误】 ", text, DoubleToString(val1, Digits()), ", ", DoubleToString(val2, Digits()));
  }

void LogInfo(string text, double val1, double val2, double val3)
  {
   if(InpLogSignals || InpLogTrades)
      Print("【信息】 ", text, DoubleToString(val1, Digits()), ", ", DoubleToString(val2, Digits()), ", ", DoubleToString(val3, Digits()));
  }

void LogError(string text, double val1, double val2, double val3)
  {
   if(InpLogErrors)
      Print("【错误】 ", text, DoubleToString(val1, Digits()), ", ", DoubleToString(val2, Digits()), ", ", DoubleToString(val3, Digits()));
  }
//+------------------------------------------------------------------+