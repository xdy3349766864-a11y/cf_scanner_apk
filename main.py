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
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock, mainthread
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.config import Config
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

# 安卓权限配置
Config.set('android', 'permissions', 'INTERNET, ACCESS_NETWORK_STATE')
Config.set('kivy', 'window_icon', 'icon.png')
Window.clearcolor = get_color_from_hex('#121212')

# 原工具核心常量（完全保留）
CF_IPV4_CIDRS = [
    "173.245.48.0/20", "103.21.244.0/22", "103.22.200.0/22", "103.31.4.0/22",
    "141.101.64.0/18", "108.162.192.0/18", "190.93.240.0/20", "188.114.96.0/20",
    "197.234.240.0/22", "198.41.128.0/17", "162.158.0.0/15", "104.16.0.0/12",
    "172.64.0.0/17", "172.64.128.0/18", "172.64.192.0/19", "172.64.224.0/22",
    "172.64.229.0/24", "172.64.230.0/23", "172.64.232.0/21", "172.64.240.0/21",
    "172.64.248.0/21", "172.65.0.0/16", "172.66.0.0/16", "172.67.0.0/16",
    "131.0.72.0/22"
]

CF_IPV6_CIDRS = [
    "2400:cb00:2049::/48", "2400:cb00:f00e::/48", "2606:4700::/32",
    "2606:4700:10::/48", "2606:4700:130::/48", "2606:4700:3000::/48",
    "2606:4700:3001::/48", "2606:4700:3002::/48", "2606:4700:3003::/48",
    "2606:4700:3004::/48", "2606:4700:3005::/48", "2606:4700:3006::/48",
    "2606:4700:3007::/48", "2606:4700:3008::/48", "2606:4700:3009::/48",
    "2606:4700:3010::/48", "2606:4700:3011::/48", "2606:4700:3012::/48",
    "2606:4700:3013::/48", "2606:4700:3014::/48", "2606:4700:3015::/48",
    "2606:4700:3016::/48", "2606:4700:3017::/48", "2606:4700:3018::/48",
    "2606:4700:3019::/48", "2606:4700:3020::/48", "2606:4700:3021::/48",
    "2606:4700:3022::/48", "2606:4700:3023::/48", "2606:4700:3024::/48",
    "2606:4700:3025::/48", "2606:4700:3026::/48", "2606:4700:3027::/48",
    "2606:4700:3028::/48", "2606:4700:3029::/48", "2606:4700:3030::/48",
    "2606:4700:3031::/48", "2606:4700:3032::/48", "2606:4700:3033::/48",
    "2606:4700:3034::/48", "2606:4700:3035::/48", "2606:4700:3036::/48",
    "2606:4700:3037::/48", "2606:4700:3038::/48", "2606:4700:3039::/48",
    "2606:4700:a0::/48", "2606:4700:a1::/48", "2606:4700:a8::/48",
    "2606:4700:a9::/48", "2606:4700:a::/48", "2606:4700:b::/48",
    "2606:4700:c::/48", "2606:4700:d0::/48", "2606:4700:d1::/48",
    "2606:4700:d::/48", "2606:4700:e0::/48", "2606:4700:e1::/48",
    "2606:4700:e2::/48", "2606:4700:e3::/48", "2606:4700:e4::/48",
    "2606:4700:e5::/48", "2606:4700:e6::/48", "2606:4700:e7::/48",
    "2606:4700:e::/48", "2606:4700:f1::/48", "2606:4700:f2::/48",
    "2606:4700:f3::/48", "2606:4700:f4::/48", "2606:4700:f5::/48",
    "2606:4700:f::/48", "2803:f800:50::/48", "2803:f800:51::/48",
    "2a06:98c1:3100::/48", "2a06:98c1:3101::/48", "2a06:98c1:3102::/48",
    "2a06:98c1:3103::/48", "2a06:98c1:3104::/48", "2a06:98c1:3105::/48",
    "2a06:98c1:3106::/48", "2a06:98c1:3107::/48", "2a06:98c1:3108::/48",
    "2a06:98c1:3109::/48", "2a06:98c1:310a::/48", "2a06:98c1:310b::/48",
    "2a06:98c1:310c::/48", "2a06:98c1:310d::/48", "2a06:98c1:310e::/48",
    "2a06:98c1:310f::/48", "2a06:98c1:3120::/48", "2a06:98c1:3121::/48",
    "2a06:98c1:3122::/48", "2a06:98c1:3123::/48", "2a06:98c1:3200::/48",
    "2a06:98c1:50::/48", "2a06:98c1:51::/48", "2a06:98c1:54::/48",
    "2a06:98c1:58::/48"
]

AIRPORT_CODES = {
    "HKG": "香港", "TPE": "台北", "KHH": "高雄", "MFM": "澳门",
    "NRT": "东京", "HND": "东京", "KIX": "大阪", "NGO": "名古屋",
    "FUK": "福冈", "CTS": "札幌", "OKA": "冲绳",
    "ICN": "首尔", "GMP": "首尔", "PUS": "釜山",
    "SIN": "新加坡", "BKK": "曼谷", "DMK": "曼谷",
    "KUL": "吉隆坡", "HKT": "普吉岛",
    "MNL": "马尼拉", "CEB": "宿务",
    "HAN": "河内", "SGN": "胡志明市",
    "JKT": "雅加达", "DPS": "巴厘岛",
    "DEL": "德里", "BOM": "孟买", "MAA": "金奈",
    "DXB": "迪拜", "AUH": "阿布扎比",
    "SJC": "圣何塞", "LAX": "洛杉矶", "SFO": "旧金山",
    "SEA": "西雅图", "PDX": "波特兰",
    "LAS": "拉斯维加斯", "PHX": "菲尼克斯",
    "DEN": "丹佛", "DFW": "达拉斯", "IAH": "休斯顿",
    "ORD": "芝加哥", "MSP": "明尼阿波利斯",
    "ATL": "亚特兰大", "MIA": "迈阿密", "MCO": "奥兰多",
    "JFK": "纽约", "EWR": "纽约", "LGA": "纽约",
    "BOS": "波士顿", "PHL": "费城", "IAD": "华盛顿",
    "YYZ": "多伦多", "YVR": "温哥华", "YUL": "蒙特利尔",
    "LHR": "伦敦", "LGW": "伦敦", "STN": "伦敦",
    "CDG": "巴黎", "ORY": "巴黎",
    "FRA": "法兰克福", "MUC": "慕尼黑", "TXL": "柏林",
    "AMS": "阿姆斯特丹", "EIN": "埃因霍温",
    "MAD": "马德里", "BCN": "巴塞罗那",
    "FCO": "罗马", "MXP": "米兰", "LIN": "米兰",
    "ZRH": "苏黎世", "GVA": "日内瓦",
    "VIE": "维也纳", "PRG": "布拉格",
    "WAW": "华沙", "KRK": "克拉科夫",
    "HEL": "赫尔辛基", "OSL": "奥斯陆", "ARN": "斯德哥尔摩",
    "CPH": "哥本哈根",
    "SYD": "悉尼", "MEL": "墨尔本", "BNE": "布里斯班",
    "PER": "珀斯", "ADL": "阿德莱德",
    "AKL": "奥克兰", "WLG": "惠灵顿",
    "GRU": "圣保罗", "GIG": "里约热内卢", "EZE": "布宜诺斯艾利斯",
    "SCL": "圣地亚哥", "LIM": "利马", "BOG": "波哥大",
    "JNB": "约翰内斯堡", "CPT": "开普敦", "CAI": "开罗",
}

PORT_OPTIONS = ["443", "2053", "2083", "2087", "2096", "8443"]

# 原工具核心函数（完全保留，无修改）
def get_iata_code_from_ip(ip: str, timeout: int = 3) -> Optional[str]:
    test_host = "speed.cloudflare.com"
    if ':' in ip:
        urls = [f"https://[{ip}]/cdn-cgi/trace", f"http://[{ip}]/cdn-cgi/trace"]
    else:
        urls = [f"https://{ip}/cdn-cgi/trace", f"http://{ip}/cdn-cgi/trace"]
    for url in urls:
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            use_ssl = url.startswith('https://')
            host = url[8:].split('/')[0].strip('[]') if use_ssl else url[7:].split('/')[0].strip('[]')
            port = 443 if use_ssl else 80
            if ':' in host:
                addrinfo = socket.getaddrinfo(host, port, socket.AF_INET6, socket.SOCK_STREAM)
                family, socktype, proto, canonname, sockaddr = addrinfo[0]
                s = socket.socket(family, socktype, proto)
                s.settimeout(timeout)
                s.connect(sockaddr)
            else:
                s = socket.create_connection((host, port), timeout=timeout)
            if use_ssl:
                s = ctx.wrap_socket(s, server_hostname=test_host)
            request = f"GET /cdn-cgi/trace HTTP/1.1\r\nHost: {test_host}\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\n\r\n".encode()
            s.sendall(request)
            data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
                if b"\r\n\r\n" in data:
                    header_end = data.find(b"\r\n\r\n")
                    body = data[header_end + 4:]
                    break
            s.close()
            response_text = body.decode('utf-8', errors='ignore')
            for line in response_text.splitlines():
                if line.startswith('colo='):
                    colo_value = line.split('=', 1)[1].strip()
                    if colo_value and colo_value.upper() != 'UNKNOWN':
                        return colo_value.upper()
            if b'CF-RAY' in data:
                for line in data.decode('utf-8', errors='ignore').split('\r\n'):
                    if line.startswith('CF-RAY:'):
                        cf_ray = line.split(':', 1)[1].strip()
                        if '-' in cf_ray:
                            parts = cf_ray.split('-')
                            for part in parts[-2:]:
                                if len(part) == 3 and part.isalpha():
                                    return part.upper()
        except Exception:
            continue
    return None

async def get_iata_code_async(session: aiohttp.ClientSession, ip: str, timeout: int = 3) -> Optional[str]:
    test_host = "speed.cloudflare.com"
    if ':' in ip:
        urls = [f"https://[{ip}]/cdn-cgi/trace", f"http://[{ip}]/cdn-cgi/trace"]
    else:
        urls = [f"https://{ip}/cdn-cgi/trace", f"http://{ip}/cdn-cgi/trace"]
    headers = {"User-Agent": "Mozilla/5.0 (Android) AppleWebKit/537.36", "Host": test_host}
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    for url in urls:
        try:
            use_ssl = url.startswith('https://')
            ssl_context = ssl_ctx if use_ssl else None
            async with session.get(url, headers=headers, ssl=ssl_context, timeout=aiohttp.ClientTimeout(total=timeout), allow_redirects=False) as response:
                if response.status == 200:
                    text = await response.text()
                    for line in text.strip().split('\n'):
                        if line.startswith('colo='):
                            colo_value = line.split('=', 1)[1].strip()
                            if colo_value and colo_value.upper() != 'UNKNOWN':
                                return colo_value.upper()
                    if 'CF-RAY' in response.headers:
                        cf_ray = response.headers['CF-RAY']
                        if '-' in cf_ray:
                            parts = cf_ray.split('-')
                            for part in parts[-2:]:
                                if len(part) == 3 and part.isalpha():
                                    return part.upper()
        except Exception:
            continue
    return None

def get_iata_translation(iata_code: str) -> str:
    return AIRPORT_CODES.get(iata_code, iata_code)

async def async_tcp_ping(ip: str, port: int, timeout: float = 1.0) -> Optional[float]:
    start_time = time.monotonic()
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=timeout)
        latency = (time.monotonic() - start_time) * 1000
        writer.close()
        await writer.wait_closed()
        return round(latency, 2)
    except Exception:
        return None

async def measure_tcp_latency(ip: str, port: int, ping_times: int = 4, timeout: float = 1.0) -> Optional[float]:
    latencies = []
    for i in range(ping_times):
        latency = await async_tcp_ping(ip, port, timeout)
        if latency is not None:
            latencies.append(latency)
        if i < ping_times - 1:
            await asyncio.sleep(0.05)
    return min(latencies) if latencies else None

class IPv4Scanner:
    def __init__(self, log_callback=None, progress_callback=None, port=443):
        self.max_workers = 50
        self.timeout = 1.0
        self.ping_times = 3
        self.running = True
        self.log_callback = log_callback
        self.progress_callback = progress_callback
        self.port = port
    def generate_ips_from_cidrs(self) -> List[str]:
        ip_list = []
        for cidr in CF_IPV4_CIDRS:
            try:
                network = ipaddress.ip_network(cidr, strict=False)
                for subnet in network.subnets(new_prefix=24):
                    if subnet.num_addresses > 2:
                        hosts = list(subnet.hosts())
                        if hosts:
                            selected_ips = random.sample(hosts, min(2, len(hosts)))
                            ip_list.extend([str(ip) for ip in selected_ips])
            except Exception as e:
                if self.log_callback:
                    self.log_callback(f"处理CIDR {cidr} 时出错: {e}")
                continue
        return ip_list
    async def test_ip_latency(self, session: aiohttp.ClientSession, ip: str) -> Optional[float]:
        return await measure_tcp_latency(ip, self.port, self.ping_times, self.timeout) if self.running else None
    async def test_single_ip(self, session: aiohttp.ClientSession, ip: str):
        if not self.running:
            return None
        latency = await self.test_ip_latency(session, ip)
        if latency is not None and latency < 230:
            iata_code = await get_iata_code_async(session, ip, self.timeout) if self.running else None
            return {
                'ip': ip, 'latency': latency, 'iata_code': iata_code,
                'chinese_name': get_iata_translation(iata_code) if iata_code else "未知地区",
                'success': True, 'ip_version': 4, 'scan_time': datetime.now().strftime("%H:%M:%S"),
                'port': self.port, 'ping_times': self.ping_times
            }
        return None
    async def batch_test_ips(self, ip_list: List[str]):
        semaphore = asyncio.Semaphore(self.max_workers)
        async def test_with_semaphore(session: aiohttp.ClientSession, ip: str):
            async with semaphore:
                return await self.test_single_ip(session, ip)
        connector = aiohttp.TCPConnector(limit=self.max_workers, force_close=True, enable_cleanup_closed=True, limit_per_host=0)
        successful_results = []
        start_time = time.time()
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [asyncio.create_task(test_with_semaphore(session, ip)) for ip in ip_list if self.running]
            completed = 0
            total = len(tasks)
            last_update_time = time.time()
            for future in asyncio.as_completed(tasks):
                if not self.running:
                    for task in tasks:
                        if not task.done():
                            task.cancel()
                    break
                result = await future
                completed += 1
                if result:
                    successful_results.append(result)
                current_time = time.time()
                if current_time - last_update_time >= 0.5 or completed == total:
                    elapsed = current_time - start_time
                    ips_per_second = completed / elapsed if elapsed > 0 else 0
                    if self.progress_callback:
                        self.progress_callback(completed, total, len(successful_results), ips_per_second)
                    last_update_time = current_time
        return successful_results
    async def run_scan_async(self):
        if self.log_callback:
            self.log_callback(f"正在生成IPv4随机IP... (端口: {self.port})")
        ip_list = self.generate_ips_from_cidrs()
        if not ip_list:
            if self.log_callback:
                self.log_callback("错误: 未能生成IPv4 IP列表")
            return None
        if self.log_callback:
            self.log_callback(f"已生成 {len(ip_list)} 个随机IPv4 IP，开始延迟测试...")
        results = await self.batch_test_ips(ip_list)
        if not self.running:
            if self.log_callback:
                self.log_callback("IPv4扫描被中止")
            return None
        return results
    def stop(self):
        self.running = False

class IPv6Scanner:
    def __init__(self, log_callback=None, progress_callback=None, port=443):
        self.max_workers = 30
        self.timeout = 1.0
        self.ping_times = 2
        self.running = True
        self.log_callback = log_callback
        self.progress_callback = progress_callback
        self.port = port
    def generate_ips_from_cidrs(self) -> List[str]:
        ip_list = []
        for cidr in CF_IPV6_CIDRS:
            try:
                network = ipaddress.ip_network(cidr, strict=False)
                if network.num_addresses > 2:
                    sample_size = min(50, network.num_addresses - 2)
                    for _ in range(sample_size):
                        random_ip_int = random.randint(int(network.network_address) + 1, int(network.broadcast_address) - 1)
                        random_ip = str(ipaddress.IPv6Address(random_ip_int))
                        ip_list.append(random_ip)
            except Exception as e:
                if self.log_callback:
                    self.log_callback(f"处理IPv6 CIDR {cidr} 时出错: {e}")
                continue
        return ip_list
    async def test_ip_latency(self, session: aiohttp.ClientSession, ip: str) -> Optional[float]:
        return await measure_tcp_latency(ip, self.port, self.ping_times, self.timeout) if self.running else None
    async def test_single_ip(self, session: aiohttp.ClientSession, ip: str):
        if not self.running:
            return None
        latency = await self.test_ip_latency(session, ip)
        if latency is not None and latency < 320:
            iata_code = await get_iata_code_async(session, ip, self.timeout) if self.running else None
            return {
                'ip': ip, 'latency': latency, 'iata_code': iata_code,
                'chinese_name': get_iata_translation(iata_code) if iata_code else "未知地区",
                'success': True, 'ip_version': 6, 'scan_time': datetime.now().strftime("%H:%M:%S"),
                'port': self.port, 'ping_times': self.ping_times
            }
        return None
    async def batch_test_ips(self, ip_list: List[str]):
        semaphore = asyncio.Semaphore(self.max_workers)
        async def test_with_semaphore(session: aiohttp.ClientSession, ip: str):
            async with semaphore:
                return await self.test_single_ip(session, ip)
        connector = aiohttp.TCPConnector(limit=self.max_workers, force_close=True, enable_cleanup_closed=True, limit_per_host=0, family=socket.AF_INET6)
        successful_results = []
        start_time = time.time()
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [asyncio.create_task(test_with_semaphore(session, ip)) for ip in ip_list if self.running]
            completed = 0
            total = len(tasks)
            last_update_time = time.time()
            for future in asyncio.as_completed(tasks):
                if not self.running:
                    for task in tasks:
                        if not task.done():
                            task.cancel()
                    break
                result = await future
                completed += 1
                if result:
                    successful_results.append(result)
                current_time = time.time()
                if current_time - last_update_time >= 0.5 or completed == total:
                    elapsed = current_time - start_time
                    ips_per_second = completed / elapsed if elapsed > 0 else 0
                    if self.progress_callback:
                        self.progress_callback(completed, total, len(successful_results), ips_per_second)
                    last_update_time = current_time
        return successful_results
    async def run_scan_async(self):
        if self.log_callback:
            self.log_callback(f"正在生成IPv6随机IP... (端口: {self.port})")
        ip_list = self.generate_ips_from_cidrs()
        if not ip_list:
            if self.log_callback:
                self.log_callback("错误: 未能生成IPv6 IP列表")
            return None
        if self.log_callback:
            self.log_callback(f"已生成 {len(ip_list)} 个随机IPv6 IP，开始延迟测试...")
        results = await self.batch_test_ips(ip_list)
        if not self.running:
            if self.log_callback:
                self.log_callback("IPv6扫描被中止")
            return None
        return results
    def stop(self):
        self.running = False

class SpeedTestWorker:
    def __init__(self, results: List[Dict], region_code: str = None, max_test_count=10, current_port=443, callback=None):
        self.results = results
        self.region_code = region_code.upper() if region_code else None
        self.max_test_count = max_test_count
        self.current_port = current_port
        self.callback = callback
        self.running = True
        self.test_host = "speed.cloudflare.com"
    def download_speed(self, ip: str, port: int) -> float:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = (
            "GET /__down?bytes=50000000 HTTP/1.1\r\n"
            f"Host: {self.test_host}\r\nUser-Agent: Mozilla/5.0 (Android)\r\n"
            "Accept: */*\r\nConnection: close\r\n\r\n"
        ).encode()
        try:
            if ':' in ip:
                addrinfo = socket.getaddrinfo(ip, port, socket.AF_INET6, socket.SOCK_STREAM)
                family, socktype, proto, canonname, sockaddr = addrinfo[0]
                sock = socket.socket(family, socktype, proto)
                sock.settimeout(5)
                sock.connect(sockaddr)
            else:
                sock = socket.create_connection((ip, port), timeout=5)
            ss = ctx.wrap_socket(sock, server_hostname=self.test_host)
            ss.sendall(req)
            start = time.time()
            data = b""
            header_done = False
            body = 0
            while time.time() - start < 3:
                buf = ss.recv(8192)
                if not buf:
                    break
                if not header_done:
                    data += buf
                    if b"\r\n\r\n" in data:
                        header_done = True
                        body += len(data.split(b"\r\n\r\n", 1)[1])
                else:
                    body += len(buf)
            ss.close()
            dur = time.time() - start
            return round((body / 1024 / 1024) / max(dur, 0.1), 2)
        except Exception as e:
            if self.callback:
                self.callback(f"测速失败 {ip}: {str(e)}")
            return 0.0
    def run(self):
        if not self.results:
            if self.callback:
                self.callback("错误：没有可用的IP进行测速")
            return []
        if self.region_code:
            filtered_results = [r for r in self.results if r.get('iata_code') and r['iata_code'].upper() == self.region_code]
            if self.callback:
                self.callback(f"开始地区测速：{self.region_code} ({AIRPORT_CODES.get(self.region_code, '未知地区')})")
        else:
            filtered_results = self.results
            if self.callback:
                self.callback("开始完全测速")
        if not filtered_results:
            if self.callback:
                self.callback("没有找到可用的IP进行测速")
            return []
        filtered_results.sort(key=lambda x: x.get('latency', float('inf')))
        target_ips = filtered_results[:min(self.max_test_count, len(filtered_results))]
        speed_results = []
        for i, ip_info in enumerate(target_ips):
            if not self.running:
                break
            ip = ip_info['ip']
            latency = ip_info.get('latency', 0)
            if self.callback:
                self.callback(f"[{i+1}/{len(target_ips)}] 正在测速 {ip}")
            download_speed = self.download_speed(ip, self.current_port)
            colo = get_iata_code_from_ip(ip, timeout=3) or ip_info.get('iata_code', 'UNKNOWN')
            speed_result = {
                'ip': ip, 'latency': latency, 'download_speed': download_speed,
                'iata_code': colo.upper(), 'chinese_name': AIRPORT_CODES.get(colo.upper(), '未知地区'),
                'test_type': '地区测速' if self.region_code else '完全测速', 'port': self.current_port
            }
            speed_results.append(speed_result)
            if self.callback:
                self.callback(f"  测速结果: {download_speed} MB/s, 地区: {speed_result['chinese_name']}")
            time.sleep(1)
        speed_results.sort(key=lambda x: x['download_speed'], reverse=True)
        if self.callback:
            self.callback(f"测速完成！成功测速 {len(speed_results)}/{len(target_ips)} 个IP")
        return speed_results
    def stop(self):
        self.running = False

# Kivy 自定义组件
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))

class RecycleViewRow(RecycleDataViewBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 40
        self.padding = [5, 5]
        self.index = None
        self.data = None
        with self.canvas.before:
            Color(*get_color_from_hex('#0A0A0A'))
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[5,5,5,5])
        self.bind(pos=self.update_rect, size=self.update_rect)
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.data = data
        return super().refresh_view_attrs(rv, index, data)
    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            if self.collide_point(*touch.pos):
                Clipboard.copy(self.data['ip'])
                App.get_running_app().show_toast(f"已复制IP: {self.data['ip'][:20]}...")
                return True
        return False

class CFScannerApp(App):
    def build(self):
        self.title = "CloudFlare 优选IP扫描工具"
        self.icon = "icon.png"
        self.scanning = False
        self.speed_testing = False
        self.scan_results = []
        self.speed_results = []
        self.current_scan_port = 443

        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 标题
        title_label = Label(text="☁️ CloudFlare 优选IP扫描工具", font_size=20, color=get_color_from_hex('#00BFFF'), bold=True, size_hint_y=None, height=50)
        main_layout.add_widget(title_label)

        # 扫描控制区
        scan_layout = GridLayout(cols=3, spacing=10, size_hint_y=None, height=60)
        self.btn_ipv4 = Button(text="IPv4 扫描", background_color=get_color_from_hex('#165DFF'), size_hint_y=None, height=50)
        self.btn_ipv4.bind(on_press=self.start_ipv4_scan)
        scan_layout.add_widget(self.btn_ipv4)

        self.btn_ipv6 = Button(text="IPv6 扫描", background_color=get_color_from_hex('#00B42A'), size_hint_y=None, height=50)
        self.btn_ipv6.bind(on_press=self.start_ipv6_scan)
        scan_layout.add_widget(self.btn_ipv6)

        self.btn_stop = Button(text="停止任务", background_color=get_color_from_hex('#F53F3F'), size_hint_y=None, height=50, disabled=True)
        self.btn_stop.bind(on_press=self.confirm_stop_all_tasks)
        scan_layout.add_widget(self.btn_stop)
        main_layout.add_widget(scan_layout)

        # 测速控制区
        speed_layout = GridLayout(cols=4, spacing=10, size_hint_y=None, height=60)
        self.input_region = TextInput(hint_text="地区码(如SJC)", size_hint_y=None, height=50, background_color=get_color_from_hex('#1E1E1E'), foreground_color=get_color_from_hex('#FFFFFF'))
        speed_layout.add_widget(self.input_region)

        self.input_speed_count = TextInput(text="10", size_hint_y=None, height=50, background_color=get_color_from_hex('#1E1E1E'), foreground_color=get_color_from_hex('#FFFFFF'))
        speed_layout.add_widget(self.input_speed_count)

        self.combo_port = Spinner(text="443", values=PORT_OPTIONS, size_hint_y=None, height=50, background_color=get_color_from_hex('#1E1E1E'), foreground_color=get_color_from_hex('#FFFFFF'))
        speed_layout.add_widget(self.combo_port)

        self.btn_area = Button(text="地区测速", background_color=get_color_from_hex('#722ED1'), size_hint_y=None, height=50, disabled=True)
        self.btn_area.bind(on_press=self.start_region_speed_test)
        speed_layout.add_widget(self.btn_area)
        main_layout.add_widget(speed_layout)

        # 第二行测速按钮
        speed_layout2 = GridLayout(cols=3, spacing=10, size_hint_y=None, height=60)
        self.btn_full = Button(text="完全测速", background_color=get_color_from_hex('#FF7D00'), size_hint_y=None, height=50, disabled=True)
        self.btn_full.bind(on_press=self.start_full_speed_test)
        speed_layout2.add_widget(self.btn_full)

        self.btn_export = Button(text="导出CSV", background_color=get_color_from_hex('#13C2C2'), size_hint_y=None, height=50, disabled=True)
        self.btn_export.bind(on_press=self.export_results)
        speed_layout2.add_widget(self.btn_export)

        self.btn_clear = Button(text="清空日志", background_color=get_color_from_hex('#666666'), size_hint_y=None, height=50)
        self.btn_clear.bind(on_press=self.clear_log)
        speed_layout2.add_widget(self.btn_clear)
        main_layout.add_widget(speed_layout2)

        # 进度条
        self.progress_bar = ProgressBar(max=100, value=0, size_hint_y=None, height=20)
        main_layout.add_widget(self.progress_bar)

        # 状态标签
        self.status_label = Label(text="✅ 就绪", color=get_color_from_hex('#00FF9C'), size_hint_y=None, height=30)
        main_layout.add_widget(self.status_label)

        # 日志区
        log_scroll = ScrollView(size_hint_y=None, height=150)
        self.log_text = Label(text="", color=get_color_from_hex('#00FF9C'), markup=True, size_hint_y=None)
        self.log_text.bind(texture_size=self.log_text.setter('size'))
        log_scroll.add_widget(self.log_text)
        main_layout.add_widget(log_scroll)

        # 结果表格
        self.rv = RecycleView()
        self.rv.layout_manager = SelectableRecycleBoxLayout()
        self.rv.data = []
        main_layout.add_widget(self.rv)

        return main_layout

    # 日志更新
    @mainthread
    def update_log(self, msg):
        current_text = self.log_text.text
        self.log_text.text = current_text + f"\n{msg}" if current_text else msg

    # 进度更新
    @mainthread
    def update_progress(self, current, total, success, speed):
        self.progress_bar.value = int(current/total*100) if total > 0 else 0
        self.status_label.text = f"🔍 扫描中：{current}/{total} | 可用：{success} | 速度：{speed:.1f} IP/秒"

    @mainthread
    def update_speed_progress(self, current, total):
        self.progress_bar.value = int(current/total*100) if total > 0 else 0
        self.status_label.text = f"⚡ 测速中：{current}/{total}"

    # 按钮状态控制
    def update_ui_state(self, running):
        self.btn_stop.disabled = not running
        self.btn_ipv4.disabled = running
        self.btn_ipv6.disabled = running
        self.btn_area.disabled = running or not bool(self.scan_results)
        self.btn_full.disabled = running or not bool(self.scan_results)
        self.btn_export.disabled = running or not bool(self.speed_results)
        self.input_region.disabled = running
        self.input_speed_count.disabled = running
        self.combo_port.disabled = running
        if not running:
            self.progress_bar.value = 0
            self.status_label.text = "✅ 就绪"

    # 扫描任务
    def start_ipv4_scan(self, instance):
        if self.scanning or self.speed_testing:
            return
        self.scanning = True
        self.update_ui_state(True)
        self.scan_results = []
        self.rv.data = []
        self.update_log("🚀 开始 IPv4 扫描...")
        self.current_scan_port = int(self.combo_port.text)
        self.scanner = IPv4Scanner(log_callback=self.update_log, progress_callback=self.update_progress, port=self.current_scan_port)
        threading.Thread(target=self.run_scan_thread, daemon=True).start()

    def start_ipv6_scan(self, instance):
        if self.scanning or self.speed_testing:
            return
        self.scanning = True
        self.update_ui_state(True)
        self.scan_results = []
        self.rv.data = []
        self.update_log("🚀 开始 IPv6 扫描...")
        self.current_scan_port = int(self.combo_port.text)
        self.scanner = IPv6Scanner(log_callback=self.update_log, progress_callback=self.update_progress, port=self.current_scan_port)
        threading.Thread(target=self.run_scan_thread, daemon=True).start()

    def run_scan_thread(self):
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(self.scanner.run_scan_async())
        loop.close()
        self.scan_finished(results)

    @mainthread
    def scan_finished(self, results):
        self.scanning = False
        self.scan_results = results
        if results:
            ipv4 = sum(1 for r in results if ':' not in r['ip'])
            ipv6 = len(results) - ipv4
            self.update_log(f"\n🎉 扫描完成！可用 IPv4：{ipv4} 个 | IPv6：{ipv6} 个")
        else:
            self.update_log("\n❌ 未找到可用IP")
        self.update_ui_state(False)

    # 测速任务
    def start_full_speed_test(self, instance):
        if not self.scan_results:
            self.update_log("❌ 请先扫描获取IP！")
            return
        self.speed_testing = True
        self.update_ui_state(True)
        count = int(self.input_speed_count.text)
        self.speed_worker = SpeedTestWorker(self.scan_results, max_test_count=count, current_port=self.current_scan_port, callback=self.update_log)
        threading.Thread(target=self.run_speed_thread, daemon=True).start()

    def start_region_speed_test(self, instance):
        region = self.input_region.text.strip().upper()
        if not region:
            self.update_log("❌ 请输入地区码！")
            return
        if not self.scan_results:
            self.update_log("❌ 请先扫描获取IP！")
            return
        self.speed_testing = True
        self.update_ui_state(True)
        count = int(self.input_speed_count.text)
        self.speed_worker = SpeedTestWorker(self.scan_results, region, count, self.current_scan_port, callback=self.update_log)
        threading.Thread(target=self.run_speed_thread, daemon=True).start()

    def run_speed_thread(self):
        results = self.speed_worker.run()
        self.speed_test_finished(results)

    @mainthread
    def speed_test_finished(self, results):
        self.speed_testing = False
        self.speed_results = results
        self.update_rv_data(results)
        self.btn_export.disabled = not bool(results)
        self.update_ui_state(False)

    # 表格数据更新
    def update_rv_data(self, results):
        rv_data = []
        for i, r in enumerate(results, 1):
            rv_data.append({
                'rank': str(i),
                'ip': r['ip'],
                'region': r['chinese_name'],
                'latency': f"{r['latency']:.2f}",
                'speed': f"{r['download_speed']:.2f}",
                'port': str(r['port']),
                'type': r['test_type']
            })
        self.rv.data = rv_data

    # 导出CSV
    def export_results(self, instance):
        if not self.speed_results:
            self.update_log("❌ 无测速结果可导出！")
            return
        try:
            from androidstorage4kivy import SharedStorage
            ss = SharedStorage()
            file_path = ss.get_cache_dir() + f"/CF扫描结果_{datetime.now().strftime('%Y%m%d')}.csv"
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, ['排名', 'IP', '地区码', '地区', '延迟', '速度', '端口', '类型'])
                writer.writeheader()
                for i, r in enumerate(self.speed_results, 1):
                    writer.writerow({
                        '排名': i, 'IP': r['ip'], '地区码': r['iata_code'],
                        '地区': r['chinese_name'], '延迟': f"{r['latency']:.2f}",
                        '速度': f"{r['download_speed']:.2f}", '端口': r['port'], '类型': r['test_type']
                    })
            ss.copy_to_shared(file_path)
            self.update_log(f"✅ 结果已导出到下载文件夹！")
        except Exception as e:
            self.update_log(f"❌ 导出失败: {str(e)}")

    # 停止任务
    def confirm_stop_all_tasks(self, instance):
        popup = Popup(title='确认停止', content=Label(text='确定要停止当前任务吗？'), size_hint=(0.8, 0.2))
        btn_yes = Button(text='确定', background_color=get_color_from_hex('#F53F3F'))
        btn_no = Button(text='取消', background_color=get_color_from_hex('#666666'))
        layout = BoxLayout(spacing=10)
        layout.add_widget(btn_yes)
        layout.add_widget(btn_no)
        popup.content = layout
        btn_yes.bind(on_press=lambda x: self.stop_all_tasks(popup))
        btn_no.bind(on_press=popup.dismiss)
        popup.open()

    def stop_all_tasks(self, popup):
        popup.dismiss()
        if hasattr(self, 'scanner'):
            self.scanner.stop()
        if hasattr(self, 'speed_worker'):
            self.speed_worker.stop()
        self.update_ui_state(False)

    # 清空日志
    def clear_log(self, instance):
        self.log_text.text = ""

    # 吐司提示
    def show_toast(self, msg):
        toast = Label(text=msg, color=get_color_from_hex('#FFFFFF'), background_color=get_color_from_hex('#000000'), size_hint=(None, None), size=(len(msg)*10, 40), pos_hint={'center_x': 0.5, 'center_y': 0.1})
        toast.opacity = 0.8
        self.root.add_widget(toast)
        Clock.schedule_once(lambda dt: self.root.remove_widget(toast), 2)

if __name__ == '__main__':
    CFScannerApp().run()