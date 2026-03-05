#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试本地部署
"""
import requests
import time

print("=" * 60)
print("测试本地部署")
print("=" * 60)
print()

# 等待服务启动
print("等待服务启动...")
time.sleep(2)

# 测试前端
print("1. 测试前端页面...")
try:
    response = requests.get('http://localhost:5039', timeout=5)
    if response.status_code == 200:
        print("   ✅ 前端页面正常 (200)")
        print(f"   页面大小: {len(response.content)} bytes")
    else:
        print(f"   ⚠️  状态码: {response.status_code}")
except Exception as e:
    print(f"   ❌ 错误: {e}")

print()

# 测试静态资源
print("2. 测试静态资源...")
try:
    # 检查index.html
    response = requests.get('http://localhost:5039/index.html', timeout=5)
    if response.status_code == 200:
        print("   ✅ index.html 正常")
        # 检查是否包含Vue应用的标记
        if 'id="app"' in response.text:
            print("   ✅ Vue应用标记存在")
        else:
            print("   ⚠️  未找到Vue应用标记")
    else:
        print(f"   ❌ index.html 状态码: {response.status_code}")
except Exception as e:
    print(f"   ❌ 错误: {e}")

print()

# 测试assets目录
print("3. 测试assets资源...")
try:
    # 尝试访问assets目录（应该返回403或404）
    response = requests.get('http://localhost:5039/assets/', timeout=5)
    print(f"   assets目录状态: {response.status_code}")
except Exception as e:
    print(f"   ❌ 错误: {e}")

print()
print("=" * 60)
print("本地部署测试完成")
print("=" * 60)
print()
print("访问地址: http://localhost:5039")
print()
print("注意: 本地部署不包含API代理")
print("      需要确保后端API运行在 http://localhost:5031")
print()
