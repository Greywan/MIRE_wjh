import json
from pathlib import Path
import pandas as pd
import os

def convert2submit(test_file: Path, prediction_file: Path, save_path: Path):
    pred_label_list = []

    for line in open(prediction_file, "r"):
        prediction_data = json.loads(line)

        pred_label = prediction_data["predict"]
        pred_label_list.append(pred_label)

    test_data = json.load(open(test_file, "r"))
    save_data = []
    for i, example in enumerate(test_data):
        example["predict"] = pred_label_list[i]
        save_data.append(example)

    df = pd.DataFrame(save_data)

    df.to_csv(save_path, index=None, encoding="utf-8-sig")


if __name__ == "__main__":
    test_file = "data/test1.json"
    root_path = '/data/users/wanjunhui/Task/Research_core/LLM/LLaMA-Factory_wjh/saves/qwen2_vl-7b_infer_result/full'
    prediction_file = os.path.join(root_path, 'epo72_step_400_result/generated_predictions.jsonl')
    save_path = "submit_full_epo72_step400.csv"
    convert2submit(test_file, prediction_file, save_path)

# end main
