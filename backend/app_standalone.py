"""
独立运行版本 - 集成前端静态文件
用于打包成独立的可执行文件
"""
from flask import send_from_directory
import os
import sys

# 导入原有的 app
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

# 添加前端路由（必须在最后，避免覆盖API路由）
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

