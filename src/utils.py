import json
import re, string
from collections import defaultdict, OrderedDict
import numpy as np
import configs
from transformers import AutoTokenizer


def normalize_text(s):
    '''
    Helper function to normalize texts
    '''
    def remove_articles(text):
        regex = re.compile(r"\b(a|an|the)\b", re.UNICODE)
        return re.sub(regex, " ", text)
    
    def remove_nonalpha(text):
        text_new = []
        for x in list(text):
            if x.isalpha() or x==" ":
                text_new.append(x)
        return "".join(text_new) #re.sub("\d", "", text)
                       
    def white_space_fix(text):
        return " ".join(text.split())
    
    def remove_punc(text):
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)
    
    def lower(text):
        return text.lower()
    
    return white_space_fix(remove_articles(remove_nonalpha(remove_punc(lower(s)))))


def get_clean_text(s):
    '''
    Normalizes text
    '''
    if not s:
        return ""
    return normalize_text(s)


def get_tokens(s):
    '''
    Tokenizes text
    '''
    if not s:
        return ""
    return normalize_text(s).split()


def substrings(str1,str2):
    '''
    Helper function to find substrings between note and response
    '''
    str_ls = [str1[i:j+1] for i in range(len(str1)) for j in range(len(str1))]
    return [st for st in str_ls if st in str1 and st in str2 and len(st) >= 5]


def format_predictions(predictions_dict):
    '''
    Helper function to format the responses provided by the model
    '''
    # order predictions by note_id
    predictions_dict = OrderedDict(sorted(predictions_dict.items()))

    # filter out unanswerable & get unique values
    preds = {note_id:list(np.unique([p for p in preds if p.lower() != 'unanswerable'])) for note_id, preds in predictions_dict.items()}

    # perform label-specific filtering
    formatted_preds = {note_id:list(np.unique(p)) for note_id, p in preds.items()}
    formatted_preds = {note_id:["<no information found>"] if len(p)==0 else p for note_id, p in formatted_preds.items()}

    return formatted_preds


def refine_ans_with_severity(predictions, which_substance):
    pred_dict = {}
    for k,v in predictions.items():
        for pred in v:
            if any(sev==pred for sev in ['severe','mild','moderate','moderate, in remission','mild, in remission','severe, in remission','moderate, in early remission','mild, in early remission','severe, in early remission','moderate, in sustained remission','mild, in sustained remission','severe, in sustained remission','in remission','in early remission','in sustained remission']):
                v.append(f"{which_substance} abuse {pred}")
                v.append(f"{which_substance} use disorder {pred}")
                v.append(f"{which_substance} use d/o {pred}")
                v.append(f"{which_substance} dependence {pred}")
        pred_dict[k] = v
    return pred_dict


def filter_on_dx(text, note, which_substance):
    '''
    Helper function to filter out possible non-SUD responses if any returned
    '''
    substance_list = json.load(open(".../data/substanceList.json"))
    sud_list = ["abuse", "dependence", "dependency", "dep", "addiction", "use disorder", "use d/o", "use do", "d/o"]
    sud_var = [f"{s}{punc}" for punc in list(""".,?/-`~"'!)(*;: """) for s in ["ud", "do"]]
    sud_list += sud_var
    sev_list = ["sev", "mild", "mod", "unspec", "compl", "continu", "remiss"]        

    text = get_clean_text(text)
    note = get_clean_text(note)
    if (text!='no information found' and text in note):
        for sub in substance_list[which_substance]:
            match = re.search(sub, text)
            if match is not None:
                stind = match.start()
                if any(sud.lower() in text[stind:].lower() for sud in sud_list):
                    return True
                elif any(sev.lower() in text[stind:].lower() for sev in sev_list): # additional filtering (not really necessary)
                    return True
                elif any(sev.lower() in text[:stind].lower() for sev in sev_list): # additional filtering (not really necessary)
                    return True
                
    elif text!='no information found':
        # check if any of the common substring contains sud info 
        cs_ls = substrings(text, note)
        for cs in cs_ls:
            for sub in substance_list[which_substance]:
                match = re.search(sub, cs)
                if match is not None:
                    stind = match.start()
                    if any(sud.lower() in cs[stind:].lower() for sud in sud_list):
                        return True
                    elif any(sev.lower() in cs[stind:].lower() for sev in sev_list): # additional filtering (not really necessary)
                        return True
                    elif any(sev.lower() in cs[:stind].lower() for sev in sev_list): # additional filtering (not really necessary)
                        return True
    return False
    
    
def postprocess_predictions(predictions_dict, notes, which_substance):
    '''
    Helper function to postprocess responses returned by the model
    '''
    preds = format_predictions(predictions_dict)
    preds = refine_ans_with_severity(preds, which_substance)
    
    # create a new dictionary with the final predictions
    processed_preds = {}
    
    pred_count = {}
    note_length = {}
    
    tokenizer = AutoTokenizer.from_pretrained(configs.model_name_or_path)

    # loop through the prediction dictionary {'0':[cand-ans1, cand-ans2],'1':[cand-ans1, cand-ans2]}
    for i,p in preds.items():
        
        # keep the answers that mention sud/severity
        if len(p) != 1:
            
            keep_preds = []
            for x in p:
                if filter_on_dx(x, notes[int(i)], which_substance):
                    keep_preds.append(x)
                    
            if len(keep_preds)==0:
                keep_preds = ["<no information found>"]
                
            processed_preds[i] = keep_preds

        elif len(p) == 1:
            if filter_on_dx(p[0], notes[int(i)], which_substance):
                processed_preds[i] = p
            else:
                processed_preds[i] = ["<no information found>"]
                
        pred_count[i] = len(processed_preds[i])  
        note_length[i] = len(tokenizer(notes[int(i)]).input_ids)
        
    return processed_preds, pred_count, note_length
