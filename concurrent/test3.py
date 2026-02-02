"""
创建多线程执行阻塞任务，避免并发执行多个任务时，任务阻塞
"""

import threading
import asyncio
import time

def blocking_task(name):
    """模拟一个阻塞任务"""
    print(f"任务 {name} 开始执行")
    time.sleep(5)  # 模拟耗时操作
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
    print("所有任务完成")


if __name__ == '__main__':
    asyncio.run(main())
