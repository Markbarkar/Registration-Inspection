#!/bin/bash

echo "========================================"
echo "  依赖安装脚本"
echo "========================================"
echo ""

# 进入项目目录
cd "$(dirname "$0")"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python3"
    exit 1
fi

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

echo "开始安装依赖..."
echo ""

# 取消代理设置（避免SSL问题）
unset http_proxy
unset https_proxy
unset all_proxy
unset HTTP_PROXY
unset HTTPS_PROXY
unset ALL_PROXY

# 方法1: 尝试清华镜像
echo "[1/4] 尝试清华镜像..."
pip install Flask==3.0.0 flask-cors==4.0.0 requests==2.31.0 pyinstaller==6.3.0 \
    --trusted-host pypi.tuna.tsinghua.edu.cn \
    -i https://pypi.tuna.tsinghua.edu.cn/simple

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 依赖安装成功！"
    exit 0
fi

# 方法2: 尝试阿里云镜像
echo "[2/4] 尝试阿里云镜像..."
pip install Flask==3.0.0 flask-cors==4.0.0 requests==2.31.0 pyinstaller==6.3.0 \
    --trusted-host mirrors.aliyun.com \
    -i https://mirrors.aliyun.com/pypi/simple/

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 依赖安装成功！"
    exit 0
fi

# 方法3: 尝试豆瓣镜像
echo "[3/4] 尝试豆瓣镜像..."
pip install Flask==3.0.0 flask-cors==4.0.0 requests==2.31.0 pyinstaller==6.3.0 \
    --trusted-host pypi.douban.com \
    -i https://pypi.douban.com/simple/

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 依赖安装成功！"
    exit 0
fi

# 方法4: 尝试官方源
echo "[4/4] 尝试官方源..."
pip install Flask==3.0.0 flask-cors==4.0.0 requests==2.31.0 pyinstaller==6.3.0

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 依赖安装成功！"
    exit 0
fi

echo ""
echo "❌ 所有安装方法都失败了"
echo ""
echo "请尝试以下方法："
echo "1. 检查网络连接"
echo "2. 临时关闭代理和VPN"
echo "3. 手动安装："
echo "   source venv/bin/activate"
echo "   pip install Flask flask-cors requests pyinstaller"
echo ""

exit 1



