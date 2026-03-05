# 🚀 立即部署指南

## 快速部署（2个命令）

### 命令1: 上传文件
打开新的PowerShell窗口，执行:
```powershell
scp dist.zip root@81.71.44.180:/data/frontend/
```
输入密码: `Yiguo9527_`

### 命令2: 部署服务
```powershell
ssh root@81.71.44.180
```
输入密码: `Yiguo9527_`

然后在SSH会话中执行（复制粘贴整行）:
```bash
cd /data/frontend && [ -d dist_backup ] && rm -rf dist_backup; [ -d dist ] && mv dist dist_backup; mkdir -p dist && unzip -q -o dist.zip -d dist && rm dist.zip && OLD_PID=$(lsof -ti:5039) && [ ! -z "$OLD_PID" ] && kill -9 $OLD_PID && sleep 2; cd dist && nohup python3 -m http.server 5039 > /dev/null 2>&1 & echo "✓ 部署完成: http://81.71.44.180:5039"
```

## 验证部署

访问: **http://81.71.44.180:5039**

## 检查服务状态

```bash
# 检查端口
lsof -i:5039

# 检查进程
ps aux | grep "http.server 5039"
```

## 如需回滚

```bash
cd /data/frontend && kill -9 $(lsof -ti:5039) && rm -rf dist && mv dist_backup dist && cd dist && nohup python3 -m http.server 5039 > /dev/null 2>&1 &
```

---

**文件已准备就绪，开始部署！** 🎉
