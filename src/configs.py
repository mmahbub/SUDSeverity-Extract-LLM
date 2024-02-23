# paths
model_name_or_path = $PATH_TO_PRETRAINED_LLM$
data_path = $PATH_TO_DATA$
file_name = $DATA_FILE_NAME_CSV$
prediction_dir = $SAVE_PREDICTION_DIR$ ##if different from output_dir 
output_dir  = $LLM_OUTPUT_DIR$
rule_output_dir = $REGEX_OUTPUT_DIR$

# model params
batch_size = 1
max_new_tokens = 100
max_length = 512
doc_stride = 128
