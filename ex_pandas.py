import os,sys
import pandas as pd


def exit_app(message: str, e: Exception = None) -> None:
    print(message)
    if e:
        print(f'{type(e).__name__}: {e}')
    input("按任意键退出...")
    sys.exit(1)
    return

if __name__ == '__main__':

    # 获取执行文件路径
    cur_dirname = os.path.dirname(__file__)

    # 输入文件
    input_path = os.path.join(cur_dirname , '行政机构人员信息.xlsx')
    # 输出文件
    output_path = os.path.join(cur_dirname , '结果表格.docx')

    # 读取Excel文件，将第一列作为索引列，第一行作为标签行
    df = pd.read_excel(input_path, header=1,  index_col=None)

    print(df.head(10))