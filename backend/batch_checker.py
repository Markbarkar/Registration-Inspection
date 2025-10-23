#!/usr/bin/env python3
"""
批量邮箱检测工具
支持从文件读取邮箱列表，并将已注册的邮箱保存到新文件
"""
import sys
import os
import re
import time
from datetime import datetime
sys.path.insert(0, '/Users/linzaizai/Desktop/check_register/backend')

from checker import StirChecker


def parse_email_file(file_path):
    """
    从文件中解析邮箱列表
    支持格式:
    - email:password
    - email
    - 每行一个邮箱
    
    返回: [(email, full_line), ...]
    """
    email_data = []
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return email_data
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                original_line = line.strip()
                
                # 跳过空行和注释
                if not original_line or original_line.startswith('#'):
                    continue
                
                # 提取邮箱（冒号前的部分）
                if ':' in original_line:
                    email = original_line.split(':')[0].strip()
                else:
                    email = original_line.strip()
                
                # 验证邮箱格式
                if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                    email_data.append((email, original_line))
                else:
                    print(f"⚠️  第 {line_num} 行: 邮箱格式不正确 - {email}")
        
        print(f"✅ 成功从文件读取 {len(email_data)} 个邮箱\n")
        
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
    
    return email_data


def save_results(results, output_file):
    """
    保存已注册的邮箱到文件
    保持原始格式（email:password）
    """
    try:
        registered_lines = []
        for result in results:
            if result['registered'] and result['status'] == 'success':
                registered_lines.append(result['original_line'])
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in registered_lines:
                f.write(line + '\n')
        
        print(f"\n✅ 已注册的邮箱已保存到: {output_file}")
        print(f"   共 {len(registered_lines)} 个已注册邮箱")
        
        return True
    except Exception as e:
        print(f"\n❌ 保存结果失败: {e}")
        return False


def save_detailed_report(results, report_file, elapsed_time):
    """
    保存详细的检测报告
    """
    try:
        registered_count = sum(1 for r in results if r['registered'] and r['status'] == 'success')
        unregistered_count = sum(1 for r in results if not r['registered'] and r['status'] == 'success')
        error_count = sum(1 for r in results if r['status'] != 'success')
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("Stir.com 邮箱检测详细报告\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            # 统计信息
            f.write("📊 统计信息\n")
            f.write("-" * 80 + "\n")
            f.write(f"总计: {len(results)} 个邮箱\n")
            f.write(f"🔴 已注册: {registered_count} 个 ({registered_count/len(results)*100:.1f}%)\n")
            f.write(f"🟢 未注册: {unregistered_count} 个 ({unregistered_count/len(results)*100:.1f}%)\n")
            f.write(f"❌ 检测失败: {error_count} 个 ({error_count/len(results)*100:.1f}%)\n")
            f.write(f"⏱️  总耗时: {elapsed_time:.2f} 秒\n")
            f.write(f"⚡ 平均速度: {elapsed_time/len(results):.2f} 秒/个\n")
            f.write("\n")
            
            # 已注册的邮箱
            f.write("🔴 已注册的邮箱\n")
            f.write("-" * 80 + "\n")
            for result in results:
                if result['registered'] and result['status'] == 'success':
                    f.write(f"{result['original_line']}\n")
            f.write("\n")
            
            # 未注册的邮箱
            f.write("🟢 未注册的邮箱\n")
            f.write("-" * 80 + "\n")
            for result in results:
                if not result['registered'] and result['status'] == 'success':
                    f.write(f"{result['original_line']}\n")
            f.write("\n")
            
            # 检测失败的邮箱
            if error_count > 0:
                f.write("❌ 检测失败的邮箱\n")
                f.write("-" * 80 + "\n")
                for result in results:
                    if result['status'] != 'success':
                        f.write(f"{result['email']} - {result['message']}\n")
                f.write("\n")
        
        print(f"✅ 详细报告已保存到: {report_file}")
        return True
    except Exception as e:
        print(f"❌ 保存报告失败: {e}")
        return False


def main():
    print("=" * 80)
    print("Stir.com 批量邮箱检测工具")
    print("=" * 80)
    
    # 配置参数
    INPUT_FILE = "/Users/linzaizai/Desktop/check_register/Our-2025-10-15-18.43.txt"
    OUTPUT_FILE = "/Users/linzaizai/Desktop/check_register/registered_emails.txt"
    REPORT_FILE = "/Users/linzaizai/Desktop/check_register/check_report.txt"
    
    # 代理设置
    USE_PROXY = False  # 改为 True 启用代理
    PROXY_URL = "http://127.0.0.1:61079"
    
    # 请求延迟（秒）
    REQUEST_DELAY = 1.5  # 每次请求间隔，避免请求过快
    
    print(f"\n📁 输入文件: {INPUT_FILE}")
    print(f"💾 输出文件: {OUTPUT_FILE}")
    print(f"📄 报告文件: {REPORT_FILE}")
    
    # 解析邮箱文件
    email_data = parse_email_file(INPUT_FILE)
    if not email_data:
        print("❌ 没有找到有效的邮箱，退出程序")
        return
    
    # 创建检测器实例
    checker = StirChecker()
    
    # 设置代理
    if USE_PROXY:
        print(f"\n🌐 使用代理: {PROXY_URL}")
        checker.set_proxy(PROXY_URL)
        
        print("测试代理连接...")
        if checker.test_proxy(PROXY_URL):
            print("✅ 代理连接成功\n")
        else:
            print("⚠️  代理连接测试失败，但将继续尝试...\n")
    else:
        print("\n🌐 不使用代理（直连）\n")
    
    print("=" * 80)
    print(f"\n开始检测 {len(email_data)} 个邮箱...")
    print(f"请求间隔: {REQUEST_DELAY} 秒\n")
    print("=" * 80)
    
    # 统计数据
    results = []
    registered_count = 0
    unregistered_count = 0
    error_count = 0
    
    # 批量检测
    start_time = time.time()
    
    for index, (email, original_line) in enumerate(email_data, 1):
        print(f"\n[{index}/{len(email_data)}] 正在检测: {email}")
        
        result = checker.check_email(email)
        result['original_line'] = original_line  # 保存原始行
        results.append(result)
        
        # 显示结果
        status_icon = "✅" if result['status'] == 'success' else "❌"
        registered_icon = "🔴" if result['registered'] else "🟢"
        
        print(f"{status_icon} 结果: {registered_icon} {result['message']}")
        
        # 更新统计
        if result['status'] == 'success':
            if result['registered']:
                registered_count += 1
            else:
                unregistered_count += 1
        else:
            error_count += 1
        
        # 显示进度
        progress = (index / len(email_data)) * 100
        print(f"进度: {progress:.1f}% | 已注册: {registered_count} | 未注册: {unregistered_count} | 失败: {error_count}")
        
        # 添加延迟，避免请求过快
        if index < len(email_data):
            time.sleep(REQUEST_DELAY)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # 打印统计结果
    print("\n" + "=" * 80)
    print("📊 检测完成 - 统计结果")
    print("=" * 80)
    print(f"总计: {len(email_data)} 个邮箱")
    print(f"🔴 已注册: {registered_count} 个 ({registered_count/len(email_data)*100:.1f}%)")
    print(f"🟢 未注册: {unregistered_count} 个 ({unregistered_count/len(email_data)*100:.1f}%)")
    print(f"❌ 检测失败: {error_count} 个 ({error_count/len(email_data)*100:.1f}%)")
    print(f"⏱️  总耗时: {elapsed_time:.2f} 秒")
    print(f"⚡ 平均速度: {elapsed_time/len(email_data):.2f} 秒/个")
    print("=" * 80)
    
    # 保存已注册的邮箱
    save_results(results, OUTPUT_FILE)
    
    # 保存详细报告
    save_detailed_report(results, REPORT_FILE, elapsed_time)
    
    print("\n✅ 所有任务完成！")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断，程序退出")
    except Exception as e:
        print(f"\n\n❌ 程序异常: {e}")
        import traceback
        traceback.print_exc()

