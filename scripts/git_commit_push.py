#!/usr/bin/env python3
"""Git 提交和推送脚本"""

import subprocess
import sys

def run_git_command(args, description):
    """执行 git 命令"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"命令: git {' '.join(args)}")
    print('='*60)
    
    try:
        result = subprocess.run(
            ['git'] + args,
            capture_output=True,
            text=True,
            timeout=30,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✓ {description} 成功")
            return True
        else:
            print(f"✗ {description} 失败 (返回码: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ {description} 超时")
        return False
    except Exception as e:
        print(f"✗ {description} 异常: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("Git 提交和推送脚本")
    print("="*60)
    
    # 1. 查看当前状态
    if not run_git_command(['status'], '查看 Git 状态'):
        print("\n警告: git status 失败，但继续执行...")
    
    # 2. 添加文件
    files_to_add = [
        'src/api/index.js',
        'src/components/admin/BonusManagement.vue'
    ]
    
    print(f"\n准备添加文件:")
    for f in files_to_add:
        print(f"  - {f}")
    
    if not run_git_command(['add'] + files_to_add, '添加文件到暂存区'):
        print("\n✗ 添加文件失败")
        return False
    
    # 3. 提交
    commit_message = "feat: update BonusManagement to use real API"
    if not run_git_command(['commit', '-m', commit_message], '提交更改'):
        print("\n注意: 提交失败（可能没有更改或已经提交）")
        # 继续执行推送
    
    # 4. 推送到远端
    if not run_git_command(['push', 'origin', 'main'], '推送到远端'):
        print("\n✗ 推送失败")
        print("\n可能的原因:")
        print("1. 网络问题")
        print("2. 需要先拉取远端更新")
        print("3. 认证问题")
        print("\n尝试先拉取:")
        if run_git_command(['pull', 'origin', 'main'], '拉取远端更新'):
            print("\n重新推送:")
            if not run_git_command(['push', 'origin', 'main'], '推送到远端'):
                return False
        else:
            return False
    
    print("\n" + "="*60)
    print("✓ 代码已成功提交并推送到远端")
    print("="*60)
    
    # 5. 显示最后一次提交
    run_git_command(['log', '-1', '--oneline'], '查看最后一次提交')
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n发生错误: {e}")
        sys.exit(1)
