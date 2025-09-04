# 增加超时时间
import asyncio
import time

async def initialize_mcp_client():
    # 增加超时时间
    timeout = 30  # 秒
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            # 尝试初始化MCP客户端
            client = await create_mcp_client()
            return client
        except Exception as e:
            print(f"Failed to initialize MCP client: {e}")
            await asyncio.sleep(1)
    
    raise TimeoutError("Failed to initialize MCP client within timeout period")