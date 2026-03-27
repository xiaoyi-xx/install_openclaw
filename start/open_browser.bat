@echo off
chcp 65001 >nul
echo 等待网关就绪（3秒）...
timeout /t 3 /nobreak >nul
start http://127.0.0.1:18789/
echo 浏览器已打开，本窗口即将关闭...
timeout /t 1 /nobreak >nul
exit