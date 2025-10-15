import asyncio
import websockets
import json
import datetime

async def test_client():
    """测试WebSocket客户端"""
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            print(f"[{datetime.datetime.now()}] 已连接到服务器: {uri}")
            
            # 发送获取状态命令
            await websocket.send(json.dumps({
                "command": "get_status"
            }))
            
            # 发送执行任务命令
            await websocket.send(json.dumps({
                "command": "execute_tasks"
            }))
            
            # 监听服务器消息
            async for message in websocket:
                try:
                    data = json.loads(message)
                    msg_type = data.get("type", "unknown")
                    timestamp = data.get("timestamp", "N/A")
                    
                    print(f"[{timestamp}] 收到消息 (类型: {msg_type}): {data}")
                    
                    # 如果收到任务完成消息，可以断开连接或继续等待
                    if msg_type == "command_response" and data.get("status") == "completed":
                        print("任务执行完成，客户端将继续监听...")
                        
                except json.JSONDecodeError:
                    print(f"收到非JSON消息: {message}")
                    
    except websockets.exceptions.ConnectionClosed:
        print("与服务器的连接已关闭")
    except Exception as e:
        print(f"客户端发生错误: {e}")

if __name__ == "__main__":
    print("启动WebSocket测试客户端...")
    asyncio.run(test_client())