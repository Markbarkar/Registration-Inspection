@echo off
chcp 65001 >nul
echo ========================================
echo   网站注册检测系统 - 启动脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.9+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] 检查虚拟环境...
if not exist "venv" (
    echo 未找到虚拟环境，正在创建...
    python -m venv venv
    if errorlevel 1 (
        echo [错误] 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo 虚拟环境创建成功
)

echo [2/3] 激活虚拟环境并安装依赖...
call venv\Scripts\activate.bat

REM 检查是否已安装Flask
python -c "import flask" >nul 2>&1
if not errorlevel 1 (
    echo 依赖已安装，跳过安装步骤
    goto :start_server
)

echo 正在安装Python依赖...

REM 尝试清华镜像
pip install -r requirements.txt --trusted-host pypi.tuna.tsinghua.edu.cn -i https://pypi.tuna.tsinghua.edu.cn/simple >nul 2>&1
if not errorlevel 1 (
    echo 依赖安装成功
    goto :start_server
)

REM 尝试阿里云镜像
echo 尝试使用阿里云镜像...
pip install -r requirements.txt --trusted-host mirrors.aliyun.com -i https://mirrors.aliyun.com/pypi/simple/ >nul 2>&1
if not errorlevel 1 (
    echo 依赖安装成功
    goto :start_server
)

REM 尝试豆瓣镜像
echo 尝试使用豆瓣镜像...
pip install -r requirements.txt --trusted-host pypi.douban.com -i https://pypi.douban.com/simple/ >nul 2>&1
if not errorlevel 1 (
    echo 依赖安装成功
    goto :start_server
)

echo [警告] 依赖安装失败，请手动运行：
echo   venv\Scripts\activate.bat
echo   pip install Flask flask-cors requests pyinstaller --trusted-host pypi.tuna.tsinghua.edu.cn -i https://pypi.tuna.tsinghua.edu.cn/simple
echo.
pause

:start_server

echo [3/3] 启动服务...
echo.
echo ========================================
echo   服务已启动！
echo   访问地址: http://localhost:5000
echo   按 Ctrl+C 停止服务
echo ========================================
echo.

python backend\app.py

pause

