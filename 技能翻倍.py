import re

def amplify_bonus_loot_values(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式匹配 value= 后面的数值
    pattern = re.compile(r'(value=)(-?\d+(\.\d+)?)')
    
    # 替换匹配到的数值，使其放大并四舍五入到小数点后两位，同时去除无效的小数点和多余的0
    def replace_match(match):
        key = match.group(1)
        value = float(match.group(2))
        amplified_value = round(value * 10, 2)
        
        # 判断是否需要保留小数部分
        if amplified_value.is_integer():
            formatted_value = int(amplified_value)
        else:
            formatted_value = amplified_value
        
        return f'{key}{formatted_value}'
    
    new_content = pattern.sub(replace_match, content)
    
    # 将修改后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

# 让用户输入文件路径
file_path = input("请输入文件路径: ")

# 执行函数
amplify_bonus_loot_values(file_path)