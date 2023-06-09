#!/bin/bash

OUTPUT_DIR=$1
STANFORD_DIR=$2
TASK=$3
EXECUTE_DIR=$4

if test -z "$OUTPUT_DIR"
then
  OUTPUT_DIR='dataset'
fi

if test -z "$STANFORD_DIR"
then
  STANFORD_DIR='../stanford-corenlp-3.9.2-minimal'
fi

if test -z "$TASK"
then
  TASK='all'
fi

if test -z "$EXECUTE_DIR"
then
  EXECUTE_DIR='.'
fi

echo "Original data can be found in https://gluebenchmark.com/"

echo "Process data to HyCxG format (depend on Hugging Face)"
python $EXECUTE_DIR/download_and_process_glue.py --task $TASK \
--out_path $OUTPUT_DIR \
--stanford_path $STANFORD_DIR
