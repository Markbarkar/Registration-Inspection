"""
独立运行版本 - 集成前端静态文件
用于打包成独立的可执行文件
"""
from flask import send_from_directory
import os
import sys

# 处理打包环境的路径问题
if getattr(sys, 'frozen', False):
    # 打包后的环境
    application_path = sys._MEIPASS
    # 将打包后的根目录添加到 Python 路径
    if application_path not in sys.path:
        sys.path.insert(0, application_path)
else:
    # 开发环境
    application_path = os.path.dirname(os.path.abspath(__file__))
    if application_path not in sys.path:
        sys.path.insert(0, application_path)

# 导入原有的 app
try:
    from app import app, checker
except ImportError as e:
    print(f"导入失败: {e}")
    print(f"当前路径: {os.getcwd()}")
    print(f"sys.path: {sys.path}")
    print(f"application_path: {application_path}")
    # 列出可用的模块
    if hasattr(sys, '_MEIPASS'):
        print(f"打包目录内容: {os.listdir(sys._MEIPASS)}")
    raise

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

# 直接覆盖 serve_frontend 视图函数,不修改路由
def serve_frontend_standalone(path=''):
    """提供前端静态文件"""
    if path and path != "" and os.path.exists(os.path.join(FRONTEND_DIST, path)):
        return send_from_directory(FRONTEND_DIST, path)
    else:
        return send_from_directory(FRONTEND_DIST, 'index.html')

# 替换原有的 serve_frontend 函数
app.view_functions['serve_frontend'] = serve_frontend_standalone

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Stir.com 邮箱注册检测系统")
    print("=" * 50)
    print("📍 访问地址: http://localhost:5001")
    print("💡 提示: 浏览器将自动打开")
    print("🛑 按 Ctrl+C 停止服务")
    print("=" * 50)
    
    # 自动打开浏览器
    import webbrowser
    import threading
    
    def open_browser():
        import time
        time.sleep(2)  # 等待服务启动
        try:
            webbrowser.open('http://localhost:5001')
            print("✅ 浏览器已打开")
        except Exception as e:
            print(f"⚠️  无法自动打开浏览器: {e}")
            print("   请手动访问: http://localhost:5001")
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    # 启动服务
    try:
        app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        input("按回车键退出...")

