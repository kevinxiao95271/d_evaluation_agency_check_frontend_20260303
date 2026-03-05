# 附加项管理更新说明

## ✅ 已完成

### 1. 移除所有模拟数据
- ✅ 单个更新使用真实 API: `POST /api/bonus`
- ✅ 编辑保存使用真实 API: `POST /api/bonus`
- ✅ 批量操作使用真实 API（逐个调用）
- ✅ 导入 bonusApi 模块

### 2. 当前功能状态

#### ✅ 可用功能
- 加载任务列表
- 加载机构列表
- 单个附加项更新（开关切换）
- 编辑对话框保存
- 批量设置主任演讲
- 批量设置秘书参与
- 批量清空

#### ⚠️ 受限功能
- 附加项列表显示（使用默认值0，因为缺少列表接口）
- 历史记录查看（提示需要后端接口）

## ❌ 缺失的后端接口

### 🔴 高优先级（必需）

#### 1. 获取附加项列表
```
GET /api/bonus/list?taskId={taskId}
```

**当前影响**: 
- 页面加载时无法显示已有的附加项数据
- 所有机构默认显示为0
- 用户看不到之前设置的附加项

**响应格式**:
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
    }
  ]
}
```

**前端代码位置**: 
- `src/components/admin/BonusManagement.vue` 第 ~150 行
- 已添加 TODO 注释

### 🟡 中优先级（推荐）

#### 2. 批量设置接口
```
POST /api/bonus/batch
```

**当前影响**:
- 批量操作需要逐个调用 API（64个机构 = 64次请求）
- 性能差，用户体验不好
- 网络开销大

**请求格式**:
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

**前端代码位置**:
- `src/components/admin/BonusManagement.vue` 第 ~220、~250、~280 行
- 已添加 TODO 注释

### 🟢 低优先级（可选）

#### 3. 历史记录接口
```
GET /api/bonus/history/{taskId}/{institutionId}
```

**当前影响**:
- 点击"历史"按钮提示功能不可用
- 无法查看附加项的修改历史

## 临时解决方案

### 当前实现
1. 使用 `POST /api/bonus` 单个更新（已测试通过）
2. 批量操作通过循环调用单个更新实现
3. 列表加载显示默认值（全部为0）

### 用户影响
- ✅ 可以正常设置和更新附加项
- ⚠️ 看不到已有的附加项数据（需要刷新或重新设置）
- ⚠️ 批量操作较慢（64个机构约需10-20秒）
- ❌ 无法查看历史记录

## 测试

### 测试脚本
```bash
python test_bonus_api.py
```

### 测试结果
- ✅ POST /api/bonus - 创建/更新成功
- ❌ GET /api/bonus/list - 404 Not Found
- ❌ POST /api/bonus/batch - 404 Not Found
- ❌ GET /api/bonus/{taskId}/{institutionId} - 404 Not Found

## 下一步

1. 🔴 **优先**: 后端实现 `GET /api/bonus/list?taskId={taskId}`
2. 🟡 **推荐**: 后端实现 `POST /api/bonus/batch`
3. 🟢 **可选**: 后端实现历史记录接口

## 相关文件

- `src/components/admin/BonusManagement.vue` - 前端组件（已更新）
- `src/api/index.js` - API 定义（已更新）
- `test_bonus_api.py` - API 测试脚本
- `BONUS_API_REQUIREMENTS.md` - 详细接口需求文档
