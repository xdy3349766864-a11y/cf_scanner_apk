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
        return Widget()  # 返回一个空挂件，界面由原生 WebView 覆盖

    @runOnMainThread
    def create_webview(self):
        activity = PythonActivity.mActivity
        webview = WebView(activity)
        
        # 配置 WebView 设置
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setDatabaseEnabled(True)
        
        # 核心：设置 WebViewClient 确保不跳转到浏览器
        webview.setWebViewClient(WebViewClient())
        
        # 加载你的网页
        webview.loadUrl("https://zy.3349766.xyz")
        
        # 将 WebView 设置为当前显示的视图
        activity.setContentView(webview)

if __name__ == '__main__':
    LumoHubApp().run()
