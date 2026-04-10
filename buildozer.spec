[app]
# 软件名称和包名
title = LumoHub
package.name = lumohub
package.domain = com.lumo

# 源码目录
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# 版本号
version = 0.1

# 权限
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# 图标 (确保你的文件夹里有这个图标文件)
icon.filename = %(source.dir)s/icon.png

# 必须包含 jnius 用于调用安卓底层
requirements = python3,kivy,pyjnius

# 屏幕方向
orientation = portrait

# 允许明文传输 (HTTP)
android.manifest.attributes = android:usesCleartextTraffic="true"
