# 部署命令清单

## 当前状态
- ✅ 代码已更新到最新版本
- ✅ 已编译完成 (dist目录)
- ✅ 已压缩 dist.zip

## 立即部署

### 使用WinSCP或FileZilla上传
1. 打开WinSCP/FileZilla
2. 连接信息：
   - 主机: 81.71.44.180
   - 用户: root
   - 密码: Yiguo9527_
   - 端口: 22
3. 上传 `dist.zip` 到 `/data/frontend/`

### 然后SSH执行部署命令

连接SSH:
```bash
ssh root@81.71.44.180
# 密码: Yiguo9527_
```

执行部署（复制整段）:
```bash
cd /data/frontend && \
[ -d dist_backup ] && rm -rf dist_backup; \
[ -d dist ] && mv dist dist_backup; \
mkdir -p dist && \
unzip -q -o dist.zip -d dist && \
rm dist.zip && \
OLD_PID=$(lsof -ti:5039) && \
[ ! -z "$OLD_PID" ] && kill -9 $OLD_PID && sleep 2; \
cd dist && \
nohup python3 -m http.server 5039 > /dev/null 2>&1 & \
echo "✓ 服务已启动: http://81.71.44.180:5039"
```

## 或者使用命令行

### Windows PowerShell
```powershell
# 1. 上传（需要输入密码）
scp dist.zip root@81.71.44.180:/data/frontend/

# 2. 部署（需要输入密码）
ssh root@81.71.44.180 "cd /data/frontend && [ -d dist_backup ] && rm -rf dist_backup; [ -d dist ] && mv dist dist_backup; mkdir -p dist && unzip -q -o dist.zip -d dist && rm dist.zip && OLD_PID=\$(lsof -ti:5039) && [ ! -z \"\$OLD_PID\" ] && kill -9 \$OLD_PID && sleep 2; cd dist && nohup python3 -m http.server 5039 > /dev/null 2>&1 & echo 'Service started'"
```

## 验证部署

访问: http://81.71.44.180:5039

检查服务:
```bash
ssh root@81.71.44.180 "lsof -i:5039"
```

## 快速回滚

如果有问题，快速回滚:
```bash
ssh root@81.71.44.180 "cd /data/frontend && kill -9 \$(lsof -ti:5039) && rm -rf dist && mv dist_backup dist && cd dist && nohup python3 -m http.server 5039 > /dev/null 2>&1 &"
```

## 文件位置

本地:
- 源码: D:\AiCode\kiro2026\d_evaluation_agency_check_frontend_20260303
- 编译: dist/
- 压缩: dist.zip

服务器:
- 部署目录: /data/frontend/
- 当前版本: /data/frontend/dist/
- 备份版本: /data/frontend/dist_backup/
