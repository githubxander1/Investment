# test_full_workflow.py

import asyncio
import logging

import pytest
from utils.helper import run_async_requests
from utils.database import DatabaseManager


@pytest.mark.asyncio
async def test_full_workflow():
    db_manager = DatabaseManager()

    # Step 1: 创建订单
    create_results = await run_async_requests(total=50, endpoint="/v1.0/declaration/create")

    for idx, res in enumerate(create_results):
        record = {
            "agent_order_no": res["payload"].get("agentOrderNo", f"unknown_{idx}"),
            "elapsed_time_ms": res["elapsed"],
            "status": res["status"],
            "response": str(res["response_data"])[:499],
            "timestamp": datetime.datetime.now()
        }

        if res["status"] == "success":
            data = res["response_data"]
            assert data.get("errCode") == "0", \
                f"错误码非0: {data.get('errCodeDes', '无描述')} - 响应内容: {data}"

            # Step 2: 撤销订单（如果创建成功）
            if data.get("auditStatus") == "110":
                cancel_payload = {
                    "agentOrderNo": res["payload"]["agentOrderNo"],
                    "requestId": str(idx)
                }
                cancel_result = await send_cancel_order(cancel_payload)
                assert cancel_result["status"] == "success", \
                    f"撤销失败: {cancel_result['response']}"

        else:
            logging.error(f"创建订单失败: {res['response']}")

        db_manager.save_result(record)

    assert len(create_results) == 50
