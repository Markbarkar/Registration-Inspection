# 打包成 EXE 文件指南

## 方案概述

本项目包含前端（React）和后端（Flask），有两种打包方案：

### 方案1：仅打包后端（推荐）
- 后端打包成 exe
- 前端构建后嵌入后端
- 优点：单个 exe 文件，简单易用
- 缺点：文件较大（约50-100MB）

### 方案2：前后端分别打包
- 后端打包成 exe
- 前端打包成独立应用
- 优点：灵活性高
- 缺点：需要分别启动

## 推荐方案：前后端一体化打包

### 步骤1：构建前端

```bash
cd /Users/linzaizai/Desktop/check_register/frontend
npm run build
```

这会在 `frontend/dist` 目录生成静态文件。

### 步骤2：修改后端，集成前端

创建新文件 `backend/app_standalone.py`：

```python
"""
独立运行版本 - 集成前端静态文件
"""
from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import sys

# 导入原有的 app.py 内容
from app import app, checker

# 获取资源路径（支持打包后的路径）
def get_resource_path(relative_path):
    """获取资源文件的绝对路径"""
    try:
        # PyInstaller 创建临时文件夹，路径存储在 _MEIPASS 中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 前端静态文件路径
FRONTEND_DIST = get_resource_path('frontend_dist')

# 添加前端路由
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """提供前端静态文件"""
    if path != "" and os.path.exists(os.path.join(FRONTEND_DIST, path)):
        return send_from_directory(FRONTEND_DIST, path)
    else:
        return send_from_directory(FRONTEND_DIST, 'index.html')

if __name__ == '__main__':
    print("=" * 50)
    print("网站注册检测系统")
    print("访问地址: http://localhost:5001")
    print("=" * 50)
    
    # 自动打开浏览器
    import webbrowser
    import threading
    def open_browser():
        import time
        time.sleep(1.5)
        webbrowser.open('http://localhost:5001')
    
    threading.Thread(target=open_browser).start()
    
    # 启动服务
    app.run(host='0.0.0.0', port=5001, debug=False)
```

### 步骤3：创建 PyInstaller 配置文件

创建 `build_exe.spec`：

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['backend/app_standalone.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('frontend/dist', 'frontend_dist'),  # 包含前端文件
        ('backend/uploads', 'uploads'),      # 包含上传文件夹
        ('backend/results', 'results'),      # 包含结果文件夹
    ],
    hiddenimports=[
        'flask',
        'flask_cors',
        'cloudscraper',
        'requests',
        'werkzeug',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='StirEmailChecker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 显示控制台窗口（可以看到日志）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加图标文件路径
)
```

### 步骤4：执行打包

```bash
cd /Users/linzaizai/Desktop/check_register

# 激活虚拟环境
source venv/bin/activate

# 使用 spec 文件打包
pyinstaller build_exe.spec

# 或者使用命令行方式（不推荐，spec 文件更灵活）
# pyinstaller --onefile \
#   --name StirEmailChecker \
#   --add-data "frontend/dist:frontend_dist" \
#   --add-data "backend/uploads:uploads" \
#   --add-data "backend/results:results" \
#   --hidden-import flask \
#   --hidden-import flask_cors \
#   --hidden-import cloudscraper \
#   backend/app_standalone.py
```

### 步骤5：测试 EXE

```bash
# 打包完成后，exe 文件在 dist 目录
cd dist
./StirEmailChecker  # Mac/Linux
# 或
StirEmailChecker.exe  # Windows
```

## 详细步骤（完整版）

### 1. 准备工作

```bash
cd /Users/linzaizai/Desktop/check_register

# 确保虚拟环境已激活
source venv/bin/activate

# 确保 pyinstaller 已安装
pip install pyinstaller

# 确保前端依赖已安装
cd frontend
npm install
cd ..
```

### 2. 构建前端

```bash
cd frontend
npm run build
cd ..
```

验证构建结果：
```bash
ls -la frontend/dist/
# 应该看到 index.html, assets/ 等文件
```

### 3. 创建独立后端文件

创建 `backend/app_standalone.py`（内容见上方）

### 4. 创建打包配置

创建 `build_exe.spec`（内容见上方）

### 5. 执行打包

```bash
# 在项目根目录
pyinstaller build_exe.spec --clean
```

参数说明：
- `--clean`：清理之前的构建缓存
- `--noconfirm`：不询问，直接覆盖

### 6. 查看结果

```bash
ls -lh dist/
# 应该看到 StirEmailChecker 可执行文件
```

### 7. 测试运行

```bash
cd dist
./StirEmailChecker
```

应该会：
1. 启动后端服务
2. 自动打开浏览器
3. 显示应用界面

## 优化建议

### 1. 减小文件大小

在 `build_exe.spec` 中添加排除项：

```python
excludes=[
    'matplotlib',
    'numpy',
    'pandas',
    'PIL',
    'tkinter',
    'test',
    'unittest',
],
```

### 2. 添加应用图标

```python
# 在 EXE() 中添加
icon='path/to/icon.ico'  # Windows
icon='path/to/icon.icns'  # Mac
```

### 3. 隐藏控制台窗口

如果不需要看到控制台日志：

```python
console=False,  # 改为 False
```

### 4. 添加版本信息（Windows）

创建 `version_info.txt`：

```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [StringStruct(u'CompanyName', u'Your Company'),
          StringStruct(u'FileDescription', u'Stir Email Checker'),
          StringStruct(u'FileVersion', u'1.0.0.0'),
          StringStruct(u'InternalName', u'StirEmailChecker'),
          StringStruct(u'LegalCopyright', u'Copyright (c) 2025'),
          StringStruct(u'OriginalFilename', u'StirEmailChecker.exe'),
          StringStruct(u'ProductName', u'Stir Email Checker'),
          StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

在 spec 文件中引用：
```python
version='version_info.txt',
```

## Windows 打包注意事项

如果在 Windows 上打包：

1. **安装 Visual C++ Redistributable**
   - 下载：https://aka.ms/vs/17/release/vc_redist.x64.exe
   - 安装后再打包

2. **路径分隔符**
   ```python
   # 使用 os.path.join 而不是硬编码路径
   os.path.join('frontend', 'dist')
   ```

3. **杀毒软件**
   - 打包的 exe 可能被误报为病毒
   - 添加到白名单或使用代码签名

## Mac 打包注意事项

1. **权限问题**
   ```bash
   chmod +x dist/StirEmailChecker
   ```

2. **创建 .app 包**
   ```python
   # 在 spec 文件中使用 BUNDLE
   app = BUNDLE(exe,
                name='StirEmailChecker.app',
                icon='icon.icns',
                bundle_identifier='com.yourcompany.stir')
   ```

## 故障排除

### 问题1：找不到模块

**错误**：`ModuleNotFoundError: No module named 'xxx'`

**解决**：在 spec 文件的 `hiddenimports` 中添加：
```python
hiddenimports=[
    'flask',
    'flask_cors',
    'cloudscraper',
    'requests',
    'werkzeug',
    'xxx',  # 添加缺失的模块
],
```

### 问题2：前端文件找不到

**错误**：404 Not Found

**解决**：
1. 确认 `frontend/dist` 存在
2. 检查 spec 文件中的 datas 路径
3. 验证 `get_resource_path()` 函数

### 问题3：文件太大

**解决**：
1. 使用 UPX 压缩：`upx=True`
2. 排除不必要的模块
3. 使用 `--onedir` 而不是 `--onefile`

### 问题4：运行时崩溃

**调试**：
1. 设置 `console=True` 查看错误信息
2. 使用 `--debug=all` 打包
3. 检查日志文件

## 分发建议

### 1. 创建安装包

**Windows**：使用 Inno Setup 或 NSIS

**Mac**：创建 DMG 文件
```bash
hdiutil create -volname "Stir Email Checker" -srcfolder dist/StirEmailChecker.app -ov -format UDZO StirEmailChecker.dmg
```

### 2. 提供使用说明

创建 `README_USER.txt`：
```
Stir Email Checker 使用说明

1. 双击运行 StirEmailChecker.exe
2. 浏览器会自动打开应用界面
3. 如未自动打开，手动访问 http://localhost:5001
4. 按照界面提示使用

注意事项：
- 首次运行可能需要允许防火墙访问
- 建议配置代理池以提高检测成功率
- 结果文件保存在程序目录的 results 文件夹
```

### 3. 包含必要文件

```
发布包/
├── StirEmailChecker.exe
├── README_USER.txt
├── 使用说明.pdf
└── 示例文件/
    └── test_emails.txt
```

## 完整打包脚本

创建 `build.sh`（Mac/Linux）或 `build.bat`（Windows）：

```bash
#!/bin/bash
# build.sh

echo "开始构建 Stir Email Checker..."

# 1. 构建前端
echo "步骤 1/3: 构建前端..."
cd frontend
npm run build
cd ..

# 2. 清理旧文件
echo "步骤 2/3: 清理旧构建..."
rm -rf build dist *.spec

# 3. 打包
echo "步骤 3/3: 打包应用..."
source venv/bin/activate
pyinstaller build_exe.spec --clean

echo "构建完成！"
echo "可执行文件位置: dist/StirEmailChecker"
```

使用：
```bash
chmod +x build.sh
./build.sh
```

## 总结

推荐使用**方案1（前后端一体化）**：

1. ✅ 构建前端：`cd frontend && npm run build`
2. ✅ 创建 `backend/app_standalone.py`
3. ✅ 创建 `build_exe.spec`
4. ✅ 执行打包：`pyinstaller build_exe.spec`
5. ✅ 测试运行：`dist/StirEmailChecker`

打包后的文件可以直接分发给用户使用，无需安装 Python 或 Node.js 环境！

