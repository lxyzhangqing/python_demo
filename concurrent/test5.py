"""
多线程同步函数中调用异步函数
"""

import threading
import asyncio

async def async_task(name):
    print(f"异步任务 {name} 开始执行")
    await asyncio.sleep(2)
    print(f"异步任务 {name} 执行完毕")
    return f"异步任务执行结果来自 {name}"


def blocking_task(name):
    """模拟一个阻塞任务"""
    print(f"任务 {name} 开始执行")

    # 正常执行
    result = asyncio.run(async_task("task-2"))
    print(result)

    # fixme: 下述代码执行报错 There is no current event loop in thread
    # results = asyncio.gather(async_task("task-3"), async_task("task-4"))
    # print(results)

    print(f"任务 {name} 执行完毕")


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
