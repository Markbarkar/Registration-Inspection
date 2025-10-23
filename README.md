# 网站注册检测系统

## 功能特性

- ✅ 检测邮箱是否在 stir.com 注册
- ✅ 支持批量检测
- ✅ 支持网络代理配置
- ✅ 现代化UI界面
- ✅ 可打包为独立exe程序

## 技术栈

### 后端
- Python 3.9+
- Flask (Web框架)
- requests (HTTP请求)
- flask-cors (跨域支持)

### 前端
- React 18
- Ant Design (UI组件库)
- Vite (构建工具)

## 环境配置

### 1. 安装Python依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 安装前端依赖

```bash
cd frontend
npm install
```

## 开发运行

### 启动后端服务

```bash
# 确保在项目根目录
python backend/app.py
```

后端服务将运行在 http://localhost:5000

### 启动前端开发服务器

```bash
cd frontend
npm run dev
```

前端服务将运行在 http://localhost:5173

## 打包为EXE

### 方法一：使用PyInstaller（推荐）

```bash
# 安装PyInstaller
pip install pyinstaller

# 打包
python build.py
```

打包完成后，可执行文件位于 `dist` 目录。

### 方法二：手动打包

```bash
# 1. 构建前端
cd frontend
npm run build

# 2. 打包后端和前端
cd ..
pyinstaller --name="注册检测系统" --onefile --windowed --add-data "frontend/dist:frontend/dist" backend/app.py
```

## 项目迁移

1. 复制整个项目文件夹到目标机器
2. 按照"环境配置"步骤安装依赖
3. 运行项目

或者直接使用打包好的exe文件，无需配置环境。

## 使用说明

1. 启动程序后，在界面中输入要检测的邮箱
2. 可以输入多个邮箱（每行一个）进行批量检测
3. 如需使用代理，在代理设置中配置代理地址
4. 点击"开始检测"按钮
5. 查看检测结果，支持导出为CSV

## 注意事项

- 请确保网络连接正常
- 使用代理时，请确保代理服务器可用
- 批量检测时建议设置适当的延迟，避免请求过快


