from kivy.app import App
from kivy.uix.widget import Widget
from jnius import autoclass
from android.runnable import runOnMainThread

# 显式调用 Android 原生类
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
PythonActivity = autoclass('org.kivy.android.PythonActivity')

class LumoHubApp(App):
    def build(self):
        self.create_webview()
        return Widget()

    @runOnMainThread
    def create_webview(self):
        activity = PythonActivity.mActivity
        webview = WebView(activity)
        
        # WebView 基础配置
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setDatabaseEnabled(True)
        
        # 关键：确保所有 URL 点击都在当前 WebView 加载
        webview.setWebViewClient(WebViewClient())
        
        # 加载目标网址
        webview.loadUrl("https://zy.3349766.xyz")
        
        # 将 WebView 设为当前 Activity 的主视图
        activity.setContentView(webview)

if __name__ == '__main__':
    LumoHubApp().run()