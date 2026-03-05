# 部署到生产服务器脚本
# 服务器: 81.71.44.180
# 目录: /data/frontend

$SERVER = "81.71.44.180"
$USER = "root"
$REMOTE_DIR = "/data/frontend"
$LOCAL_DIST = "dist"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "开始部署前端到生产服务器" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 检查dist目录
if (-not (Test-Path $LOCAL_DIST)) {
    Write-Host "错误: dist目录不存在，请先运行 npm run build" -ForegroundColor Red
    exit 1
}

Write-Host "1. 检查dist目录... OK" -ForegroundColor Green

# 2. 压缩dist目录
Write-Host "2. 压缩dist目录..." -ForegroundColor Yellow
Compress-Archive -Path "$LOCAL_DIST\*" -DestinationPath "dist.zip" -Force
Write-Host "   压缩完成: dist.zip" -ForegroundColor Green

# 3. 上传到服务器
Write-Host "3. 上传到服务器 $SERVER..." -ForegroundColor Yellow
Write-Host "   请输入服务器密码: Yiguo9527_" -ForegroundColor Gray

# 使用scp上传（需要手动输入密码）
scp dist.zip ${USER}@${SERVER}:${REMOTE_DIR}/

if ($LASTEXITCODE -eq 0) {
    Write-Host "   上传成功" -ForegroundColor Green
} else {
    Write-Host "   上传失败" -ForegroundColor Red
    exit 1
}

# 4. 在服务器上解压和部署
Write-Host "4. 在服务器上部署..." -ForegroundColor Yellow

$SSH_COMMANDS = @"
cd $REMOTE_DIR
echo '备份旧文件...'
if [ -d 'dist_backup' ]; then rm -rf dist_backup; fi
if [ -d 'dist' ]; then mv dist dist_backup; fi

echo '解压新文件...'
unzip -q -o dist.zip -d dist
rm dist.zip

echo '检查进程...'
OLD_PID=`$(lsof -ti:5039)
if [ ! -z "`$OLD_PID" ]; then
    echo "杀掉旧进程: `$OLD_PID"
    kill -9 `$OLD_PID
    sleep 2
fi

echo '启动服务...'
cd dist
nohup python3 -m http.server 5039 > /dev/null 2>&1 &
NEW_PID=`$!
echo "新进程已启动: `$NEW_PID"

sleep 2
if ps -p `$NEW_PID > /dev/null; then
    echo '服务启动成功！'
    echo '访问地址: http://81.71.44.180:5039'
else
    echo '服务启动失败！'
    exit 1
fi
"@

ssh ${USER}@${SERVER} $SSH_COMMANDS

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "部署成功！" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "访问地址: http://81.71.44.180:5039" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "部署失败，请检查错误信息" -ForegroundColor Red
}

# 清理本地临时文件
Remove-Item dist.zip -ErrorAction SilentlyContinue

Write-Host ""
