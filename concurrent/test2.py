"""
阻塞任务放到线程池中执行，避免多协程并发执行时任务阻塞
"""

import asyncio
import time

async def async_blocking_task(name, time_interval):
    """异步版本的阻塞任务"""
    print(f"任务 {name} 开始执行")

    # 采用run_in_executor 在线程池中运行阻塞函数，避免阻塞事件循环
    def time_sleep(task_time_interval):
        time.sleep(task_time_interval)

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, time_sleep, time_interval)

    print(f"任务 {name} 执行完毕")
    return f"结果来自 {name}"


async def main():
    try:
        # 并发执行多个任务，当所有任务执行完才返回
        # 任务函数必须定义为异步函数
        results = await asyncio.gather(
            async_blocking_task("task-1", 2),
            async_blocking_task("task-2", 5)
        )
        print(f"并发执行结果：{results}")
    except Exception as e:
        print(f"执行过程中发生错误: {e}")
        raise

if __name__ == '__main__':
    asyncio.run(main())
