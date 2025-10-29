# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 打包配置文件
用于将应用打包成独立的可执行文件
"""

block_cipher = None

a = Analysis(
    ['backend/app_standalone.py', 'backend/app.py', 'backend/checker.py'],  # 直接分析这些文件
    pathex=['backend'],  # 添加 backend 目录到搜索路径
    binaries=[],
    datas=[
        ('frontend/dist', 'frontend_dist'),  # 包含前端构建文件
        ('backend/uploads', 'uploads'),      # 包含上传文件夹
        ('backend/results', 'results'),      # 包含结果文件夹
    ],
    hiddenimports=[
        'flask',
        'flask_cors',
        'cloudscraper',
        'requests',
        'werkzeug',
        'werkzeug.security',
        'werkzeug.utils',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'PIL',
        'tkinter',
        'test',
        'unittest',
        'pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='StirEmailChecker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 显示控制台窗口（可以看到日志）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加图标文件路径，例如 'icon.ico'
)

