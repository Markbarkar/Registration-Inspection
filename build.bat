@echo off
REM 自动化构建脚本 - Windows

echo ========================================================================
echo 🚀 Stir Email Checker - 自动构建脚本
echo ========================================================================

REM 检查 Node.js
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 错误: 未找到 Node.js，请先安装
    pause
    exit /b 1
)

REM 检查 Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 错误: 未找到 Python，请先安装
    pause
    exit /b 1
)

REM 步骤 1: 构建前端
echo.
echo 📦 步骤 1/4: 构建前端...
echo ------------------------------------------------------------------------
cd frontend

if not exist "node_modules" (
    echo    安装前端依赖...
    call npm install
)

echo    构建前端...
call npm run build

if not exist "dist" (
    echo ❌ 错误: 前端构建失败，未找到 dist 目录
    pause
    exit /b 1
)

echo ✅ 前端构建完成
cd ..

REM 步骤 2: 准备 Python 环境
echo.
echo 🐍 步骤 2/4: 准备 Python 环境...
echo ------------------------------------------------------------------------

if not exist "venv" (
    echo    创建虚拟环境...
    python -m venv venv
)

echo    激活虚拟环境...
call venv\Scripts\activate.bat

echo    检查依赖...
pip install -q pyinstaller

echo ✅ Python 环境准备完成

REM 步骤 3: 清理旧文件
echo.
echo 🧹 步骤 3/4: 清理旧构建...
echo ------------------------------------------------------------------------
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "__pycache__" rmdir /s /q __pycache__
echo ✅ 清理完成

REM 步骤 4: 打包应用
echo.
echo 📦 步骤 4/4: 打包应用...
echo ------------------------------------------------------------------------
pyinstaller build_exe.spec --clean --noconfirm

if not exist "dist\StirEmailChecker.exe" (
    echo ❌ 错误: 打包失败，未找到可执行文件
    pause
    exit /b 1
)

echo ✅ 打包完成

REM 显示结果
echo.
echo ========================================================================
echo 🎉 构建成功！
echo ========================================================================
echo 📁 可执行文件位置: %CD%\dist\StirEmailChecker.exe
echo.
echo 🚀 运行测试:
echo    cd dist
echo    StirEmailChecker.exe
echo.
echo ========================================================================
pause

