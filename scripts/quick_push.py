import subprocess
import sys

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode == 0

print("Git 提交推送...")

# 添加所有更改
print("\n1. 添加文件...")
run("git add .")

# 提交
print("\n2. 提交...")
run('git commit -m "chore: organize files into scripts and docs folders"')

# 推送
print("\n3. 推送...")
if run("git push origin main"):
    print("\n✓ 完成")
else:
    print("\n✗ 推送失败")
