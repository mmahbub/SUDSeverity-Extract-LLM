import pandas as pd
import pickle
import json

import sys
sys.path.append('../SUD-Extract-LLM/src/')

import configs
from metrics import *
#from utils_nofilter import *
from utils import *


substance_list = json.load(open(f"{configs.main_dir}data/substanceList.json"))
substance_group = list(substance_list.keys())

df = pd.read_csv(f"{configs.data_path}{configs.file_name}", sep="\\")

print("Performance scores for notes with answers . . . .")

df_res_dict = {}
pred_all_dict = {}
pred_count_dict = {}
for which_substance in substance_group:
    notes_substance = df[df['label'].str.contains(which_substance)].reset_index(drop=True)    
    notes_substance['gt_ans'].fillna("<no information found>", inplace=True)
    ground_truth = dict(zip(list(notes_substance.index.values), notes_substance['gt_ans']))
    
    predictions = json.load(open(f"{configs.prediction_dir}predictions_{which_substance}.json"))
    clean_preds, pred_count, note_length = postprocess_predictions(predictions, notes_substance['clean_text'].values.tolist(), which_substance)
    pred_all_dict[which_substance] = clean_preds
    pred_count_dict[which_substance] = pred_count
    
    df_res = calculate_metric(ground_truth, clean_preds, pred_count, note_length, configs.output_dir, which_substance)
    df_res_dict[which_substance] = df_res
    
    print(which_substance, f"Strict match (F1)          : {df_res[df_res['ground_truth']!='<no information found>']['strict_f1'].mean()}")
    print(which_substance, f"Relaxed match (F1)         : {df_res[df_res['ground_truth']!='<no information found>']['relaxed_f1'].mean()}")
    print(which_substance, f"Strict match (F1) -- no ans: {df_res[df_res['ground_truth']=='<no information found>']['strict_f1'].mean()}")
    print("="*20)