[app]
# 应用基本信息
title = CloudFlare优选IP扫描工具
package.name = cfscanner
package.domain = org.lumohub
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
orientation = portrait
fullscreen = 0
icon.filename = icon.png

# 应用权限
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# 依赖库：关键在于明确 pyjnius 版本
requirements = python3, kivy==2.3.0, pyjnius>=1.6.0, aiohttp, androidstorage4kivy

# 安卓配置
android.api = 33
android.minapi = 21
android.ndk = 25c
android.build_tools_version = 33.0.2
android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True

# 路径保持为空，由 GitHub Actions 自动填充
android.ndk_path =
android.sdk_path =

# 编译优化
android.debug = 1
android.release = 0
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
android_sdk_update = 0
