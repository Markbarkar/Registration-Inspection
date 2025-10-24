#!/bin/bash
# 自动化构建脚本 - Mac/Linux

set -e  # 遇到错误立即退出

echo "========================================================================"
echo "🚀 Stir Email Checker - 自动构建脚本"
echo "========================================================================"

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js，请先安装"
    exit 1
fi

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3，请先安装"
    exit 1
fi

# 步骤 1: 构建前端
echo ""
echo "📦 步骤 1/4: 构建前端..."
echo "------------------------------------------------------------------------"
cd frontend

if [ ! -d "node_modules" ]; then
    echo "   安装前端依赖..."
    npm install
fi

echo "   构建前端..."
npm run build

if [ ! -d "dist" ]; then
    echo "❌ 错误: 前端构建失败，未找到 dist 目录"
    exit 1
fi

echo "✅ 前端构建完成"
cd ..

# 步骤 2: 准备 Python 环境
echo ""
echo "🐍 步骤 2/4: 准备 Python 环境..."
echo "------------------------------------------------------------------------"

if [ ! -d "venv" ]; then
    echo "   创建虚拟环境..."
    python3 -m venv venv
fi

echo "   激活虚拟环境..."
source venv/bin/activate

echo "   检查依赖..."
pip install -q pyinstaller

echo "✅ Python 环境准备完成"

# 步骤 3: 清理旧文件
echo ""
echo "🧹 步骤 3/4: 清理旧构建..."
echo "------------------------------------------------------------------------"
rm -rf build dist __pycache__
echo "✅ 清理完成"

# 步骤 4: 打包应用
echo ""
echo "📦 步骤 4/4: 打包应用..."
echo "------------------------------------------------------------------------"
pyinstaller build_exe.spec --clean --noconfirm

if [ ! -f "dist/StirEmailChecker" ]; then
    echo "❌ 错误: 打包失败，未找到可执行文件"
    exit 1
fi

echo "✅ 打包完成"

# 显示结果
echo ""
echo "========================================================================"
echo "🎉 构建成功！"
echo "========================================================================"
echo "📁 可执行文件位置: $(pwd)/dist/StirEmailChecker"
echo "📊 文件大小: $(du -h dist/StirEmailChecker | cut -f1)"
echo ""
echo "🚀 运行测试:"
echo "   cd dist"
echo "   ./StirEmailChecker"
echo ""
echo "========================================================================"

