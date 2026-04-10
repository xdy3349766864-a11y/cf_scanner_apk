[app]
title = CloudFlare优选IP扫描工具
package.name = cfscanner
package.domain = org.lumohub
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
orientation = portrait
fullscreen = 0
icon.filename = icon.png

# 权限
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# 依赖（去掉了标准库，只保留外部库）
requirements = python3, kivy==2.2.1, aiohttp, androidstorage4kivy

# 安卓配置（使用了更稳的 25c 和 API 33）
android.api = 33
android.ndk = 25c
android.build_tools_version = 33.0.2
android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True

# 预设路径留空，让 GitHub Actions 自动管理
android.ndk_path =
android.sdk_path =

[buildozer]
log_level = 2
