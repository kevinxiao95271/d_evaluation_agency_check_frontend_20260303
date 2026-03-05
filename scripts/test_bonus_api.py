#!/usr/bin/env python3
"""测试附加项管理 API"""

import requests
import json

BASE_URL = "http://localhost:5031/api"

def test_api(method, endpoint, data=None, params=None):
    """测试 API 接口"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=5)
        elif method == "DELETE":
            response = requests.delete(url, timeout=5)
        
        print(f"\n{'='*60}")
        print(f"{method} {endpoint}")
        if params:
            print(f"参数: {params}")
        if data:
            print(f"数据: {json.dumps(data, ensure_ascii=False)}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ 成功")
            print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)[:500]}")
            return result
        else:
            print(f"✗ 失败: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"{method} {endpoint}")
        print(f"✗ 异常: {e}")
        return None

print("="*60)
print("附加项管理 API 测试")
print("="*60)

# 1. 创建附加项
print("\n【测试1】创建附加项 (POST /bonus)")
bonus_data = {
    "taskId": 1,
    "institutionId": 1,
    "directorPresentation": 1,
    "secretaryParticipation": 0
}
result1 = test_api("POST", "/bonus", data=bonus_data)

# 2. 获取单个附加项
print("\n【测试2】获取单个附加项 (GET /bonus/{taskId}/{institutionId})")
result2 = test_api("GET", "/bonus/1/1")

# 3. 尝试获取列表 - 方式1
print("\n【测试3】获取列表 - 方式1 (GET /bonus?taskId=1)")
result3 = test_api("GET", "/bonus", params={"taskId": 1})

# 4. 尝试获取列表 - 方式2
print("\n【测试4】获取列表 - 方式2 (GET /bonus/list?taskId=1)")
result4 = test_api("GET", "/bonus/list", params={"taskId": 1})

# 5. 尝试获取列表 - 方式3
print("\n【测试5】获取列表 - 方式3 (GET /bonus/task/1)")
result5 = test_api("GET", "/bonus/task/1")

# 6. 更新附加项
print("\n【测试6】更新附加项 (PUT /bonus/{id})")
update_data = {
    "taskId": 1,
    "institutionId": 1,
    "directorPresentation": 1,
    "secretaryParticipation": 1
}
result6 = test_api("PUT", "/bonus/1", data=update_data)

# 7. 批量创建
print("\n【测试7】批量创建 (POST /bonus/batch)")
batch_data = [
    {"taskId": 1, "institutionId": 2, "directorPresentation": 0, "secretaryParticipation": 1},
    {"taskId": 1, "institutionId": 3, "directorPresentation": 1, "secretaryParticipation": 0}
]
result7 = test_api("POST", "/bonus/batch", data=batch_data)

print("\n" + "="*60)
print("测试完成")
print("="*60)

# 总结需要的接口
print("\n【需要的接口总结】")
print("1. ✓ POST /api/bonus - 创建/更新附加项")
print("2. ? GET /api/bonus/{taskId}/{institutionId} - 获取单个附加项")
print("3. ? GET /api/bonus/list?taskId={taskId} - 获取任务的所有附加项列表")
print("4. ? PUT /api/bonus/{id} - 更新附加项")
print("5. ? DELETE /api/bonus/{id} - 删除附加项")
print("6. ? POST /api/bonus/batch - 批量创建/更新")
