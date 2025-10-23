# 环境配置指南

本文档详细说明如何在新机器上快速配置和运行本项目。

## 前置要求

### 1. Python环境
- **版本要求**: Python 3.9 或更高版本
- **下载地址**: https://www.python.org/downloads/

#### Windows安装Python
1. 下载Python安装包
2. 运行安装程序，**务必勾选** "Add Python to PATH"
3. 安装完成后，打开命令提示符，输入 `python --version` 验证安装

#### macOS安装Python
```bash
# 使用Homebrew安装（推荐）
brew install python@3.9

# 或从官网下载安装包
```

#### Linux安装Python
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.9 python3.9-venv python3-pip

# CentOS/RHEL
sudo yum install python39 python39-pip
```

### 2. Node.js环境（仅开发时需要）
- **版本要求**: Node.js 18 或更高版本
- **下载地址**: https://nodejs.org/

## 快速开始

### 方法一：使用打包好的exe（推荐）

如果已有打包好的exe文件：
1. 双击运行 `注册检测系统.exe`
2. 系统会自动启动，浏览器访问 http://localhost:5000

### 方法二：从源码运行

#### 步骤1: 克隆或复制项目

将整个项目文件夹复制到目标机器。

#### 步骤2: 配置Python虚拟环境（推荐）

```bash
# 进入项目目录
cd check_register

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 步骤3: 安装Python依赖

```bash
pip install -r requirements.txt
```

如果安装速度慢，可以使用国内镜像：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 步骤4: 安装前端依赖（仅开发时需要）

```bash
cd frontend
npm install

# 如果npm速度慢，可以使用淘宝镜像
npm install --registry=https://registry.npmmirror.com
```

#### 步骤5: 运行项目

**开发模式（前后端分离）:**

终端1 - 启动后端:
```bash
# 确保在项目根目录
python backend/app.py
```

终端2 - 启动前端:
```bash
cd frontend
npm run dev
```

访问: http://localhost:5173

**生产模式（前后端一体）:**

```bash
# 1. 先构建前端
cd frontend
npm run build

# 2. 启动后端（会自动服务前端静态文件）
cd ..
python backend/app.py
```

访问: http://localhost:5000

## 打包为exe

### 步骤1: 确保已安装所有依赖

```bash
pip install -r requirements.txt
```

### 步骤2: 构建前端

```bash
cd frontend
npm run build
cd ..
```

### 步骤3: 执行打包脚本

```bash
python build.py
```

打包完成后，可执行文件位于 `dist` 目录。

### 手动打包（如果自动脚本失败）

```bash
# 1. 构建前端
cd frontend
npm run build
cd ..

# 2. 使用PyInstaller打包
# Windows:
pyinstaller --name=注册检测系统 --onefile --windowed --add-data "frontend/dist;frontend/dist" backend/app.py

# macOS/Linux:
pyinstaller --name=注册检测系统 --onefile --windowed --add-data "frontend/dist:frontend/dist" backend/app.py
```

## 常见问题

### 1. Python命令不可用

**问题**: 输入 `python` 提示命令不存在

**解决**:
- Windows: 确保安装时勾选了 "Add Python to PATH"，或手动添加Python到系统PATH
- macOS/Linux: 尝试使用 `python3` 代替 `python`

### 2. pip安装依赖失败

**问题**: pip安装时出现网络错误或超时

**解决**:
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. npm安装依赖失败

**问题**: npm install 时出现网络错误

**解决**:
```bash
# 使用淘宝镜像
npm install --registry=https://registry.npmmirror.com
```

### 4. 端口被占用

**问题**: 启动时提示端口5000已被占用

**解决**:
- 方法1: 关闭占用端口的程序
- 方法2: 修改 `backend/app.py` 最后一行的端口号

### 5. 打包后exe无法运行

**问题**: 双击exe没有反应或闪退

**解决**:
1. 去掉 `--windowed` 参数重新打包，查看错误信息
2. 确保前端已正确构建（frontend/dist目录存在）
3. 检查是否缺少依赖库

### 6. 检测功能不工作

**问题**: 点击检测后没有结果或报错

**解决**:
1. 检查网络连接
2. 如果stir.com需要特殊访问，配置代理
3. 查看浏览器控制台和后端日志

## 代理配置

如果需要通过代理访问stir.com：

1. 点击界面上的"代理设置"按钮
2. 输入代理地址，格式如下：
   - HTTP代理: `http://127.0.0.1:7890`
   - SOCKS5代理: `socks5://127.0.0.1:1080`
3. 点击"测试连接"验证代理是否可用

## 技术支持

如遇到其他问题，请检查：
1. Python版本是否符合要求（3.9+）
2. 所有依赖是否正确安装
3. 防火墙是否阻止了程序运行
4. 杀毒软件是否误报

## 项目结构

```
check_register/
├── backend/              # 后端代码
│   ├── app.py           # Flask应用主文件
│   ├── checker.py       # 检测逻辑
│   └── __init__.py
├── frontend/            # 前端代码
│   ├── src/            # 源代码
│   ├── dist/           # 构建输出（npm run build后生成）
│   ├── package.json    # 依赖配置
│   └── vite.config.js  # Vite配置
├── requirements.txt     # Python依赖
├── build.py            # 打包脚本
├── README.md           # 项目说明
├── SETUP.md            # 本文档
└── .gitignore          # Git忽略文件
```



