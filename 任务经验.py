import json
import os

def modify_character_xp(data):
    if isinstance(data, list):
        for item in data:
            modify_character_xp(item)
    elif isinstance(data, dict):
        for key, value in data.items():
            if key == 'characterXp':
                original_xp = value
                data[key] = value * 10
                print(f"characterXp 从 {original_xp} 修改为 {data[key]}")
            else:
                modify_character_xp(value)

# 提示用户输入文件夹路径
folder_path = input("请输入 JSON 文件夹的路径: ")

# 检查文件夹是否存在
if not os.path.exists(folder_path):
    print("文件夹未找到，请检查路径是否正确。")
    exit(1)

# 遍历文件夹内的所有文件
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        
        # 读取 JSON 文件
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"文件 {file_path} 未找到，请检查路径是否正确。")
            continue
        except json.JSONDecodeError:
            print(f"文件 {file_path} 内容不是有效的 JSON 格式。")
            continue

        # 修改 characterXp
        modify_character_xp(data)

        # 保存修改后的 JSON 文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f"{filename} 中的 characterXp 已成功增加10倍")

print("所有文件已处理完毕")