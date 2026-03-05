# 手动部署指南

## 服务器信息
- **IP**: 81.71.44.180
- **用户**: root
- **密码**: Yiguo9527_
- **部署目录**: /data/frontend
- **端口**: 5039

## 部署步骤

### 1. 本地编译
```bash
npm run build
```

### 2. 压缩dist目录
```bash
# Windows PowerShell
Compress-Archive -Path dist\* -DestinationPath dist.zip -Force

# Linux/Mac
cd dist && tar -czf ../dist.tar.gz * && cd ..
```

### 3. 上传到服务器
```bash
# 使用scp上传
scp dist.tar.gz root@81.71.44.180:/data/frontend/

# 或使用FTP工具上传到 /data/frontend/
```

### 4. SSH连接到服务器
```bash
ssh root@81.71.44.180
# 密码: Yiguo9527_
```

### 5. 在服务器上执行部署命令
```bash
cd /data/frontend

# 备份旧文件
if [ -d "dist_backup" ]; then rm -rf dist_backup; fi
if [ -d "dist" ]; then mv dist dist_backup; fi

# 解压新文件
mkdir -p dist
tar -xzf dist.tar.gz -C dist
rm dist.tar.gz

# 或者如果上传的是zip
# unzip -q -o dist.zip -d dist
# rm dist.zip

# 检查并杀掉旧进程
OLD_PID=$(lsof -ti:5039)
if [ ! -z "$OLD_PID" ]; then
    echo "杀掉旧进程: $OLD_PID"
    kill -9 $OLD_PID
    sleep 2
fi

# 启动新服务
cd dist
nohup python3 -m http.server 5039 > /dev/null 2>&1 &
NEW_PID=$!
echo "新进程已启动: $NEW_PID"

# 验证服务
sleep 2
if ps -p $NEW_PID > /dev/null; then
    echo "✓ 服务启动成功！"
    echo "访问地址: http://81.71.44.180:5039"
else
    echo "✗ 服务启动失败！"
fi
```

### 6. 验证部署
访问: http://81.71.44.180:5039

## 快速命令（一键部署）

### 在服务器上执行
```bash
cd /data/frontend && \
[ -d "dist_backup" ] && rm -rf dist_backup; \
[ -d "dist" ] && mv dist dist_backup; \
mkdir -p dist && \
tar -xzf dist.tar.gz -C dist && \
rm dist.tar.gz && \
OLD_PID=$(lsof -ti:5039) && \
[ ! -z "$OLD_PID" ] && kill -9 $OLD_PID && sleep 2; \
cd dist && \
nohup python3 -m http.server 5039 > /dev/null 2>&1 & \
echo "服务已启动，访问: http://81.71.44.180:5039"
```

## 故障排查

### 检查服务是否运行
```bash
lsof -i:5039
# 或
ps aux | grep "http.server 5039"
```

### 查看日志
```bash
# 如果有日志文件
tail -f /data/frontend/nohup.out
```

### 手动停止服务
```bash
kill -9 $(lsof -ti:5039)
```

### 手动启动服务
```bash
cd /data/frontend/dist
nohup python3 -m http.server 5039 > /dev/null 2>&1 &
```

## 使用Nginx（推荐）

如果服务器有Nginx，建议使用Nginx部署：

```nginx
server {
    listen 5039;
    server_name 81.71.44.180;
    
    root /data/frontend/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # API代理
    location /api {
        proxy_pass http://localhost:5031;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

然后重启Nginx:
```bash
nginx -t
nginx -s reload
```

## 注意事项

1. 确保服务器防火墙开放5039端口
2. 确保/data/frontend目录有写权限
3. 部署前先备份旧版本
4. 部署后验证功能是否正常
5. 如果使用Python http.server，注意它不适合生产环境，建议使用Nginx

## 回滚

如果新版本有问题，快速回滚：
```bash
cd /data/frontend
kill -9 $(lsof -ti:5039)
rm -rf dist
mv dist_backup dist
cd dist
nohup python3 -m http.server 5039 > /dev/null 2>&1 &
```
