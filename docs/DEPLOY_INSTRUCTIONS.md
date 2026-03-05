# 🚀 部署说明

## 当前状态
- ✅ 已从 Git 拉取最新代码
- ✅ 已重新构建 (npm run build)
- ✅ 已打包 dist.zip (0.44 MB)
- ✅ 准备部署到生产服务器

## 部署步骤

### 方法1: 手动部署（推荐）

#### 步骤1: 上传文件
```powershell
scp dist.zip root@81.71.44.180:/data/frontend/
```
密码: `Yiguo9527_`

#### 步骤2: SSH 登录
```powershell
ssh root@81.71.44.180
```
密码: `Yiguo9527_`

#### 步骤3: 部署（复制整行执行）
```bash
cd /data/frontend && [ -d dist_backup ] && rm -rf dist_backup; [ -d dist ] && mv dist dist_backup; mkdir -p dist && unzip -q -o dist.zip -d dist && rm dist.zip && OLD_PID=$(lsof -ti:5039) && [ ! -z "$OLD_PID" ] && kill -9 $OLD_PID && sleep 2; cd dist && nohup python3 -m http.server 5039 > /dev/null 2>&1 & echo "✓ 部署完成: http://81.71.44.180:5039"
```

### 方法2: 使用自动化脚本

#### 前提条件
```powershell
pip install paramiko scp
```

#### 执行部署
```powershell
python auto_deploy.py
```

## 验证部署

访问: http://81.71.44.180:5039

检查服务状态:
```bash
lsof -i:5039
ps aux | grep "http.server 5039"
```

## 回滚（如需要）

```bash
cd /data/frontend && kill -9 $(lsof -ti:5039) && rm -rf dist && mv dist_backup dist && cd dist && nohup python3 -m http.server 5039 > /dev/null 2>&1 &
```

## 服务器信息

- IP: 81.71.44.180
- 用户: root
- 密码: Yiguo9527_
- 目录: /data/frontend
- 端口: 5039

---

**准备就绪，可以开始部署！** 🎉
