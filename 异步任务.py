import asyncio

# 定义一个异步任务
async def task(n):
    print(f"任务 {n} 开始")
    # 异步等待1秒钟，模拟一个I/O操作
    await asyncio.sleep(1)
    print(f"任务 {n} 完成")

# 定义一个异步主函数
async def main():
    # 创建多个任务，将任务放入任务列表
    tasks = [task(i) for i in range(5)]
    # 使用 asyncio.gather 调度所有任务，并等待它们全部完成
    await asyncio.gather(*tasks)

# 启动 asyncio 事件循环并运行主函数
asyncio.run(main())