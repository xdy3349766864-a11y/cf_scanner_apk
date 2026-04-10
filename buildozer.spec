[app]
# --- 应用基本信息 ---
title = CF优选工具
package.name = cfscanner
package.domain = org.lumohub
source.dir = .
# 必须包含 png 以确保你的 ico.png 被打包进去
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
orientation = portrait
fullscreen = 0

# --- 图标配置 (已对齐你的文件名) ---
icon.filename = ico.png

# --- 权限配置 ---
# 包含网络和安卓 11+ 导出文件所需的存储权限
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# --- 依赖库 (核心修复点) ---
# 1. 升级 kivy 到 2.3.0 以适配 Python 3.11
# 2. 强制指定 pyjnius 版本以修复 "long" 报错
# 3. 包含 androidstorage4kivy 用于结果导出
requirements = python3, kivy==2.3.0, pyjnius>=1.6.0, aiohttp, androidstorage4kivy, certifi

# --- 安卓工具链配置 ---
android.api = 33
android.minapi = 21
# 使用 25c 版本，避开谷歌已失效的 25b 下载地址
android.ndk = 25c
android.build_tools_version = 33.0.2
android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True

# --- 编译路径 (留空由 GitHub 自动处理) ---
android.ndk_path =
android.sdk_path =

# --- 打包优化 ---
android.debug = 1
android.release = 0
android.allow_backup = True
android.backup_service = org.kivy.android.BackupService

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
android_sdk_update = 0
