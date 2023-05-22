#!/bin/bash

DATA_DIR=$1
OUTPUT_DIR=$2
EXECUTE_DIR=$3
PORT=9000

if test -z "$DATA_DIR"
then
  DATA_DIR='.'
fi

if test -z "$OUTPUT_DIR"
then
  OUTPUT_DIR='dataset'
fi

if test -z "$EXECUTE_DIR"
then
  EXECUTE_DIR='.'
fi

echo "Download multilingual data in mirror source of ZJU MMF"
echo "Origin data for multilingual dataset can be found in https://alt.qcri.org/semeval2016/task5/"

echo ">> 1 FRENCH"
FRENCH_TRAIN_FILE=${DATA_DIR}/french_train.raw
FRENCH_TEST_FILE=${DATA_DIR}/french_test.raw
FRENCH_OUT_DIR=${OUTPUT_DIR}/JSONABSA_French

wget -O $FRENCH_TRAIN_FILE https://expic.xlxw.org/hycxg/datamirror/french_train.raw
wget -O $FRENCH_TEST_FILE https://expic.xlxw.org/hycxg/datamirror/french_test.raw

echo "Process french raw data to HyCxG format"
python $EXECUTE_DIR/process_multilingual.py --train_file $FRENCH_TRAIN_FILE --test_file $FRENCH_TEST_FILE \
--out_path $FRENCH_OUT_DIR --lang french --port $PORT

echo ">> 2 SPANISH"
SPANISH_TRAIN_FILE=${DATA_DIR}/spanish_train.raw
SPANISH_TEST_FILE=${DATA_DIR}/spanish_test.raw
SPANISH_OUT_DIR=${OUTPUT_DIR}/JSONABSA_Spanish

wget -O $SPANISH_TRAIN_FILE https://expic.xlxw.org/hycxg/datamirror/spanish_train.raw
wget -O $SPANISH_TEST_FILE https://expic.xlxw.org/hycxg/datamirror/spanish_test.raw

echo "Process spanish raw data to HyCxG format"
python $EXECUTE_DIR/process_multilingual.py --train_file $SPANISH_TRAIN_FILE --test_file $SPANISH_TEST_FILE \
--out_path $SPANISH_OUT_DIR --lang spanish --port $PORT

echo ">> 3 TURKISH"
TURKISH_TRAIN_FILE=${DATA_DIR}/turkish_train.raw
TURKISH_TEST_FILE=${DATA_DIR}/turkish_test.raw
TURKISH_OUT_DIR=${OUTPUT_DIR}/JSONABSA_Turkish

wget -O $TURKISH_TRAIN_FILE https://expic.xlxw.org/hycxg/datamirror/turkish_train.raw
wget -O $TURKISH_TEST_FILE https://expic.xlxw.org/hycxg/datamirror/turkish_test.raw

echo "Process turkish raw data to HyCxG format"
python $EXECUTE_DIR/process_multilingual.py --train_file $TURKISH_TRAIN_FILE --test_file $TURKISH_TEST_FILE \
--out_path $TURKISH_OUT_DIR --lang turkish --port $PORT


echo ">> 4 DUTCH"
DUTCH_TRAIN_FILE=${DATA_DIR}/dutch_train.raw
DUTCH_TEST_FILE=${DATA_DIR}/dutch_test.raw
DUTCH_OUT_DIR=${OUTPUT_DIR}/JSONABSA_Dutch

wget -O $DUTCH_TRAIN_FILE https://expic.xlxw.org/hycxg/datamirror/dutch_train.raw
wget -O $DUTCH_TEST_FILE https://expic.xlxw.org/hycxg/datamirror/dutch_test.raw

echo "Process dutch raw data to HyCxG format"
python $EXECUTE_DIR/process_multilingual.py --train_file $DUTCH_TRAIN_FILE --test_file $DUTCH_TEST_FILE \
--out_path $DUTCH_OUT_DIR --lang dutch  --port $PORT
