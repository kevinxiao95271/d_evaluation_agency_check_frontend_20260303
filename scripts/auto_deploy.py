#!/usr/bin/env python3
"""
自动化部署脚本
使用 paramiko 库进行 SSH 连接和文件传输
"""

import os
import sys
import time

try:
    import paramiko
    from scp import SCPClient
except ImportError:
    print("错误: 需要安装 paramiko 和 scp 库")
    print("请运行: pip install paramiko scp")
    sys.exit(1)

# 服务器配置
SERVER = "81.71.44.180"
USER = "root"
PASSWORD = "Yiguo9527_"
PORT = 22
REMOTE_DIR = "/data/frontend"
LOCAL_FILE = "dist.zip"

def print_step(step, message):
    """打印步骤信息"""
    print(f"\n{'='*50}")
    print(f"步骤 {step}: {message}")
    print('='*50)

def upload_file(ssh_client):
    """上传文件到服务器"""
    print_step(1, "上传 dist.zip 到服务器")
    
    if not os.path.exists(LOCAL_FILE):
        print(f"错误: {LOCAL_FILE} 不存在")
        return False
    
    try:
        with SCPClient(ssh_client.get_transport()) as scp:
            scp.put(LOCAL_FILE, f"{REMOTE_DIR}/")
        print(f"✓ 上传成功: {LOCAL_FILE}")
        return True
    except Exception as e:
        print(f"✗ 上传失败: {e}")
        return False

def deploy_on_server(ssh_client):
    """在服务器上执行部署命令"""
    print_step(2, "在服务器上部署")
    
    deploy_cmd = f"""
cd {REMOTE_DIR}
echo "备份旧版本..."
[ -d dist_backup ] && rm -rf dist_backup
[ -d dist ] && mv dist dist_backup

echo "解压新版本..."
mkdir -p dist
unzip -q -o dist.zip -d dist
rm dist.zip

echo "停止旧服务..."
OLD_PID=$(lsof -ti:5039)
if [ ! -z "$OLD_PID" ]; then
    kill -9 $OLD_PID
    echo "已停止进程: $OLD_PID"
    sleep 2
fi

echo "启动新服务..."
cd dist
nohup python3 -m http.server 5039 > /dev/null 2>&1 &
NEW_PID=$!
echo "新进程已启动: $NEW_PID"

sleep 2
if ps -p $NEW_PID > /dev/null 2>&1; then
    echo "✓ 服务启动成功！"
    echo "访问地址: http://{SERVER}:5039"
else
    echo "✗ 服务启动失败！"
    exit 1
fi
"""
    
    try:
        stdin, stdout, stderr = ssh_client.exec_command(deploy_cmd)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if output:
            print(output)
        if error and "warning" not in error.lower():
            print(f"错误输出: {error}")
        
        return stdout.channel.recv_exit_status() == 0
    except Exception as e:
        print(f"✗ 部署失败: {e}")
        return False

def verify_deployment(ssh_client):
    """验证部署是否成功"""
    print_step(3, "验证部署")
    
    try:
        stdin, stdout, stderr = ssh_client.exec_command("lsof -i:5039")
        output = stdout.read().decode('utf-8')
        
        if "python" in output.lower():
            print("✓ 服务正在运行")
            print(output)
            return True
        else:
            print("✗ 服务未运行")
            return False
    except Exception as e:
        print(f"验证失败: {e}")
        return False

def main():
    """主函数"""
    print("\n" + "="*50)
    print("开始自动化部署到生产服务器")
    print("="*50)
    print(f"服务器: {SERVER}")
    print(f"用户: {USER}")
    print(f"目录: {REMOTE_DIR}")
    
    # 创建 SSH 客户端
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接服务器
        print(f"\n连接到服务器 {SERVER}...")
        ssh_client.connect(
            hostname=SERVER,
            port=PORT,
            username=USER,
            password=PASSWORD,
            timeout=10
        )
        print("✓ SSH 连接成功")
        
        # 上传文件
        if not upload_file(ssh_client):
            return 1
        
        # 部署
        if not deploy_on_server(ssh_client):
            return 1
        
        # 验证
        if not verify_deployment(ssh_client):
            return 1
        
        # 成功
        print("\n" + "="*50)
        print("✓ 部署成功！")
        print("="*50)
        print(f"访问地址: http://{SERVER}:5039")
        print("\n提示: 请在浏览器中强制刷新 (Ctrl+Shift+R)")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ 部署失败: {e}")
        return 1
    finally:
        ssh_client.close()

if __name__ == "__main__":
    sys.exit(main())
