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
# 图标（自动用你的六花PNG）
icon.filename = icon.png
# 应用权限（安卓网络权限必须）
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
# 依赖（完全匹配你的代码）
requirements = python3, kivy==2.2.1, aiohttp, asyncio, ipaddress, ssl, socket, csv, androidstorage4kivy
# 安卓SDK配置
android.api = 33
android.ndk = 25.2.9519653
android.build_tools_version = 33.0.2
android.sdk = 26.1.1
android.ndk_path =
android.sdk_path =
android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True
android.use_androidx = True
# 打包优化
android.debug = 0
android.release = 1
android.allow_backup = True
android.backup_service = org.kivy.android.BackupService

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
android_sdk_update = 0