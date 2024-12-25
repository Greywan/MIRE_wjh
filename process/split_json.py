import json
import os
from tqdm import tqdm
import random
import pandas as pd

def splitjson():
    # 假设 JSON 文件名为 'data.json'
    json_file_path = './LLaMA-Factory_wjh/data/mire/test1.json'


    # 读取 JSON 文件
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    intent_data = data[:5000]
    img_data = data[5000:]

    # 打乱数据顺序
    # random.shuffle(intent_data)
    # random.shuffle(img_data)

    # 分割数据
    # intent_train_part = intent_data[:255]
    # img_train_part = img_data[:595]

    # train_part = intent_train_part + img_train_part

    # intent_val_part = intent_data[255:]
    # img_val_part = img_data[595:]
    # val_part = intent_val_part + img_val_part

    new_json_file_path = './LLaMA-Factory_wjh/data/mire/test1_intent.json'
    # 将修改后的数据写回 JSON 文件
    with open(new_json_file_path, 'w', encoding='utf-8') as file:
        json.dump(intent_data, file, ensure_ascii=False, indent=4)

    new_json_file_path = './LLaMA-Factory_wjh/data/mire/test1_imgscene.json'
    # 将修改后的数据写回 JSON 文件
    with open(new_json_file_path, 'w', encoding='utf-8') as file:
        json.dump(img_data, file, ensure_ascii=False, indent=4)

    print("JSON 文件已成功更新")

def split_instruction_json():
    json_file = './LLaMA-Factory_wjh/data/mire/test1.json'
    # 读取原始JSON文件
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 过滤数据，只保留instruction中包含“识图专家”的元素
    img_data = [item for item in data if '识图专家' in item['instruction']]
    intent_data  = [item for item in data if '客服专家' in item['instruction']]
    
    new_json_file_path = './LLaMA-Factory_wjh/data/mire/test1_intent.json'
    # 写入新的JSON文件
    with open(new_json_file_path, 'w', encoding='utf-8') as file:
        json.dump(intent_data, file, ensure_ascii=False, indent=4)

    img_json_file_path = './LLaMA-Factory_wjh/data/mire/test1_imgscene.json'
    # 写入新的JSON文件
    with open(img_json_file_path, 'w', encoding='utf-8') as file:
        json.dump(img_data, file, ensure_ascii=False, indent=4)

def filter_and_read():
    # json_file = './data/train/train.json'
    # 读取 JSON 文件
    # with open(json_file, 'r', encoding='utf-8') as file:
    #     data = json.load(file)

    # 筛选出 output 字段为 "单品推荐" 的元素
    # filtered_data = [item for item in data if item['output'] == '单品推荐']

    # 创建 DataFrame
    # df = pd.DataFrame(data)

    # csv read and filter
    csv_file_path = './MIRE_wjh/submit_res/lora/submit.csv'
    df = pd.read_csv(csv_file_path)

    # 筛选包含“Picture 1”的行
    filtered_df = df[df['instruction'].str.contains('识图专家')]
    outsplit(filtered_df)

def outsplit(data):
    unique_outputs = data['predict'].unique()
    print(f"len of outputs:{len(unique_outputs)}")
    for output in tqdm(unique_outputs):
        if "/" in output:
            file_name = f"intent_{output[:2]}.csv"
        else:
            file_name = f"intent_{output}.csv"
        filtered_df = data[data['predict'] == output]
        print(f"Output: {output}, Count: {len(filtered_df)}")

if __name__ == "__main__":
    filter_and_read()