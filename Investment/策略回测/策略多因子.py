from jqdata import *

# 初始化函数，设定策略参数
def initialize(context):
    # 设定基准为沪深300
    set_benchmark('000300.XSHG')
    # 开启动态复权模式（真实价格）
    set_option('use_real_price', True)

    # 策略参数
    context.stock_pool = get_index_stocks('000300.XSHG')  # 股票池：沪深300成分股
    context.top_n = 15                                   # 每月选综合得分最高的15只股票
    context.rebalance_days = 1                           # 每月第1个交易日调仓
    context.max_position_per_stock = 0.08                # 单只股票最大仓位比例
    context.max_drawdown = 0.20                          # 触发清仓的最大回撤
    # 初始化历史最高净值
    context.historical_high = context.portfolio.total_value

    # 多因子参数
    context.factors = {
        'value': {'weight': 0.30},       # 价值因子（PE/PB）
        'momentum': {'weight': 0.35},    # 动量因子（120日收益率）
        'quality': {'weight': 0.20},    # 质量因子（ROE）
        'volatility': {'weight': 0.15}  # 波动率因子（90日波动率的倒数）
    }

    # 动态因子权重调整（每月根据市场状态调整）
    run_monthly(adjust_factor_weights, 1, time='before_open')

    # 定时任务（每月调仓）
    run_monthly(rebalance_portfolio, context.rebalance_days, time='open')

    # 每天更新历史最高净值
    run_daily(update_historical_high, time='after_close')

    # 记录日志
    log.info('多因子轮动策略初始化完成')

# 每天更新历史最高净值
def update_historical_high(context):
    """
    每日收盘后更新历史最高净值
    """
    current_value = context.portfolio.total_value
    if current_value > context.historical_high:
        context.historical_high = current_value
        log.info(f'更新历史最高净值: {context.historical_high:.2f}')

# 动态调整因子权重（基于市场状态）
def adjust_factor_weights(context):
    """
    根据市场状态动态调整各因子权重
    1. 趋势市场增加动量因子权重
    2. 震荡市场增加质量因子权重
    3. 恐慌市场增加价值因子权重
    """
    # 获取市场状态指标
    momentum_index = get_market_momentum(context)
    volatility_index = get_market_volatility(context)

    # 根据市场状态调整权重
    if momentum_index > 0.1:  # 强趋势市场
        log.info("市场处于强趋势状态，增加动量因子权重")
        context.factors['momentum']['weight'] = 0.45
        context.factors['value']['weight'] = 0.25
        context.factors['quality']['weight'] = 0.15
        context.factors['volatility']['weight'] = 0.15
    elif volatility_index > 0.25:  # 高波动市场
        log.info("市场处于高波动状态，增加波动率因子权重")
        context.factors['volatility']['weight'] = 0.25
        context.factors['value']['weight'] = 0.30
        context.factors['quality']['weight'] = 0.25
        context.factors['momentum']['weight'] = 0.20
    else:  # 正常市场
        log.info("市场处于正常状态，使用标准因子权重")
        context.factors['value']['weight'] = 0.30
        context.factors['momentum']['weight'] = 0.35
        context.factors['quality']['weight'] = 0.20
        context.factors['volatility']['weight'] = 0.15

    # 记录当前因子权重
    factor_weights_str = "; ".join([f"{factor}: {context.factors[factor]['weight']:.2f}"
                                     for factor in context.factors])
    log.info(f"当前因子权重: {factor_weights_str}")

# 获取市场动量
def get_market_momentum(context):
    """
    获取沪深300指数的120日收益率
    """
    prices = get_price('000300.XSHG', end_date=context.current_dt,
                      fields='close', frequency='1d', count=120, skip_paused=True)
    if len(prices) > 60:
        return float(prices.iloc[-1] / prices.iloc[0] - 1)
    return 0

# 获取市场波动率
def get_market_volatility(context):
    """
    获取沪深300指数的90日波动率
    """
    prices = get_price('000300.XSHG', end_date=context.current_dt,
                      fields='close', frequency='1d', count=90, skip_paused=True)
    if len(prices) > 60:
        returns = prices.pct_change().dropna()
        return float(returns.std() * np.sqrt(252))
    return 0

# 多因子股票选择
def select_stocks(context):
    """
    使用多因子模型筛选股票
    1. 计算每个因子的Z分数
    2. 根据权重计算综合得分
    """
    # 获取候选股票池
    candidates = []
    current_date = context.current_dt.strftime('%Y-%m-%d')

    # 创建DataFrame存储因子得分
    factor_df = pd.DataFrame(index=context.stock_pool)

    # 排除ST股和停牌股
    for stock in context.stock_pool:
        if not is_st_stock(stock) and not get_current_data()[stock].paused:
            candidates.append(stock)

    if not candidates:
        return []

    # 因子1: 价值（PE/PB综合）
    q = query(
        valuation.code,
        valuation.pe_ratio,
        valuation.pb_ratio
    ).filter(
        valuation.code.in_(candidates)
    )
    value_df = get_fundamentals(q, date=current_date)
    if not value_df.empty:
        value_df['pe_score'] = 1 / value_df['pe_ratio']  # PE越低越好
        value_df['pb_score'] = 1 / value_df['pb_ratio']  # PB越低越好
        value_df['value'] = 0.6 * value_df['pe_score'] + 0.4 * value_df['pb_score']
        factor_df = factor_df.join(value_df.set_index('code')['value'])

    # 因子2: 动量（120日收益率）
    momentum_scores = {}
    for stock in candidates:
        prices = get_price(stock, end_date=current_date,
                          fields='close', frequency='1d', count=120, skip_paused=True)
        if len(prices) > 60:
            momentum_scores[stock] = (prices.iloc[-1] / prices.iloc[0] - 1)
        else:
            momentum_scores[stock] = 0
    factor_df['momentum'] = pd.Series(momentum_scores)

    # 因子3: 质量（ROE）
    q = query(
        valuation.code,
        indicator.roe
    ).filter(
        valuation.code.in_(candidates)
    )
    quality_df = get_fundamentals(q, date=current_date)
    if not quality_df.empty:
        factor_df = factor_df.join(quality_df.set_index('code')['roe'])
        factor_df.rename(columns={'roe': 'quality'}, inplace=True)

    # 因子4: 波动率（90日波动率的倒数）
    volatility_scores = {}
    for stock in candidates:
        try:
            prices = get_price(stock, end_date=current_date,
                              fields='close', frequency='1d', count=90, skip_paused=True)
            if len(prices) > 60:
                returns = prices.pct_change().dropna()
                # 确保波动率是一个标量值（浮点数）
                volatility = float(returns.std())
                # 避免除零错误
                volatility_scores[stock] = 1 / (volatility + 0.0001)
            else:
                volatility_scores[stock] = 1
        except:
            volatility_scores[stock] = 1
    factor_df['volatility'] = pd.Series(volatility_scores)

    # 处理缺失值
    factor_df = factor_df.fillna(0)

    # 标准化每个因子（Z-score）
    for factor in context.factors:
        if factor in factor_df.columns:
            mean = factor_df[factor].mean()
            std = factor_df[factor].std()
            if std > 0:
                factor_df[factor] = (factor_df[factor] - mean) / std
            else:
                factor_df[factor] = factor_df[factor] - mean

    # 计算综合得分
    factor_df['total_score'] = 0
    for factor, config in context.factors.items():
        if factor in factor_df.columns:
            factor_df['total_score'] += factor_df[factor] * config['weight']

    # 选择得分最高的top_n只股票
    if not factor_df.empty:
        # 确保total_score是数值类型
        factor_df['total_score'] = factor_df['total_score'].astype(float)

        # 使用nlargest选择前top_n只股票
        top_stocks = factor_df['total_score'].nlargest(context.top_n).index.tolist()
        return top_stocks

    return []

# 判断ST股票
def is_st_stock(stock):
    """
    判断股票是否为ST/*ST股
    """
    current_data = get_current_data()
    stock_name = current_data[stock].name
    return "ST" in stock_name or "*ST" in stock_name

# 调仓函数
def rebalance_portfolio(context):
    # 风控检查：若当前回撤超过阈值，清仓
    if risk_control(context):
        return

    # 获取目标股票列表
    target_stocks = select_stocks(context)
    if not target_stocks:
        log.warn('本月无符合条件股票，保持空仓')
        return

    # 记录选择的股票
    log.info(f'本月选中的股票: {", ".join(target_stocks)}')

    # 分配资金：计算每只股票应分配的资金
    total_value = context.portfolio.total_value
    cash_per_stock = total_value / min(len(target_stocks), context.top_n) * 0.95

    # 卖出不在目标列表中的持仓
    for stock in context.portfolio.positions:
        if stock not in target_stocks:
            order_target_value(stock, 0)
            log.info(f'卖出 {get_security_info(stock).display_name}')

    # 买入目标股票
    for stock in target_stocks:
        current_position = context.portfolio.positions[stock].value
        target_value = min(cash_per_stock, total_value * context.max_position_per_stock)

        if current_position < target_value:
            # 计算需要买入的金额
            need_buy = target_value - current_position
            order_target_value(stock, target_value)
            log.info(f'买入 {get_security_info(stock).display_name}, 金额: {need_buy:.2f}')

# 风险控制函数
def risk_control(context):
    """
    使用自定义的历史最高净值而不是内置属性
    """
    # 计算当前回撤
    current_value = context.portfolio.total_value
    if context.historical_high > 0:
        current_drawdown = (context.historical_high - current_value) / context.historical_high
    else:
        current_drawdown = 0

    if current_drawdown >= context.max_drawdown:
        log.warn(f'最大回撤 {current_drawdown*100:.2f}% 超过阈值，执行清仓！')
        # 清空所有持仓
        for stock in list(context.portfolio.positions):
            order_target_value(stock, 0)

        # 重置历史最高净值
        context.historical_high = current_value

        return True
    return False

# 每日收盘后记录收益
def after_trading_end(context):
    # 记录当日收益
    log.info(f'账户总值: {context.portfolio.total_value:.2f}, 日收益率: {context.portfolio.returns:.4f}')