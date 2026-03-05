#!/bin/bash
# 部署到生产服务器脚本
# 服务器: 81.71.44.180
# 目录: /data/frontend

SERVER="81.71.44.180"
USER="root"
PASSWORD="Yiguo9527_"
REMOTE_DIR="/data/frontend"
LOCAL_DIST="dist"

echo "========================================"
echo "开始部署前端到生产服务器"
echo "========================================"
echo ""

# 1. 检查dist目录
if [ ! -d "$LOCAL_DIST" ]; then
    echo "错误: dist目录不存在，请先运行 npm run build"
    exit 1
fi
echo "✓ 1. 检查dist目录... OK"

# 2. 压缩dist目录
echo "2. 压缩dist目录..."
cd dist
tar -czf ../dist.tar.gz *
cd ..
echo "✓ 压缩完成: dist.tar.gz"

# 3. 上传到服务器
echo "3. 上传到服务器 $SERVER..."
scp dist.tar.gz ${USER}@${SERVER}:${REMOTE_DIR}/

if [ $? -eq 0 ]; then
    echo "✓ 上传成功"
else
    echo "✗ 上传失败"
    exit 1
fi

# 4. 在服务器上解压和部署
echo "4. 在服务器上部署..."

ssh ${USER}@${SERVER} << 'ENDSSH'
cd /data/frontend

echo "备份旧文件..."
if [ -d "dist_backup" ]; then
    rm -rf dist_backup
fi
if [ -d "dist" ]; then
    mv dist dist_backup
fi

echo "解压新文件..."
mkdir -p dist
tar -xzf dist.tar.gz -C dist
rm dist.tar.gz

echo "检查进程..."
OLD_PID=$(lsof -ti:5039)
if [ ! -z "$OLD_PID" ]; then
    echo "杀掉旧进程: $OLD_PID"
    kill -9 $OLD_PID
    sleep 2
fi

echo "启动服务..."
cd dist
nohup python3 -m http.server 5039 > /dev/null 2>&1 &
NEW_PID=$!
echo "新进程已启动: $NEW_PID"

sleep 2
if ps -p $NEW_PID > /dev/null; then
    echo "✓ 服务启动成功！"
    echo "访问地址: http://81.71.44.180:5039"
else
    echo "✗ 服务启动失败！"
    exit 1
fi
ENDSSH

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "✓ 部署成功！"
    echo "========================================"
    echo "访问地址: http://81.71.44.180:5039"
else
    echo ""
    echo "✗ 部署失败，请检查错误信息"
fi

# 清理本地临时文件
rm -f dist.tar.gz

echo ""
