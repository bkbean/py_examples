import queue
import time
from itertools import count


def get_worker_name():
    try:
        from multiprocessing import current_process
        if current_process().name != 'MainProcess':
            return current_process().name
        raise ImportError('Fallback to threading')
    except ImportError:
        from threading import current_thread
        return current_thread().name


def generic_producer(q, count, identity, start_id=0):
    whoami = get_worker_name()
    for i in range(start_id, start_id + count):
        try:
            print(f'{whoami} 生产了 {i}')
            q.put((identity, i), timeout=1)
        except queue.Full:
            print(f'{whoami} 队列已满, 等待中...')
            q.put((identity, i))  # 最终仍选择阻塞
        print(f'{whoami} 成功投放了 {i}')
        time.sleep(1)   # 模拟生产耗时

def generic_consumer(q, stop_event, identity):
    whoami = get_worker_name()
    while not stop_event.is_set():
        try:
            item = q.get(timeout=0.5)   # 缩短超时时间提高响应速度
            print(f'{whoami} 消费了 {item}')
            time.sleep(1)   # 模拟消费耗时
            q.task_done()   # 关键：标记任务完成
        except queue.Empty:
            continue

def run_task(use_multiprocessing=False, 
             producer_count=2, 
             consumer_count=3, 
             items_per_producer=10,
):
    maxsize = 64    # 限制队列大小防止内存爆炸
    if use_multiprocessing:
        print('>>> 运行进程模式')
        from multiprocessing import Event, JoinableQueue, Process as Worker
        q = JoinableQueue(maxsize=maxsize)
    else:
        print('>>> 运行线程模式')
        from queue import Queue
        from threading import Event, Thread as Worker
        q = Queue(maxsize=10)

    stop_event = Event()

    # 创建并启动生产者
    producers = []
    id_counter = count()  # 全局ID计数器
    for i in range(producer_count):
        start_id = next(id_counter) * items_per_producer
        p = Worker(name=f'Producer-{i}', target=generic_producer, args=(q, items_per_producer, f'P{i}', start_id))
        p.start()
        producers.append(p)

    # 创建并启动消费者
    consumers = []
    for i in range(consumer_count):
        c = Worker(name=f'Consumer-{i}', target=generic_consumer, args=(q, stop_event, f'C{i}'))
        c.start()
        consumers.append(c)

    # 等待所有生产者完成
    for p in producers:
        p.join()

    # 等待所有任务都被处理完
    q.join()  # 关键：等待所有 q.task_done()

    # 通知消费者停止
    stop_event.set()

    # 等待所有消费者完成
    for c in consumers:
        c.join()

    print('所有任务执行完毕！')

if __name__ == '__main__':
    # 测试线程模式
    run_task(use_multiprocessing=False, 
             producer_count=2,
             consumer_count=3,
             items_per_producer=10)
    
    # 测试进程模式
    run_task(use_multiprocessing=True, 
             producer_count=3,
             consumer_count=4,
             items_per_producer=10)