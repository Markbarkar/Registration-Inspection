# 代理池使用指南

## 功能概述

系统现已支持代理池功能，可以：
1. ✅ 配置多个代理地址
2. ✅ 自动轮换代理（每30个邮箱切换一次）
3. ✅ 切换代理时自动更新 session token
4. ✅ 避免因请求过多被封禁

## 为什么需要代理池？

### 问题
- **直连检测过多会失效**：当检测数量过多时，所有结果会显示为"未注册"（实际上是被限制了）
- **单个代理容易被封**：使用单个代理检测大量邮箱会被识别并限制

### 解决方案
使用代理池，系统会：
1. 每检测30个邮箱自动切换到下一个代理
2. 切换代理时重新初始化 session，获取新的 token
3. 轮换使用所有代理，分散请求

## 配置方法

### 方法1：通过Web界面

1. 打开 `http://localhost:5173`
2. 点击右上角"代理设置"按钮
3. 在"代理池"文本框中输入代理地址（每行一个）：
   ```
   http://127.0.0.1:7890
   http://127.0.0.1:7891
   http://127.0.0.1:7892
   ```
4. 点击"关闭"保存设置
5. 上传文件或手动输入邮箱进行检测

### 方法2：通过API

```python
import requests

# 准备文件和代理池
files = {'file': open('emails.txt', 'rb')}
data = {
    'proxy_pool': 'http://127.0.0.1:7890\nhttp://127.0.0.1:7891',
    'delay': '1'
}

# 发送请求
response = requests.post(
    'http://localhost:5001/api/upload-file',
    files=files,
    data=data
)
```

### 方法3：通过代码

```python
from checker import StirChecker

checker = StirChecker()

# 设置代理池
proxy_pool = [
    "http://127.0.0.1:7890",
    "http://127.0.0.1:7891",
    "http://127.0.0.1:7892",
]
checker.set_proxy_pool(proxy_pool)

# 批量检测
emails = ["test1@example.com", "test2@example.com", ...]
results = checker.check_batch(emails, delay=1)
```

## 代理池工作原理

```
检测流程:
1. 初始化时使用第一个代理
2. 检测邮箱 1-30：使用代理1
3. 第30个后自动切换：
   - 切换到代理2
   - 重新初始化 scraper
   - 获取新的 session token
4. 检测邮箱 31-60：使用代理2
5. 继续轮换...
```

### 关键代码逻辑

```python
def check_email(self, email: str) -> Dict:
    # 检查是否需要切换代理
    if self._should_rotate_proxy():
        print(f"📊 已检测 {self.check_count} 个邮箱，切换代理...")
        self._switch_to_next_proxy()
    
    # 增加检测计数
    self.check_count += 1
    
    # 执行检测...
```

## 代理获取建议

### 免费代理
- [Free Proxy List](https://free-proxy-list.net/)
- [ProxyScrape](https://proxyscrape.com/)
- 注意：免费代理稳定性差，建议用于测试

### 付费代理（推荐）
- [Bright Data](https://brightdata.com/)
- [Smartproxy](https://smartproxy.com/)
- [Oxylabs](https://oxylabs.io/)
- 优点：稳定、速度快、成功率高

### 本地代理工具
- **ClashX**（macOS）
- **Clash for Windows**（Windows）
- **V2Ray**（跨平台）

## 配置示例

### ClashX 配置
```yaml
# 在 ClashX 中配置多个代理端口
proxies:
  - name: "Proxy1"
    type: http
    server: 127.0.0.1
    port: 7890
  
  - name: "Proxy2"
    type: http
    server: 127.0.0.1
    port: 7891
```

### 代理池配置（Web界面）
```
http://127.0.0.1:7890
http://127.0.0.1:7891
http://127.0.0.1:7892
socks5://127.0.0.1:1080
```

## 测试代理池

### 运行测试脚本
```bash
cd /Users/linzaizai/Desktop/check_register
source venv/bin/activate
python backend/test_proxy_pool.py
```

### 预期输出
```
============================================================
测试代理池功能
============================================================

设置代理池: 3 个代理
  1. http://127.0.0.1:7890
  2. http://127.0.0.1:7891
  3. http://127.0.0.1:7892

开始检测 35 个邮箱...
预计会在第30个邮箱后切换代理

============================================================

[1/35] 检测: test1@example.com
✅ 🟢 未注册 - 邮箱未注册

...

[30/35] 检测: test30@example.com
✅ 🔴 已注册 - 邮箱已注册

📊 已检测 30 个邮箱，切换代理...
🔄 切换代理: http://127.0.0.1:7891 (代理池 2/3)
✅ 新 session 已建立，状态码: 200

[31/35] 检测: test31@example.com
✅ 🟢 未注册 - 邮箱未注册

...
```

## 参数配置

### 代理轮换频率
默认每30个邮箱切换一次，可以修改：

```python
# 在 checker.py 中修改
self.proxy_rotation_count = 30  # 改为其他数值，如 50
```

### 请求延迟
建议设置 1-2 秒：
- 太快：容易被识别为机器人
- 太慢：检测时间过长

## 故障排除

### 问题1：代理连接失败
```
❌ 错误: 代理连接失败
```
**解决方案**：
- 检查代理地址格式是否正确
- 确认代理服务正在运行
- 测试代理是否可用：`curl --proxy http://127.0.0.1:7890 https://www.google.com`

### 问题2：所有结果都是未注册
```
所有邮箱显示：🟢 未注册
```
**解决方案**：
- 可能是代理被封或直连被限制
- 尝试更换代理池
- 增加请求延迟时间

### 问题3：切换代理后仍然失败
```
🔄 切换代理后仍然检测失败
```
**解决方案**：
- 检查新代理是否可用
- 确认代理池中的所有代理都有效
- 尝试增加延迟时间

## 最佳实践

1. **使用至少3个代理**：提高成功率和稳定性
2. **设置合理延迟**：1-2秒为宜
3. **定期更换代理**：避免长期使用同一批代理
4. **监控检测结果**：如果失败率高，及时调整策略
5. **分批检测**：大量邮箱分多次检测，避免一次性检测过多

## 技术细节

### 代理切换时的操作
1. 重新创建 `cloudscraper` 实例
2. 设置新的代理配置
3. 访问注册页面获取新的 cookies 和 token
4. 重置检测计数器
5. 继续检测

### Session Token 更新
每次切换代理时，系统会：
```python
# 访问注册页面
init_response = self.scraper.get(
    f"{self.base_url}/reg/registration/en-us/stir/email",
    timeout=30
)
# 自动获取新的 cookies（包括 authtoken）
```

## 更新日志

### v1.2.0 (2025-10-23)
- ✅ 新增代理池功能
- ✅ 自动轮换代理（每30个邮箱）
- ✅ 切换代理时自动更新 token
- ✅ 优化前端代理设置界面
- ✅ 添加代理池测试脚本

