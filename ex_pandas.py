import os
import pandas as pd


if __name__ == '__main__':

    # 获取当前工作目录
    cwd = os.getcwd()
    # 获取脚本所在路径
    script_path = os.path.abspath(__file__)
    # 获取脚本所在目录
    script_dir = os.path.dirname(script_path)
    # 输入文件名
    input_filename = '全市编制数.xlsx'
    # 输出文件名
    output_filename = '结果表格.xlsx'

    print(f'当前工作目录: {cwd}')
    print(f'当前工作目录: {script_path}')
    print(f'当前工作目录: {script_dir}')

    # 输入文件
    input_path = os.path.join(cwd, 'ex_data', input_filename)
    # 输出文件
    output_path = os.path.join(cwd, output_filename)

    # 读取Excel文件，将第A-B列作为多重索引，第2-4行作为多重列名
    df = pd.read_excel(input_path, header=[1, 2, 3], index_col=[0, 1])
    df.drop('备注', axis=1, level=0, inplace=True)

    print(df.head(10))