# 新增文件: scripts/socket_monitor.py
import asyncio
import websockets
import json
import datetime
import threading
import logging
from typing import Dict, List
import pandas as pd

from Investment.THS.AutoTrade.scripts.monitor_20day import daily_check, is_trading_day
from Investment.THS.AutoTrade.utils.logger import setup_logger

# 设置日志
logger = setup_logger("socket_monitor.log")

# WebSocket服务器配置
WEBSOCKET_HOST = "localhost"
WEBSOCKET_PORT = 8765

# 全局变量存储连接的客户端
connected_clients = set()

# 监控配置
MONITORED_STOCKS = {
    "601728": "中国电信",
    "601398": "工商银行",
    "600900": "长江电力"
}

MONITORED_ETFS = {
    "508011": "嘉实物美消费REIT",
    "508005": "华夏首创奥莱REIT",
    "511380": "可转债ETF",
    "511580": "国债证金债ETF",
    "518850": "黄金ETF华夏",
    "510300": "沪深300ETF",
}

class MarketMonitor:
    def __init__(self):
        self.is_monitoring = False
        self.monitoring_thread = None
        self.last_signals = {
            'stocks': [],
            'etfs': []
        }

    async def register_client(self, websocket):
        """注册新的WebSocket客户端"""
        connected_clients.add(websocket)
        logger.info(f"新客户端连接: {websocket.remote_address}")

        # 发送当前最新信号
        if self.last_signals['stocks'] or self.last_signals['etfs']:
            await self.send_signals_to_client(websocket, self.last_signals)

        try:
            await websocket.wait_closed()
        finally:
            connected_clients.remove(websocket)
            logger.info(f"客户端断开连接: {websocket.remote_address}")

    async def send_signals_to_client(self, websocket, signals_data):
        """发送信号数据到指定客户端"""
        try:
            await websocket.send(json.dumps(signals_data, ensure_ascii=False))
        except Exception as e:
            logger.error(f"发送数据到客户端失败: {e}")

    async def broadcast_signals(self, signals_data):
        """广播信号数据到所有连接的客户端"""
        if connected_clients:
            disconnected_clients = set()
            for client in connected_clients:
                try:
                    await client.send(json.dumps(signals_data, ensure_ascii=False))
                except Exception as e:
                    logger.error(f"广播数据到客户端失败: {e}")
                    disconnected_clients.add(client)

            # 移除断开连接的客户端
            for client in disconnected_clients:
                connected_clients.discard(client)

    def start_monitoring(self):
        """启动监控线程"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            logger.info("市场监控已启动")

    def stop_monitoring(self):
        """停止监控"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
        logger.info("市场监控已停止")

    def _monitoring_loop(self):
        """监控循环（在独立线程中运行）"""
        while self.is_monitoring:
            try:
                # 检查是否为交易日和交易时间
                now = datetime.datetime.now()
                current_time = now.time()

                # 只在交易时间内检查（9:30-15:00）
                if (datetime.time(9, 30) <= current_time <= datetime.time(15, 0) and
                    is_trading_day(now.date())):

                    # 每5分钟检查一次
                    if current_time.second == 0 and current_time.minute % 5 == 0:
                        logger.info("执行市场信号检查")

                        # 检查股票信号
                        stock_signals_found, stock_signals = daily_check("stock", MONITORED_STOCKS, ma_window=20)

                        # 检查ETF信号
                        etf_signals_found, etf_signals = daily_check("etf", MONITORED_ETFS, ma_window=20)

                        # 如果有新信号，广播给所有客户端
                        if stock_signals_found or etf_signals_found:
                            signals_data = {
                                'timestamp': now.isoformat(),
                                'stocks': stock_signals,
                                'etfs': etf_signals,
                                'type': 'signals_update'
                            }

                            # 更新最后信号
                            self.last_signals = {
                                'stocks': stock_signals,
                                'etfs': etf_signals
                            }

                            # 在事件循环中广播信号
                            asyncio.run_coroutine_threadsafe(
                                self.broadcast_signals(signals_data),
                                asyncio.get_event_loop()
                            )

                # 等待一段时间再检查
                import time
                time.sleep(30)  # 每30秒检查一次时间

            except Exception as e:
                logger.error(f"监控循环出错: {e}")
                import time
                time.sleep(5)

# 创建监控实例
market_monitor = MarketMonitor()

async def handle_client(websocket, path):
    """处理客户端连接"""
    await market_monitor.register_client(websocket)

async def start_websocket_server():
    """启动WebSocket服务器"""
    server = await websockets.serve(
        handle_client,
        WEBSOCKET_HOST,
        WEBSOCKET_PORT
    )
    logger.info(f"WebSocket服务器启动在 ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
    return server

def run_socket_monitor():
    """运行Socket监控服务"""
    # 启动监控
    market_monitor.start_monitoring()

    # 启动WebSocket服务器
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    server = loop.run_until_complete(start_websocket_server())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("收到停止信号")
    finally:
        market_monitor.stop_monitoring()
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

# 客户端示例代码（可另存为单独文件）
CLIENT_EXAMPLE = '''
<!DOCTYPE html>
<html>
<head>
    <title>实时市场监控</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .signal { 
            padding: 10px; 
            margin: 5px 0; 
            border-radius: 5px; 
            background: #f0f0f0; 
        }
        .buy { border-left: 5px solid green; }
        .sell { border-left: 5px solid red; }
        .timestamp { color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>实时市场监控</h1>
    <div id="signals"></div>
    
    <script>
        const ws = new WebSocket('ws://localhost:8765');
        const signalsDiv = document.getElementById('signals');
        
        ws.onopen = function(event) {
            console.log('连接已建立');
        };
        
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            displaySignals(data);
        };
        
        ws.onerror = function(error) {
            console.log('WebSocket错误: ' + error);
        };
        
        ws.onclose = function(event) {
            console.log('连接已关闭');
        };
        
        function displaySignals(data) {
            if (data.type === 'signals_update') {
                const signalsHtml = `
                    <h2>最新信号 [${new Date(data.timestamp).toLocaleString()}]</h2>
                    <h3>股票信号</h3>
                    ${data.stocks.map(signal => `
                        <div class="signal buy">
                            <div>${signal}</div>
                            <div class="timestamp">股票信号</div>
                        </div>
                    `).join('')}
                    <h3>ETF信号</h3>
                    ${data.etfs.map(signal => `
                        <div class="signal buy">
                            <div>${signal}</div>
                            <div class="timestamp">ETF信号</div>
                        </div>
                    `).join('')}
                `;
                signalsDiv.innerHTML = signalsHtml + signalsDiv.innerHTML;
            }
        }
    </script>
</body>
</html>
'''

if __name__ == "__main__":
    run_socket_monitor()
