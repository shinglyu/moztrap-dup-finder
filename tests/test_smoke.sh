#!/bin/bash

#Must be called in the root dir

set -e

function checkFileExist {
  echo ""
  echo "Checking if file $1 exists..."
  ls -l "$1"
  if ! [ -f "$1" ]
  then
    echo "[FAIL] Fail to generate model file"
    exit 1
  fi
  echo ""
  echo "$1 content:"
  echo "-----------"
  head "$1"
  echo "-----------"
  echo ""
}


rm -f tests/tmp/*

# Test start
# training
python finddup.py fit tests/data/test_smoke_config.json 

  checkFileExist tests/tmp/test_smoke_model.pkl


# perdiction
python finddup.py perdict tests/data/test_smoke_config.json 

  checkFileExist tests/tmp/test_smoke_perdictions_1.raw.json
  checkFileExist tests/tmp/test_smoke_perdictions_1.csv

  checkFileExist tests/tmp/test_smoke_perdictions_2.raw.json
  checkFileExist tests/tmp/test_smoke_perdictions_2.csv

echo "[PASS]"
