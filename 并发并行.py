'''
异步执行可以由 ThreadPoolExecutor 使用线程或由 ProcessPoolExecutor 使用单独的进程来实现。 两者都是抽象类 Executor 定义接口的实现。

特性/方法       submit                                    map
任务执行方式    异步执行，返回 Future 对象                  阻塞执行，等待所有任务完成
结果顺序        不保证顺序（可以通过 as_completed 获取）	保证按照输入顺序返回结果
灵活性          高，可动态提交任务、控制超时、取消等         较低，主要用于批量提交任务
错误处理        可以通过 Future 捕获异常                   如果有异常，map 会抛出异常
适用场景        任务类型不一样，或者需要动态控制任务         批量处理相同任务，且对顺序有要求
'''

from concurrent.futures import Executor,ProcessPoolExecutor,ThreadPoolExecutor,as_completed
import time

def task(i:int) -> int:
    time.sleep(1)
    return i**2

def proc_map_task(number:int=100, max_workers:int=4):
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(task, range(1, number))
        for i, result in enumerate(results, start=1):
            #print(f'{i}:{result}', end='; ')
            pass

def proc_submit_task(number:int=100, max_workers:int=4):
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(task, i): i for i in range(1,number)}
        for future in as_completed(futures):
            #print(f'{futures[future]}:{future.result()}',end='; ')
            pass

def thre_map_task(number:int=100, max_workers:int=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(task, range(1, number))
        for i, result in enumerate(results, start=1):
            #print(f'{i}:{result}', end='; ')
            pass

def thre_submit_task(number:int=100, max_workers:int=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(task, i): i for i in range(1,number)}
        for future in as_completed(futures):
            #print(f'{futures[future]}:{future.result()}',end='; ')
            pass

if __name__ == '__main__':
    num=20
    start = time.perf_counter()
    proc_map_task(num)
    end = time.perf_counter()
    print(f"运行时间: {end - start:.6f} 秒\n")

    start = time.perf_counter()
    proc_submit_task(num)
    end = time.perf_counter()
    print(f"运行时间: {end - start:.6f} 秒\n")
    
    start = time.perf_counter()
    thre_map_task(num)
    end = time.perf_counter()
    print(f"运行时间: {end - start:.6f} 秒\n")
    
    start = time.perf_counter()
    thre_submit_task(num)
    end = time.perf_counter()
    print(f"运行时间: {end - start:.6f} 秒\n")
    