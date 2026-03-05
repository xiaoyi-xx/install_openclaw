@echo off
chcp 65001 >nul
powershell -ExecutionPolicy Bypass -NoProfile -Command ^
$openclaw = Get-Command openclaw -ErrorAction SilentlyContinue; ^
if (-not $openclaw) { Write-Host \"错误：找不到 openclaw 命令，请确保它已加入 PATH 或指定完整路径。\"; Read-Host \"按 Enter 退出\"; exit }; ^
Write-Host \"执行登录（忽略结果）...\"; ^
& openclaw channels login; ^
Write-Host \"启动网关...\"; ^
$gateway = Start-Process -FilePath cmd.exe -ArgumentList '/c openclaw gateway --port 18789' -PassThru -NoNewWindow; ^
Write-Host \"等待网关初始化...\"; ^
Start-Sleep -Seconds 3; ^
Start-Process \"http://127.0.0.1:18789/\"; ^
Write-Host \"浏览器已打开，网关正在运行。按任意键停止网关并退出。\"; ^
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown'); ^
Stop-Process -Id $gateway.Id -Force; ^
Write-Host \"网关已停止。\"
pause