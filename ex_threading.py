import threading,queue,time


# 定义任务函数，用于从队列中取出数据并打印
def process_data(q):
    while True:
        try:
            # 从队列中取数据
            item = q.get(timeout=3)  # 设置超时为 3 秒
            print(f"线程 {threading.current_thread().name} 处理数据: {item}")
            time.sleep(1)  # 模拟处理时间
        except queue.Empty:
            print(f"线程 {threading.current_thread().name} 没有数据可处理，退出")
            break

# 创建一个队列
q = queue.Queue()

# 将数据放入队列
for i in range(10):
    q.put(i)

# 创建两个线程
thread1 = threading.Thread(target=process_data, args=(q,), name="线程1")
thread2 = threading.Thread(target=process_data, args=(q,), name="线程2")

# 启动线程
thread1.start()
thread2.start()

# 等待线程结束
thread1.join()
thread2.join()

print("所有线程执行完毕！")
