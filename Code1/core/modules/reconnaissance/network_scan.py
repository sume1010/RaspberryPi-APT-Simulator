import nmap
import json
from config import settings


class StealthScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()

    def arp_scan(self, subnet):
        """隐蔽ARP扫描"""
        self.nm.scan(
            hosts=subnet,
            arguments='-sn -PR -T2 --max-rate 10',
            sudo=True
        )
        return [host for host in self.nm.all_hosts() if self.nm[host].state() == 'up']

    def service_detect(self, target):
        """服务指纹识别"""
        self.nm.scan(
            hosts=target,
            arguments='-sV -T3 --version-intensity 3',
            sudo=True
        )
        return {
            'os': self.nm[target]['osmatch'][0]['name'] if self.nm[target]['osmatch'] else 'Unknown',
            'services': self.nm[target].get('tcp', {})
        }