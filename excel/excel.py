import pandas as pd
import os

def read_excel(excel_file):
    print("学生信息：")
    df1 = pd.read_excel(excel_file, sheet_name="students")
    for index, row in df1.iterrows():
        print(f"第{index}行：{row['id']}, {row['name']}, {row['age']}")

    print("*" * 50)
    print("教师信息：")
    df2 = pd.read_excel(excel_file, sheet_name="teachers")
    for index, row in df2.iterrows():
        print(f"第{index}行：{row['姓名']}, {row['教学科目']}, {row['教学班级']}")


def write_excel(excel_file):
    data = {
        '姓名': ['张三','李四', '王五'],
        '年龄': [25, 30, 28],
        '城市': ['北京', '上海', '广州']
    }
    
    df = pd.DataFrame(data)
    # 写入到Excel文件
    df.to_excel(excel_file, index=False) # fixme：如果不是新文件，需要重点关注数据的覆盖问题，如果原先excel已有数据，会被全部覆盖

    
if __name__ == '__main__':
    # 获取当前文件的路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, "data.xlsx")

    # 从数据表中读取数据
    read_excel(data_file)

    # 往数据表中写入数据
    test_file = os.path.join(current_dir, "test.xlsx")
    write_excel(test_file)
