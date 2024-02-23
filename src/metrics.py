import collections, string, re
import pandas as pd


def normalize_answer(s):
    '''
    Helper function to normalize responses before calculating the metrics
    '''
    def remove_articles(text):
        regex = re.compile(r"\b(a|an|the)\b", re.UNICODE)
        return re.sub(regex, " ", text)
    
    def white_space_fix(text):
        return " ".join(text.split())
    
    def remove_punc(text):
        if "Severe/Stimulant" in text: text = text.replace("Severe/Stimulant", "Severe /Stimulant")
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)
    
    def lower(text):
        return text.lower()
    
    return white_space_fix(remove_articles(remove_punc(lower(s))))


def get_tokens(s):
    '''
    Tokenizes responses before calculating the metrics
    '''
    if not s:
        return []
    return normalize_answer(s).split()


def get_clean_ans(s):
    '''
    Normalizes responses before calculating the metrics
    '''
    if not s:
        return []
    return normalize_answer(s)


def compute_exact(a_gold, a_pred):
    '''
    Calculates strict-F1 metric scores
    '''
    return int(normalize_answer(a_gold) == normalize_answer(a_pred))


def compute_f1(a_gold, a_pred):
    '''
    Calculates relaxed-F1 metric scores
    '''
    gold_toks = get_tokens(a_gold)
    pred_toks = get_tokens(a_pred)
    common = collections.Counter(gold_toks) & collections.Counter(pred_toks)
    num_same = sum(common.values())
    if len(gold_toks) == 0 or len(pred_toks) == 0:
        return int(gold_toks == pred_toks)
    if num_same == 0:
        return 0
    
    precision = 1.0 * num_same/len(pred_toks)
    recall = 1.0 * num_same/len(gold_toks)
    f1 = (2 * precision * recall)/(precision + recall)
    
    return f1


def compute_precision(a_gold, a_pred):
    '''
    Calculates relaxed-precision metric scores
    '''
    gold_toks = get_tokens(a_gold)
    pred_toks = get_tokens(a_pred)
    common = collections.Counter(gold_toks) & collections.Counter(pred_toks)
    num_same = sum(common.values())
    if len(gold_toks) == 0 or len(pred_toks) == 0:
        return int(gold_toks == pred_toks)
    if num_same == 0:
        return 0
    
    precision = 1.0 * num_same/len(pred_toks)
    
    return precision


def compute_recall(a_gold, a_pred):
    '''
    Calculates relaxed-recall metric scores
    '''
    gold_toks = get_tokens(a_gold)
    pred_toks = get_tokens(a_pred)
    common = collections.Counter(gold_toks) & collections.Counter(pred_toks)
    num_same = sum(common.values())
    if len(gold_toks) == 0 or len(pred_toks) == 0:
        return int(gold_toks == pred_toks)
    if num_same == 0:
        return 0
    
    recall = 1.0 * num_same/len(gold_toks)
    
    return recall


def calculate_metric(ground_truth, predictions, pred_count, note_length, output_dir, which_substance):
    '''
    Calculates all metrics and saves them in a csv file
    '''
    exact_pred, rec_pred, prec_pred, f1_pred = {}, {}, {}, {}
    best_preds = {}
    for i,pred in predictions.items(): # loop through the dictionary of lists of final responses
        i = int(i)
        f1_p = [compute_f1(ground_truth[i],p) for p in pred] # list of relaxed-F1 scores for each sample to find the best response
        idx = f1_p.index(max(f1_p))
        best_preds[i] = pred[idx]
        exact_pred[i] = compute_exact(ground_truth[i], pred[idx])
        rec_pred[i] = compute_recall(ground_truth[i], pred[idx])
        prec_pred[i] = compute_precision(ground_truth[i], pred[idx])
        f1_pred[i] = compute_f1(ground_truth[i], pred[idx])

    df_res = pd.DataFrame()
    df_res['ID'] = list(best_preds.keys())
    df_res['candidate_ans_count'] = df_res['ID'].apply(str).map(pred_count)
    df_res['note_length'] = df_res['ID'].apply(str).map(note_length)
    df_res['ground_truth'] = df_res['ID'].map(ground_truth)
#    df_res['prediction'] = df_res['ID'].map(best_preds)
    df_res['strict_f1'] = df_res['ID'].map(exact_pred)
    df_res['relaxed_precision'] = df_res['ID'].map(prec_pred)
    df_res['relaxed_recall'] = df_res['ID'].map(rec_pred)
    df_res['relaxed_f1'] = df_res['ID'].map(f1_pred)
    
    # save the results in a dataframe
    df_res.to_csv(f"{output_dir}result_{which_substance}.csv", index=False)
    
    return df_res
