import json
import os
from tqdm import tqdm

def change_json():
    # 假设 JSON 文件名为 'data.json'
    json_file_path = './MIRE_wjh/data/test1/test1.json'
    # 要添加的前缀路径
    prefix_path = './data/mire/test1/images'

    # 读取 JSON 文件
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 修改每个元素的 'image' 字段
    for item in tqdm(data):
        if 'image' in item and isinstance(item['image'], list):
            image_nums = len(item['image'])
            if image_nums >=5:
                print(f"{item['id']} has {image_nums} images")
                item['image'] = item['image'][:5]
            for i, image_path in enumerate(item['image']):
                # 确保路径是字符串类型，然后添加前缀
                if isinstance(image_path, str):
                    item['image'][i] = os.path.join(prefix_path, image_path)

    new_json_file_path = './LLaMA-Factory_wjh/data/mire/test1.json'
    # 将修改后的数据写回 JSON 文件
    with open(new_json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print("JSON 文件中的 'image' 字段已成功更新。")

def change_img_path():
    # 假设 JSON 文件名为 'data.json'
    json_file_path = './train_intent.json'
    # 要添加的前缀路径
    prefix_path = './data/mire/images'

    # 读取 JSON 文件
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 修改每个元素的 'image' 字段
    for item in tqdm(data):
        # if 'image' in item:
        if 'image' in item and isinstance(item['image'], list):
            # image_nums = len(item['image'])
            # if image_nums >=5:
            #     print(f"{item['id']} has {image_nums} images")
            #     item['image'] = item['image'][:5]
            # res = []
            for i, image_path in enumerate(item['image']):
                # 确保路径是字符串类型，然后添加前缀
                if isinstance(image_path, str):
                    # image_path = image_path.replace("'","")
                    item['image'][i] = os.path.join(prefix_path, image_path)

    new_json_file_path = './LLaMA-Factory_wjh/data/mire/train_intent.json'
    # 将修改后的数据写回 JSON 文件
    with open(new_json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def merge_json():
    json_path = './LLaMA-Factory_wjh/data/mire/train.json'
    other_json_path = './LLaMA-Factory_wjh/data/mire/test_labeled_100_intent_new.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(other_json_path, 'r', encoding='utf-8') as f:
        other_data = json.load(f)
    data.extend(other_data)
    print(len(data))
    merged_json_path = './LLaMA-Factory_wjh/data/mire/train_add_test100intent.json'
    with open(merged_json_path,'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print('Merge completed successfully.')

if __name__ == "__main__":
    change_img_path()