@echo off
chcp 65001 >nul
title OpenClaw 启动器
echo 启动网关窗口...
start "OpenClaw Gateway" cmd /k "cd /d %~dp0 && start\gateway.bat"
timeout /t 5 /nobreak >nul
echo 启动浏览器窗口...
start "Open Browser" cmd /c "cd /d %~dp0 && start\open_browser.bat"

echo 主脚本运行完成，本窗口可关闭。
timeout /t 2 /nobreak >nul
exit