"""
网站注册检测系统 - 后端服务
"""
import os
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from checker import StirChecker

# 获取应用根目录
if getattr(sys, 'frozen', False):
    # 打包后的exe环境
    application_path = sys._MEIPASS
else:
    # 开发环境
    application_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=None)
CORS(app)

# 全局检测器实例
checker = StirChecker()


@app.route('/api/check', methods=['POST'])
def check_email():
    """检测单个邮箱"""
    try:
        data = request.get_json()
        email = data.get('email')
        proxy = data.get('proxy')
        
        if not email:
            return jsonify({'success': False, 'error': '邮箱不能为空'}), 400
        
        # 设置代理
        if proxy:
            checker.set_proxy(proxy)
        else:
            checker.set_proxy(None)
        
        # 执行检测
        result = checker.check_email(email)
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/check-batch', methods=['POST'])
def check_batch():
    """批量检测邮箱"""
    try:
        data = request.get_json()
        emails = data.get('emails', [])
        proxy = data.get('proxy')
        delay = data.get('delay', 1)  # 默认延迟1秒
        
        if not emails:
            return jsonify({'success': False, 'error': '邮箱列表不能为空'}), 400
        
        # 设置代理
        if proxy:
            checker.set_proxy(proxy)
        else:
            checker.set_proxy(None)
        
        # 批量检测
        results = checker.check_batch(emails, delay=delay)
        
        return jsonify({
            'success': True,
            'data': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/test-proxy', methods=['POST'])
def test_proxy():
    """测试代理连接"""
    try:
        data = request.get_json()
        proxy = data.get('proxy')
        
        if not proxy:
            return jsonify({'success': False, 'error': '代理地址不能为空'}), 400
        
        # 测试代理
        is_valid = checker.test_proxy(proxy)
        
        return jsonify({
            'success': True,
            'valid': is_valid
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# 前端静态文件服务（用于打包后的exe）
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """提供前端静态文件"""
    frontend_path = os.path.join(application_path, '..', 'frontend', 'dist')
    
    if os.path.exists(frontend_path):
        if path and os.path.exists(os.path.join(frontend_path, path)):
            return send_from_directory(frontend_path, path)
        else:
            return send_from_directory(frontend_path, 'index.html')
    else:
        return jsonify({
            'message': 'API服务运行中',
            'version': '1.0.0'
        })


if __name__ == '__main__':
    print("=" * 50)
    print("网站注册检测系统启动中...")
    print("后端服务地址: http://localhost:5001")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5001, debug=False)


