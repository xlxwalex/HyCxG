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
  OUTPUT_DIR='dataset'
fi

if test -z "$STANFORD_DIR"
then
  STANFORD_DIR='../stanford-corenlp-3.9.2-minimal'
fi

if test -z "$EXECUTE_DIR"
then
  EXECUTE_DIR='.'
fi

echo "Download colloquial data (Twitter) in mirror source of ZJU MMF"
echo "Origin data for Twitter can be found in https://github.com/songyouwei/ABSA-PyTorch/tree/master/datasets/acl-14-short-data"

TWITTER_TRAIN_FILE=${DATA_DIR}/twitter_train.raw
TWITTER_TEST_FILE=${DATA_DIR}/twitter_test.raw
TWITTER_OUT_DIR=${OUTPUT_DIR}/JSONABSA_Twitter

wget -O $TWITTER_TRAIN_FILE https://expic.xlxw.org/hycxg/datamirror/Twitter_train.raw
wget -O $TWITTER_TEST_FILE https://expic.xlxw.org/hycxg/datamirror/Twitter_test.raw

echo "Process raw data of Twitter to HyCxG format"
python $EXECUTE_DIR/process_twitter.py --train_file $TWITTER_TRAIN_FILE --test_file $TWITTER_TEST_FILE \
--out_path $TWITTER_OUT_DIR \
--stanford_path $STANFORD_DIR

echo "Download colloquial data (GermEval) in mirror source of ZJU MMF"
echo "Origin data for GermEval can be found in http://ltdata1.informatik.uni-hamburg.de/germeval2017/"
echo "Note: the GermEval dataset in our experiment is a subset. if you want to reporduce the experiment, you may download data via this script."

GERMEVAL_TRAIN_FILE=${DATA_DIR}/germeval_train.raw
GERMEVAL_VALID_FILE=${DATA_DIR}/germeval_valid.raw
GERMEVAL_TEST_FILE=${DATA_DIR}/germeval_test.raw
GERMEVAL_OUT_DIR=${OUTPUT_DIR}/JSONABSA_German

wget -O $GERMEVAL_TRAIN_FILE https://expic.xlxw.org/hycxg/datamirror/germeval_train.raw
wget -O $GERMEVAL_VALID_FILE https://expic.xlxw.org/hycxg/datamirror/germeval_valid.raw
wget -O $GERMEVAL_TEST_FILE https://expic.xlxw.org/hycxg/datamirror/germeval_test.raw

echo "Process raw data of GermEval to HyCxG format"
python $EXECUTE_DIR/process_germeval.py --train_file $GERMEVAL_TRAIN_FILE --valid_file $GERMEVAL_VALID_FILE --test_file $GERMEVAL_TEST_FILE \
--out_path $GERMEVAL_OUT_DIR