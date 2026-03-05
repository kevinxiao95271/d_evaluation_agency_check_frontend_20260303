#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动部署脚本
"""
import os
import subprocess
import sys

SERVER = "81.71.44.180"
USER = "root"
PASSWORD = "Yiguo9527_"
REMOTE_DIR = "/data/frontend"
LOCAL_FILE = "dist.zip"

print("=" * 60)
print("部署到生产服务器")
print("=" * 60)
print()

# 检查dist.zip是否存在
if not os.path.exists(LOCAL_FILE):
    print(f"❌ 错误: {LOCAL_FILE} 不存在")
    print("请先运行: npm run build")
    sys.exit(1)

print(f"✓ 找到文件: {LOCAL_FILE}")
print()

# 1. 上传文件
print("1. 上传文件到服务器...")
scp_cmd = f'scp {LOCAL_FILE} {USER}@{SERVER}:{REMOTE_DIR}/'
print(f"   执行: {scp_cmd}")
print(f"   密码: {PASSWORD}")
print()

result = subprocess.run(scp_cmd, shell=True)
if result.returncode != 0:
    print("❌ 上传失败")
    sys.exit(1)

print("✓ 上传成功")
print()

# 2. 在服务器上部署
print("2. 在服务器上部署...")

deploy_script = f"""
cd {REMOTE_DIR}
echo '备份旧文件...'
[ -d dist_backup ] && rm -rf dist_backup
[ -d dist ] && mv dist dist_backup

echo '解压新文件...'
mkdir -p dist
unzip -q -o dist.zip -d dist
rm dist.zip

echo '检查旧进程...'
OLD_PID=$(lsof -ti:5039)
if [ ! -z "$OLD_PID" ]; then
    echo "杀掉旧进程: $OLD_PID"
    kill -9 $OLD_PID
    sleep 2
fi

echo '启动新服务...'
cd dist
nohup python3 -m http.server 5039 > /dev/null 2>&1 &
NEW_PID=$!
echo "新进程已启动: $NEW_PID"

sleep 2
if ps -p $NEW_PID > /dev/null; then
    echo '✓ 服务启动成功！'
else
    echo '✗ 服务启动失败！'
    exit 1
fi
"""

ssh_cmd = f'ssh {USER}@{SERVER} "{deploy_script}"'
print(f"   执行SSH命令...")
print()

result = subprocess.run(ssh_cmd, shell=True)
if result.returncode != 0:
    print("❌ 部署失败")
    sys.exit(1)

print()
print("=" * 60)
print("✓ 部署成功！")
print("=" * 60)
print(f"访问地址: http://{SERVER}:5039")
print()
