import sys
sys.path.append('../SUD-Extract-LLM/src/')

import re
import json
import pandas as pd
from metrics import *
import configs

output_dir = configs.rule_output_dir
substance_list = json.load(open(f"{configs.main_dir}data/substanceList.json"))

def get_rule_based_predictions(note, which_substance):
    '''
    Funtion for rule-based predictions
    '''
    regex_pattern = json.load(open(f"{configs.main_dir}src/regex_patterns.json"))
    pattern_list = regex_pattern[which_substance]
    matches = [re.findall(pattern, note.lower()) for pattern in pattern_list]
#     print(matches)

    matches_clean = []
    for m in matches:
        if len(m)==0:
            pass
        else:
            for match in m:
                matches_clean.append("".join(match))
                
    matches_final = []
    matches_clean = sorted(matches_clean, key=lambda x:len(x), reverse=True)
    for m in matches_clean:
        matches_final.append(matches_clean[[m in ans for ans in matches_clean].index(True)])
    matches_final = list(set(matches_final))
    
    if len(matches_final)==0: matches_final=["<no information found>"]
        
    return matches_final


df = pd.read_csv(f"{configs.data_path}{configs.file_name}", sep='\\')

print("Performance scores for notes with answers . . . .")

df_sub_res_list = []
for which_substance in substance_list.keys():
    df_sub = df[df['label']==which_substance].reset_index(drop=True)
    df_sub['gt_ans'].fillna("<no information found>", inplace=True)
    df_sub = df_sub[['NOTE_ID', 'clean_text', 'gt_ans']]
    print(which_substance, df_sub.shape)

    df_sub['rule_based_prediction'] = df_sub['clean_text'].apply(lambda x:get_rule_based_predictions(x, which_substance))

    rs = calculate_metric(
        dict(zip(df_sub['NOTE_ID'], df_sub['gt_ans'])),
        dict(zip(df_sub['NOTE_ID'], df_sub['rule_based_prediction'])),
        dict(zip(df_sub['NOTE_ID'].apply(str), [1]*len(df_sub))),
        output_dir, which_substance)

    df_sub_res_list.append(rs)    
    
    print(which_substance, f"Strict match (F1) : {rs[rs['ground_truth']!='<no information found>']['strict_f1'].mean()}")
    print(which_substance, f"Relaxed match (F1): {rs[rs['ground_truth']!='<no information found>']['relaxed_f1'].mean()}")
    print("="*20)
        
