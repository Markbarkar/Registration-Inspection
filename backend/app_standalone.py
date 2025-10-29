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

# 全局变量存储当前端口
current_port = 5001

# 直接覆盖 serve_frontend 视图函数,不修改路由
def serve_frontend_standalone(path=''):
    """提供前端静态文件"""
    from flask import request, Response
    
    if path and path != "" and os.path.exists(os.path.join(FRONTEND_DIST, path)):
        return send_from_directory(FRONTEND_DIST, path)
    else:
        # 读取 index.html 并注入当前端口
        index_path = os.path.join(FRONTEND_DIST, 'index.html')
        with open(index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 在 <head> 标签后注入端口信息
        port_script = f'''
    <script>
      // 动态设置 API 基础 URL
      window.API_BASE_URL = 'http://localhost:{current_port}';
      console.log('API Base URL:', window.API_BASE_URL);
    </script>
'''
        html_content = html_content.replace('<head>', '<head>' + port_script)
        
        return Response(html_content, mimetype='text/html')

# 替换原有的 serve_frontend 函数
app.view_functions['serve_frontend'] = serve_frontend_standalone

def find_available_port(start_port=5001, max_attempts=10):
    """查找可用端口"""
    import socket
    
    for port in range(start_port, start_port + max_attempts):
        try:
            # 尝试绑定端口
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('0.0.0.0', port))
            sock.close()
            return port
        except OSError:
            # 端口被占用,继续尝试下一个
            continue
    
    return None


if __name__ == '__main__':
    import webbrowser
    import threading
    import time
    
    # 查找可用端口
    print("=" * 50)
    print("🚀 Stir.com 邮箱注册检测系统")
    print("=" * 50)
    print("🔍 正在检测可用端口...")
    
    port = find_available_port(start_port=5001, max_attempts=10)
    
    if port is None:
        print("❌ 错误: 无法找到可用端口 (尝试了 5001-5010)")
        print("   请关闭占用这些端口的程序后重试")
        input("按回车键退出...")
        sys.exit(1)
    
    # 更新全局端口变量,供前端使用
    current_port = port
    # 需要在模块级别更新,以便 serve_frontend_standalone 能访问
    import sys as _sys
    _sys.modules[__name__].current_port = port
    
    if port != 5001:
        print(f"⚠️  端口 5001 已被占用,使用端口 {port}")
    else:
        print(f"✅ 端口 {port} 可用")
    
    url = f'http://localhost:{port}'
    
    print("=" * 50)
    print(f"📍 访问地址: {url}")
    print("💡 提示: 浏览器将自动打开")
    print("🛑 按 Ctrl+C 停止服务")
    print("=" * 50)
    
    # 自动打开浏览器
    def open_browser():
        time.sleep(2)  # 等待服务启动
        try:
            webbrowser.open(url)
            print("✅ 浏览器已打开")
        except Exception as e:
            print(f"⚠️  无法自动打开浏览器: {e}")
            print(f"   请手动访问: {url}")
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    # 启动服务
    try:
        app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        input("按回车键退出...")

