# OpenClaw 安装和配置工具

## 目录结构

```
install/
├── config_gui.py        # OpenClaw 配置修改工具
├── install_openclaw.ps1  # OpenClaw 安装脚本（PowerShell）
└── start_openclaw.bat   # OpenClaw 启动脚本
```

## 文件说明

### 1. install_openclaw.ps1

这是一个 PowerShell 脚本，用于自动安装 OpenClaw 及其依赖项。

**功能**：
- 首先切换到用户目录
- 检查并自动安装 Node.js（如果未安装）
- 检查并自动安装 Git（如果未安装）
- 安装 OpenClaw 最新版本
- 运行 OpenClaw 新手引导并安装服务
- 详细的错误处理，避免脚本闪退

**使用方法**：
1. 右键点击 `install_openclaw.ps1` 文件
2. 选择 "以管理员身份运行"（PowerShell）
3. 按照提示操作即可完成整个安装过程

**注意事项**：
- 安装 Git 时请确保勾选 "Git from the command line" 选项
- 安装过程中会打开新的 PowerShell 窗口执行安装和配置操作
- 脚本会自动设置执行策略为 RemoteSigned，确保脚本可以正常运行

### 2. start_openclaw.bat

这是一个批处理脚本，用于启动 OpenClaw 网关并打开浏览器访问。

**功能**：
- 检查 OpenClaw 是否安装
- 执行 OpenClaw 登录（忽略结果）
- 启动 OpenClaw 网关（端口 18789）
- 自动打开浏览器访问网关
- 按任意键停止网关并退出

**使用方法**：
1. 双击运行 `start_openclaw.bat` 文件
2. 等待网关启动并自动打开浏览器
3. 使用完成后，按任意键停止网关

### 3. config_gui.py

这是一个 Python 图形界面工具，用于修改 OpenClaw 的配置文件。

**功能**：
- 图形化界面修改 OpenClaw 配置
- 支持修改元数据、模型配置、代理配置和网关配置
- 可以从 API 获取模型列表
- 自动备份配置文件

**使用方法**：
1. 确保已安装 Python 和 tkinter
2. 运行 `python config_gui.py`
3. 在界面中选择配置文件并进行修改
4. 点击 "保存配置" 保存更改

**配置选项**：
- **元数据**：版本号、最后修改时间
- **模型配置**：模型模式、提供者名称、baseUrl、apiKey、模型ID等
- **代理配置**：主模型、工作目录、最大并发数
- **网关配置**：端口、模式、绑定地址、认证令牌

## 安装流程

1. 运行 `install_openclaw.ps1` 安装 OpenClaw 及其依赖
2. 完成新手引导配置
3. 运行 `start_openclaw.bat` 启动 OpenClaw 网关
4. 使用 `config_gui.py` 根据需要修改配置

## 常见问题

### 1. 安装失败
- 检查网络连接是否正常
- 确保以管理员身份运行安装脚本
- 检查 Node.js 和 Git 是否正确安装
- 查看脚本输出的错误信息以了解具体问题

### 2. 启动失败
- 检查 OpenClaw 是否正确安装
- 确保 OpenClaw 已添加到系统 PATH
- 检查端口 18789 是否被占用

### 3. 配置问题
- 使用 `config_gui.py` 检查并修改配置
- 确保 API 密钥和模型配置正确

## 技术支持

如果遇到问题，请参考 OpenClaw 官方文档或联系技术支持。