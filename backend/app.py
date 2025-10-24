"""
网站注册检测系统 - 后端服务
"""
import os
import sys
import re
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from checker import StirChecker
from werkzeug.utils import secure_filename

# 获取应用根目录
if getattr(sys, 'frozen', False):
    # 打包后的exe环境
    application_path = sys._MEIPASS
else:
    # 开发环境
    application_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=None)
CORS(app)

# 配置上传文件
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
RESULTS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
ALLOWED_EXTENSIONS = {'txt'}

# 确保文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制16MB

# 全局检测器实例
checker = StirChecker()


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def parse_email_line(line):
    """
    解析邮箱行，格式: email:password
    返回: (email, password) 或 (email, None)
    """
    line = line.strip()
    if not line or line.startswith('#'):
        return None, None
    
    if ':' in line:
        parts = line.split(':', 1)
        email = parts[0].strip()
        password = parts[1].strip() if len(parts) > 1 else ''
        return email, password
    else:
        return line.strip(), None


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
        proxy_pool = data.get('proxy_pool', [])  # 代理池
        proxy_rotation_count = data.get('proxy_rotation_count', 30)  # 代理轮换频率
        delay = data.get('delay', 1)  # 默认延迟1秒
        
        if not emails:
            return jsonify({'success': False, 'error': '邮箱列表不能为空'}), 400
        
        # 设置代理或代理池
        if proxy_pool and len(proxy_pool) > 0:
            # 使用代理池
            checker.set_proxy_pool(proxy_pool, rotation_count=proxy_rotation_count)
        elif proxy:
            # 使用单个代理
            checker.set_proxy(proxy)
        else:
            # 不使用代理
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


@app.route('/api/upload-file', methods=['POST'])
def upload_file():
    """上传文件并批量检测"""
    try:
        # 检查文件是否存在
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': '没有上传文件'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': '文件名为空'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': '只支持 .txt 文件'}), 400
        
        # 获取其他参数
        proxy = request.form.get('proxy', '')
        proxy_pool_str = request.form.get('proxy_pool', '')
        proxy_rotation_count = int(request.form.get('proxy_rotation_count', 30))
        delay = float(request.form.get('delay', 1))
        
        # 解析代理池（用逗号或换行分隔）
        proxy_pool = []
        if proxy_pool_str:
            proxy_pool = [p.strip() for p in proxy_pool_str.replace('\n', ',').split(',') if p.strip()]
        
        # 设置代理或代理池
        if proxy_pool and len(proxy_pool) > 0:
            # 使用代理池
            checker.set_proxy_pool(proxy_pool, rotation_count=proxy_rotation_count)
        elif proxy:
            # 使用单个代理
            checker.set_proxy(proxy)
        else:
            # 不使用代理
            checker.set_proxy(None)
        
        # 读取文件内容
        content = file.read().decode('utf-8', errors='ignore')
        lines = content.split('\n')
        
        # 解析邮箱
        emails_data = []
        for line in lines:
            email, password = parse_email_line(line)
            if email:
                emails_data.append({
                    'email': email,
                    'password': password,
                    'original_line': line.strip()
                })
        
        if not emails_data:
            return jsonify({'success': False, 'error': '文件中没有找到有效的邮箱'}), 400
        
        # 批量检测
        results = []
        registered_lines = []
        
        for i, item in enumerate(emails_data):
            result = checker.check_email(item['email'])
            result['password'] = item['password']
            result['original_line'] = item['original_line']
            results.append(result)
            
            # 如果已注册，保存原始行
            if result['registered']:
                registered_lines.append(item['original_line'])
            
            # 添加延迟（最后一个不需要）
            if i < len(emails_data) - 1 and delay > 0:
                import time
                time.sleep(delay)
        
        # 保存已注册的邮箱到文件
        result_filename = None
        if registered_lines:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            result_filename = f'registered_{timestamp}.txt'
            result_path = os.path.join(app.config['RESULTS_FOLDER'], result_filename)
            
            with open(result_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(registered_lines))
        
        return jsonify({
            'success': True,
            'data': {
                'total': len(results),
                'registered': len(registered_lines),
                'unregistered': len(results) - len(registered_lines),
                'results': results,
                'result_file': result_filename
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/download-result/<filename>', methods=['GET'])
def download_result(filename):
    """下载检测结果文件"""
    try:
        # 安全检查文件名
        filename = secure_filename(filename)
        file_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'success': False, 'error': '文件不存在'}), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/plain'
        )
    
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


