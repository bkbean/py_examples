from multiprocessing import Process


def task(n):
    print(f"任务 {n} 完成")

if __name__ == "__main__":
    processes = []
    for i in range(5):
        p = Process(target=task, args=(i,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()