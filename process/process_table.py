import pandas as pd
import json
import ast
import re

def filter_table():
    # 读取CSV文件
    df = pd.read_csv('./MIRE_wjh/submit_result/submit_full_epo12_step168.csv')

    # 筛选包含“客服”的行
    filtered_df = df[df['instruction'].str.contains('Picture 1')]

    # 取前150条记录
    if len(filtered_df) > 150:
        filtered_df = filtered_df.head(150)

    # 将结果写入新的CSV文件
    filtered_df.to_csv('filtered_output_imgscene_150.csv', index=False)

def clean_and_convert_image(s):
    # 去除字符串两端的方括号和任何不必要的空格
    cleaned_s = re.sub(r'^\s*\[|\]\s*$', '', s).strip()
    # return cleaned_s
    try:
        # 尝试将清理后的字符串转换为列表
        prepare = ast.literal_eval(cleaned_s)
        if isinstance(prepare, tuple):
            return prepare
        else:
            return [prepare]
        # return ast.literal_eval(cleaned_s)
    except (ValueError, SyntaxError):
        # 如果转换失败，返回空列表或采取其他错误处理措施
        return []

def jsonfcsv():
    df = pd.read_csv('./filtered_output_100.csv')
    df.rename(columns={'predict': 'output'}, inplace=True)
    df['input'] = ''
    df['image'] = df['image'].apply(clean_and_convert_image)
    # df['image'] = df['image'].apply(lambda x: x.split(','))
    # df['image'] = df['image'].apply(lambda x: ','.join(x))
    
    # 将DataFrame转换为字典列表
    data_list = df.to_dict(orient='records')

    # 将列表导出为JSON文件
    with open('output_new_test.json', 'w', encoding='utf-8') as json_file:
        json.dump(data_list, json_file, ensure_ascii=False, indent=4)

    print("JSON文件已成功导出。")

def combinecsv():
    a_csv_file = './MIRE_wjh/submit_res/lora/submit_lora_epo5_1gpu_ga4_merge_intent_imgscene.csv'
    b_csv_file = './MIRE_wjh/submit_lora_epo5_1gpu_ga4_merge_imgscene_5k.csv'
    c_csv_file = './MIRE_wjh/submit_lora_epo5_1gpu_ga4_merge_intent_5k.csv'

    df_a = pd.read_csv(a_csv_file)
    df_b = pd.read_csv(b_csv_file)
    df_c = pd.read_csv(c_csv_file)

    for index, row in df_a.iterrows():
        if '识图专家' in row['instruction']:
            df_a.at[index, 'predict'] = df_b.loc[df_b['id'] == row['id'], 'predict'].values[0]
        elif '客服专家' in row['instruction']:
            df_a.at[index, 'predict'] = df_c.loc[df_c['id'] == row['id'], 'predict'].values[0]
        else:
            print('No match found for row:', row)
    combine_csv_path = './MIRE_wjh/submit_res/lora/submit_lora_epo5_1gpu_ga4_split_intent_imgscene.csv'
    df_a.to_csv(combine_csv_path, index=False)
    
if __name__ == '__main__':
    # jsonfcsv()
    combinecsv()