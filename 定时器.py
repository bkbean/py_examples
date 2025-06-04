import time
from enum import Enum, auto
from datetime import datetime
from threading import Event, Thread


class TimerMode(Enum):
    TIMER = auto()      # 低精度，使用 sleep 间隔
    PRECISION = auto()  # 基于时间补偿算法, 避免误差累积（适合高精度场景, 数据采集、硬件控制）

class SmartTimer:
    def __init__(self, interval, function, mode=TimerMode.TIMER):
        self.interval = interval    # 单位: 秒 (支持浮点数, 如 0.001 表示 1ms)
        self.function = function
        self.mode = mode
        self._stop_event = Event()
        self._thread = None
    
    def start(self):
        if self._thread and self._thread.is_alive():
            return  # 避免重复启动
        self._stop_event.clear()
        self._thread = Thread(target=self._run, daemon=True)
        self._thread.start()
    
    def _run(self):
        next_call = time.time()
        while not self._stop_event.is_set():
            now = time.time()
            if self.mode == TimerMode.PRECISION:
                # 精确补偿
                next_call += self.interval
                sleep_time = max(0, next_call - now)
            else:
                # 普通 sleep 间隔
                sleep_time = self.interval

            if sleep_time > 0:
                time.sleep(sleep_time)
            self.function()

            if self.mode == TimerMode.TIMER:
                # 每次函数执行后重新设定下次时间（可能有漂移）
                next_call = time.time()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=1.0)

    # _enter__ 和 __exit__ 是 上下文管理协议 (Context Management Protocol) 的两个魔术方法, 配合 with 语句使用, 可以实现资源的自动管理
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

def timer_task():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    print(f'[定时任务] {current_time}')


if __name__ == '__main__':
    print('=== 定时器模式测试 ===')
    print('1. TIMER模式 (可能有累积误差)')
    print('2. PRECISION模式 (高精度)')

    choice = input('请选择模式 (1/2): ').strip()
    mode = TimerMode.TIMER if choice == '1' else TimerMode.PRECISION

    with SmartTimer(1.0, timer_task, mode):
        input('定时器运行中，按回车停止...\n')

    # 自动调用 stop()，线程安全退出
    print('定时器已停止')
