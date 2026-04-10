from kivy.app import App
from kivy.uix.webview import WebView  # 注意：在安卓上通常需要 jnius 调用原生
from android.runnable import runOnMainThread
from jnius import autoclass

# 导入安卓原生类
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
android_activity = autoclass('org.kivy.android.PythonActivity').mActivity

class LumoHubApp(App):
    def build(self):
        self.create_webview()
        return None  # Kivy 界面留空，直接覆盖原生 WebView

    @runOnMainThread
    def create_webview(self):
        webview = WebView(android_activity)
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        
        # 核心：确保跳转不跳出 App
        webview.setWebViewClient(WebViewClient())
        
        android_activity.setContentView(webview)
        webview.loadUrl("https://zy.3349766.xyz")

if __name__ == '__main__':
    LumoHubApp().run()
