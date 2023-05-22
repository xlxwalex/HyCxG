#!/bin/bash

DATA_DIR=$1
OUTPUT_DIR=$2
STANFORD_DIR=$3
EXECUTE_DIR=$4

if test -z "$DATA_DIR"
then
  DATA_DIR='.'
fi

if test -z "$OUTPUT_DIR"
then
  OUTPUT_DIR='JSON_Counterfactual'
fi

if test -z "$STANFORD_DIR"
then
  STANFORD_DIR='../stanford-corenlp-3.9.2-minimal'
fi

if test -z "$EXECUTE_DIR"
then
  EXECUTE_DIR='.'
fi

echo "Download counterfactual data in mirror source of ZJU  MMF"
echo "Origin data can be found in https://github.com/Jiaqi1008/SemEval2020_Task5"

TRAIN_FILE=${DATA_DIR}/counterfactual_train.csv
TEST_FILE=${DATA_DIR}/counterfactual_test.csv
wget -O $TRAIN_FILE https://expic.xlxw.org/hycxg/datamirror/subtask1_train.csv
wget -O $TEST_FILE https://expic.xlxw.org/hycxg/datamirror/subtask1_test.csv

echo "Process csv data to HyCxG format"
python $EXECUTE_DIR/process_counterfactual.py --train_file $TRAIN_FILE --test_file $TEST_FILE \
--out_path $OUTPUT_DIR \
--stanford_path $STANFORD_DIR
