import ijson
import io
import time


def multi_array_stream_parser(chunks):
    """
    同时解析 tasks 和 users 数组，任意项就绪即打印
    """

    # 模拟文件流包装器
    class StreamBuffer(io.RawIOBase):
        def __init__(self, gen):
            self.gen = gen
            self.leftover = b""

        def readinto(self, b):
            try:
                if not self.leftover:
                    self.leftover = next(self.gen).encode('utf-8')
                n = min(len(b), len(self.leftover))
                b[:n], self.leftover = self.leftover[:n], self.leftover[n:]
                return n
            except StopIteration:
                return 0

    try:
        buffer = StreamBuffer(chunks)
        parser = ijson.parse(buffer)
        builder = None

        for prefix, event, value in parser:
            if prefix == 'name' and event == 'string':
                print(f"✅ 名称 [就绪]: {value}")

            if prefix.startswith("tasks.item") or prefix.startswith("users.item"):
                if event == "start_map" and prefix in ["tasks.item", "users.item"]:
                    builder = ijson.ObjectBuilder(map_type=dict)

            if builder:
                builder.event(event, value)

                if event == "end_map" and prefix in ["tasks.item", "users.item"]:
                    full_obj = builder.value
                    
                    obj_type = "task" if prefix.startswith("tasks.item") else "user"
                    
                    if obj_type == "task":
                        print(f"✅ [就绪] 类别: {obj_type} | 数据: {full_obj}")
                    elif obj_type == "user":
                        print(f"✅ [就绪] 类别: {obj_type} | 数据: {full_obj}")

                    builder = None  # 重置构造器
    except ijson.common.IncompleteJSONError:
        pass


# --- 模拟 LLM 流式输出 ---
def mock_mixed_llm_stream():
    # 模拟一个交替或随机输出 tasks 和 users 的 JSON
    json_str = """
    {
      "name": "test",
      "tasks": [
        {"id": "t1", "title": "Task One"},
        {"id": "t2", "title": "Task Two"}
      ],
      "users": [
        {"id": "u1", "name": "Alice"},
        {"id": "u2", "name": "Bob"}
      ]
    }
    """
    # 逐字发送，模拟真实的流式延迟
    for char in json_str:
        yield char
        time.sleep(0.02)  # 模拟输出速度


if __name__ == "__main__":
    print("开始监听多数组流...")
    multi_array_stream_parser(mock_mixed_llm_stream())
