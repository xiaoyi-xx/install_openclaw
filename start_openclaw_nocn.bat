start "OpenClaw Gateway" cmd /k "cd /d %~dp0 && start\gateway_nocn.bat"
timeout /t 5 /nobreak >nul
start "Open Browser" cmd /c "cd /d %~dp0 && start\open_browser_nocn.bat"    
timeout /t 2 /nobreak >nul
exit