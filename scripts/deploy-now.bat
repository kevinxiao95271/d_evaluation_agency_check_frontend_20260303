@echo off
echo ========================================
echo 部署到生产服务器
echo ========================================
echo.

echo 1. 上传dist.zip到服务器...
pscp -pw Yiguo9527_ dist.zip root@81.71.44.180:/data/frontend/
if errorlevel 1 (
    echo 上传失败，尝试使用scp...
    scp dist.zip root@81.71.44.180:/data/frontend/
)

echo.
echo 2. 在服务器上部署...
plink -pw Yiguo9527_ root@81.71.44.180 "cd /data/frontend && [ -d dist_backup ] && rm -rf dist_backup; [ -d dist ] && mv dist dist_backup; mkdir -p dist && unzip -q -o dist.zip -d dist && rm dist.zip && OLD_PID=$(lsof -ti:5039) && [ ! -z \"$OLD_PID\" ] && kill -9 $OLD_PID && sleep 2; cd dist && nohup python3 -m http.server 5039 > /dev/null 2>&1 & echo 'Service started on port 5039'"

echo.
echo ========================================
echo 部署完成！
echo 访问: http://81.71.44.180:5039
echo ========================================
pause
