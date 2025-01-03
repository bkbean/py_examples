from threading import Event, Timer
import time


# 创建一个事件对象
stop_event = Event()

def timer_task():
    print(f'{time.time():.2f} >', end='')
    if not stop_event.is_set():  # 如果事件没有被设置，继续循环
        print('E', end='')
        # 再次启动定时器，实现循环
        Timer(2.0, timer_task).start()
    print(f'<')

# 启动循环定时器
print('按下回车键以停止定时器...')
timer_task()

# 主线程继续执行其他任务
# 主线程等待用户操作来停止定时器
try:
    input('')
finally:
    stop_event.set()  # 设置事件，通知定时器线程退出
    print('定时器已停止，主线程退出')