//+------------------------------------------------------------------+
//|                     EngulfSignalEA.mq5                           |
//|                     吞噬形态信号EA                                 |
//+------------------------------------------------------------------+
//| 功能说明：
//| 本EA基于K线形态（阳线买入，阴线卖出）进行交易，具有完整的交易统计和报告功能。
//| 最新版本新增了基于账户价值的动态手数管理功能，可以根据账户余额自动调整交易手数。
//|
//| 资金管理功能说明：
//| 1. 动态手数计算：根据账户净值和设定的风险参数自动计算最优交易手数
//| 2. 风险控制：通过设置每笔交易的风险百分比或固定风险金额来控制亏损
//| 3. 手数限制：可以设定最小和最大交易手数，避免过大或过小的交易量
//| 4. 多种风险计算模式：支持基于止损点数和固定风险金额两种计算方式
//|
//| 使用方法：
//| 1. 在EA参数中开启"UseDynamicLotSize"选项启用动态手数
//| 2. 设置"RiskPerTrade"参数（每笔交易的风险百分比）或"FixedRiskAmount"（固定风险金额）
//| 3. 选择合适的"RiskCalculationType"计算方式（0-基于止损点数，1-基于固定风险）
//| 4. 根据需要调整"MinLotSize"和"MaxLotSize"限制手数范围
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

// 交易量过滤参数
input bool UseVolumeFilter = true;       // 启用交易量过滤
input double VolumeMultiplier = 1.5;     // 交易量倍数阈值
input int VolumePeriod = 20;             // 计算平均交易量的周期

// 趋势过滤参数
input bool UseTrendFilter = true;        // 启用趋势过滤
input int TrendPeriod = 50;              // 趋势检测周期(移动平均线周期)
input int TrendConfirmationPeriod = 20;  // 趋势确认周期(较短移动平均线)

// 吞没形态参数
input double MinEngulfRatio = 0.8;       // 最小吞没比例 (前一根K线的百分比)
input bool AllowPartialEngulf = false;   // 允许部分吞没 (不完全覆盖前一根K线)
input int MinBodySize = 1;               // 最小K线实体大小 (点数)

// 交易时间参数
input bool UseTimeFilter = false;        // 使用交易时间过滤器
input int TradingStartHour = 0;          // 开始交易时间（小时）
input int TradingEndHour = 24;           // 结束交易时间（小时）

// 市场自适应参数
input bool UseAdaptiveParameters = false; // 使用自适应参数
input int VolatilityPeriod = 20;         // 波动率计算周期
input double VolatilityFactor = 1.5;     // 波动率因子

// 信号控制参数
input bool UseSignalFrequencyControl = true; // 使用信号频率控制
input int MinSignalInterval = 30;         // 最小信号间隔 (分钟)
input double MinSignalQualityScore = 0.6; // 最小信号质量评分 (0-1)

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

// 信号控制变量
datetime g_lastBuySignalTime = 0;       // 上次买入信号时间
datetime g_lastSellSignalTime = 0;      // 上次卖出信号时间

//+------------------------------------------------------------------+
//| 计算信号质量评分                                                 |
//| 参数说明:                                                        |
//|   isBullish    - 是否为看涨信号                                  |
//|   prevVolume   - 前一根K线的交易量                              |
//|   avgVolume    - 平均交易量                                      |
//|   trendDirection - 趋势方向 (1:上涨, -1:下跌, 0:横盘)            |
//|   volatility   - 当前市场波动率                                  |
//|   engulfRatio  - 吞没形态的相对大小比例                          |
//| 返回值:                                                          |
//|   信号质量评分 (0.0-1.0)，分数越高信号质量越好                    |
//+------------------------------------------------------------------+
double CalculateSignalQuality(bool isBullish, double prevVolume, double avgVolume, int trendDirection, double volatility, double engulfRatio)
{
    double score = 0.5; // 基础分数，所有信号起始评分
    
    // 交易量评分 (0-0.2) - 交易量高于平均水平的信号更可靠
    double volumeScore = MathMin(0.2, (prevVolume/avgVolume) * 0.1);
    score += volumeScore;
    
    // 趋势方向评分 (0-0.3) - 与趋势同向的信号更可靠
    if(isBullish && trendDirection == 1) score += 0.3; // 看涨信号且上涨趋势
    else if(!isBullish && trendDirection == -1) score += 0.3; // 看跌信号且下跌趋势
    else if(trendDirection == 0) score += 0.1; // 横盘趋势中信号强度中等
    
    // 吞没比例评分 (0-0.2) - 吞没比例越大，信号强度越高
    double engulfScore = MathMin(0.2, (engulfRatio-1.0) * 0.1);
    score += engulfScore;
    
    // 波动率评分 (0-0.1) - 市场波动率接近设定阈值时，信号更可靠
    double volatilityFactor = 0.1 - MathAbs(volatility - VolatilityFactor) * 0.05;
    score += MathMax(0.0, volatilityFactor);
    
    // 确保评分在合理范围内 (0.0-1.0)
    return MathMin(1.0, MathMax(0.0, score));
}

//+------------------------------------------------------------------+
//| 检查信号频率控制                                                 |
//| 功能: 防止在短时间内产生过多交易信号，减少噪音交易                 |
//| 参数说明:                                                        |
//|   isBuySignal - 是否为买入信号                                    |
//| 返回值:                                                          |
//|   true  - 通过频率检查，可以执行交易                              |
//|   false - 未通过频率检查，跳过此次交易                            |
//+------------------------------------------------------------------+
bool CheckSignalFrequency(bool isBuySignal)
{
    // 如果未启用信号频率控制，直接返回通过
    if(!UseSignalFrequencyControl) return true;
    
    // 根据信号类型获取上次信号时间
    datetime lastSignalTime = (isBuySignal ? g_lastBuySignalTime : g_lastSellSignalTime);
    int minutesSinceLastSignal = (TimeCurrent() - lastSignalTime) / 60;
    
    // 检查距离上次信号的时间是否满足最小间隔要求
    if(minutesSinceLastSignal < MinSignalInterval)
    {
        LogMessage("信号频率控制：上次信号后仅" + (string)minutesSinceLastSignal + "分钟，需等待至少" + (string)MinSignalInterval + "分钟", 2);
        return false;
    }
    
    // 更新最后信号时间，记录此次信号
    if(isBuySignal)
        g_lastBuySignalTime = TimeCurrent();
    else
        g_lastSellSignalTime = TimeCurrent();
    
    return true;
}

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
    LogMessage("EA参数设置 - 止损: ", (string)StopLoss, ", 止盈: ", (string)TakeProfit, ", 手数: ", DoubleToString(Lots, 2), 3);
    LogMessage("追踪止损设置 - 启用: ", (string)UseTrailingStop, ", 点数: ", (string)TrailingStop, 3);
    
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
    LogMessage("账户价值初始化: ", DoubleToString(accountValue, 2), 3);
    
    // 如果启用动态手数，计算初始手数
    if(UseDynamicLotSize)
    {
        double calculatedLot = CalculateLotSize();
        LogMessage("动态手数计算: ", DoubleToString(calculatedLot, 2), 3);
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
    LogMessage("EngulfSignalEA去初始化，原因: ", (string)reason);
}

//+------------------------------------------------------------------+
//| EA主函数                                                        |
//+------------------------------------------------------------------+
void OnTick()
{
    // 更新账户价值（用于动态手数计算）
    UpdateAccountValue();
    
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
//| 计算平均交易量                                                    |
//+------------------------------------------------------------------+
double CalculateAverageVolume(int period)
{
    double sumVolume = 0.0;
    int availableBars = MathMin(Bars, period);
    
    // 计算指定周期内的平均交易量
    for(int i = 1; i <= availableBars; i++)
    {
        sumVolume += Volume[i];
    }
    
    return sumVolume / availableBars;
}

//+------------------------------------------------------------------+
//| 计算简单移动平均线                                                |
//+------------------------------------------------------------------+
double CalculateSMA(int period)
{
    double sumClose = 0.0;
    int availableBars = MathMin(Bars, period);
    
    // 计算指定周期内的简单移动平均线
    for(int i = 1; i <= availableBars; i++)
    {
        sumClose += Close[i];
    }
    
    return sumClose / availableBars;
}

//+------------------------------------------------------------------+
//| 检测趋势方向                                                    |
//+------------------------------------------------------------------+
int DetectTrend()
{
    // 计算两条不同周期的移动平均线
    double longSMA = CalculateSMA(TrendPeriod);
    double shortSMA = CalculateSMA(TrendConfirmationPeriod);
    
    // 计算移动平均线的方向变化
    double longSMAPrev = CalculateSMA(TrendPeriod + 1);
    double shortSMAPrev = CalculateSMA(TrendConfirmationPeriod + 1);
    
    LogMessage("趋势分析: 长期SMA=" + DoubleToString(longSMA, Digits) + ", 短期SMA=" + DoubleToString(shortSMA, Digits), 3);
    
    // 确定趋势方向
    // 1 = 上涨趋势, -1 = 下跌趋势, 0 = 横盘
    if(shortSMA > longSMA && shortSMAPrev > longSMAPrev)
    {
        return 1; // 上涨趋势
    }
    else if(shortSMA < longSMA && shortSMAPrev < longSMAPrev)
    {
        return -1; // 下跌趋势
    }
    else
    {
        return 0; // 横盘
    }
}

//+------------------------------------------------------------------+
//| 分析K线信号 - 实现吞没形态识别与多维度过滤机制                  |
//| 功能: 检测吞没形态交易信号，应用多种过滤机制，并执行相应的交易操作   |
//| 核心流程:                                                        |
//|   1. 数据量检查 - 确保有足够K线数据进行分析                       |
//|   2. 时间过滤 - 检查是否在设定的交易时间范围内                    |
//|   3. 获取K线数据 - 收集前前K线和前K线的OHLCV数据                  |
//|   4. 交易量过滤 - 确保信号有足够的交易量支持                      |
//|   5. 趋势过滤 - 确定当前市场趋势方向                              |
//|   6. 吞没形态识别 - 检测看涨或看跌吞没形态，并考虑实体大小和比例    |
//|   7. 波动率计算 - 根据市场波动率调整信号敏感度                      |
//|   8. 信号质量评分 - 综合评估信号质量                              |
//|   9. 信号频率控制 - 防止在短时间内产生过多交易                      |
//| 10. 执行交易操作 - 买入或卖出操作                                |
//+------------------------------------------------------------------+
void AnalyzeSignal()
{
    // 确保有足够的K线数据进行吞没形态分析和趋势检测
    int requiredBars = MathMax(3, MathMax(MathMax(VolumePeriod + 1, TrendPeriod + 1), VolatilityPeriod + 1));
    if(Bars < requiredBars)
    {
        LogMessage("K线数据不足，需要至少" + (string)requiredBars + "根K线，当前仅有" + (string)Bars + "根", 2);
        return;
    }
    
    // 交易时间过滤检查
    if(UseTimeFilter)
    {
        datetime now = TimeLocal();
        int currentHour = TimeHour(now);
        if(currentHour < TradingStartHour || currentHour >= TradingEndHour)
        {
            LogMessage("当前时间不在交易时间范围内，跳过信号分析", 3);
            return;
        }
    }
    
    // 获取当前K线和前一根K线的数据
    // 使用[2]表示前前一根K线(已完成)，[1]表示前一根K线(已完成)，[0]表示当前K线(可能未完成)
    double prevPrevOpen = Open[2];
    double prevPrevClose = Close[2];
    double prevPrevHigh = High[2];
    double prevPrevLow = Low[2];
    
    double prevOpen = Open[1];
    double prevClose = Close[1];
    double prevHigh = High[1];
    double prevLow = Low[1];
    long prevVolume = Volume[1]; // 获取前一根K线的交易量
    
    datetime prevTime = Time[1];
    
    LogMessage("分析K线信号 (吞没形态识别) - 时间: " + TimeToString(prevTime, TIME_DATE|TIME_MINUTES), 3);
    
    // 交易量过滤检查
    bool volumeCondition = true;
    if(UseVolumeFilter)
    {
        double avgVolume = CalculateAverageVolume(VolumePeriod);
        volumeCondition = (prevVolume >= avgVolume * VolumeMultiplier);
        
        LogMessage("交易量检查: 当前=" + IntegerToString(prevVolume) + ", 平均=" + DoubleToString(avgVolume, 2) + ", 阈值倍数=" + DoubleToString(VolumeMultiplier, 2) + ", 条件=" + (volumeCondition ? "满足" : "不满足"), 3);
        
        // 如果不满足交易量条件，直接返回
        if(!volumeCondition)
        {
            LogMessage("交易量不足，忽略信号", 3);
            return;
        }
    }
    
    // 趋势过滤检查
    int trendDirection = 0;
    if(UseTrendFilter)
    {
        trendDirection = DetectTrend();
        string trendText = (trendDirection == 1 ? "上涨" : (trendDirection == -1 ? "下跌" : "横盘"));
        LogMessage("趋势方向: " + trendText, 3);
    }
    
    // 计算K线幅度和实体大小
    double prevPrevRange = prevPrevHigh - prevPrevLow;
    double prevRange = prevHigh - prevLow;
    double prevPrevBody = MathAbs(prevPrevClose - prevPrevOpen);
    double prevBody = MathAbs(prevClose - prevOpen);
    
    // 计算点值大小
    double pointSize = SymbolInfoDouble(Symbol(), SYMBOL_POINT);
    
    // 检查最小K线实体大小
    bool minBodySizeCondition = (prevBody >= MinBodySize * pointSize) && (prevPrevBody >= MinBodySize * pointSize);
    if(!minBodySizeCondition)
    {
        LogMessage("K线实体大小不符合要求，当前实体: " + DoubleToString(prevBody/pointSize, 2) + "点, 前一根实体: " + DoubleToString(prevPrevBody/pointSize, 2) + "点", 3);
    }
    
    // 检查看涨吞没形态
    bool isBullishEngulfing = false;
    if(minBodySizeCondition && volumeCondition && prevPrevClose < prevPrevOpen && prevClose > prevOpen)
    {
        if(AllowPartialEngulf)
        {
            // 部分吞没：前一根K线收盘价高于前前一根K线开盘价，且前一根K线开盘价低于前前一根K线收盘价
            isBullishEngulfing = (prevClose > prevPrevOpen && prevOpen < prevPrevClose);
        }
        else
        {
            // 完全吞没：前一根K线最高价高于前前一根K线最高价，且前一根K线最低价低于前前一根K线最低价
            isBullishEngulfing = (prevHigh >= prevPrevHigh && prevLow <= prevPrevLow);
        }
        
        // 检查吞没比例
        if(isBullishEngulfing && MinEngulfRatio > 0)
        {
            double engulfRatio = prevRange / prevPrevRange;
            isBullishEngulfing = (engulfRatio >= MinEngulfRatio);
            LogMessage("看涨吞没比例: " + DoubleToString(engulfRatio, 2) + " (要求: " + DoubleToString(MinEngulfRatio, 2) + ")", 3);
        }
    }
    
    // 检查看跌吞没形态
    bool isBearishEngulfing = false;
    if(minBodySizeCondition && volumeCondition && prevPrevClose > prevPrevOpen && prevClose < prevOpen)
    {
        if(AllowPartialEngulf)
        {
            // 部分吞没：前一根K线收盘价低于前前一根K线开盘价，且前一根K线开盘价高于前前一根K线收盘价
            isBearishEngulfing = (prevClose < prevPrevOpen && prevOpen > prevPrevClose);
        }
        else
        {
            // 完全吞没：前一根K线最高价高于前前一根K线最高价，且前一根K线最低价低于前前一根K线最低价
            isBearishEngulfing = (prevHigh >= prevPrevHigh && prevLow <= prevPrevLow);
        }
        
        // 检查吞没比例
        if(isBearishEngulfing && MinEngulfRatio > 0)
        {
            double engulfRatio = prevRange / prevPrevRange;
            isBearishEngulfing = (engulfRatio >= MinEngulfRatio);
            LogMessage("看跌吞没比例: " + DoubleToString(engulfRatio, 2) + " (要求: " + DoubleToString(MinEngulfRatio, 2) + ")", 3);
        }
    }
    
    // 计算市场波动率（用于自适应参数）
    double volatility = 0;
    if(UseAdaptiveParameters)
    {
        volatility = CalculateVolatility(VolatilityPeriod);
        LogMessage("市场波动率: " + DoubleToString(volatility, 5), 3);
    }
    
    // 处理看涨吞没信号
    if(isBullishEngulfing)
    {
        // 趋势过滤：买入信号只在上涨趋势或横盘时执行
        bool trendFilterForBuy = (!UseTrendFilter || trendDirection == 1 || trendDirection == 0);
        
        // 自适应过滤：根据市场波动率调整信号敏感度
        bool volatilityFilterForBuy = true;
        if(UseAdaptiveParameters && volatility > 0)
        {
            double effectiveVolatilityFactor = VolatilityFactor * 2;
            if(volatility > effectiveVolatilityFactor)
            {
                // 高波动市场需要更强的确认条件：成交量必须明显增加
                double avgVolume = CalculateAverageVolume(VolumePeriod);
                volatilityFilterForBuy = (prevVolume >= avgVolume * 1.5);
                if(!volatilityFilterForBuy)
                {
                    LogMessage("高波动市场中，成交量不足（当前: " + IntegerToString(prevVolume) + ", 平均: " + DoubleToString(avgVolume, 2) + ")", 2);
                }
            }
        }
        
        if(trendFilterForBuy && volatilityFilterForBuy)
        {
            // 记录信号详情
            string signalDetails = "看涨吞没信号 - 前前K线: " + 
                                  DoubleToString(prevPrevOpen, Digits) + "/" + 
                                  DoubleToString(prevPrevClose, Digits) + ", 前K线: " + 
                                  DoubleToString(prevOpen, Digits) + "/" + 
                                  DoubleToString(prevClose, Digits) + ", 交易量: " + 
                                  IntegerToString(prevVolume);
            LogMessage(signalDetails, 2);
            
            LogMessage("检测到看涨吞没形态且符合趋势方向 - 执行买入操作", 2);
            
            // 检查是否已有多头持仓
            if(PositionSelect(Symbol()) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
            {
                LogMessage("已有多头持仓，不执行新的买入操作", 3);
                return;
            }
            
            // 计算信号质量评分
            double avgVolume = CalculateAverageVolume(VolumePeriod);
            double prevPrevRange = prevPrevHigh - prevPrevLow;
            double prevRange = prevHigh - prevLow;
            double engulfRatio = (prevPrevRange > 0) ? (prevRange / prevPrevRange) : 1.0;
            double signalQuality = CalculateSignalQuality(true, prevVolume, avgVolume, trendDirection, volatility, engulfRatio);
            
            LogMessage("买入信号质量评分: " + DoubleToString(signalQuality, 2) + " (最小要求: " + DoubleToString(MinSignalQualityScore, 2) + ")", 2);
            
            // 信号质量过滤
            if(signalQuality >= MinSignalQualityScore)
            {
                // 信号频率控制
                if(CheckSignalFrequency(true))
                {
                    LogMessage("信号质量和频率验证通过，执行买入操作", 2);
                    // 执行买入操作
                    ExecuteBuyOrder();
                }
                else
                {
                    LogMessage("信号频率控制未通过，跳过买入操作", 2);
                }
            }
            else
            {
                LogMessage("信号质量评分低于阈值，跳过买入操作", 2);
            }
        }
        else if(!trendFilterForBuy)
        {
            LogMessage("检测到看涨吞没形态但不符合趋势方向（当前为下跌趋势），忽略买入信号", 2);
        }
    }
    // 处理看跌吞没信号
    else if(isBearishEngulfing)
    {
        // 趋势过滤：卖出信号只在下跌趋势或横盘时执行
        bool trendFilterForSell = (!UseTrendFilter || trendDirection == -1 || trendDirection == 0);
        
        // 自适应过滤：根据市场波动率调整信号敏感度
        bool volatilityFilterForSell = true;
        if(UseAdaptiveParameters && volatility > 0)
        {
            double effectiveVolatilityFactor = VolatilityFactor * 2;
            if(volatility > effectiveVolatilityFactor)
            {
                // 高波动市场需要更强的确认条件：成交量必须明显增加
                double avgVolume = CalculateAverageVolume(VolumePeriod);
                volatilityFilterForSell = (prevVolume >= avgVolume * 1.5);
                if(!volatilityFilterForSell)
                {
                    LogMessage("高波动市场中，成交量不足（当前: " + IntegerToString(prevVolume) + ", 平均: " + DoubleToString(avgVolume, 2) + ")", 2);
                }
            }
        }
        
        if(trendFilterForSell && volatilityFilterForSell)
        {
            // 记录信号详情
            string signalDetails = "看跌吞没信号 - 前前K线: " + 
                                  DoubleToString(prevPrevOpen, Digits) + "/" + 
                                  DoubleToString(prevPrevClose, Digits) + ", 前K线: " + 
                                  DoubleToString(prevOpen, Digits) + "/" + 
                                  DoubleToString(prevClose, Digits) + ", 交易量: " + 
                                  IntegerToString(prevVolume);
            LogMessage(signalDetails, 2);
            
            LogMessage("检测到看跌吞没形态且符合趋势方向 - 执行卖出操作", 2);
            
            // 检查是否已有空头持仓
            if(PositionSelect(Symbol()) && PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL)
            {
                LogMessage("已有空头持仓，不执行新的卖出操作", 3);
                return;
            }
            
            // 计算信号质量评分
            double avgVolume = CalculateAverageVolume(VolumePeriod);
            double prevPrevRange = prevPrevHigh - prevPrevLow;
            double prevRange = prevHigh - prevLow;
            double engulfRatio = (prevPrevRange > 0) ? (prevRange / prevPrevRange) : 1.0;
            double signalQuality = CalculateSignalQuality(false, prevVolume, avgVolume, trendDirection, volatility, engulfRatio);
            
            LogMessage("卖出信号质量评分: " + DoubleToString(signalQuality, 2) + " (最小要求: " + DoubleToString(MinSignalQualityScore, 2) + ")", 2);
            
            // 信号质量过滤
            if(signalQuality >= MinSignalQualityScore)
            {
                // 信号频率控制
                if(CheckSignalFrequency(false))
                {
                    LogMessage("信号质量和频率验证通过，执行卖出操作", 2);
                    // 执行卖出操作
                    ExecuteSellOrder();
                }
                else
                {
                    LogMessage("信号频率控制未通过，跳过卖出操作", 2);
                }
            }
            else
            {
                LogMessage("信号质量评分低于阈值，跳过卖出操作", 2);
            }
        }
        else if(!trendFilterForSell)
        {
            LogMessage("检测到看跌吞没形态但不符合趋势方向（当前为上涨趋势），忽略卖出信号", 2);
        }
    }
    else
    {
        LogMessage("未检测到有效吞没形态", 3);
    }
}

//+------------------------------------------------------------------+
//| 计算市场波动率                                                   |
//+------------------------------------------------------------------+
//| 功能: 计算指定周期内的平均价格波幅，作为市场波动率的衡量指标        |
//| 参数说明:                                                        |
//|   period - 计算周期长度，即要分析的K线数量                         |
//| 返回值:                                                          |
//|   平均波动率值，表示该周期内的平均价格波动幅度                      |
//| 计算原理:                                                        |
//|   使用简化版的ATR (平均真实波幅) 计算方法，取每个K线的最高价减最低价  |
//|   然后计算平均值作为市场波动率指标                                |
double CalculateVolatility(int period)
{
    double sumRange = 0;
    
    // 计算平均真实波幅 (ATR的简化版)
    for(int i = 1; i <= period; i++)
    {
        double range = High[i] - Low[i];
        sumRange += range;
    }
    
    // 返回平均波动率值
    return sumRange / period;
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
    double currentAsk = SymbolInfoDouble(Symbol(), SYMBOL_ASK);
    double currentBid = SymbolInfoDouble(Symbol(), SYMBOL_BID);
    double point = SymbolInfoDouble(Symbol(), SYMBOL_POINT);
    double spread = (currentAsk - currentBid) / point;
    
    // 计算动态手数
    double lotSize = CalculateLotSize();
    
    // 计算止损和止盈价格
    double stopLossPrice = currentAsk - StopLoss * point;
    double takeProfitPrice = currentAsk + TakeProfit * point;
    
    LogMessage("准备执行买入订单 - 货币对: " + Symbol() + ", 周期: " + EnumToString(Period()) + 
               ", 手数: " + DoubleToString(lotSize, 2) + ", 当前价格: " + DoubleToString(currentAsk, Digits) + 
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
        request.volume = lotSize;
        request.type = ORDER_TYPE_BUY;
        request.price = currentAsk;
        request.sl = stopLossPrice;
        request.tp = takeProfitPrice;
        request.deviation = 3;
        request.magic = 12345;
        request.comment = "EngulfSignalEA买入";
        
        // 记录详细日志
        LogMessage("尝试发送买入订单: 品种=" + Symbol() + ", 手数=" + DoubleToString(lotSize, 2) + ", 价格=" + DoubleToString(request.price, Digits), 4);
        
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
                RecordTradeHistory(result.order, POSITION_TYPE_BUY, result.price, lotSize);
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
                    currentAsk = SymbolInfoDouble(Symbol(), SYMBOL_ASK);
                    currentBid = SymbolInfoDouble(Symbol(), SYMBOL_BID);
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
                currentAsk = SymbolInfoDouble(Symbol(), SYMBOL_ASK);
                currentBid = SymbolInfoDouble(Symbol(), SYMBOL_BID);
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
    double currentAsk = SymbolInfoDouble(Symbol(), SYMBOL_ASK);
    double currentBid = SymbolInfoDouble(Symbol(), SYMBOL_BID);
    double point = SymbolInfoDouble(Symbol(), SYMBOL_POINT);
    double spread = (currentAsk - currentBid) / point;
    
    // 计算动态手数
    double lotSize = CalculateLotSize();
    
    // 计算止损和止盈价格
    double stopLossPrice = currentBid + StopLoss * point;
    double takeProfitPrice = currentBid - TakeProfit * point;
    
    LogMessage("准备执行卖出订单 - 货币对: " + Symbol() + ", 周期: " + EnumToString(Period()) + 
               ", 手数: " + DoubleToString(lotSize, 2) + ", 当前价格: " + DoubleToString(currentBid, Digits) + 
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
        request.volume = lotSize;
        request.type = ORDER_TYPE_SELL;
        request.price = currentBid;
        request.sl = stopLossPrice;
        request.tp = takeProfitPrice;
        request.deviation = 3;
        request.magic = 12345;
        request.comment = "EngulfSignalEA卖出";
        
        // 记录详细日志
        LogMessage("尝试发送卖出订单: 品种=" + Symbol() + ", 手数=" + DoubleToString(lotSize, 2) + ", 价格=" + DoubleToString(request.price, Digits), 4);
        
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
                RecordTradeHistory(result.order, POSITION_TYPE_SELL, result.price, lotSize);
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
                    currentBid = SymbolInfoDouble(Symbol(), SYMBOL_BID);
                    stopLossPrice = currentBid + StopLoss * point;
                    takeProfitPrice = currentBid - TakeProfit * point;
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
                currentBid = SymbolInfoDouble(Symbol(), SYMBOL_BID);
                stopLossPrice = currentBid + StopLoss * point;
                takeProfitPrice = currentBid - TakeProfit * point;
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
            request.price = SymbolInfoDouble(Symbol(), SYMBOL_BID);
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
            request.price = SymbolInfoDouble(Symbol(), SYMBOL_ASK);
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
        // 获取当前市场数据
        double point = SymbolInfoDouble(Symbol(), SYMBOL_POINT);
        int positionType = (int)PositionGetInteger(POSITION_TYPE);
        double currentPrice = (positionType == POSITION_TYPE_BUY) ? SymbolInfoDouble(Symbol(), SYMBOL_BID) : SymbolInfoDouble(Symbol(), SYMBOL_ASK);
        double openPrice = PositionGetDouble(POSITION_PRICE_OPEN);
        double stopLoss = PositionGetDouble(POSITION_SL);
        long ticket = PositionGetInteger(POSITION_TICKET);
        double profit = PositionGetDouble(POSITION_PROFIT);
        
        LogMessage("检查追踪止损 - 持仓类型: " + (positionType == POSITION_TYPE_BUY ? "多头" : "空头") + 
                   ", 当前利润: " + DoubleToString(profit, 2), 4);
        
        // 多头持仓追踪止损
        if(positionType == POSITION_TYPE_BUY)
        {
            double newStopLoss = currentPrice - TrailingStop * point;
            double distanceFromOpen = (currentPrice - openPrice) / point;
            
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
            double newStopLoss = currentPrice + TrailingStop * point;
            double distanceFromOpen = (openPrice - currentPrice) / point;
            
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
bool SetStopLossAndTakeProfit(ulong ticket, int orderType, double stopLossPoints, double takeProfitPoints)
{
    // 检查是否可以交易
    if(!CanTrade())
    {
        LogMessage("跳过止损止盈设置，交易条件不满足", 2);
        return false;
    }
    
    // 获取当前市场数据
    double point = SymbolInfoDouble(Symbol(), SYMBOL_POINT);
    
    // 计算新的止损止盈价格
    double sl = 0.0, tp = 0.0;
    double openPrice = PositionGetDouble(POSITION_PRICE_OPEN);
    
    if(orderType == ORDER_TYPE_BUY)
    {
        sl = openPrice - stopLossPoints * point;
        tp = openPrice + takeProfitPoints * point;
    }
    else if(orderType == ORDER_TYPE_SELL)
    {
        sl = openPrice + stopLossPoints * point;
        tp = openPrice - takeProfitPoints * point;
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
    
    // 检查是否有未成交的相同方向订单（MQL5风格）
    for(int i = 0; i < OrdersTotal(); i++)
    {
        // 选择订单
        if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))
        {
            // 获取订单类型
            int orderType = (int)OrderGetInteger(ORDER_TYPE);
            
            // 将订单类型转换为对应的持仓类型进行比较
            int mappedOrderType = -1;
            if(orderType == ORDER_TYPE_BUY || orderType == ORDER_TYPE_BUY_LIMIT || orderType == ORDER_TYPE_BUY_STOP)
                mappedOrderType = POSITION_TYPE_BUY;
            else if(orderType == ORDER_TYPE_SELL || orderType == ORDER_TYPE_SELL_LIMIT || orderType == ORDER_TYPE_SELL_STOP)
                mappedOrderType = POSITION_TYPE_SELL;
            
            // 检查订单品种和类型是否匹配
            string orderSymbol = OrderGetString(ORDER_SYMBOL);
            if(mappedOrderType == positionType && orderSymbol == Symbol())
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
void RecordTradeHistory(ulong orderTicket, int positionType, double price, double volume)
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
void LogOrderDetails(ulong orderTicket, int level=2)
{
    // 检查日志级别
    if(level > LogLevel) return;
    
    // 尝试获取订单详情（MQL5风格）
    if(PositionSelectByTicket(orderTicket))
    {
        string orderType = (PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY) ? "买入" : "卖出";
        double volume = PositionGetDouble(POSITION_VOLUME);
        double price = PositionGetDouble(POSITION_PRICE_OPEN);
        double sl = PositionGetDouble(POSITION_SL);
        double tp = PositionGetDouble(POSITION_TP);
        datetime openTime = PositionGetInteger(POSITION_TIME);
        string comment = PositionGetString(POSITION_COMMENT);
        
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
        FileWriteString(fileHandle, "<tr><td>净利润</td><td class='" + ((stats.grossProfit - stats.grossLoss) >= 0 ? "positive" : "negative") + "'>" + DoubleToString(stats.grossProfit - stats.grossLoss, 2) + "</td></tr>\n");
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
