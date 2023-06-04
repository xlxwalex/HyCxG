#!/bin/bash
# Copyright 2023 The ZJU MMF Authors (Lvxiaowei Xu, Jianwang Wu, Jiawei Peng, Zhilin Gong, Ming Cai * and Tianxiang Wang).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Train HyCxG
# Global Variable (!!! SHOULD ADAPT TO YOUR CONFIGURATION !!!)
PLM_PATH_ABBR=bert-base-uncased
NUM_WORKERS=1     # Recommand: The bigger the better, if possible.

# ABSA
python train_hycxg.py --mode train --checkp hyper_cxg_mams \
--data_name JSONABSA_MAMS --num_classes 3 --num_workers $NUM_WORKERS \
--lm_path $PLM_PATH_ABBR --lm_group BERT

# GLUE - Base model
# Note: for STS task, the num_classes need to be set to 1
python train_hycxg.py --mode train --checkp hyper_cxg_mrpc  \
--data_name JSONGLUE_MRPC --num_classes 2 --num_workers $NUM_WORKERS \
--lm_path $PLM_PATH_ABBR --lm_group RoBERTa

# GLUE - Large model
python train_hycxg.py --mode train --checkp hyper_cxg_mrpc  \
--data_name JSONGLUE_MRPC --num_classes 2 --num_workers $NUM_WORKERS \
--lm_hidden_size 1024 --inter_size 4096 \
--lm_path $PLM_PATH_ABBR --lm_group RoBERTa