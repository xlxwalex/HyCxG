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

echo "Download ABSA data in mirror source of ZJU MMF"
echo "Origin data for ABSA data (Not official) for Rest14/Lap14/Rest15/Rest16 can be found in https://github.com/GeneZC/ASGCN/tree/master/datasets"
echo "Origin data for ABSA data (official) for MAMS can be found in https://github.com/siat-nlp/MAMS-for-ABSA"

echo ">> 1.1 Rest 14 Dataset (train + test)"
Rest14_TRAIN_FILE=${DATA_DIR}/rest14_train.raw
Rest14_VALID_FILE=${DATA_DIR}/rest14_test.raw
Rest14_TEST_FILE=${DATA_DIR}/rest14_test.raw
Rest14_OUT_DIR=${OUTPUT_DIR}/JSONABSA_Rest14

wget -O $Rest14_TRAIN_FILE https://expic.xlxw.org/hycxg/datamirror/rest14_train.raw
wget -O $Rest14_TEST_FILE https://expic.xlxw.org/hycxg/datamirror/rest14_test.raw

echo "Process raw data (train + test) of Rest 14 to HyCxG format"
python $EXECUTE_DIR/process_absa.py --train_file $Rest14_TRAIN_FILE --valid_file $Rest14_VALID_FILE --test_file $Rest14_TEST_FILE \
--out_path $Rest14_OUT_DIR \
--stanford_path $STANFORD_DIR

echo ">> 1.2 Rest 14 Dataset (train + valid + test)"
Rest14_TRAIN_SPLIT_FILE=${DATA_DIR}/rest14_train_split.raw
Rest14_VALID_SPLIT_FILE=${DATA_DIR}/rest14_valid_split.raw
Rest14_OUT_DIR=${OUTPUT_DIR}/JSONABSA_Rest14Split

wget -O $Rest14_TRAIN_SPLIT_FILE https://expic.xlxw.org/hycxg/datamirror/rest14_train_split.raw
wget -O $Rest14_VALID_SPLIT_FILE https://expic.xlxw.org/hycxg/datamirror/rest14_valid_split.raw

echo "Process raw data (train + valid + test) of Rest 14 to HyCxG format"
python $EXECUTE_DIR/process_absa.py --train_file $Rest14_TRAIN_SPLIT_FILE --valid_file $Rest14_VALID_SPLIT_FILE --test_file $Rest14_TEST_FILE \
--out_path $Rest14_OUT_DIR \
--stanford_path $STANFORD_DIR

echo ">> 2.1 Lap 14 Dataset (train + test)"
Lap14_TRAIN_FILE=${DATA_DIR}/lap14_train.raw
Lap14_VALID_FILE=${DATA_DIR}/lap14_test.raw
Lap14_TEST_FILE=${DATA_DIR}/lap14_test.raw
Lap14_OUT_DIR=${OUTPUT_DIR}/JSONABSA_Lap14

wget -O $Lap14_TRAIN_FILE https://expic.xlxw.org/hycxg/datamirror/laptop_train.raw
wget -O $Lap14_TEST_FILE https://expic.xlxw.org/hycxg/datamirror/laptop_test.raw

echo "Process raw data (train + test) of Lap 14 to HyCxG format"
python $EXECUTE_DIR/process_absa.py --train_file $Lap14_TRAIN_FILE --valid_file $Lap14_VALID_FILE --test_file $Lap14_TEST_FILE \
--out_path $Lap14_OUT_DIR \
--stanford_path $STANFORD_DIR

echo ">> 2.2 Lap 14 Dataset (train + valid + test)"
Lap14_TRAIN_SPLIT_FILE=${DATA_DIR}/lap14_train_split.raw
Lap14_VALID_SPLIT_FILE=${DATA_DIR}/lap14_valid_split.raw
Lap14_OUT_DIR=${OUTPUT_DIR}/JSONABSA_Lap14Split

wget -O $Lap14_TRAIN_SPLIT_FILE https://expic.xlxw.org/hycxg/datamirror/lap14_train_split.raw
wget -O $Lap14_VALID_SPLIT_FILE https://expic.xlxw.org/hycxg/datamirror/lap14_valid_split.raw

echo "Process raw data (train + valid + test) of Lap 14 to HyCxG format"
python $EXECUTE_DIR/process_absa.py --train_file $Lap14_TRAIN_SPLIT_FILE --valid_file $Lap14_VALID_SPLIT_FILE --test_file $Lap14_TEST_FILE \
--out_path $Lap14_OUT_DIR \
--stanford_path $STANFORD_DIR

echo ">> 3.1 Rest 15 Dataset (train + test)"
Rest15_TRAIN_FILE=${DATA_DIR}/rest15_train.raw
Rest15_VALID_FILE=${DATA_DIR}/rest15_test.raw
Rest15_TEST_FILE=${DATA_DIR}/rest15_test.raw
Rest15_OUT_DIR=${OUTPUT_DIR}/JSONABSA_Rest15

wget -O $Rest15_TRAIN_FILE https://expic.xlxw.org/hycxg/datamirror/rest15_train.raw
wget -O $Rest15_TEST_FILE https://expic.xlxw.org/hycxg/datamirror/rest15_test.raw

echo "Process raw data (train + test) of Rest 15 to HyCxG format"
python $EXECUTE_DIR/process_absa.py --train_file $Rest15_TRAIN_FILE --valid_file $Rest15_VALID_FILE --test_file $Rest15_TEST_FILE \
--out_path $Rest15_OUT_DIR \
--stanford_path $STANFORD_DIR

echo ">> 3.2 Rest 15 Dataset (train + valid + test)"
Rest15_TRAIN_SPLIT_FILE=${DATA_DIR}/rest15_train_split.raw
Rest15_VALID_SPLIT_FILE=${DATA_DIR}/rest15_valid_split.raw
Rest15_OUT_DIR=${OUTPUT_DIR}/JSONABSA_Rest15Split

wget -O $Rest15_TRAIN_SPLIT_FILE https://expic.xlxw.org/hycxg/datamirror/rest15_train_split.raw
wget -O $Rest15_VALID_SPLIT_FILE https://expic.xlxw.org/hycxg/datamirror/rest15_valid_split.raw

echo "Process raw data (train + valid + test) of Rest 15 to HyCxG format"
python $EXECUTE_DIR/process_absa.py --train_file $Rest15_TRAIN_SPLIT_FILE --valid_file $Rest15_VALID_SPLIT_FILE --test_file $Rest15_TEST_FILE \
--out_path $Rest15_OUT_DIR \
--stanford_path $STANFORD_DIR

echo ">> 4.1 Rest 16 Dataset (train + test)"
Rest16_TRAIN_FILE=${DATA_DIR}/rest16_train.raw
Rest16_VALID_FILE=${DATA_DIR}/rest16_test.raw
Rest16_TEST_FILE=${DATA_DIR}/rest16_test.raw
Rest16_OUT_DIR=${OUTPUT_DIR}/JSONABSA_Rest16

wget -O $Rest16_TRAIN_FILE https://expic.xlxw.org/hycxg/datamirror/rest16_train.raw
wget -O $Rest16_TEST_FILE https://expic.xlxw.org/hycxg/datamirror/rest16_test.raw

echo "Process raw data (train + test) of Rest 16 to HyCxG format"
python $EXECUTE_DIR/process_absa.py --train_file $Rest16_TRAIN_FILE --valid_file $Rest16_VALID_FILE --test_file $Rest16_TEST_FILE \
--out_path $Rest16_OUT_DIR \
--stanford_path $STANFORD_DIR

echo ">> 4.2 Rest 16 Dataset (train + valid + test)"
Rest16_TRAIN_SPLIT_FILE=${DATA_DIR}/rest16_train_split.raw
Rest16_VALID_SPLIT_FILE=${DATA_DIR}/rest16_valid_split.raw
Rest16_OUT_DIR=${OUTPUT_DIR}/JSONABSA_Rest16Split

wget -O $Rest16_TRAIN_SPLIT_FILE https://expic.xlxw.org/hycxg/datamirror/rest16_train_split.raw
wget -O $Rest16_VALID_SPLIT_FILE https://expic.xlxw.org/hycxg/datamirror/rest16_valid_split.raw

echo "Process raw data (train + valid + test) of Rest 16 to HyCxG format"
python $EXECUTE_DIR/process_absa.py --train_file $Rest16_TRAIN_SPLIT_FILE --valid_file $Rest16_VALID_SPLIT_FILE --test_file $Rest16_TEST_FILE \
--out_path $Rest16_OUT_DIR \
--stanford_path $STANFORD_DIR

echo ">> 5 MAMS Dataset (train + valid + test)"
MAMS_TRAIN_SPLIT_FILE=${DATA_DIR}/rest16_train_split.raw
MAMS_VALID_SPLIT_FILE=${DATA_DIR}/rest16_valid_split.raw
MAMS_TEST_FILE=${DATA_DIR}/rest16_test.raw
MAMS_OUT_DIR=${OUTPUT_DIR}/JSONABSA_MAMS

wget -O $MAMS_TRAIN_SPLIT_FILE https://expic.xlxw.org/hycxg/datamirror/Mams_Train.xml.seg
wget -O $MAMS_VALID_SPLIT_FILE https://expic.xlxw.org/hycxg/datamirror/Mams_Valid.xml.seg
wget -O $MAMS_TEST_FILE https://expic.xlxw.org/hycxg/datamirror/Mams_Test_Gold.xml.seg

echo "Process raw data (train + valid + test) of Rest 16 to HyCxG format"
python $EXECUTE_DIR/process_absa.py --train_file $MAMS_TRAIN_SPLIT_FILE --valid_file $MAMS_VALID_SPLIT_FILE --test_file $MAMS_TEST_FILE \
--out_path $MAMS_OUT_DIR \
--stanford_path $STANFORD_DIR