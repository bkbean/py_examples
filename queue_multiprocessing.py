from multiprocessing import Event, Process, Queue
import queue
import time

# 定义一个简单的函数，用于向队列中添加元素
def producer(q, count):
    for i in range(count):
        print(f'生产者生产了 {i}')
        q.put(i)
        time.sleep(1)  # 模拟生产耗时

# 定义一个简单的函数，用于从队列中取出元素
def consumer(q, stop_event):
    while not stop_event.is_set():
        try:
            item = q.get(timeout=1)  # 设置超时以检测stop_event
            print(f'消费者消费了 {item}')
            time.sleep(0.5)  # 模拟消费耗时
        except queue.Empty:
            continue  # 超时后继续循环以检查stop_event

if __name__ == '__main__':
    # 创建一个Queue实例
    # 除了 task_done() 和 join() 之外，Queue  实现了标准库类 queue.Queue 中所有的方法。
    queue = Queue()
    # 创建停止事件
    stop_event = Event()
    # 创建生产者和消费者进程
    p = Process(target=producer, args=(queue, 10))
    c = Process(target=consumer, args=(queue, stop_event))
    
    # 启动进程
    p.start()
    c.start()

    # 等待生产者进程结束
    p.join()
    # 通知消费者进程停止
    stop_event.set()
    # 等待消费者进程结束
    c.join()

    print("所有任务执行完毕！")