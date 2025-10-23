#!/bin/bash

echo "========================================"
echo "  网站注册检测系统 - 启动脚本"
echo "========================================"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python3，请先安装Python 3.9+"
    exit 1
fi

echo "[1/3] 检查虚拟环境..."
if [ ! -d "venv" ]; then
    echo "未找到虚拟环境，正在创建..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[错误] 创建虚拟环境失败"
        exit 1
    fi
    echo "虚拟环境创建成功"
fi

echo "[2/3] 激活虚拟环境并安装依赖..."
source venv/bin/activate

# 检查是否已安装Flask
python -c "import flask" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "依赖已安装，跳过安装步骤"
else
    echo "正在安装Python依赖..."
    
    # 尝试不使用代理直接安装
    pip install -r requirements.txt --proxy http://127.0.0.1:61079 --trusted-host pypi.org --trusted-host files.pythonhosted.org
    
    if [ $? -ne 0 ]; then
        echo "尝试使用阿里云镜像..."
        pip install -r requirements.txt --trusted-host mirrors.aliyun.com -i https://mirrors.aliyun.com/pypi/simple/ 2>/dev/null
    fi
    
    if [ $? -ne 0 ]; then
        echo "尝试使用豆瓣镜像..."
        pip install -r requirements.txt --trusted-host pypi.douban.com -i https://pypi.douban.com/simple/ 2>/dev/null
    fi
    
    if [ $? -ne 0 ]; then
        echo "[警告] 依赖安装失败，请手动运行："
        echo "  source venv/bin/activate"
        echo "  pip install Flask flask-cors requests pyinstaller --trusted-host pypi.tuna.tsinghua.edu.cn -i https://pypi.tuna.tsinghua.edu.cn/simple"
        echo ""
        read -p "按回车键尝试继续运行..."
    else
        echo "依赖安装成功"
    fi
fi

echo "[3/3] 启动服务..."
echo ""
echo "========================================"
echo "  服务已启动！"
echo "  访问地址: http://localhost:5001"
echo "  按 Ctrl+C 停止服务"
echo "========================================"
echo ""

python backend/app.py

