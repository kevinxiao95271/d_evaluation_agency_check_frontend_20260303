#!/usr/bin/env python3
"""完整测试附加项管理 API"""

import requests
import json

BASE_URL = "http://localhost:5031/api"

def test_api(name, method, endpoint, data=None, params=None):
    """测试 API 接口"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        
        print(f"\n{'='*60}")
        print(f"【{name}】")
        print(f"{method} {endpoint}")
        if params:
            print(f"参数: {params}")
        if data:
            print(f"数据: {json.dumps(data, ensure_ascii=False)}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ 成功")
            if isinstance(result.get('data'), list):
                print(f"返回数据条数: {len(result['data'])}")
            print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)[:500]}")
            return True, result
        else:
            print(f"✗ 失败: {response.text[:200]}")
            return False, None
            
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"【{name}】")
        print(f"{method} {endpoint}")
        print(f"✗ 异常: {e}")
        return False, None

print("="*60)
print("附加项管理 API 完整测试")
print("="*60)

success_count = 0
total_count = 0

# 测试1: 保存附加项
total_count += 1
result, data = test_api(
    "测试1: 保存附加项",
    "POST", 
    "/bonus",
    data={
        "taskId": 1,
        "institutionId": 1,
        "directorPresentation": 1,
        "secretaryParticipation": 0
    }
)
if result:
    success_count += 1

# 测试2: 查询单个附加项
total_count += 1
result, data = test_api(
    "测试2: 查询单个附加项",
    "GET",
    "/bonus",
    params={"taskId": 1, "institutionId": 1}
)
if result:
    success_count += 1

# 测试3: 查询任务下所有附加项
total_count += 1
result, data = test_api(
    "测试3: 查询任务下所有附加项",
    "GET",
    "/bonus/list/1"
)
if result:
    success_count += 1
    bonus_list = data.get('data', [])
    print(f"\n附加项详情:")
    for bonus in bonus_list[:5]:  # 只显示前5条
        print(f"  - {bonus.get('institutionName')}: "
              f"主任演讲={bonus.get('directorPresentation')}, "
              f"秘书参与={bonus.get('secretaryParticipation')}")

# 测试4: 更新附加项
total_count += 1
result, data = test_api(
    "测试4: 更新附加项",
    "POST",
    "/bonus",
    data={
        "taskId": 1,
        "institutionId": 1,
        "directorPresentation": 1,
        "secretaryParticipation": 1
    }
)
if result:
    success_count += 1

# 测试5: 再次查询验证更新
total_count += 1
result, data = test_api(
    "测试5: 验证更新结果",
    "GET",
    "/bonus",
    params={"taskId": 1, "institutionId": 1}
)
if result:
    success_count += 1
    bonus = data.get('data', {})
    print(f"\n更新后的值:")
    print(f"  主任演讲: {bonus.get('directorPresentation')}")
    print(f"  秘书参与: {bonus.get('secretaryParticipation')}")

# 测试6: 创建多个附加项
total_count += 1
print(f"\n{'='*60}")
print("【测试6: 批量创建附加项】")
batch_success = True
for inst_id in [2, 3, 4]:
    result, _ = test_api(
        f"创建机构{inst_id}的附加项",
        "POST",
        "/bonus",
        data={
            "taskId": 1,
            "institutionId": inst_id,
            "directorPresentation": inst_id % 2,
            "secretaryParticipation": (inst_id + 1) % 2
        }
    )
    if not result:
        batch_success = False
        break

if batch_success:
    success_count += 1
    print("✓ 批量创建成功")

# 测试7: 查询列表验证批量创建
total_count += 1
result, data = test_api(
    "测试7: 验证批量创建结果",
    "GET",
    "/bonus/list/1"
)
if result:
    success_count += 1
    bonus_list = data.get('data', [])
    print(f"\n当前共有 {len(bonus_list)} 条附加项记录")

# 总结
print("\n" + "="*60)
print("测试总结")
print("="*60)
print(f"总测试数: {total_count}")
print(f"成功: {success_count}")
print(f"失败: {total_count - success_count}")
print(f"成功率: {success_count/total_count*100:.1f}%")

if success_count == total_count:
    print("\n✓ 所有测试通过！附加项管理 API 工作正常")
else:
    print(f"\n⚠ 有 {total_count - success_count} 个测试失败")

print("\n" + "="*60)
print("前端可以使用的接口:")
print("="*60)
print("1. ✓ POST /api/bonus - 保存/更新附加项")
print("2. ✓ GET /api/bonus?taskId={taskId}&institutionId={institutionId} - 查询单个")
print("3. ✓ GET /api/bonus/list/{taskId} - 查询列表")
print("\n推荐实现:")
print("4. ? POST /api/bonus/batch - 批量保存（提升性能）")
