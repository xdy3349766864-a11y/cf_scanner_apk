from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock, mainthread
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.config import Config

import random
import time
import ipaddress
import asyncio
import aiohttp
from datetime import datetime
import csv
import os
import threading

# 界面与图标初步配置
Config.set('kivy', 'window_icon', 'ico.png')
Window.clearcolor = get_color_from_hex('#121212')

# --- 核心配置 ---
PORT_OPTIONS = ["443", "2053", "2083", "2087", "2096", "8443"]

async def measure_tcp_latency(ip, port, timeout=1.0):
    start = time.monotonic()
    try:
        _, writer = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=timeout)
        latency = (time.monotonic() - start) * 1000
        writer.close()
        await writer.wait_closed()
        return round(latency, 2)
    except: return None

# --- 列表组件 ---
class RecycleViewRow(RecycleDataViewBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 45
        with self.canvas.before:
            Color(*get_color_from_hex('#1E1E1E'))
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[5])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos, self.rect.size = self.pos, self.size

    def refresh_view_attrs(self, rv, index, data):
        self.data = data
        self.clear_widgets()
        self.add_widget(Label(text=data['ip'], size_hint_x=0.5))
        self.add_widget(Label(text=f"{data['latency']}ms", size_hint_x=0.3))
        self.add_widget(Label(text="点击复制", size_hint_x=0.2, color=(0,0.7,1,1)))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            Clipboard.copy(self.data['ip'])
            App.get_running_app().show_toast(f"已复制: {self.data['ip']}")
            return True

# --- 主程序 ---
class CFScannerApp(App):
    def build(self):
        self.icon = 'ico.png'
        self.scan_results = []
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="CloudFlare 优选工具", font_size=24, bold=True, size_hint_y=None, height=60))
        
        ctrl = GridLayout(cols=2, spacing=10, size_hint_y=None, height=120)
        self.btn_scan = Button(text="开始扫描", background_color=get_color_from_hex('#165DFF'))
        self.btn_scan.bind(on_press=self.run_scan)
        ctrl.add_widget(self.btn_scan)
        
        self.btn_export = Button(text="导出结果", background_color=get_color_from_hex('#00B42A'), disabled=True)
        self.btn_export.bind(on_press=self.export_to_android)
        ctrl.add_widget(self.btn_export)
        
        self.port_spinner = Spinner(text="443", values=PORT_OPTIONS)
        ctrl.add_widget(self.port_spinner)
        
        self.log_view = Label(text="准备就绪", size_hint_y=None, height=40)
        ctrl.add_widget(self.log_view)
        layout.add_widget(ctrl)
        
        self.rv = RecycleView()
        self.rv.viewclass = 'RecycleViewRow'
        self.rv_layout = RecycleBoxLayout(orientation='vertical', size_hint_y=None, default_size=(None, 45), default_size_hint=(1, None))
        self.rv_layout.bind(minimum_height=self.rv_layout.setter('height'))
        self.rv.add_widget(self.rv_layout)
        layout.add_widget(self.rv)
        
        return layout

    @mainthread
    def update_log(self, text): self.log_view.text = text

    def run_scan(self, instance):
        self.btn_scan.disabled = True
        threading.Thread(target=self._scan_thread, daemon=True).start()

    def _scan_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.update_log("生成测试 IP...")
        # 模拟生成 CF 常用 IP 段
        ips = [f"104.{random.randint(16,20)}.{random.randint(1,254)}.{random.randint(1,254)}" for _ in range(50)]
        
        results = []
        for i, ip in enumerate(ips):
            self.update_log(f"测试进度: {i+1}/50")
            lat = loop.run_until_complete(measure_tcp_latency(ip, int(self.port_spinner.text)))
            if lat:
                results.append({'ip': ip, 'latency': lat})
        
        self.scan_results = sorted(results, key=lambda x: x['latency'])
        self.update_ui_results()

    @mainthread
    def update_ui_results(self):
        self.rv.data = self.scan_results
        self.btn_scan.disabled = False
        self.btn_export.disabled = False
        self.update_log(f"扫描完成，找到 {len(self.scan_results)} 个可用 IP")

    def export_to_android(self, instance):
        try:
            from androidstorage4kivy import SharedStorage
            ss = SharedStorage()
            filename = f"CF_IP_{datetime.now().strftime('%H%M%S')}.csv"
            cache_path = os.path.join(self.user_data_dir, filename)
            with open(cache_path, 'w', encoding='utf-8-sig') as f:
                f.write("IP,延迟\n")
                for r in self.scan_results:
                    f.write(f"{r['ip']},{r['latency']}\n")
            ss.copy_to_shared(cache_path)
            self.show_toast("已存至系统【下载】文件夹")
        except Exception as e:
            self.show_toast(f"导出失败: {e}")

    def show_toast(self, text):
        popup = Popup(title='提示', content=Label(text=text), size_hint=(0.7, 0.3))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

if __name__ == '__main__':
    CFScannerApp().run()
