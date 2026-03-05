# 附加项管理 API 需求

## 当前状态

### ✅ 已有接口
- **POST /api/bonus** - 创建/更新附加项（已测试通过）
  - 请求体: `{ taskId, institutionId, directorPresentation, secretaryParticipation }`
  - 响应: 返回创建的附加项数据

### ❌ 缺失接口

#### 1. 获取任务的所有附加项列表（必需）
```
GET /api/bonus/list?taskId={taskId}
```
**用途**: 附加项管理页面需要显示某个任务下所有机构的附加项数据

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": 1,
      "taskId": 1,
      "institutionId": 1,
      "institutionName": "临床检验中心",
      "directorPresentation": 1,
      "secretaryParticipation": 0,
      "filledBy": "管理员",
      "updateTime": "2026-03-05 10:30:00"
    },
    {
      "id": 2,
      "taskId": 1,
      "institutionId": 2,
      "institutionName": "医疗设备管理质控中心",
      "directorPresentation": 0,
      "secretaryParticipation": 1,
      "filledBy": "管理员",
      "updateTime": "2026-03-05 11:00:00"
    }
  ]
}
```

**说明**: 
- 如果某个机构没有附加项记录，可以不返回（前端会默认为0）
- 或者返回所有机构，没有记录的默认值为0

#### 2. 获取单个附加项（可选，优先级低）
```
GET /api/bonus/{taskId}/{institutionId}
```
**用途**: 查询特定机构在特定任务下的附加项

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "taskId": 1,
    "institutionId": 1,
    "institutionName": "临床检验中心",
    "directorPresentation": 1,
    "secretaryParticipation": 0,
    "filledBy": "管理员",
    "updateTime": "2026-03-05 10:30:00"
  }
}
```

#### 3. 更新附加项（可选，如果 POST 支持更新则不需要）
```
PUT /api/bonus/{id}
```
**请求体**: 
```json
{
  "directorPresentation": 1,
  "secretaryParticipation": 1
}
```

**说明**: 如果 POST /api/bonus 已经支持 upsert（存在则更新，不存在则创建），则此接口可以不需要

#### 4. 批量创建/更新（推荐，提高性能）
```
POST /api/bonus/batch
```
**请求体**:
```json
[
  {
    "taskId": 1,
    "institutionId": 1,
    "directorPresentation": 1,
    "secretaryParticipation": 0
  },
  {
    "taskId": 1,
    "institutionId": 2,
    "directorPresentation": 0,
    "secretaryParticipation": 1
  }
]
```

**用途**: 批量设置功能（批量设置主任演讲、批量设置秘书参与、批量清空）

## 前端需求场景

### 场景1: 加载附加项列表
1. 用户选择考核任务
2. 前端调用 `GET /api/bonus/list?taskId=1`
3. 显示所有机构的附加项状态

### 场景2: 单个更新
1. 用户切换某个机构的开关
2. 前端调用 `POST /api/bonus` 更新单条记录

### 场景3: 批量操作
1. 用户点击"批量设置主任演讲"
2. 前端调用 `POST /api/bonus/batch` 批量更新所有机构

## 优先级

### 🔴 高优先级（必需）
1. **GET /api/bonus/list?taskId={taskId}** - 获取列表（前端无法工作）

### 🟡 中优先级（推荐）
2. **POST /api/bonus/batch** - 批量操作（提升用户体验）

### 🟢 低优先级（可选）
3. GET /api/bonus/{taskId}/{institutionId} - 单个查询
4. PUT /api/bonus/{id} - 更新（如果 POST 支持 upsert 则不需要）

## 临时方案

在后端接口完善之前，前端可以：
1. 获取机构列表 `GET /api/institution/list`
2. 为每个机构调用 `POST /api/bonus` 创建默认记录（全部为0）
3. 用户修改时调用 `POST /api/bonus` 更新

但这种方案效率低，不推荐长期使用。

## 测试脚本

已创建测试脚本: `test_bonus_api.py`
运行: `python test_bonus_api.py`
