from core.c2_server import C2Server
from core.resource_monitor import ResourceDashboard
from modules.reconnaissance.network_scan import StealthScanner
from config import paths, settings
import signal
import sys


class APTSimulator:
    def __init__(self):
        self.c2 = C2Server()
        self.dashboard = ResourceDashboard()
        self.scanner = StealthScanner()

    def _signal_handler(self, sig, frame):
        """优雅退出处理"""
        print("\n\033[33m[!] 正在清理资源...\033[0m")
        sys.exit(0)

    def start(self):
        """系统启动"""
        paths.init()
        signal.signal(signal.SIGINT, self._signal_handler)

        print("\033[36m[+] 启动C2服务器...\033[0m")
        self.c2.run()

        print("\033[36m[+] 启动资源监控...\033[0m")
        self.dashboard.display()

        print("\033[36m[+] 执行初始侦察...\033[0m")
        targets = self.scanner.arp_scan('192.168.1.0/24')
        print(f"发现活跃主机: {len(targets)}")


if __name__ == "__main__":
    apt = APTSimulator()
    apt.start()