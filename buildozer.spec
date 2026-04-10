[app]
title = LumoHub
package.name = lumohub
package.domain = com.lumo

# 包含的文件后缀
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# 版本和权限
version = 1.0
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# --- 图标设置 ---
icon.filename = %(source.dir)s/ico.png

# 必须包含 pyjnius 以支持 WebView 调用
requirements = python3,kivy,pyjnius

orientation = portrait
fullscreen = 1

# 允许明文传输（如果是 https 则不影响，如果是 http 必须开启）
android.manifest.attributes = android:usesCleartextTraffic="true"

# 针对 Android 12+ 的适配（可选但建议）
android.api = 31
android.minapi = 21
