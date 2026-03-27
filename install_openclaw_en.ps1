# OpenClaw Installation Script
# PowerShell Implementation

# First switch to user directory
Write-Host "Switching to user directory..."
try {
    Set-Location -Path $env:USERPROFILE -ErrorAction Stop
    Write-Host "Current directory: $pwd"
} catch {
    Write-Host "Failed to switch directory: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Please manually switch to user directory and run this script again."
    Read-Host "Press Enter to exit..."
    exit
}
# Check if running as administrator
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    # If not administrator, restart self with admin privileges
    Start-Process -FilePath "powershell.exe" -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# Script body that requires administrator privileges
Write-Host "Script is running with administrator privileges..."
# Main script execution
try {
    # Check if Node.js is installed
    Write-Host "Checking Node.js environment..."
    $nodeFound = $false
    try {
        # Try to find node.exe in PATH
        $nodePath = Get-Command node -ErrorAction SilentlyContinue
        if ($nodePath) {
            $nodeVersion = node -v
            Write-Host "Node.js environment detected: $nodeVersion"
            $nodeFound = $true
        } else {
            # Check common installation paths
            $commonPaths = @(
                "$env:ProgramFiles\nodejs\node.exe",
                "$env:ProgramFiles (x86)\nodejs\node.exe",
                "$env:USERPROFILE\AppData\Local\Programs\nodejs\node.exe"
            )
            foreach ($path in $commonPaths) {
                if (Test-Path -Path $path) {
                    $nodeVersion = & $path -v
                    Write-Host "Node.js environment detected: $nodeVersion"
                    $nodeFound = $true
                    break
                }
            }
        }
    } catch {
        Write-Host "Error checking Node.js environment: $($_.Exception.Message)" -ForegroundColor Red
    }

    if (-not $nodeFound) {
        Write-Host "Node.js environment not detected."
        Write-Host
        $installNode = Read-Host "Would you like to automatically download and install Node.js? (y/n)"
        if ($installNode -eq "y" -or $installNode -eq "Y") {
            Write-Host "Getting latest Node.js LTS version..."
            try {
                # Try to get latest LTS version information
                $nodeMsiPath = "$env:USERPROFILE\nodejs.msi"
                
                # First try using fixed LTS version
                $ltsUrl = "https://nodejs.org/dist/v24.14.0/node-v24.14.0-x64.msi"
                Write-Host "Downloading Node.js v24.14.0 LTS version..."
                Write-Host "Download URL: $ltsUrl"
                Invoke-WebRequest -Uri $ltsUrl -OutFile $nodeMsiPath -ErrorAction Stop
                
                Write-Host "Installing Node.js LTS version..."
                Start-Process -FilePath "msiexec.exe" -ArgumentList "/i $nodeMsiPath /qn" -Wait
                if (Test-Path -Path $nodeMsiPath) {
                    Remove-Item -Path $nodeMsiPath -Force
                }
                Write-Host "Node.js LTS version installed successfully!"
                $needRestart = $true
            } catch {
                Write-Host "Failed to download or install Node.js: $($_.Exception.Message)" -ForegroundColor Red
                Write-Host "Please manually download and install Node.js LTS version."
                Write-Host "Download URL: https://nodejs.org/en/download"
                Read-Host "Press Enter to exit..."
                exit
            }
        } else {
            Write-Host "Please install Node.js before running this script."
            Write-Host "Download URL: https://nodejs.org/"
            Read-Host "Press Enter to exit..."
            exit
        }
    }

    # Check if Git is installed
    Write-Host "Checking Git environment..."
    $gitFound = $false
    try {
        # Try to find git.exe in PATH
        $gitPath = Get-Command git -ErrorAction SilentlyContinue
        if ($gitPath) {
            $gitVersion = git --version
            Write-Host "Git environment detected: $gitVersion"
            $gitFound = $true
        } else {
            # Check common installation paths
            $commonPaths = @(
                "$env:ProgramFiles\Git\bin\git.exe",
                "$env:ProgramFiles (x86)\Git\bin\git.exe",
                "$env:USERPROFILE\AppData\Local\Programs\Git\bin\git.exe"
            )
            foreach ($path in $commonPaths) {
                if (Test-Path -Path $path) {
                    $gitVersion = & $path --version
                    Write-Host "Git environment detected: $gitVersion"
                    $gitFound = $true
                    break
                }
            }
        }
    } catch {
        Write-Host "Error checking Git environment: $($_.Exception.Message)" -ForegroundColor Red
    }

    if (-not $gitFound) {
        Write-Host "Git environment not detected."
        Write-Host
        $installGit = Read-Host "Would you like to automatically install Git? (y/n)"
        if ($installGit -eq "y" -or $installGit -eq "Y") {
            Write-Host "Installing Git..."
            try {
                # Download and install directly from domestic source
                $gitExePath = "$env:USERPROFILE\git.exe"
                $gitUrl = "https://cdn.npmmirror.com/binaries/git-for-windows/v2.53.0.windows.1/Git-2.53.0-64-bit.exe"
                
                Write-Host "Downloading Git..."
                Write-Host "Download URL: $gitUrl"
                Invoke-WebRequest -Uri $gitUrl -OutFile $gitExePath -ErrorAction Stop
                Write-Host "Installing Git..."
                Start-Process -FilePath $gitExePath -Wait
                
                if (Test-Path -Path $gitExePath) {
                    Remove-Item -Path $gitExePath -Force
                }
                
                Write-Host "Git installed successfully!"
                $needRestart = $true
            } catch {
                Write-Host "Failed to download or install Git: $($_.Exception.Message)" -ForegroundColor Red
                Write-Host "Please manually download and install Git."
                Write-Host "Download URL: https://git-scm.com/download/win"
                Read-Host "Press Enter to exit..."
                exit
            }
        } else {
            Write-Host "Please install Git before running this script."
            Write-Host "Download URL: https://git-scm.com/download/win"
            Read-Host "Press Enter to exit..."
            exit
        }
    }

    # Check if script restart is needed
    if ($needRestart) {
        Write-Host
        Write-Host "Environment installation completed, please restart this script to continue installing OpenClaw."
        Read-Host "Press Enter to exit..."
        exit
    }

    # Install OpenClaw
    Write-Host "Preparing to install OpenClaw..."
    Write-Host
    $installChoice = Read-Host "Would you like to install OpenClaw? (y/n)"
    if ($installChoice -eq "y" -or $installChoice -eq "Y") {
        Write-Host "Opening new window to install OpenClaw..."
        # Use simple command parameters to avoid script block complexity
        $installCommand = "Write-Host 'Current directory: $pwd'; Write-Host 'Installing OpenClaw...'; npm install -g openclaw@latest; if ($LASTEXITCODE -eq 0) { Write-Host 'OpenClaw installed successfully!' } else { Write-Host 'Installation failed, please check network connection or permissions.' }; Read-Host 'Press Enter to close window...'"
        try {
            Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -Command $installCommand" -WindowStyle Normal -Wait
        } catch {
            Write-Host "Failed to start installation window: $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "Installation cancelled."
        Read-Host "Press Enter to run onboarding..."
    }

    # Run onboarding
    Write-Host
    $onboardChoice = Read-Host "Would you like to run onboarding and install services? (y/n)"
    if ($onboardChoice -eq "y" -or $onboardChoice -eq "Y") {
        Write-Host "Opening new window to run onboarding..."
        # Use simple command parameters
        $onboardCommand = "Write-Host 'Executing command: openclaw onboard --install-daemon'; openclaw onboard --install-daemon; Write-Host 'Onboarding completed!'; Read-Host 'Press Enter to close window...'"
        try {
            Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -Command $onboardCommand" -WindowStyle Normal -Wait
        } catch {
            Write-Host "Failed to start onboarding window: $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "Skipping onboarding."
    }

    Write-Host
    Write-Host "========================================="
    Write-Host "OpenClaw installation and configuration completed!"
    Write-Host "========================================="
    Read-Host "Press Enter to exit..."
} catch {
    # Catch global errors
    Write-Host "Error occurred during script execution: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
}
