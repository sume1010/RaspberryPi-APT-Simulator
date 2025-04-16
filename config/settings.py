import os
import platform


class Settings:
    # 系统信息
    SYSTEM_ARCH = 'aarch64' if 'aarch64' in platform.machine() else 'armv7l'
    KALI_VERSION = '2023.4'

    # 网络配置
    C2_IP = '0.0.0.0'
    C2_PORT = 4433
    DNS_EXFIL = '8.8.4.4'

    # 资源限制
    MAX_CPU_TEMP = 75  # 摄氏度
    MAX_MEM_USAGE = 85  # 百分比
    MAX_DISK_USAGE = 90

    # 路径配置
    BASE_DIR = '/opt/aptsim'
    PAYLOAD_DIR = f'{BASE_DIR}/.payloads'
    DATA_DIR = f'{BASE_DIR}/.data'

    # 监控配置
    MONITOR_REFRESH = 3  # 秒


settings = Settings()