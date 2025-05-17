# create.py - 添加性能测试逻辑

import asyncio
import datetime
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any

from faker import Faker

from CompanyProject.巴迪克.Tax.Api.create import CreateOrderAPI


def run_single_request(api_client: CreateOrderAPI, payload: dict) -> Dict[str, Any]:
    """执行一次请求并返回结果与耗时"""
    start_time = time.time()
    result = api_client.create_order(payload)
    end_time = time.time()
    return {
        "result": result,
        "elapsed": end_time - start_time
    }


def performance_test_concurrent(total_requests: int = 50, concurrent_users: int = 10):
    """
    使用线程池并发执行性能测试
    :param total_requests: 总请求数
    :param concurrent_users: 同时并发用户数
    """
    print(f"\n🚀 开始性能测试：共 {total_requests} 次请求，{concurrent_users} 并发")

    # 初始化 API 客户端
    api_client = CreateOrderAPI(company_name="tax_agent002@linshiyou.com")
    fake = Faker()

    # 构造请求参数模板
    base_payload = {
        "merchantId": "600009M0000001",
        "paymentType": "StaticMandiriVA",
        "amount": "0.01",
        "agentOrderNo": "",
        "payOrderNo": "",
        "sourceAgentOrderNo": "",
        "productName": lambda: fake.name(),
        "requestId": "1"
    }

    results = []
    with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
        futures = []
        for i in range(total_requests):
            today = datetime.datetime.now().strftime("%Y%m%d")
            payload = base_payload.copy()
            payload["agentOrderNo"] = f"AgentOrderNo{today}{i}"
            payload["payOrderNo"] = f"PayOrder{today}{i}"
            payload["productName"] = fake.name()

            futures.append(executor.submit(run_single_request, api_client, payload))

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

    # 分析结果
    success_count = sum(1 for r in results if 'error' not in r['result'])
    elapsed_times = [r['elapsed'] * 1000 for r in results]  # 转换为毫秒
    avg_time = statistics.mean(elapsed_times)
    max_time = max(elapsed_times)
    min_time = min(elapsed_times)
    error_rate = (len(results) - success_count) / len(results) * 100

    print("\n📊 性能测试结果：")
    print(f"✅ 成功请求：{success_count}/{total_requests}")
    print(f"❌ 错误率：{error_rate:.2f}%")
    print(f"⏱️  平均响应时间：{avg_time:.2f} ms")
    print(f"⏱️  最快响应时间：{min_time:.2f} ms")
    print(f"⏱️  最慢响应时间：{max_time:.2f} ms")


if __name__ == "__main__":
    # 原有的单次测试保留
    ...

    # 新增：性能测试入口
    performance_test_concurrent(total_requests=100, concurrent_users=20)
