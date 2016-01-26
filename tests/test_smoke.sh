#!/bin/bash

#Must be called in the root dir

set -e

python finddup.py fit tests/data/test_smoke_config.json 

ls tests/tmp/test_smoke_model.pkl
if ! [ -f tests/tmp/test_smoke_model.pkl ]
then
  echo "[FAIL] Fail to generate model file"
  exit 1
fi
head tests/tmp/test_smoke_model.pkl

echo "================"

python finddup.py perdict tests/data/test_smoke_config.json 

ls tests/tmp/test_smoke_perdictions.raw.json
if ! [ -f tests/tmp/test_smoke_perdictions.raw.json ]
then
  echo "[FAIL] Fail to generate perdiction file"
  exit 1
fi
head tests/tmp/test_smoke_perdictions.raw.json

ls tests/tmp/test_smoke_perdictions.csv
if ! [ -f tests/tmp/test_smoke_perdictions.csv ]
then
  echo "[FAIL] Fail to generate perdiction file"
  exit 1
fi
head tests/tmp/test_smoke_perdictions.csv

echo "[PASS]"
