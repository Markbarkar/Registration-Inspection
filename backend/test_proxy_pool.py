#!/usr/bin/env python3
"""
测试代理池功能
"""
import sys
sys.path.insert(0, '/Users/linzaizai/Desktop/check_register/backend')

from checker import StirChecker

def main():
    print("=" * 60)
    print("测试代理池功能")
    print("=" * 60)
    
    # 创建检测器实例
    checker = StirChecker()
    
    # 设置代理池（示例）
    proxy_pool = [
        "http://127.0.0.1:61079",
        "http://abc4841381_82v3-zone-star-region-US:AAAAaaaa9527@na.9dc1b25972c51e1b.abcproxy.vip:4950"
        # 添加更多代理...
    ]
    
    print(f"\n设置代理池: {len(proxy_pool)} 个代理")
    for i, p in enumerate(proxy_pool, 1):
        print(f"  {i}. {p}")
    
    checker.set_proxy_pool(proxy_pool)
    
    # 测试邮箱列表（35个，会触发代理切换）
    test_emails = [
        "test1@example.com",
        "test2@example.com",
        "test3@example.com",
        "salustianomarty458@gmail.com",
        "test5@example.com",
    ] * 7  # 35个邮箱
    
    print(f"\n开始检测 {len(test_emails)} 个邮箱...")
    print(f"预计会在第30个邮箱后切换代理\n")
    print("=" * 60)
    
    results = []
    for i, email in enumerate(test_emails, 1):
        print(f"\n[{i}/{len(test_emails)}] 检测: {email}")
        result = checker.check_email(email)
        
        status = "✅" if result['status'] == 'success' else "❌"
        registered = "🔴 已注册" if result['registered'] else "🟢 未注册"
        
        print(f"{status} {registered} - {result['message']}")
        results.append(result)
        
        # 简单延迟
        import time
        time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print("检测完成！")
    print(f"总计: {len(results)}")
    print(f"已注册: {sum(1 for r in results if r['registered'])}")
    print(f"未注册: {sum(1 for r in results if not r['registered'])}")
    print(f"失败: {sum(1 for r in results if r['status'] != 'success')}")

if __name__ == "__main__":
    main()

