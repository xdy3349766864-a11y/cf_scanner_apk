[app]
# 应用基本信息
title = CF优选工具
package.name = cfscanner
package.domain = org.lumohub
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
orientation = portrait
fullscreen = 0

# 你的图片文件名
icon.filename = ico.png

# 必须包含这些库，特别是针对 Python 3.11 的修复
requirements = python3, kivy==2.3.0, pyjnius>=1.6.0, aiohttp, androidstorage4kivy, certifi

android.permissions = INTERNET, ACCESS_NETWORK_STATE, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
# 避开 404 的 NDK 版本
android.ndk = 25c
android.build_tools_version = 33.0.2
android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
