from kivy.app import App
from kivy.uix.widget import Widget
from jnius import autoclass
from android.runnable import runOnMainThread

# 调用 Android 原生类
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
        
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setDatabaseEnabled(True)
        
        # 核心：确保跳转不跳出 App
        webview.setWebViewClient(WebViewClient())
        
        webview.loadUrl("https://zy.3349766.xyz")
        activity.setContentView(webview)

if __name__ == '__main__':
    LumoHubApp().run()