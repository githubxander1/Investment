# tests/test_api_performance.py

import asyncio
import datetime
import logging

import pytest
from ..utils.helper import run_async_requests
from ..utils.database import DatabaseManager


@pytest.mark.asyncio
async def test_performance_create_order():
    db_manager = DatabaseManager()
    results = await run_async_requests(total=50)

    for idx, res in enumerate(results):
        # 获取原始 payload 和 response data
        payload = res.get("payload", {})
        data = res.get("response_data", {})

        # 构造数据库记录字段
        record = {
            "agent_order_no": payload.get("agentOrderNo", f"unknown_{idx}"),
            "elapsed_time_ms": res["elapsed"],
            "status": res["status"],
            "response": str(data)[:499],
            "timestamp": datetime.datetime.now()
        }

        # 添加断言逻辑
        if res["status"] == "success":
            assert data.get("errCode") == "0", \
                f"错误码非0: {data.get('errCodeDes', '无描述')} - 响应内容: {data}"
        else:
            logging.error(f"请求失败: {payload}, 错误信息: {res['response']}")

        # 存入数据库（可选）
        db_manager.save_result(record)

    assert len(results) == 50
