#!/bin/bash

OUT_PATH=CxGProcessor/data
# (English, Turkish, Dutch, Spanish, French, German)
LANGUAGE_1=$1
LANGUAGE_2=$2
LANGUAGE_3=$3
LANGUAGE_4=$4
LANGUAGE_5=$5
LANGUAGE_6=$6

if [ -d "$OUT_PATH" ]; then
    echo "$OUT_PATH folder exists, pass"
else
    echo "$OUT_PATH folder does not exist, please check"
    set -e
fi

if test -z "$LANGUAGE_1"
then
  LANGUAGE_1=all
fi

echo "Downloading construction grammar dictionaries"
echo "Original data for construction grammar dictionaries of languages can be found in (c2xg package) https://github.com/jonathandunn/c2xg/tree/master/c2xg/data/dictionaries"

for LANG in $LANGUAGE_1 $LANGUAGE_2 $LANGUAGE_3 $LANGUAGE_4 $LANGUAGE_5 $LANGUAGE_6
do
  # English
  if [[ "$LANG" == "eng" ]] || [[ "$LANG" == "all" ]];then
    wget -O $OUT_PATH/eng.DICT https://expic.xlxw.org/hycxg/cxgdict/eng.DICT
    wget -O $OUT_PATH/eng.RDR https://expic.xlxw.org/hycxg/cxgdict/eng.RDR
    wget -O $OUT_PATH/eng.clusters.fastText.v2.gz https://expic.xlxw.org/hycxg/cxgdict/eng.clusters.fastText.v2.gz
  fi
  # Tukrish
  if [[ "$LANG" == "tur" ]] || [[ "$LANG" == "all" ]];then
    wget -O $OUT_PATH/tur.DICT https://expic.xlxw.org/hycxg/cxgdict/tur.DICT
    wget -O $OUT_PATH/tur.RDR https://expic.xlxw.org/hycxg/cxgdict/tur.RDR
    wget -O $OUT_PATH/tur.clusters.fastText.v2.gz https://expic.xlxw.org/hycxg/cxgdict/tur.clusters.fastText.v2.gz
  fi
  # French
  if [[ "$LANG" == "fra" ]] || [[ "$LANG" == "all" ]];then
    wget -O $OUT_PATH/fra.DICT https://expic.xlxw.org/hycxg/cxgdict/fra.DICT
    wget -O $OUT_PATH/fra.RDR https://expic.xlxw.org/hycxg/cxgdict/fra.RDR
    wget -O $OUT_PATH/fra.clusters.fastText.v2.gz https://expic.xlxw.org/hycxg/cxgdict/fra.clusters.fastText.v2.gz
  fi
  # Spanish
  if [[ "$LANG" == "spa" ]] || [[ "$LANG" == "all" ]];then
    wget -O $OUT_PATH/spa.DICT https://expic.xlxw.org/hycxg/cxgdict/spa.DICT
    wget -O $OUT_PATH/spa.RDR https://expic.xlxw.org/hycxg/cxgdict/spa.RDR
    wget -O $OUT_PATH/spa.clusters.fastText.v2.gz https://expic.xlxw.org/hycxg/cxgdict/spa.clusters.fastText.v2.gz
  fi
  # German
  if [[ "$LANG" == "deu" ]] || [[ "$LANG" == "all" ]];then
    wget -O $OUT_PATH/deu.DICT https://expic.xlxw.org/hycxg/cxgdict/deu.DICT
    wget -O $OUT_PATH/deu.RDR https://expic.xlxw.org/hycxg/cxgdict/deu.RDR
    wget -O $OUT_PATH/deu.clusters.fastText.v2.gz https://expic.xlxw.org/hycxg/cxgdict/deu.clusters.fastText.v2.gz
  fi
  # Dutch
  if [[ "$LANG" == "nld" ]] || [[ "$LANG" == "all" ]];then
    wget -O $OUT_PATH/nld.DICT https://expic.xlxw.org/hycxg/cxgdict/nld.DICT
    wget -O $OUT_PATH/nld.RDR https://expic.xlxw.org/hycxg/cxgdict/nld.RDR
    wget -O $OUT_PATH/nld.clusters.fastText.v2.gz https://expic.xlxw.org/hycxg/cxgdict/nld.clusters.fastText.v2.gz
  fi
done

echo "The CxG vocab of languages are stored in $OUT_PATH"
