import os
import sys

print("="*60)
print("Git 提交和推送")
print("="*60)

# 添加文件
print("\n1. 添加文件...")
ret1 = os.system('git add src/api/index.js src/components/admin/BonusManagement.vue')
print(f"返回码: {ret1}")

# 提交
print("\n2. 提交...")
ret2 = os.system('git commit -m "feat: update BonusManagement to use real API"')
print(f"返回码: {ret2}")

# 推送
print("\n3. 推送...")
ret3 = os.system('git push origin main')
print(f"返回码: {ret3}")

print("\n" + "="*60)
if ret3 == 0:
    print("✓ 完成")
else:
    print("✗ 推送失败")
print("="*60)
