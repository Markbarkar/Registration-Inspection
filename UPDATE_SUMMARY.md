# 更新总结 - 自定义代理轮换频率

## 🎉 新增功能

### 自定义代理轮换频率
现在用户可以自定义每检测多少个邮箱后切换代理，不再固定为30个。

## 📝 更新内容

### 1. 后端更新 (`backend/checker.py`)

#### 新增方法
```python
def set_proxy_rotation_count(self, count: int):
    """设置代理轮换频率"""
    if count > 0:
        self.proxy_rotation_count = count
```

#### 增强方法
```python
def set_proxy_pool(self, proxy_list: List[str], rotation_count: int = None):
    """设置代理池，支持自定义轮换频率"""
    # rotation_count 参数可选，默认使用 self.proxy_rotation_count (30)
```

### 2. 后端API更新 (`backend/app.py`)

#### 批量检测API
```python
@app.route('/api/check-batch', methods=['POST'])
def check_batch():
    proxy_rotation_count = data.get('proxy_rotation_count', 30)  # 新增参数
    checker.set_proxy_pool(proxy_pool, rotation_count=proxy_rotation_count)
```

#### 文件上传API
```python
@app.route('/api/upload-file', methods=['POST'])
def upload_file():
    proxy_rotation_count = int(request.form.get('proxy_rotation_count', 30))  # 新增参数
    checker.set_proxy_pool(proxy_pool, rotation_count=proxy_rotation_count)
```

### 3. 前端更新 (`frontend/src/App.jsx`)

#### 新增状态
```javascript
const [proxyRotationCount, setProxyRotationCount] = useState(30);
```

#### 新增UI组件
在代理设置模态框中添加：
```jsx
<div>
  <div className="label">
    代理轮换频率
    <Tooltip title="每检测多少个邮箱后切换到下一个代理">
      <span style={{ marginLeft: 8, color: '#999' }}>ℹ️</span>
    </Tooltip>
  </div>
  <Input
    type="number"
    min={1}
    max={100}
    value={proxyRotationCount}
    onChange={(e) => setProxyRotationCount(parseInt(e.target.value) || 30)}
    style={{ width: 200 }}
    addonAfter="个邮箱"
  />
  <div className="hint">
    建议设置为 20-50 之间，默认 30 个邮箱切换一次
  </div>
</div>
```

#### 更新API调用
```javascript
formData.append('proxy_rotation_count', proxyRotationCount);
```

## 🎯 使用方法

### Web界面使用

1. 打开应用：`http://localhost:5173`
2. 点击"代理设置"
3. 设置代理池（多个代理地址）
4. 设置"代理轮换频率"（例如：20、30、50）
5. 点击关闭保存

### 代码使用

```python
from checker import StirChecker

checker = StirChecker()

# 方法1：设置代理池时指定
checker.set_proxy_pool(
    ['http://proxy1', 'http://proxy2'],
    rotation_count=20  # 每20个邮箱切换
)

# 方法2：单独设置
checker.set_proxy_rotation_count(25)
```

### API使用

```bash
# 文件上传
curl -X POST http://localhost:5001/api/upload-file \
  -F "file=@emails.txt" \
  -F "proxy_pool=http://proxy1
http://proxy2" \
  -F "proxy_rotation_count=20" \
  -F "delay=1"
```

## 📊 控制台日志示例

### 设置代理池时
```
======================================================================
🌐 代理池配置
   代理数量: 2
   1. http://127.0.0.1:61079
   2. ***@na.9dc1b25972c51e1b.abcproxy.vip:4950
   轮换策略: 每 20 个邮箱切换
======================================================================
```

### 达到切换阈值时
```
[20] 检测 test20@example.com (代理 1/2) -> 🟢 邮箱未注册

📊 已检测 20 个邮箱，达到切换阈值，准备切换代理...

======================================================================
🔄 代理切换
   当前代理: ***@na.9dc1b25972c51e1b.abcproxy.vip:4950
   代理索引: 2/2
   已检测数: 20 个邮箱
======================================================================
```

## 🧪 测试脚本

### 测试自定义频率
```bash
cd /Users/linzaizai/Desktop/check_register
source venv/bin/activate
python backend/test_custom_rotation.py
```

这个脚本会：
- 设置轮换频率为10（而不是默认的30）
- 检测15个邮箱
- 在第10个邮箱后自动切换代理
- 显示完整的日志输出

## 💡 建议配置

### 根据代理数量
- **2个代理**：20-30
- **3-5个代理**：30-40
- **5+个代理**：40-50

### 根据代理类型
- **免费代理**：10-20（频繁切换）
- **付费代理**：30-50（稳定性高）
- **专用代理**：40-60（独享IP）

### 根据检测数量
- **<100个**：20-30
- **100-500个**：30-40
- **500+个**：30-50

## 📚 相关文档

- [代理轮换频率设置指南](ROTATION_COUNT_GUIDE.md) - 详细使用说明
- [代理池使用指南](PROXY_POOL_GUIDE.md) - 代理池基础
- [控制台日志说明](CONSOLE_LOGS_GUIDE.md) - 日志解读

## ✅ 功能清单

- ✅ 后端支持自定义轮换频率
- ✅ 前端UI添加轮换频率输入
- ✅ API支持轮换频率参数
- ✅ 控制台日志显示当前频率
- ✅ 默认值：30个邮箱
- ✅ 范围：1-100个邮箱
- ✅ 实时生效，无需重启

## 🎨 UI截图说明

代理设置模态框现在包含：
1. **单个代理地址** - 输入框
2. **代理池** - 多行文本框
3. **代理轮换频率** - 数字输入框（新增）⭐
4. **批量检测延迟** - 数字输入框

## 🔧 技术细节

### 参数传递流程
```
前端输入 → FormData/JSON → 后端API → checker.set_proxy_pool() → 生效
```

### 验证逻辑
```python
if rotation_count is not None and rotation_count > 0:
    self.proxy_rotation_count = rotation_count
```

### 切换判断
```python
def _should_rotate_proxy(self):
    if not self.proxy_pool or len(self.proxy_pool) <= 1:
        return False
    return self.check_count >= self.proxy_rotation_count
```

## 🚀 升级步骤

如果您已经在使用旧版本：

1. **更新后端代码**
   ```bash
   cd /Users/linzaizai/Desktop/check_register
   # 后端代码已自动更新
   ```

2. **重启后端服务**
   ```bash
   # 停止旧服务（Ctrl+C）
   source venv/bin/activate
   python backend/app.py
   ```

3. **更新前端代码**
   ```bash
   cd frontend
   # 前端代码已自动更新
   ```

4. **重启前端服务**
   ```bash
   # 停止旧服务（Ctrl+C）
   npm run dev
   ```

5. **刷新浏览器**
   - 打开 `http://localhost:5173`
   - 硬刷新：Cmd+Shift+R (Mac) 或 Ctrl+Shift+R (Windows)

## 📈 性能影响

- **切换频率降低**（如10）：
  - ✅ 更好地分散请求
  - ✅ 降低单个代理压力
  - ⚠️ 增加总切换次数（每次2-3秒）

- **切换频率提高**（如50）：
  - ✅ 减少切换开销
  - ✅ 提高整体速度
  - ⚠️ 单个代理请求更多

## 🎯 总结

现在系统更加灵活，用户可以根据：
- 代理数量
- 代理质量
- 检测数量
- 网站限制

自由调整代理轮换频率，获得最佳的检测效果！

默认值30适合大多数场景，如有特殊需求可以灵活调整。

