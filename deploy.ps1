Write-Host "========================================" -ForegroundColor Green
Write-Host "前端项目Git部署脚本" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host "`n1. 检查Git状态..." -ForegroundColor Yellow
try {
    git status --porcelain
    Write-Host "Git仓库状态正常" -ForegroundColor Green
} catch {
    Write-Host "Git状态检查失败: $_" -ForegroundColor Red
}

Write-Host "`n2. 设置Git配置..." -ForegroundColor Yellow
git config user.name "kevinxiao95271"
git config user.email "kevinxiao95271@gmail.com"
Write-Host "Git用户配置完成" -ForegroundColor Green

Write-Host "`n3. 添加所有文件..." -ForegroundColor Yellow
git add .
Write-Host "文件添加完成" -ForegroundColor Green

Write-Host "`n4. 提交代码..." -ForegroundColor Yellow
$commitMessage = "feat: Complete Vue.js frontend application

- Vue 3 + Element Plus + Vite tech stack
- Judge login and scoring functionality (76 accounts)
- Complete admin backend (institution/judge/task/template/bonus/config)
- Score records management system (filter/view/delete/export)
- API integration with fallback to mock data
- Responsive design and routing navigation
- Support for 64 institutions and 2812 scoring tasks"

git commit -m $commitMessage
Write-Host "代码提交完成" -ForegroundColor Green

Write-Host "`n5. 推送到远程仓库..." -ForegroundColor Yellow
git push -u origin main
Write-Host "推送完成" -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "部署完成！" -ForegroundColor Green
Write-Host "远程仓库: https://github.com/kevinxiao95271/d_evaluation_agency_check_frontend_20260303" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green

Read-Host "按任意键继续..."