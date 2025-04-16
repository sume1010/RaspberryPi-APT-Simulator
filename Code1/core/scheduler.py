import time
import random
import subprocess
from gpiozero import CPUTemperature
from config import settings


class AttackScheduler:
    def __init__(self):
        self.cpu = CPUTemperature()
        self.task_queue = []
        self.current_load = 0

    def _get_system_load(self):
        """获取当前系统负载"""
        return {
            'cpu_temp': self.cpu.temperature,
            'cpu_usage': psutil.cpu_percent(),
            'mem_usage': psutil.virtual_memory().percent
        }

    def _adjust_attack_intensity(self):
        """动态调整攻击强度"""
        load = self._get_system_load()

        if load['cpu_temp'] > settings.MAX_CPU_TEMP - 10:
            return 0.5  # 降频模式
        elif load['mem_usage'] > settings.MAX_MEM_USAGE - 15:
            return 0.7  # 节流模式
        else:
            return 1.0  # 全速模式

    def add_task(self, task_func, args=()):
        """添加攻击任务"""
        self.task_queue.append((task_func, args))

    def execute_chain(self):
        """执行攻击链"""
        while self.task_queue:
            current_factor = self._adjust_attack_intensity()

            if current_factor < 0.3:
                time.sleep(10)  # 冷却等待
                continue

            task = self.task_queue.pop(0)
            try:
                # 随机延迟增加隐蔽性
                delay = random.randint(0, 5) * current_factor
                time.sleep(delay)

                # 启动子进程执行任务
                subprocess.Popen(
                    ["python3", "-c",
                     f"from {task[0].__module__} import {task[0].__name__}; {task[0].__name__}(*{task[1]})"],
                    stderr=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL
                )

            except Exception as e:
                print(f"任务执行失败: {str(e)}")

            time.sleep(5 * current_factor)