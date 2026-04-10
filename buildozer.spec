[app]
title = LumoHub
package.name = lumohub
package.domain = com.lumo
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# 图标：确保仓库里有这个文件
icon.filename = %(source.dir)s/ico.png

# 必须包含 pyjnius 否则 main.py 会崩溃
requirements = python3,kivy==2.2.1,pyjnius

android.permissions = INTERNET, ACCESS_NETWORK_STATE
orientation = portrait
fullscreen = 1

# 兼容性设置
android.archs = arm64-v8a, armeabi-v7a
android.allow_mixed_content = True
android.manifest.attributes = android:usesCleartextTraffic="true"
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 31

[buildozer]
log_level = 2
warn_on_root = 1