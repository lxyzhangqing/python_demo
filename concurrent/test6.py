import threading
import asyncio

async def async_task(name):
    print(f"异步任务 {name} 开始执行")
    await asyncio.sleep(2)
    print(f"异步任务 {name} 执行完毕")
    return f"异步任务执行结果来自 {name}"

def blocking_task_error(name):
    """模拟一个阻塞任务"""
    print(f"任务 {name} 开始执行")

    # fixme: 下述代码执行报错 There is no current event loop in thread
    results = asyncio.gather(async_task("task-2"), async_task("task-3"))
    print(results)

    print(f"任务 {name} 执行完毕")


# 解决方式-1
def blocking_task_v1(name):
    """模拟一个阻塞任务"""
    print(f"任务 {name} 开始执行")

    # 在新线程中运行异步任务
    async def run_async_tasks():
        results = await asyncio.gather(
            async_task("task-2"),
            async_task("task-3")
        )
        return results

    # 在当前线程中创建并运行新的事件循环
    results = asyncio.run(run_async_tasks())
    print(results)

    print(f"任务 {name} 执行完毕")


# 解决方式-2
def blocking_task_v2(name):
    """模拟一个阻塞任务"""
    print(f"任务 {name} 开始执行")

    # 创建新的事件循环
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)

    try:
        async def run_async_tasks():
            results = await asyncio.gather(
                async_task("task-2"),
                async_task("task-3")
            )
            return results

        results = new_loop.run_until_complete(run_async_tasks())
        print(results)

        print(f"任务 {name} 执行完毕")
    finally:
        new_loop.close()


def blocking_task(name):
    # blocking_task_error(name)
    blocking_task_v1(name)
    blocking_task_v2(name)


async def main():
    # 创建并启动线程
    thread = threading.Thread(target=blocking_task, args=("task-1",))
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
