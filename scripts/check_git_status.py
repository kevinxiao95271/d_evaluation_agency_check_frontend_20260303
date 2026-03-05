import subprocess

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    return result.stdout + result.stderr

print("="*60)
print("检查 Git 状态")
print("="*60)

print("\n1. 当前分支和状态:")
print(run_cmd("git status"))

print("\n2. 最后一次提交:")
print(run_cmd("git log -1 --oneline"))

print("\n3. 远端状态:")
print(run_cmd("git remote -v"))

print("\n4. 本地和远端的差异:")
print(run_cmd("git log origin/main..HEAD --oneline"))

print("="*60)
