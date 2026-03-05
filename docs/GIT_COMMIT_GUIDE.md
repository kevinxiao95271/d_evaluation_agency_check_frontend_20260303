# Git 提交指南

## 需要提交的文件

### 核心代码文件（必须提交）
1. `src/api/index.js` - 更新了 bonusApi 接口定义
2. `src/components/admin/BonusManagement.vue` - 更新了附加项管理组件

## 手动提交步骤

### 方法1: 使用 Git Bash 或命令行

打开新的终端窗口（不要在 Kiro 中执行），执行以下命令：

```bash
# 1. 进入项目目录
cd D:\AiCode\kiro2026\d_evaluation_agency_check_frontend_20260303

# 2. 查看状态
git status

# 3. 添加修改的文件
git add src/api/index.js src/components/admin/BonusManagement.vue

# 4. 提交
git commit -m "feat: update BonusManagement to use real API"

# 5. 推送到远端
git push origin main
```

### 方法2: 使用 VS Code

1. 打开 VS Code
2. 点击左侧的"源代码管理"图标
3. 查看更改的文件
4. 勾选要提交的文件：
   - src/api/index.js
   - src/components/admin/BonusManagement.vue
5. 输入提交信息: "feat: update BonusManagement to use real API"
6. 点击"提交"
7. 点击"推送"

### 方法3: 使用 GitHub Desktop

1. 打开 GitHub Desktop
2. 选择项目仓库
3. 查看更改的文件
4. 勾选要提交的文件
5. 输入提交信息
6. 点击"Commit to main"
7. 点击"Push origin"

## 提交信息

```
feat: update BonusManagement to use real API

- 使用 GET /api/bonus/list/{taskId} 加载附加项列表
- 使用 POST /api/bonus 保存/更新附加项
- 移除历史记录功能，简化界面
- 添加调试日志便于排查问题
- 修复刷新后数据丢失问题
```

## 更改内容说明

### src/api/index.js
- 更新 bonusApi.get() 接口路径
- 更新 bonusApi.getList() 接口路径（从查询参数改为路径参数）

### src/components/admin/BonusManagement.vue
- loadBonusData() 方法：调用真实 API 加载附加项列表
- updateBonus() 方法：添加调试日志
- saveBonus() 方法：添加调试日志
- 移除 historyVisible、historyRecords 相关代码
- 移除 viewHistory() 方法
- 移除历史记录对话框

## 验证提交

提交后，可以在 GitHub 上查看：
1. 访问仓库页面
2. 查看最新的 commit
3. 确认文件已更新

## 如果遇到冲突

如果推送时遇到冲突：

```bash
# 1. 拉取最新代码
git pull origin main

# 2. 解决冲突（如有）
# 编辑冲突文件，保留正确的代码

# 3. 添加解决后的文件
git add .

# 4. 提交
git commit -m "merge: resolve conflicts"

# 5. 推送
git push origin main
```

## 注意事项

1. 不要提交测试文件和临时文档（已在 .gitignore 中）
2. 只提交核心代码文件
3. 确保提交信息清晰明了
4. 推送前确认本地代码已测试通过

---

**准备就绪，可以开始提交！**
