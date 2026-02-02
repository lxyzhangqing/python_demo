import asyncio
import time

async def async_blocking_task(name, time_interval):
    """异步版本的阻塞任务"""
    print(f"任务 {name} 开始执行")

    # fixme: 阻塞睡眠会导致该任务的睡眠期间，其他任务也无法执行，直到该任务完成，失去并发的意义
    # time.sleep(time_interval)

    await asyncio.sleep(time_interval)  # 使用异步睡眠替代阻塞睡眠

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
