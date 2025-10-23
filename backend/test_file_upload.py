#!/usr/bin/env python3
"""
测试文件上传API
"""
import requests
import os

def test_file_upload():
    """测试文件上传检测功能"""
    
    # API地址
    url = "http://localhost:5001/api/upload-file"
    
    # 测试文件路径
    test_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Our-2025-10-15-18.43.txt')
    
    if not os.path.exists(test_file):
        print(f"❌ 测试文件不存在: {test_file}")
        return
    
    print("=" * 60)
    print("测试文件上传批量检测API")
    print("=" * 60)
    print(f"\n上传文件: {test_file}\n")
    
    # 准备文件和数据
    files = {
        'file': open(test_file, 'rb')
    }
    
    data = {
        'proxy': '',  # 不使用代理
        'delay': '1'  # 1秒延迟
    }
    
    try:
        # 发送请求
        print("正在上传并检测...")
        response = requests.post(url, files=files, data=data)
        
        print(f"\n状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                data = result['data']
                print("\n✅ 检测成功！")
                print(f"\n统计信息:")
                print(f"  - 总计: {data['total']}")
                print(f"  - 已注册: {data['registered']}")
                print(f"  - 未注册: {data['unregistered']}")
                
                if data.get('result_file'):
                    print(f"\n📄 已注册邮箱已保存到: {data['result_file']}")
                
                print(f"\n详细结果:")
                for r in data['results']:
                    status = "🔴 已注册" if r['registered'] else "🟢 未注册"
                    print(f"  {status} - {r['email']}")
                    if r.get('password'):
                        print(f"    密码: {r['password']}")
                    print(f"    消息: {r['message']}")
                    print(f"    响应: {r['raw_response']}")
                    print()
            else:
                print(f"❌ 检测失败: {result.get('error')}")
        else:
            print(f"❌ 请求失败: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保后端服务已启动")
        print("   启动命令: python backend/app.py")
    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        files['file'].close()

if __name__ == "__main__":
    test_file_upload()

