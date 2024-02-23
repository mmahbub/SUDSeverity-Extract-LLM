import torch
from torch.utils.data import DataLoader

import sys
import pandas as pd
import numpy as np
from collections import defaultdict
import json
from tqdm import tqdm
tqdm.pandas()
# pd.set_option('max_colwidth', 1000)

import transformers
from transformers import T5Tokenizer, T5ForConditionalGeneration, AutoTokenizer
import gc

# import custom library
sys.path.append('../SUD-Extract-LLM/src/')
import configs
from generate_prompt import *
from preprocess_notes import *


def predict(model, tokenizer, notes, prompt, batch_size, 
            max_new_tokens, max_length, doc_stride):
    '''
    Function to extract information using zero-shot prompting
    '''
    # tokenize prompt+note
    input_ids = tokenizer([prompt] * len(notes['clean_text']), notes['clean_text'].tolist(),
                          return_tensors="pt", truncation="only_second", padding='max_length',
                          return_overflowing_tokens=True, stride=doc_stride,
                          return_offsets_mapping=True, max_length=max_length)  # max_length=512,
        
    chunk_to_note_map = input_ids.pop("overflow_to_sample_mapping")
    input_ids = input_ids.input_ids
    input_ids = input_ids.to('cuda')

    print('Size of input_ids', input_ids.shape)

    dataloader = DataLoader(input_ids, shuffle=False, batch_size=batch_size)
    chunk_dataloader = DataLoader(chunk_to_note_map, shuffle=False, batch_size=batch_size)

    assert len(dataloader) == len(chunk_dataloader)

    predictions = defaultdict(list)

    all_times = []
    total_n_examples = 0
        
    for data, note_idx in tqdm(zip(dataloader, chunk_dataloader), total=len(dataloader)):
        total_n_examples += len(note_idx)
        outputs = model.generate(data, max_new_tokens = max_new_tokens) 
        preds = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        
        for i, n in enumerate(note_idx.cpu()):
            predictions[n.item()].append(preds[i])
        
        data.detach()
        outputs.detach()
            
    return predictions


def run(which_substance, df):
    '''
    Function to run inference
    '''
    notes_substance = df[df['label'].str.contains(which_substance)].reset_index(drop=True)
    print(f"Running inference on {notes_substance.shape[0]} clinical notes . . . .")
    
    prompt_desc = which_substance
    prompt = get_prompt(prompt_desc)

    print(f"Zero-shot Prompt:\n{prompt}")
    
    predictions = predict(model, tokenizer, notes_substance, prompt, configs.batch_size, 
                          configs.max_new_tokens, configs.max_length, configs.doc_stride)
    
    with open(f"{configs.prediction_dir}predictions_{which_substance}.json", "w") as f:
        json.dump(predictions, f, indent=4)
        
    torch.cuda.empty_cache()
    gc.collect()

    torch.cuda.empty_cache()
    gc.collect()

    return predictions


print(f"Loading model and tokenizer from {configs.model_name_or_path} . . . .")
model = T5ForConditionalGeneration.from_pretrained(configs.model_name_or_path, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(configs.model_name_or_path)


df = pd.read_csv(f"{configs.data_path}{configs.file_name}", sep="\\")

# preprocess notes
# df['clean_text'] = df['ReportText'].progress_apply(clean_text)

for which_substance in ['alcohol', 'opioid', 'cannabis', 'sedative, hypnotic, or anxiolytic',
                        'cocaine', 'amphetamine', 'caffeine', 'hallucinogen', 'nicotine', 
                        'inhalant', 'other psychoactive']:
    
    print(f"Starting inference for {which_substance} use disorder diagnosis . . . .")
    run(which_substance, df)
    print(f'Inference Completed . . . .')
    print("="*20)
    
    
    
