
import json
from tqdm import tqdm
import os
import copy
import sys
sys.path.append(os.path.abspath('./'))
from ocr_read import OcrImageToText
import pandas as pd
import re

def add_ocrjson():
    # 假设 JSON 文件名为 'data.json'
    json_file_path = './data/mire/train_test.json'
    # 要添加的前缀路径
    prefix_path = './data/mire/train/images'

    ocr = OcrImageToText()
    ocr.init_model()
    # 读取 JSON 文件
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 修改每个元素的 'image' 字段
    for item in tqdm(data):
        
        image_nums = len(item['image'])
        instruction = item['instruction']
        output = item['output']
        images = [os.path.join(prefix_path, img_path) for img_path in item['image']]
        desc = ""
        if image_nums >= 1:
            blocks = instruction.split("<image>")
            new_instruction = "".join(blocks[:-1]) + "<image>" + blocks[-1]
            new_instruction = copy.deepcopy(instruction)
            for img in images:
                desc += ocr.ocr_image_to_string(img)
            images = images[-1:]

        image_desc = ''
        if len(images) > 0:
            image_desc = f"<image> 图片文本描述： {desc}"
            instruction = instruction.replace("<image>", image_desc)
            item['instruction'] = instruction

    new_json_file_path = './data/mire/train_addocr.json'
    # 将修改后的数据写回 JSON 文件
    with open(new_json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print("JSON 文件中的 'image' 字段已成功更新。")

def add_ocrjson_update():
    # 假设 JSON 文件名为 'data.json'
    json_file_path = './data/mire/train/train.json'
    # 要添加的前缀路径
    prefix_path = './data/mire/train/images'

    ocr = OcrImageToText()
    ocr.init_model()
    # 读取 JSON 文件
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 处理数据并构建两个数据结构
    processed_data_without_ocr = []
    processed_data_with_ocr = []

    # 修改每个元素的 'image' 字段
    for item in tqdm(data):
        item_copy_without_ocr = item.copy()  # 创建不包含OCR数据的副本
        item_copy_with_ocr = item.copy()

        image_nums = len(item['image'])
        instruction = item['instruction']
        output = item['output']
        images = [os.path.join(prefix_path, img_path) for img_path in item['image']]
        desc = ""
        ocrs = []
        if image_nums >= 1:
            pattern = r'<image>'
            matches = re.finditer(pattern, instruction)
            new_text = []
            last_end = 0

            for id, match in enumerate(matches):
                start, end = match.span()
                new_text.append(instruction[last_end:start])
                desc = ocr.ocr_image_to_string(images[id])
                new_text.append(f'<image> 图片文本描述： {desc}')
                ocrs.append(desc)
                last_end = end

            new_text.append(instruction[last_end:])
            new_instruction = "".join(new_text)
            item_copy_without_ocr['instruction'] = new_instruction
            item_copy_with_ocr['instruction'] = new_instruction
            item_copy_with_ocr['ocr'] = ocrs
        processed_data_without_ocr.append(item_copy_without_ocr)
        processed_data_with_ocr.append(item_copy_with_ocr)

    # 保存一个 csv 文件
    # 将处理后的数据转换为DataFrame并写入CSV
    new_csv_file_path = './data/mire/train_addocr.csv'
    df = pd.DataFrame(processed_data_with_ocr)
    df.to_csv(new_csv_file_path, index=False, encoding='utf-8')
    
    # for item in tqdm(data):
    #     del item['ocr']
    new_json_file_path = './data/mire/train_addocr.json'
    # 将修改后的数据写回 JSON 文件
    with open(new_json_file_path, 'w', encoding='utf-8') as file:
        json.dump(processed_data_without_ocr, file, ensure_ascii=False, indent=4)
    print("JSON 文件中的字段已成功更新。")

# def add_ocrcsv():
#     # 假设 JSON 文件名为 'data.json'
#     file_path = './data/mire/train/train_imgscene.csv'
#     # 要添加的前缀路径
#     prefix_path = './data/mire/train/images'
#     df = pd.read_csv(file_path)
    

#     # 修改每个元素的 'image' 字段
#     for index, row in df.iterrows():
        
#         image_nums = len(item['image'])
#         instruction = item['instruction']
#         output = item['output']
#         images = [os.path.join(prefix_path, img_path) for img_path in item['image']]
#         desc = ""
#         if image_nums >= 1:
#             blocks = instruction.split("<image>")
#             new_instruction = "".join(blocks[:-1]) + "<image>" + blocks[-1]
#             new_instruction = copy.deepcopy(instruction)
#             for img in images[-3:]:
#                 desc += ocr_image_to_string(img)
#             images = images[-1:]

#         image_desc = ''
#         if len(images) > 0:
#             image_desc = f"<image> 图片文本描述： {desc}"
#             instruction = instruction.replace("<image>", image_desc)
#             item['instruction'] = instruction

#     new_json_file_path = './data/mire/train_addocr.json'
#     # 将修改后的数据写回 JSON 文件
#     with open(new_json_file_path, 'w', encoding='utf-8') as file:
#         json.dump(data, file, ensure_ascii=False, indent=4)

#     print("JSON 文件中的 'image' 字段已成功更新。")

if __name__ == '__main__':
    add_ocrjson_update()