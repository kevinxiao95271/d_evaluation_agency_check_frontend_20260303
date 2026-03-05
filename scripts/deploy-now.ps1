# 自动化部署脚本 - PowerShell版本
# 服务器: 81.71.44.180

$SERVER = "81.71.44.180"
$USER = "root"
$PASSWORD = "Yiguo9527_"
$REMOTE_DIR = "/data/frontend"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "开始部署前端到生产服务器" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 dist.zip 是否存在
if (-not (Test-Path "dist.zip")) {
    Write-Host "错误: dist.zip 不存在" -ForegroundColor Red
    exit 1
}
Write-Host "✓ 检查 dist.zip... OK" -ForegroundColor Green

# 使用 plink 和 pscp (PuTTY工具) 或者提示用户手动操作
Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "请按以下步骤手动部署:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

Write-Host "步骤1: 上传文件" -ForegroundColor Cyan
Write-Host "在新的PowerShell窗口执行:" -ForegroundColor White
Write-Host "  scp dist.zip root@81.71.44.180:/data/frontend/" -ForegroundColor Gray
Write-Host "  密码: Yiguo9527_" -ForegroundColor Gray
Write-Host ""

Write-Host "步骤2: SSH登录并部署" -ForegroundColor Cyan
Write-Host "在新的PowerShell窗口执行:" -ForegroundColor White
Write-Host "  ssh root@81.71.44.180" -ForegroundColor Gray
Write-Host "  密码: Yiguo9527_" -ForegroundColor Gray
Write-Host ""

Write-Host "步骤3: 在服务器上执行部署命令" -ForegroundColor Cyan
Write-Host "复制以下命令到SSH会话中执行:" -ForegroundColor White
Write-Host ""
Write-Host "cd /data/frontend && [ -d dist_backup ] && rm -rf dist_backup; [ -d dist ] && mv dist dist_backup; mkdir -p dist && unzip -q -o dist.zip -d dist && rm dist.zip && OLD_PID=`$(lsof -ti:5039) && [ ! -z `"`$OLD_PID`" ] && kill -9 `$OLD_PID && sleep 2; cd dist && nohup python3 -m http.server 5039 > /dev/null 2>&1 & echo `"✓ 部署完成: http://81.71.44.180:5039`"" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "或者使用一键部署命令 (需要安装 sshpass):" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "bash deploy-to-server.sh" -ForegroundColor Gray
Write-Host ""

Write-Host "部署完成后访问: http://81.71.44.180:5039" -ForegroundColor Green
