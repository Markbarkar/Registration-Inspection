#!/usr/bin/env python3
"""
测试代理池功能（带详细日志）
"""
import sys
sys.path.insert(0, '/Users/linzaizai/Desktop/check_register/backend')

from checker import StirChecker
import time

def main():
    print("\n" + "="*70)
    print("🚀 Stir.com 邮箱检测系统 - 代理池测试")
    print("="*70)
    
    # 创建检测器实例
    checker = StirChecker()
    
    # 设置代理池
    proxy_pool = [
        "http://127.0.0.1:61079",
        "http://abc4841381_82v3-zone-star-region-US:AAAAaaaa9527@na.9dc1b25972c51e1b.abcproxy.vip:4950"
    ]
    
    checker.set_proxy_pool(proxy_pool)
    
    # 测试邮箱列表（35个，会触发代理切换）
    test_emails = [
        # 前30个
        "test1@example.com",
        "test2@example.com",
        "test3@example.com",
        "salustianomarty458@gmail.com",
        "test5@example.com",
        "test6@example.com",
        "test7@example.com",
        "test8@example.com",
        "test9@example.com",
        "test10@example.com",
        "test11@example.com",
        "test12@example.com",
        "test13@example.com",
        "test14@example.com",
        "test15@example.com",
        "test16@example.com",
        "test17@example.com",
        "test18@example.com",
        "test19@example.com",
        "test20@example.com",
        "test21@example.com",
        "test22@example.com",
        "test23@example.com",
        "test24@example.com",
        "test25@example.com",
        "test26@example.com",
        "test27@example.com",
        "test28@example.com",
        "test29@example.com",
        "test30@example.com",
        # 第31个会触发代理切换
        "test31@example.com",
        "test32@example.com",
        "test33@example.com",
        "test34@example.com",
        "test35@example.com",
    ]
    
    print(f"\n📋 开始批量检测 {len(test_emails)} 个邮箱")
    print(f"⏱️  预计在第 30 个邮箱后切换代理\n")
    
    results = []
    start_time = time.time()
    
    for email in test_emails:
        result = checker.check_email(email)
        results.append(result)
        
        # 简单延迟
        time.sleep(0.5)
    
    elapsed_time = time.time() - start_time
    
    # 统计结果
    print("\n" + "="*70)
    print("📊 检测完成 - 统计结果")
    print("="*70)
    print(f"⏱️  总耗时: {elapsed_time:.2f} 秒")
    print(f"📧 总计: {len(results)} 个邮箱")
    print(f"🔴 已注册: {sum(1 for r in results if r['registered'])} 个")
    print(f"🟢 未注册: {sum(1 for r in results if not r['registered'])} 个")
    print(f"❌ 失败: {sum(1 for r in results if r['status'] != 'success')} 个")
    print(f"⚡ 平均速度: {elapsed_time/len(results):.2f} 秒/个")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()

