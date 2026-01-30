## 一、事件循环的核心作用

1. 任务调度

    管理协程（Coroutine）、回调（Callback）和Future对象，决定哪个任务在何时执行。

2. I/O多路复用
   
   监听文件描述符、网络套接字等资源的状态变化，当I/O操作就绪时触发回调。

3. 协程状态管理

   通过await挂起协程，保存上下文，并在条件满足时恢复执行

## 事件循环的生命周期

1. 创建与启动
- 推荐使用asyncio.run(main())自动创建并运行事件循环（Python 3.7+）。
- 手动操作时：
     ```python
     loop = asyncio.new_event_loop()
     asyncio.set_event_loop(loop)
     loop.run_until_complete(main())
     loop.close()
     ```

2. 停止与关闭
- loop.stop()：停止事件循环。
- loop.close()：关闭循环并清理资源（需确保循环已停止）

## 三、关键API与使用场景

1. 任务调度

   - asyncio.create_task(coro)

       将协程封装为Task并加入就绪队列，立即调度执行。

   - loop.call_soon(callback)

       安排回调函数在下一轮循环迭代执行（非线程安全）。

   - 延迟执行

       ```python
       loop.call_later(delay, callback)  # 延迟delay秒后执行
       loop.call_at(when, callback)      # 在绝对时间when执行
       ```

2. Future与Promise
   - loop.create_future()
        
      创建与事件循环绑定的Future对象，用于跨协程传递结果。

   - await future

       暂停协程直到Future完成，避免阻塞事件循环。

3. 定时任务
   - 周期性任务示例
        ```python
        async def periodic_task():
            while True:
                print("Running...")
                await asyncio.sleep(1)
        asyncio.create_task(periodic_task())
        ```

## 四、底层机制解析
1. 协作式调度
    
    事件循环通过轮询（Polling）检查任务状态，而非抢占式调度。协程需主动await让出控制权。

2. I/O多路复用实现

    Linux使用epoll，Windows使用IOCP，底层通过selectors模块实现。

    注册感兴趣的I/O事件（如socket.recv），当事件就绪时触发回调。

3. 线程安全
   - loop.call_soon_threadsafe()用于跨线程调度回调。
   - 避免在协程中直接调用阻塞函数（如time.sleep()），改用await asyncio.sleep()。

### 五、高级特性
1. 子进程管理

    ```python

    proc = await asyncio.create_subprocess_exec(
        "ping", "8.8.8.8",
        stdout=asyncio.subprocess.PIPE
    )
    output = await proc.stdout.read()
    ```

2. 信号处理

    ```python
    loop.add_signal_handler(signal.SIGINT, lambda: loop.stop())
    ```

3. 自定义事件循环策略

    适用于多线程/多进程场景，如WindowsSelectorEventLoopPolicy。

## 六、常见误区与调试
1. 阻塞事件循环

    在协程中执行CPU密集型或同步I/O操作会导致整个循环卡顿，需使用loop.run_in_executor()委托给线程池。

2. 任务泄漏

    未正确取消未完成的任务可能导致内存泄漏，可通过asyncio.all_tasks()监控。

3. 版本兼容性

    注意get_event_loop()在Python 3.10+的行为变化，推荐使用get_running_loop()。

## 七、实战示例：Web服务器

```python
from aiohttp import web

async def handle(request):
    return web.Response(text="Hello, World!")

app = web.Application()
app.router.add_get('/', handle)

web.run_app(app)  # 内部自动管理事件循环
```
