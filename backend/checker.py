"""
Stir.com 注册检测核心逻辑
"""
import cloudscraper
import time
import re
import os
from typing import Dict, List, Optional

# 清除可能干扰的环境变量代理设置
for proxy_var in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']:
    if proxy_var in os.environ:
        del os.environ[proxy_var]


class StirChecker:
    """Stir.com 邮箱注册检测器"""
    
    def __init__(self):
        # 使用 cloudscraper 绕过 Cloudflare 保护
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'darwin',
                'desktop': True
            }
        )
        self.proxy = None
        self.base_url = "https://stir.com"
        self.api_url = "https://stir.com/reg/regapi/registration/verify"
        
        # 设置请求头，模拟真实浏览器
        self.scraper.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://stir.com',
            'Referer': 'https://stir.com/reg/registration/en-us/stir/email',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        })
    
    def set_proxy(self, proxy: Optional[str]):
        """设置代理"""
        if proxy:
            self.proxy = {
                'http': proxy,
                'https': proxy
            }
            self.scraper.proxies = self.proxy
        else:
            self.proxy = None
            self.scraper.proxies = None
    
    def test_proxy(self, proxy: str) -> bool:
        """测试代理是否可用"""
        try:
            proxies = {
                'http': proxy,
                'https': proxy
            }
            response = requests.get(
                'https://www.google.com',
                proxies=proxies,
                timeout=10
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def _validate_email(self, email: str) -> bool:
        """验证邮箱格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def check_email(self, email: str) -> Dict:
        """
        检测邮箱是否在 stir.com 注册
        
        返回格式:
        {
            'email': '邮箱地址',
            'registered': True/False,
            'status': 'success/error',
            'message': '详细信息',
            'timestamp': '检测时间戳'
        }
        """
        result = {
            'email': email,
            'registered': False,
            'status': 'error',
            'message': '',
            'timestamp': int(time.time())
        }
        
        # 验证邮箱格式
        if not self._validate_email(email):
            result['message'] = '邮箱格式不正确'
            return result
        
        try:
            # 步骤1: 先访问注册页面获取 cookie（绕过 Cloudflare）
            try:
                init_response = self.scraper.get(
                    f"{self.base_url}/reg/registration/en-us/stir/email",
                    timeout=30
                )
                # 等待一小段时间，模拟人类行为
                time.sleep(1)
            except Exception as e:
                # 如果初始访问失败，继续尝试
                pass
            
            # 步骤2: 使用 Stir.com 的注册验证 API
            response = self.scraper.post(
                self.api_url,
                json={
                    'email': email,
                    'firstName': 'Test'  # 可选字段
                },
                timeout=30
            )
            
            # 分析响应
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # 检查 success 字段和 errors 数组
                    if data.get('success') == False and 'errors' in data:
                        # 检查错误列表
                        errors = data.get('errors', [])
                        for error in errors:
                            error_key = error.get('key', '').lower()
                            # email_unavailable 表示邮箱已被占用
                            if 'unavailable' in error_key or 'taken' in error_key or 'exist' in error_key:
                                result['registered'] = True
                                result['message'] = '邮箱已注册'
                                result['status'] = 'success'
                                break
                        else:
                            # 如果没有匹配到已注册的错误，可能是其他验证错误
                            result['registered'] = False
                            result['message'] = '邮箱未注册或验证失败'
                            result['status'] = 'success'
                    elif data.get('success') == True:
                        # success=true 表示验证通过，邮箱可用（未注册）
                        result['registered'] = False
                        result['message'] = '邮箱未注册'
                        result['status'] = 'success'
                    else:
                        # 其他情况，检查是否有错误信息
                        error_msg = str(data.get('message', data.get('error', ''))).lower()
                        if 'already' in error_msg or 'exist' in error_msg or 'registered' in error_msg or 'taken' in error_msg or 'unavailable' in error_msg:
                            result['registered'] = True
                            result['message'] = '邮箱已注册'
                        else:
                            result['registered'] = False
                            result['message'] = '邮箱未注册'
                        result['status'] = 'success'
                except Exception as e:
                    result['message'] = f'解析响应失败: {str(e)}'
                    
            elif response.status_code == 400:
                # 400 通常表示邮箱已存在或验证失败
                try:
                    data = response.json()
                    error_msg = str(data.get('message', data.get('error', ''))).lower()
                    if 'already' in error_msg or 'exist' in error_msg or 'registered' in error_msg or 'taken' in error_msg:
                        result['registered'] = True
                        result['message'] = '邮箱已注册'
                    else:
                        result['registered'] = False
                        result['message'] = data.get('message', '验证失败')
                    result['status'] = 'success'
                except:
                    result['message'] = f'检测失败: HTTP {response.status_code}'
                    
            elif response.status_code == 409:
                # 409 Conflict 通常表示邮箱已存在
                result['registered'] = True
                result['message'] = '邮箱已注册'
                result['status'] = 'success'
                
            elif response.status_code == 403:
                # Cloudflare 保护
                result['message'] = 'Cloudflare 保护阻止访问，请稍后重试或使用代理'
                
            else:
                result['message'] = f'检测失败: HTTP {response.status_code}'
        
        except Exception as e:
            error_str = str(e).lower()
            if 'timeout' in error_str:
                result['message'] = '请求超时，请检查网络连接或代理设置'
            elif 'proxy' in error_str:
                result['message'] = '代理连接失败，请检查代理设置'
            elif 'cloudflare' in error_str:
                result['message'] = 'Cloudflare 保护无法绕过'
            else:
                result['message'] = f'检测出错: {str(e)}'
        
        return result
    
    def _check_by_password_reset(self, email: str) -> bool:
        """
        通过密码重置接口检测邮箱是否注册
        
        很多网站的密码重置功能会提示邮箱是否存在
        """
        try:
            reset_url = f"{self.base_url}/api/v1/auth/forgot-password"
            
            response = self.session.post(
                reset_url,
                json={'email': email},
                proxies=self.proxy,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # 分析返回信息
                message = str(data.get('message', '')).lower()
                
                # 如果提示邮件已发送，说明邮箱存在
                if 'sent' in message or 'email sent' in message or '已发送' in message:
                    return True
                
                # 如果提示邮箱不存在
                if 'not found' in message or 'does not exist' in message or '不存在' in message:
                    return False
                
                # 如果返回成功但没有明确信息，假设邮箱存在
                if data.get('success'):
                    return True
            
            elif response.status_code == 404:
                # 邮箱不存在
                return False
            
            # 默认返回False（无法确定）
            return False
        
        except Exception:
            # 如果密码重置方法也失败，返回False
            return False
    
    def check_batch(self, emails: List[str], delay: float = 1.0) -> List[Dict]:
        """
        批量检测邮箱
        
        Args:
            emails: 邮箱列表
            delay: 每次请求之间的延迟（秒）
        
        Returns:
            检测结果列表
        """
        results = []
        
        for i, email in enumerate(emails):
            # 检测邮箱
            result = self.check_email(email)
            results.append(result)
            
            # 添加延迟（最后一个不需要延迟）
            if i < len(emails) - 1 and delay > 0:
                time.sleep(delay)
        
        return results


