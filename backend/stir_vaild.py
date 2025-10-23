"""
Stir.com 注册验证 API 测试脚本
用于测试邮箱是否已注册
"""
import cloudscraper
import json
import sys
import os
import time

# 清除可能干扰的环境变量代理设置
for proxy_var in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']:
    if proxy_var in os.environ:
        del os.environ[proxy_var]


def test_stir_email(email: str, proxy: str = None):
    """
    测试邮箱是否在 Stir.com 注册
    
    Args:
        email: 要检测的邮箱地址
        proxy: 代理地址，格式如 http://127.0.0.1:7890
    
    Returns:
        dict: 包含检测结果的字典
    """
    url = "https://stir.com/reg/regapi/registration/verify"
    
    # 设置代理
    proxies = None
    if proxy:
        proxies = {
            'http': proxy,
            'https': proxy
        }
    
    # 创建 cloudscraper session 以绕过 Cloudflare 保护
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'darwin',
            'desktop': True
        }
    )
    
    if proxies:
        scraper.proxies = proxies
    
    try:
        print(f"\n{'='*60}")
        print(f"正在检测邮箱: {email}")
        print(f"使用代理: {proxy if proxy else '无'}")
        print(f"{'='*60}\n")
        
        # 步骤1: 先访问注册页面，获取必要的 cookie
        print("步骤1: 访问注册页面获取 cookie...")
        init_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        }
        
        init_response = scraper.get(
            "https://stir.com/reg/registration/en-us/stir/email",
            headers=init_headers,
            timeout=30
        )
        
        print(f"初始访问状态码: {init_response.status_code}")
        print(f"获取到的 Cookies: {scraper.cookies.get_dict()}\n")
        
        # 等待一小段时间，模拟人类行为
        time.sleep(2)
        
        # 步骤2: 发送验证请求
        print("步骤2: 发送邮箱验证请求...")
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": "https://stir.com",
            "pragma": "no-cache",
            "referer": "https://stir.com/reg/registration/en-us/stir/email",
            "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        }
        
        # 简化的数据，只包含必要字段
        data = {
            "email": email,
            "firstName": "Test",  # 可选字段
        }
        
        response = scraper.post(
            url, 
            headers=headers, 
            json=data,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}\n")
        
        # 尝试解析JSON响应
        try:
            response_data = response.json()
            print(f"响应内容 (JSON):")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
            
            # 分析响应判断是否已注册
            result = {
                'email': email,
                'status_code': response.status_code,
                'registered': False,
                'message': '',
                'raw_response': response_data
            }
            
            # 根据不同的响应判断邮箱状态
            if response.status_code == 200:
                # 成功响应，邮箱可能未注册
                result['registered'] = False
                result['message'] = '邮箱未注册'
            elif response.status_code == 400:
                # 可能是邮箱已存在或其他错误
                error_msg = response_data.get('message', '').lower()
                if 'already' in error_msg or 'exist' in error_msg or 'registered' in error_msg:
                    result['registered'] = True
                    result['message'] = '邮箱已注册'
                else:
                    result['message'] = response_data.get('message', '验证失败')
            elif response.status_code == 409:
                # 冲突，通常表示邮箱已存在
                result['registered'] = True
                result['message'] = '邮箱已注册'
            else:
                result['message'] = f'未知状态: {response.status_code}'
            
            return result
            
        except json.JSONDecodeError:
            print(f"响应内容 (文本):")
            print(response.text)
            
            return {
                'email': email,
                'status_code': response.status_code,
                'registered': None,
                'message': '无法解析响应',
                'raw_response': response.text
            }
    
    except Exception as e:
        error_str = str(e).lower()
        print(f"❌ 错误: {e}")
        
        if 'cloudflare' in error_str:
            message = 'Cloudflare 保护无法绕过'
        elif 'proxy' in error_str:
            message = f'代理连接失败: {str(e)}'
        elif 'timeout' in error_str:
            message = '请求超时'
        else:
            message = f'请求失败: {str(e)}'
        
        return {
            'email': email,
            'status_code': None,
            'registered': None,
            'message': message,
            'error': str(e)
        }


if __name__ == "__main__":
    # 测试邮箱
    test_emails = [
        "salustianomarty458@gmail.com",  # 原始测试邮箱
        "test123456789@example.com",     # 测试邮箱（可能未注册）
    ]
    
    # 代理设置（如果需要）
    # proxy = "http://abc4841381_82v3-zone-star-region-US:AAAAaaaa9527@na.9dc1b25972c51e1b.abcproxy.vip:4950"
    proxy = "http://127.0.0.1:61079"
    # proxy = None  # 不使用代理
    
    # 如果命令行提供了邮箱参数
    if len(sys.argv) > 1:
        test_emails = [sys.argv[1]]
    
    if len(sys.argv) > 2:
        proxy = sys.argv[2]
    
    # 执行测试
    for email in test_emails:
        result = test_stir_email(email, proxy)
        print(f"\n{'='*60}")
        print(f"检测结果:")
        print(f"  邮箱: {result['email']}")
        print(f"  状态: {result['message']}")
        print(f"  已注册: {result['registered']}")
        print(f"{'='*60}\n")
