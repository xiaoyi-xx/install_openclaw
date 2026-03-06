# OpenClaw 安装脚本
# 使用 PowerShell 实现

# 首先切换到用户目录
Write-Host "切换到用户目录..."
try {
    Set-Location -Path $env:USERPROFILE -ErrorAction Stop
    Write-Host "当前目录: $pwd"
} catch {
    Write-Host "切换目录失败: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "请手动切换到用户目录后再运行此脚本。"
    Read-Host "按 Enter 键退出..."
    exit
}
# 检查当前是否以管理员身份运行
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    # 如果不是管理员，则重新启动自身并请求管理员权限
    Start-Process -FilePath "powershell.exe" -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# 以下是你的脚本主体，需要管理员权限才能运行的代码
Write-Host "脚本正在以管理员身份运行..."
# 主脚本执行
try {
    # 检查 Node.js 是否安装
    Write-Host "检查 Node.js 环境..."
    $nodeFound = $false
    try {
        # 尝试在PATH中查找node.exe
        $nodePath = Get-Command node -ErrorAction SilentlyContinue
        if ($nodePath) {
            $nodeVersion = node -v
            Write-Host "Node.js 环境已检测到: $nodeVersion"
            $nodeFound = $true
        } else {
            # 检查常见安装路径
            $commonPaths = @(
                "$env:ProgramFiles\nodejs\node.exe",
                "$env:ProgramFiles (x86)\nodejs\node.exe",
                "$env:USERPROFILE\AppData\Local\Programs\nodejs\node.exe"
            )
            foreach ($path in $commonPaths) {
                if (Test-Path -Path $path) {
                    $nodeVersion = & $path -v
                    Write-Host "Node.js 环境已检测到: $nodeVersion"
                    $nodeFound = $true
                    break
                }
            }
        }
    } catch {
        Write-Host "检查 Node.js 环境时出错: $($_.Exception.Message)" -ForegroundColor Red
    }

    if (-not $nodeFound) {
        Write-Host "未检测到 Node.js 环境。"
        Write-Host
        $installNode = Read-Host "是否自动下载并安装 Node.js？ (y/n)"
        if ($installNode -eq "y" -or $installNode -eq "Y") {
            Write-Host "正在获取最新的 Node.js LTS 版本..."
            try {
                # 尝试获取最新的 LTS 版本信息
                $nodeMsiPath = "$env:USERPROFILE\nodejs.msi"
                
                # 首先尝试使用固定的 LTS 版本
                $ltsUrl = "https://nodejs.org/dist/v24.14.0/node-v24.14.0-x64.msi"
                Write-Host "正在下载 Node.js v24.14.0 LTS 版本..."
                Write-Host "下载地址: $ltsUrl"
                Invoke-WebRequest -Uri $ltsUrl -OutFile $nodeMsiPath -ErrorAction Stop
                
                Write-Host "正在安装 Node.js LTS 版本..."
                Start-Process -FilePath "msiexec.exe" -ArgumentList "/i $nodeMsiPath /qn" -Wait
                if (Test-Path -Path $nodeMsiPath) {
                    Remove-Item -Path $nodeMsiPath -Force
                }
                Write-Host "Node.js LTS 版本安装成功！"
                $needRestart = $true
            } catch {
                Write-Host "下载或安装 Node.js 失败: $($_.Exception.Message)" -ForegroundColor Red
                Write-Host "请手动下载并安装 Node.js LTS 版本。"
                Write-Host "下载地址: https://nodejs.org/en/download"
                Read-Host "按 Enter 键退出..."
                exit
            }
        } else {
            Write-Host "请先安装 Node.js 后再运行此脚本。"
            Write-Host "下载地址: https://nodejs.org/"
            Read-Host "按 Enter 键退出..."
            exit
        }
    }

    # 检查 Git 是否安装
    Write-Host "检查 Git 环境..."
    $gitFound = $false
    try {
        # 尝试在PATH中查找git.exe
        $gitPath = Get-Command git -ErrorAction SilentlyContinue
        if ($gitPath) {
            $gitVersion = git --version
            Write-Host "Git 环境已检测到: $gitVersion"
            $gitFound = $true
        } else {
            # 检查常见安装路径
            $commonPaths = @(
                "$env:ProgramFiles\Git\bin\git.exe",
                "$env:ProgramFiles (x86)\Git\bin\git.exe",
                "$env:USERPROFILE\AppData\Local\Programs\Git\bin\git.exe"
            )
            foreach ($path in $commonPaths) {
                if (Test-Path -Path $path) {
                    $gitVersion = & $path --version
                    Write-Host "Git 环境已检测到: $gitVersion"
                    $gitFound = $true
                    break
                }
            }
        }
    } catch {
        Write-Host "检查 Git 环境时出错: $($_.Exception.Message)" -ForegroundColor Red
    }

    if (-not $gitFound) {
        Write-Host "未检测到 Git 环境。"
        Write-Host
        $installGit = Read-Host "是否自动安装 Git？ (y/n)"
        if ($installGit -eq "y" -or $installGit -eq "Y") {
            Write-Host "正在安装 Git..."
            try {
                # 直接从国内源下载安装
                $gitExePath = "$env:USERPROFILE\git.exe"
                $gitUrl = "https://cdn.npmmirror.com/binaries/git-for-windows/v2.53.0.windows.1/Git-2.53.0-64-bit.exe"
                
                Write-Host "正在下载 Git..."
                Write-Host "下载地址: $gitUrl"
                Invoke-WebRequest -Uri $gitUrl -OutFile $gitExePath -ErrorAction Stop
                Write-Host "正在安装 Git..."
                Start-Process -FilePath $gitExePath -Wait
                
                if (Test-Path -Path $gitExePath) {
                    Remove-Item -Path $gitExePath -Force
                }
                
                Write-Host "Git 安装成功！"
                $needRestart = $true
            } catch {
                Write-Host "下载或安装 Git 失败: $($_.Exception.Message)" -ForegroundColor Red
                Write-Host "请手动下载并安装 Git。"
                Write-Host "下载地址: https://git-scm.com/download/win"
                Read-Host "按 Enter 键退出..."
                exit
            }
        } else {
            Write-Host "请先安装 Git 后再运行此脚本。"
            Write-Host "下载地址: https://git-scm.com/download/win"
            Read-Host "按 Enter 键退出..."
            exit
        }
    }

    # 检查是否需要重启脚本
    if ($needRestart) {
        Write-Host
        Write-Host "环境安装完成，请重新运行此脚本以继续安装 OpenClaw。"
        Read-Host "按 Enter 键退出..."
        exit
    }

    # 安装 OpenClaw
    Write-Host "准备安装 OpenClaw..."
    Write-Host
    $installChoice = Read-Host "是否安装 OpenClaw？ (y/n)"
    if ($installChoice -eq "y" -or $installChoice -eq "Y") {
        Write-Host "正在打开新窗口安装 OpenClaw..."
        # 使用简单的命令参数，避免脚本块的复杂性
        $installCommand = "Write-Host '当前目录: $pwd'; Write-Host '正在安装 OpenClaw...'; npm install -g openclaw@latest; if ($LASTEXITCODE -eq 0) { Write-Host 'OpenClaw 安装成功！' } else { Write-Host '安装失败，请检查网络连接或权限。' }; Read-Host '按 Enter 键关闭窗口...'"
        try {
            Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -Command $installCommand" -WindowStyle Normal -Wait
        } catch {
            Write-Host "启动安装窗口失败: $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "取消安装。"
        Read-Host "按 Enter 键退出..."
        exit
    }

    # 运行新手引导
    Write-Host
    $onboardChoice = Read-Host "是否进入新手引导并安装服务？ (y/n)"
    if ($onboardChoice -eq "y" -or $onboardChoice -eq "Y") {
        Write-Host "正在打开新窗口运行新手引导..."
        # 使用简单的命令参数
        $onboardCommand = "Write-Host '执行命令: openclaw onboard --install-daemon'; openclaw onboard --install-daemon; Write-Host '新手引导完成！'; Read-Host '按 Enter 键关闭窗口...'"
        try {
            Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -Command $onboardCommand" -WindowStyle Normal -Wait
        } catch {
            Write-Host "启动新手引导窗口失败: $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "跳过新手引导。"
    }

    Write-Host
    Write-Host "========================================="
    Write-Host "OpenClaw 安装和配置完成！"
    Write-Host "========================================="
    Read-Host "按 Enter 键退出..."
} catch {
    # 捕获全局错误
    Write-Host "脚本执行过程中发生错误: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "按 Enter 键退出..."
}
