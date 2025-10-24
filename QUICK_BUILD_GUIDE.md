# 快速打包指南

## 🚀 一键打包（推荐）

### Mac/Linux 用户

```bash
cd /Users/linzaizai/Desktop/check_register
./build.sh
```

### Windows 用户

```cmd
cd C:\path\to\check_register
build.bat
```

脚本会自动完成：
1. ✅ 构建前端
2. ✅ 准备 Python 环境
3. ✅ 清理旧文件
4. ✅ 打包应用

## 📦 手动打包步骤

如果自动脚本失败，可以手动执行：

### 步骤 1: 构建前端

```bash
cd frontend
npm run build
cd ..
```

### 步骤 2: 激活 Python 环境

```bash
source venv/bin/activate  # Mac/Linux
# 或
venv\Scripts\activate.bat  # Windows
```

### 步骤 3: 安装 PyInstaller

```bash
pip install pyinstaller
```

### 步骤 4: 执行打包

```bash
pyinstaller build_exe.spec --clean
```

### 步骤 5: 测试运行

```bash
cd dist
./StirEmailChecker  # Mac/Linux
# 或
StirEmailChecker.exe  # Windows
```

## 📁 打包结果

打包成功后，可执行文件位于：
```
dist/
├── StirEmailChecker       # Mac/Linux
└── StirEmailChecker.exe   # Windows
```

文件大小约：50-100MB

## ✅ 验证打包

运行可执行文件后，应该：
1. ✅ 显示启动信息
2. ✅ 自动打开浏览器
3. ✅ 访问 http://localhost:5001
4. ✅ 看到应用界面

## ⚠️ 常见问题

### 问题1：前端构建失败

**错误**：`npm run build` 失败

**解决**：
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### 问题2：找不到模块

**错误**：`ModuleNotFoundError`

**解决**：在 `build_exe.spec` 的 `hiddenimports` 中添加缺失模块

### 问题3：文件太大

**解决**：
- 在 `build_exe.spec` 中添加更多排除项
- 使用 `--onedir` 代替 `--onefile`

### 问题4：Mac 上无法运行

**错误**：权限被拒绝

**解决**：
```bash
chmod +x dist/StirEmailChecker
```

### 问题5：Windows 杀毒软件拦截

**解决**：
- 添加到白名单
- 或使用代码签名证书

## 📝 打包前检查清单

- [ ] 前端代码已更新
- [ ] 后端代码已更新
- [ ] 依赖已安装（`requirements.txt`）
- [ ] 前端依赖已安装（`package.json`）
- [ ] 虚拟环境已激活
- [ ] PyInstaller 已安装

## 🎯 优化建议

### 减小文件大小

1. 排除不必要的模块（在 spec 文件中）
2. 使用 UPX 压缩
3. 删除测试文件

### 提高启动速度

1. 使用 `--onedir` 模式
2. 减少 `hiddenimports`
3. 优化代码

### 提升用户体验

1. 添加应用图标
2. 隐藏控制台窗口（生产环境）
3. 创建安装程序

## 📚 详细文档

查看完整打包指南：[BUILD_EXE_GUIDE.md](BUILD_EXE_GUIDE.md)

## 🎉 完成！

打包成功后，您可以：
- 分发给其他用户
- 在没有 Python/Node.js 的机器上运行
- 创建安装程序
- 发布到应用商店

祝您使用愉快！

