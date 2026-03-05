@echo off
cd /d %USERPROFILE%
pause
rem 设置代码页为UTF-8，避免中文乱码
chcp 65001 >nul

rem 启用命令扩展和延迟变量扩展
setlocal enabledelayedexpansion

echo =========================================
echo OpenClaw 安装脚本
echo =========================================
echo.
echo 请确保以管理员身份运行此脚本！
echo.

rem 初始化变量
set "need_restart=0"

rem 检查 Node.js 是否安装
echo 检查 Node.js 环境...
node -v >nul 2>&1
if %errorlevel% neq 0 (
    echo 未检测到 Node.js 环境。
    echo.
    set /p "install_node=是否自动下载并安装 Node.js？ (y/n): "
    if /i "!install_node!" equ "y" (
        echo 正在下载 Node.js...
        bitsadmin /transfer "NodeJS" https://nodejs.org/dist/latest/node-v20.11.1-x64.msi %cd%\nodejs.msi
        if %errorlevel% neq 0 (
            echo 下载失败，请手动下载并安装 Node.js。
            echo 下载地址: https://nodejs.org/
            echo 安装完成后请重新运行此脚本。
            pause
            exit /b 0
        )
        echo 正在安装 Node.js...
        msiexec /i nodejs.msi /qn
        if %errorlevel% neq 0 (
            echo 安装失败，请手动安装 Node.js。
            echo 安装完成后请重新运行此脚本。
            pause
            exit /b 0
        )
        echo Node.js 安装成功！
        del nodejs.msi
        set "need_restart=1"
    ) else (
        echo 请先安装 Node.js 后再运行此脚本。
        echo 下载地址: https://nodejs.org/
        pause
        exit /b 0
    )
) else (
    echo Node.js 环境已检测到。
)
pause

rem 检查 Git 是否安装
echo 检查 Git 环境...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 未检测到 Git 环境。
    echo.
    set /p "install_git=是否自动下载并安装 Git？ (y/n): "
    if /i "!install_git!" equ "y" (
        echo 正在下载 Git...
        bitsadmin /transfer "Git" https://github.com/git-for-windows/git/releases/latest/download/Git-2.44.0-64-bit.exe %cd%\git.exe
        if %errorlevel% neq 0 (
            echo 下载失败，请手动下载并安装 Git。
            echo 下载地址: https://git-scm.com/download/win
            echo 安装完成后请重新运行此脚本。
            pause
            exit /b 0
        )
        echo 提示: 安装过程中请确保勾选 "Git from the command line" 选项。
        echo 正在安装 Git...
        start /wait git.exe
        if %errorlevel% neq 0 (
            echo 安装失败，请手动安装 Git。
            echo 安装完成后请重新运行此脚本。
            pause
            exit /b 0
        )
        echo Git 安装成功！
        del git.exe
        set "need_restart=1"
    ) else (
        echo 请先安装 Git 后再运行此脚本。
        echo 下载地址: https://git-scm.com/download/win
        pause
        exit /b 0
    )
) else (
    echo Git 环境已检测到。
)
pause

rem 检查是否需要重启脚本
if %need_restart% equ 1 (
    echo.
    echo 环境安装完成，请重新运行此脚本以继续安装 OpenClaw。
    pause
    exit /b 0
)

rem 安装 OpenClaw
echo 准备安装 OpenClaw...
echo.
set /p "install_choice=是否安装 OpenClaw？ (y/n): "
if /i "!install_choice!" equ "y" (
    echo 正在打开新窗口安装 OpenClaw...
    start "OpenClaw 安装" /wait cmd /c "cd /d %USERPROFILE% && echo 当前目录: %CD% && npm install -g openclaw@latest && echo OpenClaw 安装成功！ && pause"
    if %errorlevel% neq 0 (
        echo 安装失败，请检查网络连接或权限。
        echo 请在解决问题后重新运行此脚本。
        pause
        exit /b 0
    )
    echo OpenClaw 安装成功！
) else (
    echo 取消安装。
    pause
    exit /b 0
)
pause

echo.
set /p "onboard_choice=是否进入新手引导并安装服务？ (y/n): "
if /i "!onboard_choice!" equ "y" (
    echo 正在打开新窗口运行新手引导...
    echo 执行命令: openclaw onboard --install-daemon
    start "OpenClaw 新手引导" /wait cmd /c "cd /d %USERPROFILE% && openclaw onboard --install-daemon && echo 新手引导完成！ && pause"
) else (
    echo 跳过新手引导。
)
pause

echo.
echo =========================================
echo OpenClaw 安装和配置完成！
echo =========================================
pause
