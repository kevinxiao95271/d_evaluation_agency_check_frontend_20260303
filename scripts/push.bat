@echo off
echo ====================================
echo Git Commit and Push
echo ====================================

echo.
echo Adding files...
git add src/api/index.js src/components/admin/BonusManagement.vue

echo.
echo Committing...
git commit -m "feat: update BonusManagement to use real API"

echo.
echo Pushing...
git push origin main

echo.
echo ====================================
echo Done
echo ====================================
pause
