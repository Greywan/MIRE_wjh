import pandas as pd
import json
import ast
import re
import os
import shutil

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
    
def moveimg_fromcsv():
    destination_directory = './choose_images'
    os.makedirs(destination_directory, exist_ok=True)
    old_img_dir = './data/test1/images'
    df = pd.read_csv('./data/epo12_step168_imgscene_150.csv')
    # df.rename(columns={'predict': 'output'}, inplace=True)
    # df['input'] = ''
    df['image'] = df['image'].apply(clean_and_convert_image)

    for index, row in df.iterrows():
        image_paths = row['image']
        for img_path in image_paths:
            ori_img_path = os.path.join(old_img_dir, img_path)
            index_name = index+2
            new_img_path = os.path.join(destination_directory, f'{index_name}_{img_path}')
            shutil.copyfile(ori_img_path, new_img_path)
    

if __name__ == "__main__":
    moveimg_fromcsv()