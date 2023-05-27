#!/bin/bash

DETECT_FLAG=dataset/Vocab
# (English, Turkish, Dutch, Spanish, French, German)
LANGUAGE_1=$1
LANGUAGE_2=$2
LANGUAGE_3=$3
LANGUAGE_4=$4
LANGUAGE_5=$5
LANGUAGE_6=$6

if [ -d "$DETECT_FLAG" ]; then
    OUT_PATH=$DETECT_FLAG
else
    OUT_PATH='Vocab'
fi

if [ -d "$OUT_PATH" ]; then
    echo "$OUT_PATH folder exists, pass"
else
    echo "$OUT_PATH folder does not exist, try to mkdir"
    mkdir "$OUT_PATH"
fi

VOCAB_DIR=$OUT_PATH/CxG

if [ -d "$VOCAB_DIR" ]; then
    echo "$VOCAB_DIR folder exists, pass"
else
    echo "$VOCAB_DIR folder does not exist, try to mkdir"
    mkdir "$VOCAB_DIR"
fi

if test -z "$LANGUAGE_1"
then
  LANGUAGE_1=all
fi

echo "Downloading special_tokens_map.json"
wget -O $OUT_PATH/special_tokens_map.json https://expic.xlxw.org/hycxg/cxgvocab/special_tokens_map.json

echo "Downloading construction grammar list"
echo "Original data for construction grammar list of languages can be found in (c2xg package) https://github.com/jonathandunn/c2xg/tree/master/c2xg/data/models"

for LANG in $LANGUAGE_1 $LANGUAGE_2 $LANGUAGE_3 $LANGUAGE_4 $LANGUAGE_5 $LANGUAGE_6
do
  # English
  if [[ "$LANG" == "eng" ]] || [[ "$LANG" == "all" ]];then
    wget -O $VOCAB_DIR/construction.txt https://expic.xlxw.org/hycxg/cxgvocab/construction.txt
    wget -O $VOCAB_DIR/construction.pkl https://expic.xlxw.org/hycxg/cxgvocab/construction.pkl
  fi
  # Tukrish
  if [[ "$LANG" == "tur" ]] || [[ "$LANG" == "all" ]];then
    wget -O $VOCAB_DIR/tur.construction.txt https://expic.xlxw.org/hycxg/cxgvocab/tur.construction.txt
    wget -O $VOCAB_DIR/tur.construction.pkl https://expic.xlxw.org/hycxg/cxgvocab/tur.construction.pkl
  fi
  # French
  if [[ "$LANG" == "fra" ]] || [[ "$LANG" == "all" ]];then
    wget -O $VOCAB_DIR/fra.construction.txt https://expic.xlxw.org/hycxg/cxgvocab/fra.construction.txt
    wget -O $VOCAB_DIR/fra.construction.pkl https://expic.xlxw.org/hycxg/cxgvocab/fra.construction.pkl
  fi
  # Spanish
  if [[ "$LANG" == "spa" ]] || [[ "$LANG" == "all" ]];then
    wget -O $VOCAB_DIR/spa.construction.txt https://expic.xlxw.org/hycxg/cxgvocab/spa.construction.txt
    wget -O $VOCAB_DIR/spa.construction.pkl https://expic.xlxw.org/hycxg/cxgvocab/spa.construction.pkl
  fi
  # German
  if [[ "$LANG" == "deu" ]] || [[ "$LANG" == "all" ]];then
    wget -O $VOCAB_DIR/deu.construction.txt https://expic.xlxw.org/hycxg/cxgvocab/deu.construction.txt
    wget -O $VOCAB_DIR/deu.construction.pkl https://expic.xlxw.org/hycxg/cxgvocab/deu.construction.pkl
  fi
  # Dutch
  if [[ "$LANG" == "nld" ]] || [[ "$LANG" == "all" ]];then
    wget -O $VOCAB_DIR/nld.construction.txt https://expic.xlxw.org/hycxg/cxgvocab/nld.construction.txt
    wget -O $VOCAB_DIR/nld.construction.pkl https://expic.xlxw.org/hycxg/cxgvocab/nld.construction.pkl
  fi
done

echo "The CxG vocab of languages are stored in $OUT_PATH"
