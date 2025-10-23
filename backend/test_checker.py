#!/usr/bin/env python3
"""
测试 StirChecker 类
"""
import sys
sys.path.insert(0, '/Users/linzaizai/Desktop/check_register/backend')

from checker import StirChecker

def main():
    print("=" * 60)
    print("测试 Stir.com 邮箱检测器")
    print("=" * 60)
    
    # 创建检测器实例
    checker = StirChecker()
    
    # 测试邮箱列表
    test_emails = [
        "test1@example.com",
        "salustianomarty458@gmail.com",
        "test_nonexistent_99999@example.com",  # 未注册的邮箱
    ]
    
    # 代理设置（可选）
    # 如果需要使用代理，取消下面的注释
    USE_PROXY = False  # 改为 True 启用代理
    PROXY_URL = "http://127.0.0.1:61079"
    
    if USE_PROXY:
        print(f"\n使用代理: {PROXY_URL}")
        checker.set_proxy(PROXY_URL)
        
        # 测试代理是否可用
        print("测试代理连接...")
        if checker.test_proxy(PROXY_URL):
            print("✅ 代理连接成功\n")
        else:
            print("❌ 代理连接失败，将继续尝试...\n")
    else:
        print("\n不使用代理（直连）\n")
    
    print("=" * 60)
    
    for email in test_emails:
        print(f"\n正在检测: {email}")
        result = checker.check_email(email)
        
        status_icon = "✅" if result['status'] == 'success' else "❌"
        registered_icon = "🔴" if result['registered'] else "🟢"
        
        print(f"{status_icon} 结果:")
        print(f"  - 邮箱: {result['email']}")
        print(f"  - 状态: {result['status']}")
        print(f"  - {registered_icon} 已注册: {result['registered']}")
        print(f"  - 消息: {result['message']}")
        print(f"  - 时间戳: {result['timestamp']}")
        print(f"  - 响应: {result['raw_response']}")
        print("-" * 60)
    
    print("\n测试完成！")

if __name__ == "__main__":
    main()

