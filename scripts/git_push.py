#!/usr/bin/env python3
"""Git 提交和推送脚本"""

import subprocess
import sys

def run_command(cmd):
    """执行命令并返回结果"""
    print(f"\n执行: {cmd}")
    print("="*60)
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"错误: {e}")
        return False

print("="*60)
print("Git 提交和推送")
print("="*60)

# 1. 查看状态
if not run_command("git status"):
    print("✗ git status 失败")
    sys.exit(1)

# 2. 添加文件
print("\n添加修改的文件...")
if not run_command("git add src/api/index.js src/components/admin/BonusManagement.vue"):
    print("✗ git add 失败")
    sys.exit(1)

# 3. 提交
print("\n提交更改...")
commit_msg = "feat: update BonusManagement to use real API"
if not run_command(f'git commit -m "{commit_msg}"'):
    print("✗ git commit 失败（可能没有更改）")
    # 继续执行，可能已经提交过了

# 4. 推送
print("\n推送到远端...")
if not run_command("git push origin main"):
    print("✗ git push 失败")
    sys.exit(1)

print("\n" + "="*60)
print("✓ 代码已成功推送到远端")
print("="*60)
