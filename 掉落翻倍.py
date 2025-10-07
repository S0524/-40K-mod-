import re

def amplify_bonus_loot_values(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式找到所有 BonusLootQuantity=, BonusLootRarity=, 和 BonusLootQuality= 后面的数值
    pattern = re.compile(r'(BonusLootQuantity=|BonusLootRarity=|BonusLootQuality=)(\d+)')
    
    # 替换匹配到的数值，使其放大10倍
    def replace_match(match):
        key = match.group(1)
        value = int(match.group(2))
        return f'{key}{value * 10}'
    
    new_content = pattern.sub(replace_match, content)
    
    # 将修改后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

# 让用户输入文件路径
file_path = input("请输入文件路径: ")

# 执行函数
amplify_bonus_loot_values(file_path)