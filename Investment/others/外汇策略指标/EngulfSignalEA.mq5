//+------------------------------------------------------------------+
//|                     EngulfSignalEA.mq5                           |
//+------------------------------------------------------------------+
#property copyright ""
#property link      ""
#property version   "1.00"
#property strict

// EA交易参数
input int TakeProfit = 200;   // 止盈点数
input int StopLoss = 100;     // 止损点数
input double Lots = 0.1;      // 交易手数
input bool UseTrailingStop = false; // 使用追踪止损
input int TrailingStop = 50;  // 追踪止损点数

// 日志设置
input bool EnableFileLogging = true; // 启用文件日志
input string LogFileName = "EngulfSignalEA"; // 日志文件名
input int LogLevel = 2; // 日志级别 (1=错误, 2=警告, 3=信息, 4=详细)

// 全局变量
bool IsNewBar = false;        // 新K线标志
int LastBarIndex = -1;        // 上一个K线的索引
string LogFilePath = "";     // 日志文件路径

// 错误处理参数
input int MaxRetryAttempts = 3; // 最大重试次数
input int RetryDelayMs = 500;   // 重试延迟（毫秒）

// 错误状态变量
int ErrorCount = 0;          // 连续错误计数
int MaxErrorCount = 10;      // 最大连续错误数（超过将暂停交易）
bool TradingPaused = false;  // 交易暂停标志
string LastErrorDescription = ""; // 最后错误描述

// 绩效统计参数
input bool EnableStatistics = true;      // 启用交易统计
input int ReportInterval = 24;           // 报告生成间隔(小时)
input bool GenerateHTMLReport = true;    // 生成HTML报告

// 资金管理参数
input bool UseDynamicLotSize = true;     // 使用动态手数计算
input double RiskPerTrade = 1.0;         // 每笔交易风险百分比
input double MinLotSize = 0.01;          // 最小交易手数
input double MaxLotSize = 5.0;           // 最大交易手数
input int RiskCalculationType = 0;       // 风险计算类型 (0=基于止损点数, 1=固定金额)
input double FixedRiskAmount = 50.0;     // 固定风险金额(当RiskCalculationType=1时使用)

// 交易统计结构体
typedef struct
{
    int totalTrades;                     // 总交易次数
    int winningTrades;                   // 盈利交易次数
    int losingTrades;                    // 亏损交易次数
    int breakEvenTrades;                 // 持平交易次数
    double grossProfit;                  // 总盈利金额
    double grossLoss;                    // 总亏损金额
    double maxDrawdown;                  // 最大回撤
    double maxDrawdownPercent;           // 最大回撤百分比
    double profitFactor;                 // 盈利因子
    double winRate;                      // 胜率
    double averageProfit;                // 平均盈利
    double averageLoss;                  // 平均亏损
    double initialBalance;               // 初始账户余额
    double bestTrade;                    // 最佳单笔交易
    double worstTrade;                   // 最差单笔交易
    double equityHigh;                   // 最高净值
    double equityLow;                    // 最低净值
    datetime lastTradeTime;              // 最后交易时间
    datetime lastReportTime;             // 最后报告生成时间
} TradingStatistics;

// 交易统计实例
TradingStatistics stats;

// 资金管理相关变量
double accountValue = 0.0;              // 账户价值(用于资金管理)

//+------------------------------------------------------------------+
//| EA初始化函数                                                     |
//+------------------------------------------------------------------+
int OnInit()
{
    // 初始化日志系统
    InitializeLogging();
    
    // 记录初始化日志
    LogMessage("EngulfSignalEA初始化开始", 3);
    
    // 记录EA参数设置
    LogMessage("EA参数设置 - 止损: " + (string)StopLoss + ", 止盈: " + (string)TakeProfit + ", 手数: " + DoubleToString(Lots, 2), 3);
    LogMessage("追踪止损设置 - 启用: " + (string)UseTrailingStop + ", 点数: " + (string)TrailingStop, 3);
    
    // 获取当前K线索引
    LastBarIndex = Bars - 1;
    
    // 记录账户信息
    LogAccountInfo(3);
    
    // 初始化交易统计数据
    if(EnableStatistics)
    {
        stats.totalTrades = 0;
        stats.winningTrades = 0;
        stats.losingTrades = 0;
        stats.breakEvenTrades = 0;
        stats.grossProfit = 0.0;
        stats.grossLoss = 0.0;
        stats.maxDrawdown = 0.0;
        stats.maxDrawdownPercent = 0.0;
        stats.profitFactor = 0.0;
        stats.winRate = 0.0;
        stats.averageProfit = 0.0;
        stats.averageLoss = 0.0;
        stats.initialBalance = AccountInfoDouble(ACCOUNT_BALANCE);
        stats.bestTrade = 0.0;
        stats.worstTrade = 0.0;
        stats.equityHigh = AccountInfoDouble(ACCOUNT_EQUITY);
        stats.equityLow = AccountInfoDouble(ACCOUNT_EQUITY);
        stats.lastTradeTime = TimeCurrent();
        stats.lastReportTime = TimeCurrent();
        
        LogMessage("交易统计系统已初始化", 3);
    }
    
    // 初始化账户价值（用于资金管理）
    accountValue = AccountInfoDouble(ACCOUNT_EQUITY);
    LogMessage("账户价值初始化: " + DoubleToString(accountValue, 2), 3);
    
    // 如果启用动态手数，计算初始手数
    if(UseDynamicLotSize)
    {
        double calculatedLot = CalculateLotSize();
        LogMessage("动态手数计算: " + DoubleToString(calculatedLot, 2), 3);
    }
    
    // 初始化完成日志
    LogMessage("EngulfSignalEA初始化完成", 3);
    
    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| EA去初始化函数                                                   |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    LogMessage("EngulfSignalEA去初始化，原因: " + (string)reason);
}

//+------------------------------------------------------------------+
//| EA主函数                                                        |
//+------------------------------------------------------------------+
void OnTick()
{
    // 检查是否有新K线形成
    CheckNewBar();
    
    // 如果有新K线，分析信号并执行交易
    if(IsNewBar)
    {
        // 重置新K线标志
        IsNewBar = false;
        
        // 分析当前K线信号
        AnalyzeSignal();
    }
    
    // 应用追踪止损（如果启用）
    if(UseTrailingStop)
        ApplyTrailingStop();
        
    // 定期生成交易报告
    if(EnableStatistics && (TimeCurrent() - stats.lastReportTime >= ReportInterval * 3600))
    {
        GenerateTradingReport();
        stats.lastReportTime = TimeCurrent();
    }
}

//+------------------------------------------------------------------+
//| 检查新K线形成                                                    |
//+------------------------------------------------------------------+
void CheckNewBar()
{
    int currentBar = Bars - 1;
    
    if(currentBar != LastBarIndex)
    {
        IsNewBar = true;
        LastBarIndex = currentBar;
        LogMessage("检测到新K线，时间: " + TimeToString(Time[0], TIME_DATE|TIME_MINUTES));
    }
}

//+------------------------------------------------------------------+
//| 分析K线信号                                                      |
//+------------------------------------------------------------------+
void AnalyzeSignal()
{
    // 获取当前K线数据
    double open = Open[1];   // 使用[1]获取已完成的K线
    double close = Close[1];
    double high = High[1];
    double low = Low[1];
    datetime time = Time[1];
    
    LogMessage("分析K线信号 (" + TimeToString(time, TIME_DATE|TIME_MINUTES) + ") - 开盘: " + DoubleToString(open, Digits) + 
               ", 最高: " + DoubleToString(high, Digits) + ", 最低: " + DoubleToString(low, Digits) + 
               ", 收盘: " + DoubleToString(close, Digits), 3);
    
    // 计算K线变化百分比
    double changePercent = ((close - open) / open) * 100.0;
    LogMessage("K线变化: " + DoubleToString(changePercent, 4) + "%", 4);
    
    // 检查买入信号：收盘价高于开盘价（阳线）
    if(close > open)
    {
        LogMessage("检测到买入信号: 阳线K线", 3);
        // 检查是否已有多头持仓
        if(PositionSelect(Symbol()) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
        {
            LogMessage("已有多头持仓，不执行新的买入操作", 3);
            return;
        }
        
        // 执行买入操作
        ExecuteBuyOrder();
    }
    // 检查卖出信号：收盘价低于开盘价（阴线）
    else if(close < open)
    {
        LogMessage("检测到卖出信号: 阴线K线", 3);
        // 检查是否已有空头持仓
        if(PositionSelect(Symbol()) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL)
        {
            LogMessage("已有空头持仓，不执行新的卖出操作", 3);
            return;
        }
        
        // 执行卖出操作
        ExecuteSellOrder();
    }
    else
    {
        LogMessage("无信号: 平盘K线", 3);
    }
}

//+------------------------------------------------------------------+
//| 执行买入订单                                                     |
//+------------------------------------------------------------------+
void ExecuteBuyOrder()
{
    // 检查是否可以交易
    if(!CanTrade())
    {
        LogMessage("跳过买入订单执行，交易条件不满足", 2);
        return;
    }
    
    // 检查是否已有多头持仓或订单
    if(HasExistingPosition(POSITION_TYPE_BUY))
    {
        LogMessage("检测到已有多头持仓或订单，跳过买入操作", 2);
        return;
    }
    
    // 获取当前市场数据
    double currentAsk = Ask;
    double currentBid = Bid;
    double spread = (Ask - Bid) / Point;
    
    // 计算止损和止盈价格
    double stopLossPrice = currentAsk - StopLoss * Point;
    double takeProfitPrice = currentAsk + TakeProfit * Point;
    
    LogMessage("准备执行买入订单 - 货币对: " + Symbol() + ", 周期: " + EnumToString(Period()) + 
               ", 手数: " + DoubleToString(Lots, 2) + ", 当前价格: " + DoubleToString(currentAsk, Digits) + 
               ", 点差: " + DoubleToString(spread, 0) + "点", 2);
    LogMessage("止损价格: " + DoubleToString(stopLossPrice, Digits) + 
               " (" + (string)StopLoss + "点), 止盈价格: " + DoubleToString(takeProfitPrice, Digits) + 
               " (" + (string)TakeProfit + "点)", 2);
    
    // 平仓任何空头头寸
    CloseSellPositions();
    
    // 记录下单前账户状态
    LogAccountInfo(4);
    
    // 执行买入订单，支持重试
    MqlTradeRequest request;
    MqlTradeResult result;
    int retryCount = 0;
    bool success = false;
    
    // 尝试执行订单，支持重试
    while(retryCount <= MaxRetryAttempts && !success)
    {
        // 初始化请求结构
        ZeroMemory(request);
        ZeroMemory(result);
        ResetLastError();
        
        request.action = TRADE_ACTION_DEAL;
        request.symbol = Symbol();
        request.volume = Lots;
        request.type = ORDER_TYPE_BUY;
        request.price = currentAsk;
        request.sl = stopLossPrice;
        request.tp = takeProfitPrice;
        request.deviation = 3;
        request.magic = 12345;
        request.comment = "EngulfSignalEA买入";
        
        // 记录详细日志
        LogMessage("尝试发送买入订单: 品种=" + Symbol() + ", 手数=" + DoubleToString(Lots, 2) + ", 价格=" + DoubleToString(request.price, Digits), 4);
        
        if(OrderSend(request, result))
        {
            if(result.retcode == TRADE_RETCODE_DONE || result.retcode == TRADE_RETCODE_PLACED)
            {
                LogMessage("买入订单执行成功，订单号: " + (string)result.order + ", 成交价格: " + DoubleToString(result.price, Digits), 1);
                // 记录订单详情
                LogOrderDetails(result.order, 2);
                // 记录下单后账户状态
                LogAccountInfo(3);
                // 记录交易历史
                RecordTradeHistory(result.order, POSITION_TYPE_BUY, result.price, Lots);
                HandleError(ERR_SUCCESS, "ExecuteBuyOrder", false); // 重置错误计数
                success = true;
            }
            else
            {
                // 订单发送失败，但OrderSend函数调用成功
                bool isRetryable = HandleError(result.retcode, "ExecuteBuyOrder");
                LogMessage("买入订单执行失败，返回代码: " + (string)result.retcode + ", 错误信息: " + ErrorDescription(result.retcode) + ", 重试次数: " + (string)retryCount, 2);
                
                // 检查是否需要重试
                if(isRetryable && retryCount < MaxRetryAttempts)
                {
                    retryCount++;
                    LogMessage("将在 " + (string)RetryDelayMs + "ms 后重试买入订单 (第" + (string)retryCount + "次)", 2);
                    Sleep(RetryDelayMs);
                    // 刷新价格
                    currentAsk = Ask;
                    currentBid = Bid;
                }
                else
                {
                    break;
                }
            }
        }
        else
        {
            // OrderSend函数调用失败
            int errorCode = GetLastError();
            bool isRetryable = HandleError(errorCode, "ExecuteBuyOrder");
            LogMessage("买入订单发送失败，错误代码: " + (string)errorCode + ", 错误信息: " + ErrorDescription(errorCode) + ", 重试次数: " + (string)retryCount, 1);
            
            // 检查是否需要重试
            if(isRetryable && retryCount < MaxRetryAttempts)
            {
                retryCount++;
                LogMessage("将在 " + (string)RetryDelayMs + "ms 后重试买入订单 (第" + (string)retryCount + "次)", 2);
                Sleep(RetryDelayMs);
                // 刷新价格
                currentAsk = Ask;
                currentBid = Bid;
            }
            else
            {
                break;
            }
        }
    }
}

//+------------------------------------------------------------------+
//| 执行卖出订单                                                     |
//+------------------------------------------------------------------+
void ExecuteSellOrder()
{
    // 检查是否可以交易
    if(!CanTrade())
    {
        LogMessage("跳过卖出订单执行，交易条件不满足", 2);
        return;
    }
    
    // 检查是否已有空头持仓或订单
    if(HasExistingPosition(POSITION_TYPE_SELL))
    {
        LogMessage("检测到已有空头持仓或订单，跳过卖出操作", 2);
        return;
    }
    
    // 获取当前市场数据
    double currentAsk = Ask;
    double currentBid = Bid;
    double spread = (Ask - Bid) / Point;
    
    // 计算止损和止盈价格
    double stopLossPrice = currentBid + StopLoss * Point;
    double takeProfitPrice = currentBid - TakeProfit * Point;
    
    LogMessage("准备执行卖出订单 - 货币对: " + Symbol() + ", 周期: " + EnumToString(Period()) + 
               ", 手数: " + DoubleToString(Lots, 2) + ", 当前价格: " + DoubleToString(currentBid, Digits) + 
               ", 点差: " + DoubleToString(spread, 0) + "点", 2);
    LogMessage("止损价格: " + DoubleToString(stopLossPrice, Digits) + 
               " (" + (string)StopLoss + "点), 止盈价格: " + DoubleToString(takeProfitPrice, Digits) + 
               " (" + (string)TakeProfit + "点)", 2);
    
    // 平仓任何多头头寸
    CloseBuyPositions();
    
    // 记录下单前账户状态
    LogAccountInfo(4);
    
    // 执行卖出订单，支持重试
    MqlTradeRequest request;
    MqlTradeResult result;
    int retryCount = 0;
    bool success = false;
    
    // 尝试执行订单，支持重试
    while(retryCount <= MaxRetryAttempts && !success)
    {
        // 初始化请求结构
        ZeroMemory(request);
        ZeroMemory(result);
        ResetLastError();
        
        request.action = TRADE_ACTION_DEAL;
        request.symbol = Symbol();
        request.volume = Lots;
        request.type = ORDER_TYPE_SELL;
        request.price = currentBid;
        request.sl = stopLossPrice;
        request.tp = takeProfitPrice;
        request.deviation = 3;
        request.magic = 12345;
        request.comment = "EngulfSignalEA卖出";
        
        // 记录详细日志
        LogMessage("尝试发送卖出订单: 品种=" + Symbol() + ", 手数=" + DoubleToString(Lots, 2) + ", 价格=" + DoubleToString(request.price, Digits), 4);
        
        if(OrderSend(request, result))
        {
            if(result.retcode == TRADE_RETCODE_DONE || result.retcode == TRADE_RETCODE_PLACED)
            {
                LogMessage("卖出订单执行成功，订单号: " + (string)result.order + ", 成交价格: " + DoubleToString(result.price, Digits), 1);
                // 记录订单详情
                LogOrderDetails(result.order, 2);
                // 记录下单后账户状态
                LogAccountInfo(3);
                // 记录交易历史
                RecordTradeHistory(result.order, POSITION_TYPE_SELL, result.price, Lots);
                HandleError(ERR_SUCCESS, "ExecuteSellOrder", false); // 重置错误计数
                success = true;
            }
            else
            {
                // 订单发送失败，但OrderSend函数调用成功
                bool isRetryable = HandleError(result.retcode, "ExecuteSellOrder");
                LogMessage("卖出订单执行失败，返回代码: " + (string)result.retcode + ", 错误信息: " + ErrorDescription(result.retcode) + ", 重试次数: " + (string)retryCount, 2);
                
                // 检查是否需要重试
                if(isRetryable && retryCount < MaxRetryAttempts)
                {
                    retryCount++;
                    LogMessage("将在 " + (string)RetryDelayMs + "ms 后重试卖出订单 (第" + (string)retryCount + "次)", 2);
                    Sleep(RetryDelayMs);
                    // 刷新价格
                    currentBid = Bid;
                    stopLossPrice = currentBid + StopLoss * Point;
                    takeProfitPrice = currentBid - TakeProfit * Point;
                }
                else
                {
                    break;
                }
            }
        }
        else
        {
            // OrderSend函数调用失败
            int errorCode = GetLastError();
            bool isRetryable = HandleError(errorCode, "ExecuteSellOrder");
            LogMessage("卖出订单发送失败，错误代码: " + (string)errorCode + ", 错误信息: " + ErrorDescription(errorCode) + ", 重试次数: " + (string)retryCount, 1);
            
            // 检查是否需要重试
            if(isRetryable && retryCount < MaxRetryAttempts)
            {
                retryCount++;
                LogMessage("将在 " + (string)RetryDelayMs + "ms 后重试卖出订单 (第" + (string)retryCount + "次)", 2);
                Sleep(RetryDelayMs);
                // 刷新价格
                currentBid = Bid;
                stopLossPrice = currentBid + StopLoss * Point;
                takeProfitPrice = currentBid - TakeProfit * Point;
            }
            else
            {
                break;
            }
        }
    }
}

//+------------------------------------------------------------------+
//| 平仓所有多头头寸                                                 |
//+------------------------------------------------------------------+
void CloseBuyPositions()
{
    // 检查是否可以交易
    if(!CanTrade())
    {
        LogMessage("跳过多头头寸平仓，交易条件不满足", 2);
        return;
    }
    
    // 检查是否有多头持仓
    if(PositionSelect(Symbol()) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
    {
        long positionTicket = PositionGetInteger(POSITION_TICKET);
        double volume = PositionGetDouble(POSITION_VOLUME);
        double openPrice = PositionGetDouble(POSITION_PRICE_OPEN);
        double currentProfit = PositionGetDouble(POSITION_PROFIT);
        
        LogMessage("准备平仓多头头寸 - 订单号: " + (string)positionTicket + ", 手数: " + DoubleToString(volume, 2) + 
                   ", 开仓价格: " + DoubleToString(openPrice, Digits) + ", 当前盈亏: " + DoubleToString(currentProfit, 2), 2);
        
        // 使用新的交易API平仓，支持重试
        MqlTradeRequest request;
        MqlTradeResult result;
        int retryCount = 0;
        bool success = false;
        
        // 尝试执行平仓，支持重试
        while(retryCount <= MaxRetryAttempts && !success)
        {
            // 初始化请求结构
            ZeroMemory(request);
            ZeroMemory(result);
            ResetLastError();
            
            request.action = TRADE_ACTION_DEAL;
            request.symbol = Symbol();
            request.volume = volume;
            request.type = ORDER_TYPE_SELL;
            request.price = Bid;
            request.deviation = 3;
            request.magic = 12345;
            request.comment = "EngulfSignalEA平仓多头";
            
            // 记录详细日志
            LogMessage("尝试多头头寸平仓: 订单号=" + (string)positionTicket + ", 手数=" + DoubleToString(volume, 2) + ", 价格=" + DoubleToString(request.price, Digits), 4);
            
            if(OrderSend(request, result))
            {
                if(result.retcode == TRADE_RETCODE_DONE || result.retcode == TRADE_RETCODE_PLACED)
                {
                    LogMessage("多头头寸平仓成功，订单号: " + (string)result.order + ", 成交价格: " + DoubleToString(result.price, Digits), 1);
                    LogMessage("平仓盈亏: " + DoubleToString(currentProfit, 2), 1);
                    // 记录平仓后账户状态
                    LogAccountInfo(3);
                    HandleError(ERR_SUCCESS, "CloseBuyPositions", false); // 重置错误计数
                    success = true;
                }
                else
                {
                    // 平仓失败，但OrderSend函数调用成功
                    bool isRetryable = HandleError(result.retcode, "CloseBuyPositions");
                    LogMessage("多头头寸平仓失败，返回代码: " + (string)result.retcode + ", 错误信息: " + ErrorDescription(result.retcode) + ", 重试次数: " + (string)retryCount, 2);
                    
                    // 检查是否需要重试
                    if(isRetryable && retryCount < MaxRetryAttempts)
                    {
                        retryCount++;
                        LogMessage("将在 " + (string)RetryDelayMs + "ms 后重试多头头寸平仓 (第" + (string)retryCount + "次)", 2);
                        Sleep(RetryDelayMs);
                    }
                    else
                    {
                        break;
                    }
                }
            }
            else
            {
                // OrderSend函数调用失败
                int errorCode = GetLastError();
                bool isRetryable = HandleError(errorCode, "CloseBuyPositions");
                LogMessage("多头头寸平仓请求失败，错误代码: " + (string)errorCode + ", 错误信息: " + ErrorDescription(errorCode) + ", 重试次数: " + (string)retryCount, 1);
                
                // 检查是否需要重试
                if(isRetryable && retryCount < MaxRetryAttempts)
                {
                    retryCount++;
                    LogMessage("将在 " + (string)RetryDelayMs + "ms 后重试多头头寸平仓 (第" + (string)retryCount + "次)", 2);
                    Sleep(RetryDelayMs);
                }
                else
                {
                    break;
                }
            }
        }
    }
}

//+------------------------------------------------------------------+
//| 平仓所有空头头寸                                                 |
//+------------------------------------------------------------------+
void CloseSellPositions()
{
    // 检查是否可以交易
    if(!CanTrade())
    {
        LogMessage("跳过空头头寸平仓，交易条件不满足", 2);
        return;
    }
    
    // 检查是否有空头持仓
    if(PositionSelect(Symbol()) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL)
    {
        long positionTicket = PositionGetInteger(POSITION_TICKET);
        double volume = PositionGetDouble(POSITION_VOLUME);
        double openPrice = PositionGetDouble(POSITION_PRICE_OPEN);
        double currentProfit = PositionGetDouble(POSITION_PROFIT);
        
        LogMessage("准备平仓空头头寸 - 订单号: " + (string)positionTicket + ", 手数: " + DoubleToString(volume, 2) + 
                   ", 开仓价格: " + DoubleToString(openPrice, Digits) + ", 当前盈亏: " + DoubleToString(currentProfit, 2), 2);
        
        // 使用新的交易API平仓，支持重试
        MqlTradeRequest request;
        MqlTradeResult result;
        int retryCount = 0;
        bool success = false;
        
        // 尝试执行平仓，支持重试
        while(retryCount <= MaxRetryAttempts && !success)
        {
            // 初始化请求结构
            ZeroMemory(request);
            ZeroMemory(result);
            ResetLastError();
            
            request.action = TRADE_ACTION_DEAL;
            request.symbol = Symbol();
            request.volume = volume;
            request.type = ORDER_TYPE_BUY;
            request.price = Ask;
            request.deviation = 3;
            request.magic = 12345;
            request.comment = "EngulfSignalEA平仓空头";
            
            // 记录详细日志
            LogMessage("尝试空头头寸平仓: 订单号=" + (string)positionTicket + ", 手数=" + DoubleToString(volume, 2) + ", 价格=" + DoubleToString(request.price, Digits), 4);
            
            if(OrderSend(request, result))
            {
                if(result.retcode == TRADE_RETCODE_DONE || result.retcode == TRADE_RETCODE_PLACED)
                {
                    LogMessage("空头头寸平仓成功，订单号: " + (string)result.order + ", 成交价格: " + DoubleToString(result.price, Digits), 1);
                    LogMessage("平仓盈亏: " + DoubleToString(currentProfit, 2), 1);
                    // 记录平仓后账户状态
                    LogAccountInfo(3);
                    HandleError(ERR_SUCCESS, "CloseSellPositions", false); // 重置错误计数
                    success = true;
                }
                else
                {
                    // 平仓失败，但OrderSend函数调用成功
                    bool isRetryable = HandleError(result.retcode, "CloseSellPositions");
                    LogMessage("空头头寸平仓失败，返回代码: " + (string)result.retcode + ", 错误信息: " + ErrorDescription(result.retcode) + ", 重试次数: " + (string)retryCount, 2);
                    
                    // 检查是否需要重试
                    if(isRetryable && retryCount < MaxRetryAttempts)
                    {
                        retryCount++;
                        LogMessage("将在 " + (string)RetryDelayMs + "ms 后重试空头头寸平仓 (第" + (string)retryCount + "次)", 2);
                        Sleep(RetryDelayMs);
                    }
                    else
                    {
                        break;
                    }
                }
            }
            else
            {
                // OrderSend函数调用失败
                int errorCode = GetLastError();
                bool isRetryable = HandleError(errorCode, "CloseSellPositions");
                LogMessage("空头头寸平仓请求失败，错误代码: " + (string)errorCode + ", 错误信息: " + ErrorDescription(errorCode) + ", 重试次数: " + (string)retryCount, 1);
                
                // 检查是否需要重试
                if(isRetryable && retryCount < MaxRetryAttempts)
                {
                    retryCount++;
                    LogMessage("将在 " + (string)RetryDelayMs + "ms 后重试空头头寸平仓 (第" + (string)retryCount + "次)", 2);
                    Sleep(RetryDelayMs);
                }
                else
                {
                    break;
                }
            }
        }
    }
}

//+------------------------------------------------------------------+
//| 应用追踪止损                                                     |
//+------------------------------------------------------------------+
void ApplyTrailingStop()
{
    // 检查是否可以交易
    if(!CanTrade())
    {
        LogMessage("跳过追踪止损检查，交易条件不满足", 3);
        return;
    }
    
    // 检查是否有持仓
    if(PositionSelect(Symbol()))
    {
        int positionType = (int)PositionGetInteger(POSITION_TYPE);
        double currentPrice = (positionType == POSITION_TYPE_BUY) ? Bid : Ask;
        double openPrice = PositionGetDouble(POSITION_PRICE_OPEN);
        double stopLoss = PositionGetDouble(POSITION_SL);
        long ticket = PositionGetInteger(POSITION_TICKET);
        double profit = PositionGetDouble(POSITION_PROFIT);
        
        LogMessage("检查追踪止损 - 持仓类型: " + (positionType == POSITION_TYPE_BUY ? "多头" : "空头") + 
                   ", 当前利润: " + DoubleToString(profit, 2), 4);
        
        // 多头持仓追踪止损
        if(positionType == POSITION_TYPE_BUY)
        {
            double newStopLoss = currentPrice - TrailingStop * Point;
            double distanceFromOpen = (currentPrice - openPrice) / Point;
            
            LogMessage("多头持仓 - 当前价格: " + DoubleToString(currentPrice, Digits) + 
                       ", 当前止损: " + DoubleToString(stopLoss, Digits) + 
                       ", 新止损: " + DoubleToString(newStopLoss, Digits) + 
                       ", 距离开仓: " + DoubleToString(distanceFromOpen, 0) + "点", 4);
            
            if(newStopLoss > stopLoss && distanceFromOpen > TrailingStop)
            {
                LogMessage("触发多头追踪止损更新条件", 3);
                UpdateStopLoss(ticket, newStopLoss, POSITION_TYPE_BUY);
            }
        }
        // 空头持仓追踪止损
        else if(positionType == POSITION_TYPE_SELL)
        {
            double newStopLoss = currentPrice + TrailingStop * Point;
            double distanceFromOpen = (openPrice - currentPrice) / Point;
            
            LogMessage("空头持仓 - 当前价格: " + DoubleToString(currentPrice, Digits) + 
                       ", 当前止损: " + DoubleToString(stopLoss, Digits) + 
                       ", 新止损: " + DoubleToString(newStopLoss, Digits) + 
                       ", 距离开仓: " + DoubleToString(distanceFromOpen, 0) + "点", 4);
            
            if(newStopLoss < stopLoss && distanceFromOpen > TrailingStop)
            {
                LogMessage("触发空头追踪止损更新条件", 3);
                UpdateStopLoss(ticket, newStopLoss, POSITION_TYPE_SELL);
            }
        }
    }
}

//+------------------------------------------------------------------+
//| 更新止损价格                                                     |
//+------------------------------------------------------------------+
bool UpdateStopLoss(long ticket, double newStopLoss, int positionType)
{
    // 更新止损，支持重试
    MqlTradeRequest request;
    MqlTradeResult result;
    int retryCount = 0;
    bool success = false;
    string positionTypeName = (positionType == POSITION_TYPE_BUY) ? "多头" : "空头";
    
    // 尝试执行止损更新，支持重试
    while(retryCount <= MaxRetryAttempts && !success)
    {
        // 初始化请求结构
        ZeroMemory(request);
        ZeroMemory(result);
        ResetLastError();
        
        request.action = TRADE_ACTION_SLTP;
        request.symbol = Symbol();
        request.position = ticket;
        request.sl = newStopLoss;
        request.tp = PositionGetDouble(POSITION_TP);
        
        // 记录详细日志
        LogMessage("尝试更新" + positionTypeName + "持仓止损: 订单号=" + (string)ticket + ", 新止损=" + DoubleToString(newStopLoss, Digits), 4);
        
        if(OrderSend(request, result))
        {
            if(result.retcode == TRADE_RETCODE_DONE || result.retcode == TRADE_RETCODE_PLACED)
            {
                LogMessage(positionTypeName + "持仓止损更新成功，订单号: " + (string)ticket, 3);
                HandleError(ERR_SUCCESS, "UpdateStopLoss", false); // 重置错误计数
                success = true;
            }
            else
            {
                // 止损更新失败，但OrderSend函数调用成功
                bool isRetryable = HandleError(result.retcode, "UpdateStopLoss");
                LogMessage(positionTypeName + "持仓止损更新失败，返回代码: " + (string)result.retcode + ", 错误信息: " + ErrorDescription(result.retcode) + ", 重试次数: " + (string)retryCount, 2);
                
                // 检查是否需要重试
                if(isRetryable && retryCount < MaxRetryAttempts)
                {
                    retryCount++;
                    LogMessage("将在 " + (string)RetryDelayMs + "ms 后重试" + positionTypeName + "持仓止损更新 (第" + (string)retryCount + "次)", 3);
                    Sleep(RetryDelayMs);
                }
                else
                {
                    break;
                }
            }
        }
        else
        {
            // OrderSend函数调用失败
            int errorCode = GetLastError();
            bool isRetryable = HandleError(errorCode, "UpdateStopLoss");
            LogMessage(positionTypeName + "持仓止损更新请求失败，错误代码: " + (string)errorCode + ", 错误信息: " + ErrorDescription(errorCode) + ", 重试次数: " + (string)retryCount, 2);
            
            // 检查是否需要重试
            if(isRetryable && retryCount < MaxRetryAttempts)
            {
                retryCount++;
                LogMessage("将在 " + (string)RetryDelayMs + "ms 后重试" + positionTypeName + "持仓止损更新 (第" + (string)retryCount + "次)", 3);
                Sleep(RetryDelayMs);
            }
            else
            {
                break;
            }
        }
    }
    
    return success;
}

//+------------------------------------------------------------------+
//| 设置止损止盈                                                     |
//+------------------------------------------------------------------+
bool SetStopLossAndTakeProfit(long ticket, int orderType, double stopLossPoints, double takeProfitPoints)
{
    // 检查是否可以交易
    if(!CanTrade())
    {
        LogMessage("跳过止损止盈设置，交易条件不满足", 2);
        return false;
    }
    
    // 计算新的止损止盈价格
    double sl = 0.0, tp = 0.0;
    double openPrice = PositionGetDouble(POSITION_PRICE_OPEN);
    
    if(orderType == ORDER_TYPE_BUY)
    {
        sl = openPrice - stopLossPoints * Point;
        tp = openPrice + takeProfitPoints * Point;
    }
    else if(orderType == ORDER_TYPE_SELL)
    {
        sl = openPrice + stopLossPoints * Point;
        tp = openPrice - takeProfitPoints * Point;
    }
    
    // 更新止损止盈，支持重试
    MqlTradeRequest request;
    MqlTradeResult result;
    int retryCount = 0;
    bool success = false;
    
    // 尝试执行止损止盈更新，支持重试
    while(retryCount <= MaxRetryAttempts && !success)
    {
        // 初始化请求结构
        ZeroMemory(request);
        ZeroMemory(result);
        ResetLastError();
        
        request.action = TRADE_ACTION_SLTP;
        request.symbol = Symbol();
        request.position = ticket;
        request.sl = sl;
        request.tp = tp;
        
        // 记录详细日志
        LogMessage("尝试设置订单止损止盈: 订单号=" + (string)ticket + ", 止损=" + DoubleToString(sl, Digits) + ", 止盈=" + DoubleToString(tp, Digits), 4);
        
        if(OrderSend(request, result))
        {
            if(result.retcode == TRADE_RETCODE_DONE || result.retcode == TRADE_RETCODE_PLACED)
            {
                LogMessage("订单止损止盈设置成功，订单号: " + (string)ticket, 3);
                HandleError(ERR_SUCCESS, "SetStopLossAndTakeProfit", false); // 重置错误计数
                success = true;
            }
            else
            {
                // 止损止盈更新失败，但OrderSend函数调用成功
                bool isRetryable = HandleError(result.retcode, "SetStopLossAndTakeProfit");
                LogMessage("订单止损止盈设置失败，返回代码: " + (string)result.retcode + ", 错误信息: " + ErrorDescription(result.retcode) + ", 重试次数: " + (string)retryCount, 2);
                
                // 检查是否需要重试
                if(isRetryable && retryCount < MaxRetryAttempts)
                {
                    retryCount++;
                    LogMessage("将在 " + (string)RetryDelayMs + "ms 后重试止损止盈设置 (第" + (string)retryCount + "次)", 3);
                    Sleep(RetryDelayMs);
                }
                else
                {
                    break;
                }
            }
        }
        else
        {
            // OrderSend函数调用失败
            int errorCode = GetLastError();
            bool isRetryable = HandleError(errorCode, "SetStopLossAndTakeProfit");
            LogMessage("订单止损止盈设置请求失败，错误代码: " + (string)errorCode + ", 错误信息: " + ErrorDescription(errorCode) + ", 重试次数: " + (string)retryCount, 2);
            
            // 检查是否需要重试
            if(isRetryable && retryCount < MaxRetryAttempts)
            {
                retryCount++;
                LogMessage("将在 " + (string)RetryDelayMs + "ms 后重试止损止盈设置 (第" + (string)retryCount + "次)", 3);
                Sleep(RetryDelayMs);
            }
            else
            {
                break;
            }
        }
    }
    
    return success;
}

//+------------------------------------------------------------------+
//| 初始化日志系统                                                   |
//+------------------------------------------------------------------+
void InitializeLogging()
{
    // 创建日志文件路径
    string timestamp = TimeToString(TimeCurrent(), TIME_DATE);
    timestamp = StringReplace(timestamp, ".", "-");
    LogFilePath = TerminalInfoString(TERMINAL_DATA_PATH) + "\\MQL5\\Files\\" + LogFileName + "_" + timestamp + ".log";
    
    LogMessage("日志系统初始化，日志文件: " + LogFilePath, 3);
    
    // 写入日志文件头部信息
    if(EnableFileLogging)
    {
        int fileHandle = FileOpen(LogFilePath, FILE_WRITE|FILE_TXT);
        if(fileHandle != INVALID_HANDLE)
        {
            FileWriteString(fileHandle, "===== EngulfSignalEA 日志 =====\n");
            FileWriteString(fileHandle, "开始时间: " + TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS) + "\n");
            FileWriteString(fileHandle, "货币对: " + Symbol() + "\n");
            FileWriteString(fileHandle, "周期: " + EnumToString(Period()) + "\n");
            FileWriteString(fileHandle, "====================================\n\n");
            FileClose(fileHandle);
        }
        else
        {
            Print("无法创建日志文件: " + LogFilePath + ", 错误代码: " + (string)GetLastError());
        }
    }
}

//+------------------------------------------------------------------+
//| 详细日志记录函数                                                 |
//+------------------------------------------------------------------+
//+------------------------------------------------------------------+
//| 错误处理函数                                                     |
//+------------------------------------------------------------------+
bool HandleError(int errorCode, string operation, bool incrementErrorCount=true)
{
    // 获取错误描述
    string errorDesc = ErrorDescription(errorCode);
    string fullError = operation + " - 错误代码: " + (string)errorCode + ", 错误信息: " + errorDesc;
    
    // 记录错误
    LogMessage(fullError, 1);
    
    // 更新错误状态
    LastErrorDescription = fullError;
    
    if(incrementErrorCount)
    {
        ErrorCount++;
        
        // 检查是否需要暂停交易
        if(ErrorCount >= MaxErrorCount)
        {
            TradingPaused = true;
            LogMessage("连续错误次数达到上限 (" + (string)MaxErrorCount + "), 交易已暂停", 1);
        }
    }
    else
    {
        // 成功操作后重置错误计数
        ErrorCount = 0;
        TradingPaused = false;
    }
    
    // 判断错误是否可恢复
    switch(errorCode)
    {
        case ERR_NO_ERROR:
        case ERR_SUCCESS:
            return true;
        
        // 可恢复的错误
        case ERR_MARKET_CLOSED:
        case ERR_INVALID_PRICE:
        case ERR_REQUOTE:
        case ERR_PRICE_CHANGED:
        case ERR_PRICE_OFF:
            LogMessage("临时错误，可能需要重试: " + errorDesc, 2);
            return false;
        
        // 不可恢复的严重错误
        case ERR_NOT_ENOUGH_MONEY:
        case ERR_INVALID_ACCOUNT:
        case ERR_INVALID_TRADE_PARAMS:
            LogMessage("严重错误，交易参数需要修正: " + errorDesc, 1);
            return false;
        
        default:
            return false;
    }
}

//+------------------------------------------------------------------+
//| 重置错误计数                                                     |
//+------------------------------------------------------------------+
void ResetErrorCount()
{
    ErrorCount = 0;
    TradingPaused = false;
    LogMessage("错误计数已重置", 3);
}

//+------------------------------------------------------------------+
//| 检查交易是否可以继续                                             |
//+------------------------------------------------------------------+
bool CanTrade()
{
    if(TradingPaused)
    {
        LogMessage("交易已暂停，原因: " + LastErrorDescription, 2);
        return false;
    }
    
    // 检查交易环境
    if(!IsTradeAllowed())
    {
        LogMessage("交易不允许，请检查交易权限和自动交易设置", 1);
        return false;
    }
    
    // 检查账户状态
    if(AccountInfoInteger(ACCOUNT_TRADE_ALLOWED) != 1)
    {
        LogMessage("账户不允许交易", 1);
        return false;
    }
    
    // 检查连接状态
    if(TerminalInfoInteger(TERMINAL_CONNECTED) != 1)
    {
        LogMessage("未连接到交易服务器", 1);
        return false;
    }
    
    return true;
}

//+------------------------------------------------------------------+
//| 日志消息函数                                                     |
//+------------------------------------------------------------------+
void LogMessage(string message, int level=3)
{
    // 检查日志级别
    if(level > LogLevel) return;
    
    // 获取日志级别描述
    string levelStr;
    switch(level)
    {
        case 1: levelStr = "[错误]"; break;
        case 2: levelStr = "[警告]"; break;
        case 3: levelStr = "[信息]"; break;
        case 4: levelStr = "[详细]"; break;
        default: levelStr = "[未知]";
    }
    
    // 记录时间戳
    string timestamp = TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS);
    string logEntry = timestamp + " " + levelStr + " " + message;
    
    // 输出到EA日志
    Print(logEntry);
    
    // 写入文件（如果启用）
    if(EnableFileLogging)
    {
        ResetLastError();
        int fileHandle = FileOpen(LogFilePath, FILE_WRITE|FILE_TXT|FILE_APPEND);
        if(fileHandle != INVALID_HANDLE)
        {
            FileWriteString(fileHandle, logEntry + "\n");
            FileClose(fileHandle);
        }
        else
        {
            // 如果无法写入文件，至少输出到EA日志
            int errorCode = GetLastError();
            Print("无法写入日志文件: " + LogFilePath + ", 错误代码: " + (string)errorCode + ", " + ErrorDescription(errorCode));
        }
    }
}

//+------------------------------------------------------------------+
//| 记录账户信息                                                     |
//+------------------------------------------------------------------+
void LogAccountInfo(int level=3)
{
    // 检查日志级别
    if(level > LogLevel) return;
    
    // 获取账户信息
    string accountName = AccountInfoString(ACCOUNT_NAME);
    double balance = AccountInfoDouble(ACCOUNT_BALANCE);
    double equity = AccountInfoDouble(ACCOUNT_EQUITY);
    double margin = AccountInfoDouble(ACCOUNT_MARGIN);
    double freeMargin = AccountInfoDouble(ACCOUNT_FREEMARGIN);
    double profit = AccountInfoDouble(ACCOUNT_PROFIT);
    int positions = AccountInfoInteger(ACCOUNT_POSITIONS);
    
    // 记录账户信息
    LogMessage("账户信息 - 名称: " + accountName + ", 余额: " + DoubleToString(balance, 2) + ", 净值: " + DoubleToString(equity, 2), level);
    LogMessage("保证金: " + DoubleToString(margin, 2) + ", 可用保证金: " + DoubleToString(freeMargin, 2) + ", 总盈亏: " + DoubleToString(profit, 2), level);
    LogMessage("当前持仓数: " + (string)positions, level);
}

//+------------------------------------------------------------------+
//| 检查是否存在相同方向的持仓或未成交订单                           |
//+------------------------------------------------------------------+
bool HasExistingPosition(int positionType)
{
    // 检查是否有相同方向的持仓
    if(PositionSelect(Symbol()))
    {
        int currentPositionType = (int)PositionGetInteger(POSITION_TYPE);
        if(currentPositionType == positionType)
        {
            return true;
        }
    }
    
    // 检查是否有未成交的相同方向订单
    for(int i = 0; i < OrdersTotal(); i++)
    {
        if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
        {
            int orderType = OrderType();
            // 将订单类型转换为对应的持仓类型进行比较
            int mappedOrderType = (orderType == OP_BUY) ? POSITION_TYPE_BUY : 
                                  (orderType == OP_SELL) ? POSITION_TYPE_SELL : -1;
            
            if(mappedOrderType == positionType && OrderSymbol() == Symbol())
            {
                return true;
            }
        }
    }
    
    return false;
}

//+------------------------------------------------------------------+
//| 记录交易历史                                                     |
//+------------------------------------------------------------------+
void RecordTradeHistory(long orderTicket, int positionType, double price, double volume)
{
    // 记录交易历史信息，用于后续的交易统计和分析
    string tradeType = (positionType == POSITION_TYPE_BUY) ? "多头" : "空头";
    LogMessage("记录交易历史: 订单号=" + (string)orderTicket + ", 类型=" + tradeType + ", 价格=" + DoubleToString(price, Digits) + ", 手数=" + DoubleToString(volume, 2), 4);
    
    // 这里可以扩展为将交易历史保存到文件或数据库中
    // 为后续的交易绩效统计功能做准备
}

//+------------------------------------------------------------------+
//| 记录订单详情                                                     |
//+------------------------------------------------------------------+
void LogOrderDetails(long orderTicket, int level=2)
{
    // 检查日志级别
    if(level > LogLevel) return;
    
    // 尝试获取订单详情
    if(OrderSelect(orderTicket, SELECT_BY_TICKET))
    {
        string orderType = (OrderType() == OP_BUY) ? "买入" : "卖出";
        double volume = OrderLots();
        double price = OrderOpenPrice();
        double sl = OrderStopLoss();
        double tp = OrderTakeProfit();
        datetime openTime = OrderOpenTime();
        string comment = OrderComment();
        
        LogMessage("订单详情 - 订单号: " + (string)orderTicket + ", 类型: " + orderType + ", 手数: " + DoubleToString(volume, 2), level);
        LogMessage("开仓价格: " + DoubleToString(price, Digits) + ", 止损: " + ((sl == 0) ? "未设置" : DoubleToString(sl, Digits)) + ", 止盈: " + ((tp == 0) ? "未设置" : DoubleToString(tp, Digits)), level);
        LogMessage("开仓时间: " + TimeToString(openTime, TIME_DATE|TIME_SECONDS) + ", 备注: " + comment, level);
    }
    else
    {
        LogMessage("无法获取订单详情，订单号: " + (string)orderTicket + ", 错误代码: " + (string)GetLastError(), 1);
    }
}

//+------------------------------------------------------------------+
//| 更新交易统计数据                                                 |
//+------------------------------------------------------------------+
void UpdateTradingStatistics(double tradeProfit)
{
    if(!EnableStatistics) return;
    
    // 更新交易计数
    stats.totalTrades++;
    stats.lastTradeTime = TimeCurrent();
    
    // 更新盈亏统计
    if(tradeProfit > 0)
    {
        stats.winningTrades++;
        stats.grossProfit += tradeProfit;
        
        // 更新最佳交易记录
        if(tradeProfit > stats.bestTrade)
        {
            stats.bestTrade = tradeProfit;
        }
    }
    else if(tradeProfit < 0)
    {
        stats.losingTrades++;
        stats.grossLoss += MathAbs(tradeProfit);
        
        // 更新最差交易记录
        if(tradeProfit < stats.worstTrade)
        {
            stats.worstTrade = tradeProfit;
        }
    }
    else
    {
        stats.breakEvenTrades++;
    }
    
    // 更新净值记录
    double currentEquity = AccountInfoDouble(ACCOUNT_EQUITY);
    if(currentEquity > stats.equityHigh)
    {
        stats.equityHigh = currentEquity;
    }
    if(currentEquity < stats.equityLow)
    {
        stats.equityLow = currentEquity;
    }
    
    // 计算最大回撤
    double drawdown = stats.equityHigh - currentEquity;
    if(drawdown > stats.maxDrawdown)
    {
        stats.maxDrawdown = drawdown;
        stats.maxDrawdownPercent = (drawdown / stats.equityHigh) * 100.0;
    }
    
    // 更新统计指标
    UpdateStatisticsMetrics();
    
    LogMessage("交易统计更新 - 交易ID: " + (string)stats.totalTrades + ", 盈亏: " + DoubleToString(tradeProfit, 2), 4);
}

//+------------------------------------------------------------------+
//| 更新统计指标                                                     |
//+------------------------------------------------------------------+
void UpdateStatisticsMetrics()
{
    // 计算胜率
    if(stats.totalTrades > 0)
    {
        stats.winRate = (double)stats.winningTrades / stats.totalTrades * 100.0;
    }
    
    // 计算平均盈利
    if(stats.winningTrades > 0)
    {
        stats.averageProfit = stats.grossProfit / stats.winningTrades;
    }
    
    // 计算平均亏损
    if(stats.losingTrades > 0)
    {
        stats.averageLoss = stats.grossLoss / stats.losingTrades;
    }
    
    // 计算盈利因子
    if(stats.grossLoss > 0)
    {
        stats.profitFactor = stats.grossProfit / stats.grossLoss;
    }
}

//+------------------------------------------------------------------+
//| 生成交易报告                                                     |
//+------------------------------------------------------------------+
void GenerateTradingReport()
{
    if(!EnableStatistics) return;
    
    LogMessage("===== 交易绩效报告 =====", 3);
    LogMessage("报告生成时间: " + TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS), 3);
    LogMessage("总交易次数: " + (string)stats.totalTrades, 3);
    LogMessage("盈利交易: " + (string)stats.winningTrades + " (" + DoubleToString(stats.winRate, 2) + "%)", 3);
    LogMessage("亏损交易: " + (string)stats.losingTrades, 3);
    LogMessage("持平交易: " + (string)stats.breakEvenTrades, 3);
    LogMessage("总盈利: " + DoubleToString(stats.grossProfit, 2), 3);
    LogMessage("总亏损: " + DoubleToString(stats.grossLoss, 2), 3);
    LogMessage("净利润: " + DoubleToString(stats.grossProfit - stats.grossLoss, 2), 3);
    LogMessage("盈利因子: " + DoubleToString(stats.profitFactor, 2), 3);
    LogMessage("平均盈利: " + DoubleToString(stats.averageProfit, 2), 3);
    LogMessage("平均亏损: " + DoubleToString(stats.averageLoss, 2), 3);
    LogMessage("最佳交易: " + DoubleToString(stats.bestTrade, 2), 3);
    LogMessage("最差交易: " + DoubleToString(stats.worstTrade, 2), 3);
    LogMessage("最大回撤: " + DoubleToString(stats.maxDrawdown, 2) + " (" + DoubleToString(stats.maxDrawdownPercent, 2) + "%)", 3);
    LogMessage("初始余额: " + DoubleToString(stats.initialBalance, 2), 3);
    LogMessage("当前余额: " + DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE), 2), 3);
    LogMessage("最高净值: " + DoubleToString(stats.equityHigh, 2), 3);
    LogMessage("最低净值: " + DoubleToString(stats.equityLow, 2), 3);
    LogMessage("=======================", 3);
    
    // 保存报告到文件
    SaveReportToFile();
    
    // 生成HTML报告
    if(GenerateHTMLReport)
    {
        GenerateHTMLReport();
    }
}

//+------------------------------------------------------------------+
//| 保存报告到文件                                                   |
//+------------------------------------------------------------------+
void SaveReportToFile()
{
    string timestamp = TimeToString(TimeCurrent(), TIME_DATE);
    timestamp = StringReplace(timestamp, ".", "-");
    string reportPath = TerminalInfoString(TERMINAL_DATA_PATH) + "\\MQL5\\Files\\EngulfSignalReport_" + timestamp + ".txt";
    
    int fileHandle = FileOpen(reportPath, FILE_WRITE|FILE_TXT);
    if(fileHandle != INVALID_HANDLE)
    {
        // 写入报告头部
        FileWriteString(fileHandle, "===== EngulfSignalEA 交易绩效报告 =====\n");
        FileWriteString(fileHandle, "报告生成时间: " + TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS) + "\n");
        FileWriteString(fileHandle, "货币对: " + Symbol() + "\n");
        FileWriteString(fileHandle, "周期: " + EnumToString(Period()) + "\n");
        FileWriteString(fileHandle, "====================================\n\n");
        
        // 写入统计数据
        FileWriteString(fileHandle, "交易统计:\n");
        FileWriteString(fileHandle, "总交易次数: " + (string)stats.totalTrades + "\n");
        FileWriteString(fileHandle, "盈利交易: " + (string)stats.winningTrades + " (" + DoubleToString(stats.winRate, 2) + "%)\n");
        FileWriteString(fileHandle, "亏损交易: " + (string)stats.losingTrades + "\n");
        FileWriteString(fileHandle, "持平交易: " + (string)stats.breakEvenTrades + "\n");
        FileWriteString(fileHandle, "\n盈亏统计:\n");
        FileWriteString(fileHandle, "总盈利: " + DoubleToString(stats.grossProfit, 2) + "\n");
        FileWriteString(fileHandle, "总亏损: " + DoubleToString(stats.grossLoss, 2) + "\n");
        FileWriteString(fileHandle, "净利润: " + DoubleToString(stats.grossProfit - stats.grossLoss, 2) + "\n");
        FileWriteString(fileHandle, "盈利因子: " + DoubleToString(stats.profitFactor, 2) + "\n");
        FileWriteString(fileHandle, "平均盈利: " + DoubleToString(stats.averageProfit, 2) + "\n");
        FileWriteString(fileHandle, "平均亏损: " + DoubleToString(stats.averageLoss, 2) + "\n");
        FileWriteString(fileHandle, "\n风险统计:\n");
        FileWriteString(fileHandle, "最大回撤: " + DoubleToString(stats.maxDrawdown, 2) + " (" + DoubleToString(stats.maxDrawdownPercent, 2) + "%)\n");
        FileWriteString(fileHandle, "最佳交易: " + DoubleToString(stats.bestTrade, 2) + "\n");
        FileWriteString(fileHandle, "最差交易: " + DoubleToString(stats.worstTrade, 2) + "\n");
        FileWriteString(fileHandle, "\n账户信息:\n");
        FileWriteString(fileHandle, "初始余额: " + DoubleToString(stats.initialBalance, 2) + "\n");
        FileWriteString(fileHandle, "当前余额: " + DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE), 2) + "\n");
        FileWriteString(fileHandle, "最高净值: " + DoubleToString(stats.equityHigh, 2) + "\n");
        FileWriteString(fileHandle, "最低净值: " + DoubleToString(stats.equityLow, 2) + "\n");
        
        FileClose(fileHandle);
        LogMessage("交易报告已保存: " + reportPath, 3);
    }
    else
    {
        LogMessage("无法创建交易报告文件: " + reportPath + ", 错误代码: " + (string)GetLastError(), 1);
    }
}

//+------------------------------------------------------------------+
//| 生成HTML报告                                                     |
//+------------------------------------------------------------------+
void GenerateHTMLReport()
{
    string timestamp = TimeToString(TimeCurrent(), TIME_DATE);
    timestamp = StringReplace(timestamp, ".", "-");
    string htmlPath = TerminalInfoString(TERMINAL_DATA_PATH) + "\\MQL5\\Files\\EngulfSignalReport_" + timestamp + ".html";
    
    int fileHandle = FileOpen(htmlPath, FILE_WRITE|FILE_TXT);
    if(fileHandle != INVALID_HANDLE)
    {
        // HTML头部
        FileWriteString(fileHandle, "<!DOCTYPE html>\n<html>\n<head>\n");
        FileWriteString(fileHandle, "<title>EngulfSignalEA 交易绩效报告</title>\n");
        FileWriteString(fileHandle, "<style>\n");
        FileWriteString(fileHandle, "body { font-family: Arial, sans-serif; margin: 20px; }\n");
        FileWriteString(fileHandle, "h1, h2 { color: #2c3e50; }\n");
        FileWriteString(fileHandle, ".header { background-color: #f8f9fa; padding: 10px; border-radius: 5px; }\n");
        FileWriteString(fileHandle, ".stats { display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px; }\n");
        FileWriteString(fileHandle, ".card { background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 5px; padding: 15px; flex: 1 1 300px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }\n");
        FileWriteString(fileHandle, ".positive { color: #27ae60; }\n");
        FileWriteString(fileHandle, ".negative { color: #e74c3c; }\n");
        FileWriteString(fileHandle, "table { width: 100%; border-collapse: collapse; margin-top: 10px; }\n");
        FileWriteString(fileHandle, "th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }\n");
        FileWriteString(fileHandle, "th { background-color: #f2f2f2; }\n");
        FileWriteString(fileHandle, "</style>\n");
        FileWriteString(fileHandle, "</head>\n<body>\n");
        
        // 报告标题
        FileWriteString(fileHandle, "<div class='header'>\n<h1>EngulfSignalEA 交易绩效报告</h1>\n");
        FileWriteString(fileHandle, "<p>报告生成时间: " + TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS) + "</p>\n");
        FileWriteString(fileHandle, "<p>货币对: " + Symbol() + " | 周期: " + EnumToString(Period()) + "</p>\n");
        FileWriteString(fileHandle, "</div>\n");
        
        // 统计卡片
        FileWriteString(fileHandle, "<div class='stats'>\n");
        
        // 交易计数卡片
        FileWriteString(fileHandle, "<div class='card'>\n<h2>交易计数</h2>\n<table>\n");
        FileWriteString(fileHandle, "<tr><th>项目</th><th>数值</th></tr>\n");
        FileWriteString(fileHandle, "<tr><td>总交易次数</td><td>" + (string)stats.totalTrades + "</td></tr>\n");
        FileWriteString(fileHandle, "<tr><td>盈利交易</td><td class='positive'>" + (string)stats.winningTrades + "</td></tr>\n");
        FileWriteString(fileHandle, "<tr><td>亏损交易</td><td class='negative'>" + (string)stats.losingTrades + "</td></tr>\n");
        FileWriteString(fileHandle, "<tr><td>持平交易</td><td>" + (string)stats.breakEvenTrades + "</td></tr>\n");
        FileWriteString(fileHandle, "<tr><td>胜率</td><td>" + DoubleToString(stats.winRate, 2) + "%</td></tr>\n");
        FileWriteString(fileHandle, "</table>\n</div>\n");
        
        // 盈亏统计卡片
        FileWriteString(fileHandle, "<div class='card'>\n<h2>盈亏统计</h2>\n<table>\n");
        FileWriteString(fileHandle, "<tr><th>项目</th><th>数值</th></tr>\n");
        FileWriteString(fileHandle, "<tr><td>总盈利</td><td class='positive'>" + DoubleToString(stats.grossProfit, 2) + "</td></tr>\n");
        FileWriteString(fileHandle, "<tr><td>总亏损</td><td class='negative'>" + DoubleToString(stats.grossLoss, 2) + "</td></tr>\n");
        FileWriteString(fileHandle, "<tr><td>净利润</td><td class='" + ((stats.grossProfit - stats.grossLoss) >= 0 ? "positive">" : "negative">") + DoubleToString(stats.grossProfit - stats.grossLoss, 2) + "</td></tr>\n");
        FileWriteString(fileHandle, "<tr><td>盈利因子</td><td>" + DoubleToString(stats.profitFactor, 2) + "</td></tr>\n");
        FileWriteString(fileHandle, "<tr><td>平均盈利</td><td class='positive'>" + DoubleToString(stats.averageProfit, 2) + "</td></tr>\n");
        FileWriteString(fileHandle, "<tr><td>平均亏损</td><td class='negative'>" + DoubleToString(stats.averageLoss, 2) + "</td></tr>\n");
        FileWriteString(fileHandle, "</table>\n</div>\n");
        
        // 风险统计卡片
        FileWriteString(fileHandle, "<div class='card'>\n<h2>风险统计</h2>\n<table>\n");
        FileWriteString(fileHandle, "<tr><th>项目</th><th>数值</th></tr>\n");
        FileWriteString(fileHandle, "<tr><td>最大回撤</td><td class='negative'>" + DoubleToString(stats.maxDrawdown, 2) + " (" + DoubleToString(stats.maxDrawdownPercent, 2) + "%)</td></tr>\n");
        FileWriteString(fileHandle, "<tr><td>最佳交易</td><td class='positive'>" + DoubleToString(stats.bestTrade, 2) + "</td></tr>\n");
        FileWriteString(fileHandle, "<tr><td>最差交易</td><td class='negative'>" + DoubleToString(stats.worstTrade, 2) + "</td></tr>\n");
        FileWriteString(fileHandle, "</table>\n</div>\n");
        
        // 账户信息卡片
        FileWriteString(fileHandle, "<div class='card'>\n<h2>账户信息</h2>\n<table>\n");
        FileWriteString(fileHandle, "<tr><th>项目</th><th>数值</th></tr>\n");
        FileWriteString(fileHandle, "<tr><td>初始余额</td><td>" + DoubleToString(stats.initialBalance, 2) + "</td></tr>\n");
        FileWriteString(fileHandle, "<tr><td>当前余额</td><td>" + DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE), 2) + "</td></tr>\n");
        FileWriteString(fileHandle, "<tr><td>最高净值</td><td class='positive'>" + DoubleToString(stats.equityHigh, 2) + "</td></tr>\n");
        FileWriteString(fileHandle, "<tr><td>最低净值</td><td class='negative'>" + DoubleToString(stats.equityLow, 2) + "</td></tr>\n");
        FileWriteString(fileHandle, "</table>\n</div>\n");
        
        FileWriteString(fileHandle, "</div>\n");
        FileWriteString(fileHandle, "</body>\n</html>");
        
        FileClose(fileHandle);
        LogMessage("HTML交易报告已生成: " + htmlPath, 3);
    }
    else
    {
        LogMessage("无法创建HTML报告文件: " + htmlPath + ", 错误代码: " + (string)GetLastError(), 1);
    }
}

//+------------------------------------------------------------------+
//| 计算动态交易手数                                                 |
//+------------------------------------------------------------------+
double CalculateLotSize()
{
    // 更新账户价值
    accountValue = AccountInfoDouble(ACCOUNT_EQUITY);
    double lotSize = Lots; // 默认使用输入的手数
    
    if(UseDynamicLotSize)
    {
        // 获取最小交易量和交易量步长
        double minLot = SymbolInfoDouble(Symbol(), SYMBOL_VOLUME_MIN);
        double lotStep = SymbolInfoDouble(Symbol(), SYMBOL_VOLUME_STEP);
        
        // 根据风险计算类型计算手数
        if(RiskCalculationType == 0) // 基于止损点数计算
        {
            // 确保止损点数有效
            if(StopLoss > 0)
            {
                // 计算每手止损价值
                double pointValue = SymbolInfoDouble(Symbol(), SYMBOL_TRADE_TICK_VALUE);
                double pointSize = SymbolInfoDouble(Symbol(), SYMBOL_POINT);
                double stopLossValuePerLot = StopLoss * pointValue * pointSize;
                
                // 如果点价值为0（某些交叉盘），使用替代计算方法
                if(stopLossValuePerLot <= 0)
                {
                    LogMessage("无法计算止损价值，使用默认手数", 2);
                    return(AdjustLotSize(lotSize, minLot, lotStep));
                }
                
                // 根据账户价值和风险百分比计算手数
                double riskAmount = accountValue * (RiskPerTrade / 100.0);
                lotSize = riskAmount / stopLossValuePerLot;
                
                LogMessage("基于止损点数的手数计算: 账户价值=" + DoubleToString(accountValue, 2) + 
                          ", 风险金额=" + DoubleToString(riskAmount, 2) + ", 每手止损价值=" + 
                          DoubleToString(stopLossValuePerLot, 2), 4);
            }
        }
        else if(RiskCalculationType == 1) // 基于固定风险金额计算
        {
            // 使用固定风险金额
            double riskAmount = FixedRiskAmount;
            
            // 计算每手价值（简化版，使用100点为基准）
            double pointValue = SymbolInfoDouble(Symbol(), SYMBOL_TRADE_TICK_VALUE);
            double pointSize = SymbolInfoDouble(Symbol(), SYMBOL_POINT);
            double valuePerLot = 100 * pointValue * pointSize;
            
            if(valuePerLot > 0)
            {
                lotSize = riskAmount / valuePerLot;
                
                LogMessage("基于固定风险的手数计算: 风险金额=" + DoubleToString(riskAmount, 2) + 
                          ", 每手价值=" + DoubleToString(valuePerLot, 2), 4);
            }
        }
        
        // 调整手数以符合交易规则
        lotSize = AdjustLotSize(lotSize, minLot, lotStep);
    }
    
    LogMessage("最终计算手数: " + DoubleToString(lotSize, 2), 3);
    return(lotSize);
}

//+------------------------------------------------------------------+
//| 调整手数以符合交易规则                                           |
//+------------------------------------------------------------------+
double AdjustLotSize(double calculatedLot, double minLot, double lotStep)
{
    // 确保不小于最小手数
    if(calculatedLot < minLot)
    {
        LogMessage("计算手数小于最小手数，调整为: " + DoubleToString(minLot, 2), 3);
        return(minLot);
    }
    
    // 确保不大于最大手数
    if(calculatedLot > MaxLotSize)
    {
        LogMessage("计算手数大于最大手数，调整为: " + DoubleToString(MaxLotSize, 2), 3);
        return(MaxLotSize);
    }
    
    // 按照步长调整手数
    calculatedLot = NormalizeDouble(MathRound(calculatedLot / lotStep) * lotStep, 2);
    
    return(calculatedLot);
}

//+------------------------------------------------------------------+
//| 更新账户价值                                                     |
//+------------------------------------------------------------------+
void UpdateAccountValue()
{
    double newEquity = AccountInfoDouble(ACCOUNT_EQUITY);
    
    // 检查账户价值变化
    if(MathAbs(newEquity - accountValue) > accountValue * 0.01) // 如果变化超过1%
    {
        accountValue = newEquity;
        LogMessage("账户价值更新: " + DoubleToString(accountValue, 2), 4);
    }
}
