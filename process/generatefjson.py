import json
import pandas as pd
import os
from tqdm import tqdm
def filter_and_export():
    json_file = './data/train/train.json'
    # 读取 JSON 文件
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 筛选出 output 字段为 "单品推荐" 的元素
    # filtered_data = [item for item in data if item['output'] == '单品推荐']

    # 创建 DataFrame
    df = pd.DataFrame(data)

    # 筛选包含“Picture 1”的行
    filtered_df = df[df['instruction'].str.contains('客服专家')]

    # 将 DataFrame 写入 CSV 文件
    filtered_df.to_csv('train_intent.csv', index=False, encoding='utf-8-sig')

    print("CSV 文件已生成: recommended_items.csv")


def readsplitcsv():
    file_path = './data/train_split/train_intent.csv'
    df = pd.read_csv(file_path)
    unique_outputs = df['output'].unique()

    print(f"len of outputs:{len(unique_outputs)}")
    for output in tqdm(unique_outputs):
        if "/" in output:
            file_name = f"intent_{output[:2]}.csv"
        else:
            file_name = f"intent_{output}.csv"
        filtered_df = df[df['output'] == output]
        print(f"Output: {output}, Count: {len(filtered_df)}")
        save_path = os.path.join('./data/train_split/intent', file_name)
        filtered_df.to_csv(save_path, index=False, encoding='utf-8-sig')
    
if __name__ == '__main__':
    readsplitcsv()