import json
import os

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "../dataset/Vocab/special_tokens_map.json")), mode="r", encoding="utf-8") as f:
    special_tokens_map = json.load(f)

UNK_TOKEN = special_tokens_map["unk_token"]
CLS_TOKEN = special_tokens_map["cls_token"]
SEP_TOKEN = special_tokens_map["sep_token"]
PAD_TOKEN = special_tokens_map["pad_token"]

CONST_TOKEN_MODE_WORD = 'WORD'
CONST_TOKEN_MODE_CXG  = 'CXG'