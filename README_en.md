# OpenClaw Installation and Configuration Tools

This project provides a complete set of tools for installing, starting, and configuring OpenClaw, supporting automated deployment and graphical configuration management on Windows platforms.

## Directory Structure

```
install_openclaw/
├── start/                # Startup-related scripts
│   ├── gateway.bat       # Gateway startup script
│   ├── gateway_nocn.bat  # Gateway startup script (no Chinese)
│   ├── open_browser.bat  # Browser opening script
│   └── open_browser_nocn.bat  # Browser opening script (no Chinese)
├── LICENSE               # License file
├── README.md             # Chinese documentation
├── README_en.md          # English documentation
├── config_gui.py         # OpenClaw configuration modification tool (Python GUI)
├── install_openclaw.ps1  # OpenClaw installation script (PowerShell, Chinese)
├── install_openclaw_en.ps1  # OpenClaw installation script (PowerShell, English)
├── start_openclaw.bat    # OpenClaw startup script (batch)
└── start_openclaw_nocn.bat  # OpenClaw startup script (no Chinese)
```

## Quick Start

### 1. Install OpenClaw

#### Chinese Version (Recommended)

Run the PowerShell installation script to automatically install all dependencies:

```powershell
# Right-click OpenClaw.ps1 and select "Run with PowerShell"
```

#### English Version

If you use an English system or prefer an English interface, you can use the English version of the installation script:

```powershell
# Right-click OpenClaw_en.ps1 and select "Run with PowerShell"
```

The installation script will automatically perform the following operations:

- Switch to user directory
- Automatically check and obtain administrator privileges
- Detect and install Node.js (if not installed)
- Detect and install Git (if not installed)
- Install the latest version of OpenClaw
- Run onboarding and configure services
- Comprehensive error handling and prompts

### 2. Start OpenClaw

Double-click the startup script:

```bash
start_openclaw.bat
```

The script will automatically:

- Check OpenClaw installation status
- Perform login operation
- Start gateway (port 18789)
- Automatically open browser to access gateway
- Press any key to stop gateway service

**Alternative Startup Option:**
If you encounter startup failure or Chinese display issues, you can use the no-Chinese version of the startup script:

```bash
start_openclaw_nocn.bat
```

### 3. Configuration Management

Use the graphical interface tool to modify configuration:

```bash
python config_gui.py
```

## File Descriptions

### install_openclaw\_openclaw\.ps1

PowerShell automated installation script (Chinese version), responsible for deploying the complete OpenClaw environment.

**Main features:**

- Automatically switch to user directory
- Automatically check and obtain administrator privileges
- Node.js automatic detection and installation (LTS version v24.14.0)
- Git automatic detection and installation (download from domestic source)
- Latest OpenClaw version installation
- Automatic onboarding execution
- Service installation and configuration
- Comprehensive error handling mechanism
- Chinese-friendly prompt messages

**Prerequisites:**

- Windows 7 or higher
- Stable network connection
- Script will automatically request administrator privileges

### install_openclaw\_openclaw\_en.ps1

PowerShell automated installation script (English version), with the same functionality as the Chinese version but all prompt messages are in English.

**Applicable scenarios:**

- English Windows systems
- Non-Chinese language environments
- Users who prefer English interface

### start\_openclaw\.bat

Batch startup script for quickly starting OpenClaw gateway service.

**Main features:**

- Installation status check
- Automatic login verification
- Gateway startup (port 18789)
- Automatic browser opening
- Convenient stop mechanism

**Usage instructions:**
After double-clicking to run, wait for the gateway to start completely, and the browser will open automatically. After operation is complete, press any key to stop the service.

### start\_openclaw\_nocn.bat

No-Chinese version of the startup script, suitable for:

- English systems or non-Chinese environments
- Chinese display garbled issues
- Main startup script failure situations

**Usage method:**

```bash
# Double-click to run
start_openclaw_nocn.bat
```

### config\_gui.py

Python graphical interface configuration management tool, providing visual configuration modification functionality.

**Main features:**

- Graphical configuration interface
- Multiple configuration type management
- API model list retrieval
- Automatic configuration file backup
- Real-time configuration preview

**Configuration options:**

| Category              | Content                                              |
| :-------------------- | :--------------------------------------------------- |
| Metadata              | Version number, last modified time                   |
| Model Configuration   | Model mode, provider name, baseUrl, apiKey, model ID |
| Proxy Configuration   | Main model, working directory, maximum concurrency   |
| Gateway Configuration | Port, mode, binding address, authentication token    |

**Dependencies:**

- Python 3.x
- tkinter (built-in with Python)

### start/ Directory

Contains startup-related auxiliary scripts:

- **gateway.bat**: Specifically used to start OpenClaw gateway service
- **gateway\_nocn.bat**: Gateway startup script (no Chinese)
- **open\_browser.bat**: Specifically used to open browser to access gateway
- **open\_browser\_nocn.bat**: Browser opening script (no Chinese)

## Detailed Installation Process

### Step 1: Run Installation Script

#### Chinese Version

1. Find the `install_openclaw.ps1` file
2. Right-click → select "Run with PowerShell"
3. If UAC prompt appears, click "Yes" to grant administrator privileges
4. Follow the prompts to complete installation

#### English Version

1. Find the `install_openclaw_en.ps1` file
2. Right-click → select "Run with PowerShell"
3. If UAC prompt appears, click "Yes" to grant administrator privileges
4. Follow the prompts to complete installation

### Step 2: Environment Detection and Installation

The script will automatically:

- Detect Node.js environment, automatically download and install if not installed
- Detect Git environment, automatically download and install from domestic source if not installed
- After installation, prompt to restart the script to continue

### Step 3: OpenClaw Installation

1. After environment preparation is complete, the script will prompt whether to install OpenClaw
2. After confirmation, a new window will open to execute the installation
3. After installation is complete, the installation result will be displayed

### Step 4: Onboarding Configuration

1. After installation is complete, the script will prompt whether to enter onboarding
2. After confirmation, a new window will open to execute onboarding
3. Follow the prompts to complete service configuration

### Step 5: Start Service

```bash
# Double-click to run
start_openclaw.bat

# If you encounter startup issues, try using the no-Chinese version
# start_openclaw_nocn.bat
```

### Step 6: (Optional) Modify Configuration

If you need to adjust configuration:

```bash
# Run configuration tool
python config_gui.py
```

## Common Issues

### Installation Failure

**Possible causes:**

- Unstable network connection
- Insufficient permissions
- Dependency installation failure
- Download source access issues

**Solutions:**

- Check network connection
- Ensure running with administrator privileges
- Confirm Node.js and Git are correctly installed
- Check script output error messages
- If download fails, manually download and install dependencies

### Startup Failure

**Possible causes:**

- OpenClaw not correctly installed
- Environment variables not configured
- Port occupied
- Chinese display issues

**Solutions:**

- Confirm OpenClaw is successfully installed
- Check PATH environment variable
- Check port 18789 occupancy
- Try using the no-Chinese version of the startup script: `start_openclaw_nocn.bat`
- Re-run the installation script to fix issues

### Configuration Issues

**Possible causes:**

- Configuration file format error
- Invalid API key
- Incorrect model configuration

**Solutions:**

- Use `config_gui.py` to check configuration
- Confirm API key is valid
- Verify model parameters
- Refer to OpenClaw official documentation

## Technical Support

If you encounter issues, please refer to:

- OpenClaw official documentation
- Community technical support channels

## License

This project only provides installation and configuration tools. For related licenses, please refer to the OpenClaw main project.

***

**Other language version:** [中文 README](README_zh.md)
