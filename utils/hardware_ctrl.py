from gpiozero import LED, Button
import time


class HardwareController:
    def __init__(self):
        self.trigger_pin = Button(17)
        self.status_led = LED(27)
        self._setup_callbacks()

    def _setup_callbacks(self):
        """设置GPIO回调"""
        self.trigger_pin.when_pressed = self._on_trigger

    def _on_trigger(self):
        """物理触发攻击链"""
        self.status_led.blink(0.1, 0.1, 5)
        os.system(f"python3 {settings.BASE_DIR}/start_attack.py &")

    def indicate_status(self, status_code):
        """LED状态指示"""
        patterns = {
            0: (1, 1),  # 常亮：准备就绪
            1: (0.5, 0.5),  # 慢闪：运行中
            2: (0.1, 0.1)  # 快闪：警告状态
        }
        self.status_led.blink(*patterns[status_code])