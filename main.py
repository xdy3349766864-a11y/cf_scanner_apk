from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock, mainthread
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.core.window import Window

import sys
import random
import time
import ipaddress
import asyncio
import aiohttp
import socket
import ssl
from datetime import datetime
from typing import List, Optional, Dict
import csv
import os
import threading

# 注意：Config.set 权限部分已移除，由 buildozer.spec 统一管理
Window.clearcolor = get_color_from_hex('#121212')

# --- 核心数据配置 ---
CF_IPV4_CIDRS = ["173.245.48.0/20", "103.21.244.0/22", "103.22.200.0/22", "103.31.4.0/22", "141.101.64.0/18", "108.162.192.0/18", "190.93.240.0/20", "188.114.96.0/20", "197.234.240.0/22", "198.41.128.0/17", "162.158.0.0/15", "104.16.0.0/12", "172.64.0.0/17", "172.64.128.0/18", "172.64.192.0/19", "172.64.224.0/22", "172.64.229.0/24", "172.64.230.0/23", "172.64.232.0/21", "172.64.240.0/21", "172.64.248.0/21", "172.65.0.0/16", "172.66.0.0/16", "172.67.0.0/16", "131.0.72.0/22"]
CF_IPV6_CIDRS = ["2400:cb00:2049::/48", "2606:4700::/32", "2606:4700:10::/48"]
AIRPORT_CODES = {"HKG": "香港", "TPE": "台北", "SJC": "圣何塞", "LAX": "洛杉矶", "SFO": "旧金山", "JFK": "纽约", "TYO": "东京", "SIN": "新加坡"}
PORT_OPTIONS = ["443", "2053", "2083", "2087", "2096", "8443"]

# --- 逻辑工具函数 ---
async def measure_tcp_latency(ip: str, port: int, timeout: float = 1.0) -> Optional[float]:
    start = time.monotonic()
    try:
        _, writer = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=timeout)
        latency = (time.monotonic() - start) * 1000
        writer.close()
        await writer.wait_closed()
        return round(latency, 2)
    except: return None

# --- UI 组件 ---
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
        self.add_widget(Label(text=data['ip'], size_hint_x=0.4))
        self.add_widget(Label(text=f"{data['latency']}ms", size_hint_x=0.2))
        self.add_widget(Label(text=data['region'], size_hint_x=0.2))
        self.add_widget(Label(text=f"{data['speed']}MB/s", size_hint_x=0.2))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            Clipboard.copy(self.data['ip'])
            App.get_running_app().show_toast(f"已复制: {self.data['ip']}")
            return True

# --- 主程序 ---
class CFScannerApp(App):
    def build(self):
        self.scan_results = []
        self.speed_results = []
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 头部
        layout.add_widget(Label(text="CloudFlare 优选工具", font_size=24, bold=True, size_hint_y=None, height=60))
        
        # 控制区
        ctrl = GridLayout(cols=2, spacing=10, size_hint_y=None, height=120)
        self.btn_scan = Button(text="开始扫描 (IPv4)", background_color=get_color_from_hex('#165DFF'))
        self.btn_scan.bind(on_press=self.run_scan)
        ctrl.add_widget(self.btn_scan)
        
        self.btn_export = Button(text="导出结果", background_color=get_color_from_hex('#00B42A'), disabled=True)
        self.btn_export.bind(on_press=self.export_to_android)
        ctrl.add_widget(self.btn_export)
        
        self.port_spinner = Spinner(text="443", values=PORT_OPTIONS)
        ctrl.add_widget(self.port_spinner)
        
        self.status_label = Label(text="准备就绪")
        ctrl.add_widget(self.status_label)
        layout.add_widget(ctrl)
        
        # 日志
        self.log_view = Label(text="等待操作...", size_hint_y=None, height=100, color=(0,1,0.6,1))
        layout.add_widget(self.log_view)
        
        # 结果列表
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
        threading.Thread(target=self._scan_thread, daemon=True).start()

    def _scan_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.update_log("正在生成随机 IP...")
        # 简化版生成逻辑
        ips = [str(ipaddress.IPv4Address(random.randint(2899907584, 2901481471))) for _ in range(50)]
        
        self.update_log("开始延迟测试...")
        results = []
        for ip in ips:
            lat = loop.run_until_complete(measure_tcp_latency(ip, int(self.port_spinner.text)))
            if lat:
                results.append({'ip': ip, 'latency': lat, 'region': '未知', 'speed': '0.00'})
        
        self.scan_results = sorted(results, key=lambda x: x['latency'])
        self.update_ui_results()

    @mainthread
    def update_ui_results(self):
        self.rv.data = self.scan_results
        self.update_log(f"扫描完成，找到 {len(self.scan_results)} 个可用 IP")
        self.btn_export.disabled = False

    def export_to_android(self, instance):
        try:
            from androidstorage4kivy import SharedStorage
            ss = SharedStorage()
            filename = f"CF_IP_{datetime.now().strftime('%H%M%S')}.csv"
            # 必须先写入应用的私有目录
            cache_path = os.path.join(self.user_data_dir, filename)
            with open(cache_path, 'w', encoding='utf-8-sig') as f:
                f.write("IP,延迟,地区\n")
                for r in self.scan_results:
                    f.write(f"{r['ip']},{r['latency']},{r['region']}\n")
            # 关键：调用系统接口复制到 Download 文件夹
            ss.copy_to_shared(cache_path)
            self.show_toast("已导出到系统下载文件夹")
        except Exception as e:
            self.update_log(f"导出出错: {e}")

    def show_toast(self, text):
        popup = Popup(title='提示', content=Label(text=text), size_hint=(0.6, 0.2))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

if __name__ == '__main__':
    CFScannerApp().run()
