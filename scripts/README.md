# Scripts 目录

本目录包含项目相关的脚本文件。

## 部署脚本

### 自动化部署
- `auto_deploy.py` - 自动化部署脚本（使用 paramiko）
- `deploy.py` - 部署脚本
- `deploy-now.bat` - Windows 批处理部署
- `deploy-now.ps1` - PowerShell 部署脚本
- `deploy-to-server.ps1` - 部署到服务器（PowerShell）
- `deploy-to-server.sh` - 部署到服务器（Bash）

### 本地测试
- `test_local_deployment.py` - 本地部署测试

## Git 脚本

- `push.bat` - 快速提交推送（推荐）
- `git_commit_push.py` - Git 提交推送（Python 完整版）
- `simple_git_push.py` - Git 提交推送（Python 简化版）
- `git_push.py` - Git 推送脚本
- `git-commit.bat` - Git 提交批处理
- `direct_git.py` - 直接执行 Git 命令
- `check_git_status.py` - 检查 Git 状态

## API 测试脚本

- `test_api.py` - 完整 API 测试（15个接口）
- `test_bonus_api.py` - 附加项 API 测试
- `test_bonus_complete.py` - 附加项完整测试（推荐）
- `test_bonus_frontend.html` - 附加项前端测试页面

## 使用说明

### 快速部署
```bash
# Windows
scripts\push.bat

# 或使用 Python
python scripts/push.bat
```

### API 测试
```bash
# 测试所有 API
python scripts/test_api.py

# 测试附加项 API
python scripts/test_bonus_complete.py
```

### 检查 Git 状态
```bash
python scripts/check_git_status.py
```

## 注意事项

1. 部署脚本需要配置服务器信息
2. Git 脚本会自动提交和推送代码
3. API 测试脚本需要后端服务运行在 localhost:5031
