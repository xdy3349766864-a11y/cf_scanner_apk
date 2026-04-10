from kivy.app import App
from kivy.uix.widget import Widget
from jnius import autoclass
from android.runnable import runOnMainThread

# 显式调用安卓底层原生组件
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
        
        # 启用 JavaScript 和本地存储
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        
        # 核心：拦截 URL 跳转，不唤起系统浏览器
        webview.setWebViewClient(WebViewClient())
        
        # 加载你的网页
        webview.loadUrl("https://zy.3349766.xyz")
        
        # 覆盖 Activity 视图
        activity.setContentView(webview)

if __name__ == '__main__':
    LumoHubApp().run()
