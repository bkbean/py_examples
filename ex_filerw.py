import os,sys,json


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

filename = r'text_files/pi-billion.txt'
rfilename = 'result.json'

if os.path.exists(rfilename):
    with open(rfilename) as f:
        result = json.load(f)
    print(result)
    sys.exit()

try:
    with open(filename) as f:
        lines = f.readlines()
except FileNotFoundError:
    print(f'Error: The file {filename} does not exist.')
    sys.exit(-1)

pi_str = ''
for line in lines:
    pi_str += line.strip()

print(f'{pi_str[:52]}')
print(f'len: {len(pi_str)}')

total_digits, result = count_digits(100)
percentage_count = {digit: f'{(count/total_digits)*100:.2f}%' for digit, count in result.items()}

# 输出百分比并保留两位小数
print(f'数字 数量 百分比')
for k, v in result.items():
    print(f'{k:>2}: {v:>8} {percentage_count[k]:>8}')

with open(rfilename, 'w') as f:
    json.dump(result, f, indent=4)