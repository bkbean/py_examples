'''
queue 模块实现了多生产者、多消费者队列。
这特别适用于消息必须安全地在多线程间交换的线程编程。
模块中的 Queue 类实现了所有所需的锁定语义。
'''
from threading import Event, Thread, current_thread
import queue
import time

# 生产者线程
def producer(q, count):
    for i in range(count):
        print(f'{current_thread().name} 生产了 {i}')
        q.put(i)
        time.sleep(1)  # 模拟生产耗时

# 消费者线程
def consumer(q, stop_event):
    while not stop_event.is_set():
        try:
            item = q.get(timeout=1)  # 设置超时以检测stop_event
            print(f'{current_thread().name} 消费了 {item}')
            # 表示前面排队的任务已经被完成。被队列的消费者线程使用。
            # 每个 get() 被用于获取一个任务， 后续调用 task_done() 告诉队列，该任务的处理已经完成。
            q.task_done()
            time.sleep(0.5)  # 模拟消费耗时
        except queue.Empty:
            continue  # 超时后继续循环以检查stop_event
    
    # 处理剩余的项目
    while not q.empty():
        item = q.get()
        print(f'{current_thread().name} 消费了 {item}')
        q.task_done()

if __name__ == '__main__':
    # 创建队列
    # class queue.Queue(maxsize=0)          FIFO 队列构造函数
    # class queue.LifoQueue(maxsize=0)      LIFO 队列构造函数
    # class queue.PriorityQueue(maxsize=0)  优先级队构造函数
    # maxsize 是个整数，用于设置可以放入队列中的项目数的上限。
    # 当达到这个大小的时候，插入操作将阻塞至队列中的项目被消费掉。如果 maxsize 小于等于零，队列尺寸为无限大。
    q = queue.Queue()
    # 创建停止事件
    stop_event = Event()
    # 创建生产者线程
    producer_thread = Thread(name='Thread-P1', target=producer, args=(q, 10))
    # 创建消费者线程
    consumer_thread1 = Thread(name='Thread-C1', target=consumer, args=(q, stop_event))
    consumer_thread2 = Thread(name='Thread-C2', target=consumer, args=(q, stop_event))

    # 启动线程
    producer_thread.start()
    consumer_thread1.start()
    consumer_thread2.start()

    # 等待生产者线程结束
    producer_thread.join()
    # 通知消费者线程停止
    stop_event.set()
    # 等待队列被处理完(阻塞至队列中所有的元素都被接收和处理完毕)
    q.join()
    # 等待消费者线程结束
    consumer_thread1.join()
    consumer_thread2.join()

    print("所有任务执行完毕！")