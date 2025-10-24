#!/usr/bin/env python3
"""
测试自定义代理轮换频率
"""
import sys
sys.path.insert(0, '/Users/linzaizai/Desktop/check_register/backend')

from checker import StirChecker
import time

def main():
    print("\n" + "="*70)
    print("🚀 测试自定义代理轮换频率")
    print("="*70)
    
    # 创建检测器实例
    checker = StirChecker()
    
    # 设置代理池，自定义轮换频率为 10 个邮箱
    proxy_pool = [
        "http://127.0.0.1:61079",
        "http://abc4841381_82v3-zone-star-region-US:AAAAaaaa9527@na.9dc1b25972c51e1b.abcproxy.vip:4950"
    ]
    
    # 设置轮换频率为 10（而不是默认的30）
    rotation_count = 10
    
    print(f"\n设置代理池，轮换频率: {rotation_count} 个邮箱\n")
    checker.set_proxy_pool(proxy_pool, rotation_count=rotation_count)
    
    # 测试邮箱列表（15个，会在第10个后触发切换）
    test_emails = [
        f"test{i}@example.com" for i in range(1, 16)
    ]
    
    print(f"\n📋 开始检测 {len(test_emails)} 个邮箱")
    print(f"⏱️  预计在第 {rotation_count} 个邮箱后切换代理\n")
    
    results = []
    start_time = time.time()
    
    for email in test_emails:
        result = checker.check_email(email)
        results.append(result)
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
    print(f"🔄 轮换频率: 每 {rotation_count} 个邮箱切换")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()

