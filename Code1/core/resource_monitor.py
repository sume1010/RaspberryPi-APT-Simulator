import time
import psutil
import sys
from datetime import datetime
from config import settings


class ResourceDashboard:
    def __init__(self):
        self.colors = {
            'title': '\033[1;35m',
            'ok': '\033[38;5;46m',
            'warn': '\033[38;5;208m',
            'alert': '\033[1;31m',
            'reset': '\033[0m'
        }
        self.graph_symbols = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

    def _get_temp(self):
        try:
            with open('/sys/class/thermal/thermal_zone0/temp') as f:
                return int(f.read()) / 1000
        except:
            return 0.0

    def _generate_gauge(self, value, max_val):
        filled = int((value / max_val) * 20)
        bar = '█' * filled + '-' * (20 - filled)
        color = self.colors['ok']
        if value > max_val * 0.8:
            color = self.colors['alert']
        elif value > max_val * 0.6:
            color = self.colors['warn']
        return f"{color}{bar}{self.colors['reset']} {value:.1f}°C"

    def display(self):
        """显示动态仪表盘"""
        while True:
            # 获取数据
            stats = {
                'time': datetime.now().strftime("%H:%M:%S"),
                'cpu_temp': self._get_temp(),
                'cpu_usage': psutil.cpu_percent(),
                'mem_usage': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent
            }

            # 构建显示
            sys.stdout.write('\x1b[H\x1b[J')  # 清屏
            print(f"{self.colors['title']}=== 树莓派APT监控系统 ==={self.colors['reset']}")
            print(f"CPU温度: {self._generate_gauge(stats['cpu_temp'], settings.MAX_CPU_TEMP)}")
            print(f"内存使用: {self._generate_gauge(stats['mem_usage'], 100)}")
            print(f"磁盘使用: {self._generate_gauge(stats['disk_usage'], 100)}")
            print(f"{self.colors['ok']}Last Update: {stats['time']}{self.colors['reset']}\n")

            time.sleep(settings.MONITOR_REFRESH)