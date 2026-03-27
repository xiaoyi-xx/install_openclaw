# OpenClaw 安装和配置工具

本项目提供了一套完整的 OpenClaw 安装、启动和配置工具，支持 Windows 平台的自动化部署和图形化配置管理。

## 目录结构

```
install/
├── start/                # 启动相关脚本
│   ├── gateway.bat       # 网关启动脚本
│   ├── gateway_nocn.bat  # 网关启动脚本（无中文）
│   ├── open_browser.bat  # 浏览器打开脚本
│   └── open_browser_nocn.bat  # 浏览器打开脚本（无中文）
├── LICENSE               # 许可证文件
├── README.md             # 英文说明文档
├── README_zh.md          # 中文说明文档
├── config_gui.py         # OpenClaw 配置修改工具（Python GUI）
├── install_openclaw.ps1  # OpenClaw 安装脚本（PowerShell，中文）
├── install_openclaw_en.ps1  # OpenClaw 安装脚本（PowerShell，英文）
├── start_openclaw.bat    # OpenClaw 启动脚本（批处理）
└── start_openclaw_nocn.bat  # OpenClaw 启动脚本（无中文）
```

## 快速开始

### 1. 安装 OpenClaw

#### 中文版本（推荐）
运行 PowerShell 安装脚本，自动完成所有依赖项的安装：

```powershell
# 右键点击 install_openclaw.ps1，选择"以PowerShell运行"
```

#### 英文版本
如果您使用英文系统或更喜欢英文界面，可以使用英文版本的安装脚本：

```powershell
# 右键点击 install_openclaw_en.ps1，选择"以PowerShell运行"
```

安装脚本会自动完成以下操作：
- 切换到用户目录
- 自动检查并获取管理员权限
- 检测并安装 Node.js（如未安装）
- 检测并安装 Git（如未安装）
- 安装 OpenClaw 最新版本
- 运行新手引导并配置服务
- 完善的错误处理和提示

### 2. 启动 OpenClaw

双击运行启动脚本：

```bash
start_openclaw.bat
```

脚本会自动：
- 检查 OpenClaw 安装状态
- 执行登录操作
- 启动网关（端口 18789）
- 自动打开浏览器访问网关
- 按任意键停止网关服务

**备选启动方案：**
如果遇到启动失败或中文显示问题，可以使用无中文版本的启动脚本：

```bash
start_openclaw_nocn.bat
```

### 3. 配置管理

使用图形界面工具修改配置：

```bash
python config_gui.py
```

## 文件说明

### install_openclaw.ps1

PowerShell 自动化安装脚本（中文版本），负责部署完整的 OpenClaw 环境。

**主要功能：**
- 自动切换到用户目录
- 自动检查并获取管理员权限
- Node.js 自动检测与安装（LTS 版本 v24.14.0）
- Git 自动检测与安装（从国内源下载）
- OpenClaw 最新版安装
- 新手引导自动执行
- 服务安装与配置
- 完善的错误处理机制
- 中文友好的提示信息

**使用前提：**
- Windows 7 或更高版本
- 稳定的网络连接
- 脚本会自动请求管理员权限

### install_openclaw_en.ps1

PowerShell 自动化安装脚本（英文版本），功能与中文版本相同，但所有提示信息均为英文。

**适用场景：**
- 英文 Windows 系统
- 非中文语言环境
- 喜欢英文界面的用户

### start_openclaw.bat

批处理启动脚本，用于快速启动 OpenClaw 网关服务。

**主要功能：**
- 安装状态检查
- 自动登录验证
- 网关启动（端口 18789）
- 浏览器自动打开
- 便捷的停止机制

**使用说明：**
双击运行后，等待网关启动完成，浏览器会自动打开。操作完成后按任意键停止服务。

### start_openclaw_nocn.bat

无中文版本的启动脚本，适用于：
- 英文系统或非中文环境
- 中文显示乱码问题
- 主启动脚本启动失败的情况

**使用方法：**
```bash
# 双击运行
start_openclaw_nocn.bat
```

### config_gui.py

Python 图形界面配置管理工具，提供可视化的配置修改功能。

**主要功能：**
- 图形化配置界面
- 多种配置类型管理
- API 模型列表获取
- 配置文件自动备份
- 实时配置预览

**配置选项：**

| 分类 | 包含内容 |
|------|----------|
| 元数据 | 版本号、最后修改时间 |
| 模型配置 | 模型模式、提供者名称、baseUrl、apiKey、模型ID |
| 代理配置 | 主模型、工作目录、最大并发数 |
| 网关配置 | 端口、模式、绑定地址、认证令牌 |

**依赖项：**
- Python 3.x
- tkinter（Python 内置）

### start/ 目录

包含启动相关的辅助脚本：

- **gateway.bat**：专门用于启动 OpenClaw 网关服务
- **gateway_nocn.bat**：网关启动脚本（无中文）
- **open_browser.bat**：专门用于打开浏览器访问网关
- **open_browser_nocn.bat**：浏览器打开脚本（无中文）

## 详细安装流程

### 步骤一：运行安装脚本

#### 中文版本
1. 找到 `install_openclaw.ps1` 文件
2. 右键点击 → 选择"以PowerShell运行"
3. 如弹出 UAC 提示，请点击"是"授予管理员权限
4. 按照提示完成安装

#### 英文版本
1. 找到 `install_openclaw_en.ps1` 文件
2. 右键点击 → 选择"以PowerShell运行"
3. 如弹出 UAC 提示，请点击"是"授予管理员权限
4. 按照提示完成安装

### 步骤二：环境检测与安装

脚本会自动：
- 检测 Node.js 环境，如未安装则自动下载并安装
- 检测 Git 环境，如未安装则从国内源自动下载并安装
- 安装完成后会提示重启脚本以继续

### 步骤三：OpenClaw 安装

1. 环境准备完成后，脚本会提示是否安装 OpenClaw
2. 确认后会打开新窗口执行安装
3. 安装完成后会显示安装结果

### 步骤四：新手引导配置

1. 安装完成后，脚本会提示是否进入新手引导
2. 确认后会打开新窗口执行新手引导
3. 按照提示完成服务配置

### 步骤五：启动服务

```bash
# 双击运行
start_openclaw.bat

# 如果遇到启动问题，尝试使用无中文版本
# start_openclaw_nocn.bat
```

### 步骤六：（可选）修改配置

如需调整配置：

```bash
# 运行配置工具
python config_gui.py
```

## 常见问题

### 安装失败

**可能原因：**
- 网络连接不稳定
- 权限不足
- 依赖项安装失败
- 下载源访问问题

**解决方案：**
- 检查网络连接
- 确保以管理员权限运行
- 确认 Node.js 和 Git 已正确安装
- 查看脚本输出的错误信息
- 如下载失败，可手动下载并安装依赖项

### 启动失败

**可能原因：**
- OpenClaw 未正确安装
- 环境变量未配置
- 端口被占用
- 中文显示问题

**解决方案：**
- 确认 OpenClaw 已成功安装
- 检查 PATH 环境变量
- 检查端口 18789 占用情况
- 尝试使用无中文版本的启动脚本：`start_openclaw_nocn.bat`
- 重新运行安装脚本修复问题

### 配置问题

**可能原因：**
- 配置文件格式错误
- API 密钥无效
- 模型配置不正确

**解决方案：**
- 使用 `config_gui.py` 检查配置
- 确认 API 密钥有效
- 验证模型参数
- 参考 OpenClaw 官方文档

## 技术支持

如遇问题，请参考：
- OpenClaw 官方文档
- 社区技术支持渠道

## 许可证

本项目仅提供安装和配置工具，相关许可证请参考 OpenClaw 主项目。

---

**其他语言版本：** [English README](README.md)