@echo off
echo ========================================
echo 前端项目部署脚本
echo ========================================

echo 1. 检查Git状态...
git status

echo.
echo 2. 设置Git配置...
git config user.name "kevinxiao95271"
git config user.email "kevinxiao95271@gmail.com"

echo.
echo 3. 添加所有文件...
git add .

echo.
echo 4. 提交代码...
git commit -m "feat: Vue.js frontend application for evaluation system"

echo.
echo 5. 推送到远程仓库...
git push -u origin main

echo.
echo 部署完成！
pause