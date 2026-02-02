import threading
import asyncio

async def async_task(name):
    print(f"异步任务 {name} 开始执行")
    await asyncio.sleep(2)
    print(f"异步任务 {name} 执行完毕")
    return f"异步任务执行结果来自 {name}"


def blocking_task(name, loop):
    """模拟一个阻塞任务"""
    print(f"任务 {name} 开始执行")

    async def run_async_tasks():
        results = await asyncio.gather(
            async_task("task-2"),
            async_task("task-3")
        )
        return results

    # 将协程提交到指定事件循环
    future = asyncio.run_coroutine_threadsafe(run_async_tasks(), loop)
    results = future.result()  # 等待结果
    print(results)


async def main():
    loop = asyncio.get_running_loop()  # 获取当前事件循环

    # 创建并启动线程
    thread = threading.Thread(target=blocking_task, args=("task-1", loop))
    thread.start()

    for i in range(1, 7):
        # 主线成做自己的事情
        print(f"主线程正在运行，迭代次数为 {i}")
        await asyncio.sleep(1)

    # 等待线程完成
    thread.join()
    print(f"所有任务完成")


if __name__ == '__main__':
    asyncio.run(main())
