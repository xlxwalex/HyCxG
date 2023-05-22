#!/bin/bash

DATA_DIR=$1
OUTPUT_DIR=$2
STANFORD_DIR=$3

if test -z "$DATA_DIR"
then
  DATA_DIR='.'
fi

if test -z "$OUTPUT_DIR"
then
  OUTPUT_DIR='dataset'
fi

if test -z "$STANFORD_DIR"
then
  STANFORD_DIR='stanford-corenlp-3.9.2-minimal'
fi

if [ -d "$STANFORD_DIR" ]; then
    echo "$STANFORD_DIR exists, pass"
else
    echo "$STANFORD_DIR does not exist, try to download"
    python download_stanfordcore.py
fi

# Download and process ABSA datasets
bash ABSA/download_and_process_absa.sh $DATA_DIR $OUTPUT_DIR $STANFORD_DIR ABSA

# Download and process GLUE datasets
bash GLUE/download_and_process_glue.sh $OUTPUT_DIR $STANFORD_DIR all GLUE

# Download and process Colloquial datasets
bash Colloquial/download_and_process_colloquial.sh $DATA_DIR $OUTPUT_DIR $STANFORD_DIR Colloquial

# Download and process Counterfactual datasets
bash Counterfactual/download_and_process_counterfactual.sh $DATA_DIR $OUTPUT_DIR $STANFORD_DIR Counterfactual

# Download and process Multilingual datasets
bash Multilingual/download_and_process_multilingual.sh $DATA_DIR $OUTPUT_DIR Multilingual