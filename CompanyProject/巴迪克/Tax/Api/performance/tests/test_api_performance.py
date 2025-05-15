# tests/test_api_performance.py
import asyncio
import pytest
from utils.helper import run_async_requests
from utils.database import DatabaseManager


@pytest.mark.asyncio
async def test_performance_create_order():
    db_manager = DatabaseManager()
    results = await run_async_requests(total=50)

    for idx, res in enumerate(results):
        record = {
            "agent_order_no": f"AgentOrderNo20250515{idx}",
            "elapsed_time_ms": res["elapsed"],
            "status": res["status"],
            "response": res["response"],
            "timestamp": datetime.datetime.now()
        }
        db_manager.save_result(record)

    assert len(results) == 50
