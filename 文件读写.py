import json
import sys
from pathlib import Path

def count_digits(pi_str: str) -> tuple[int, dict[str, int]]:
    # 初始化一个字典，用于记录每个数字的出现次数
    digit_count = {str(i): 0 for i in range(10)}
    total_digits = 0

    # 遍历字符串中的每个字符
    for char in pi_str:
        # 检查字符是否为数字
        if char.isdigit():
            # 将字符作为键，增加对应的值
            digit_count[char] += 1
            total_digits += 1

    return total_digits, digit_count

def print_results(result: dict):
    """打印统计结果"""
    print(f'数字 数量 百分比')
    for digit, (count, percentage) in result.items():
        print(f'{digit:>2}: {count:>8} {percentage:>8}')

def process_pi_file(input_file: Path, output_file: Path) -> dict:
    """处理PI文件并返回统计结果"""
    try:
        with input_file.open() as f:
            pi_str = ''.join(line.strip() for line in f.readlines())
    except FileNotFoundError:
        print(f'Error: The file {input_file} does not exist.')
        sys.exit(-1)

    print(f'{pi_str[:52]}...')
    print(f'len: {len(pi_str)}')
    total_digits, counts = count_digits(pi_str)
    percentages = {d: f'{(c/total_digits)*100:.2f}%' for d, c in counts.items()}
    
    return {digit: (count, percentages[digit]) for digit, count in counts.items()}


def main():
    input_file = Path('data/pi_million.txt')
    output_file = Path('output/result.json')
    
    # 确保输出目录存在
    output_file.parent.mkdir(parents=True, exist_ok=True)
    # 如果结果文件已存在，直接读取并打印
    if output_file.is_file():
        with output_file.open() as f:
            result = json.load(f)
        print_results(result)
        return

    # 处理PI文件并保存结果
    result = process_pi_file(input_file, output_file)
    print_results(result)
    
    with output_file.open('w') as f:
        json.dump(result, f, indent=4)

if __name__ == '__main__':
    main()