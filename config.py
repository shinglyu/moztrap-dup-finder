## ===== Training =====
# Use pre-downloaded json
# https://moztrap.mozilla.org/api/v1/caseversion/?format=json&productversion=217
#localJson = "./input/mid_217.json"
trainLocalJson="./input/full_217.json"
#localJson="./input/full_217.json.full"
groundtruth_filename= "./input/ground-truth-217.csv"

## ===== Perdiction =====
perdictLocalJson="./input/full_274.json"

## ===== Auto Download Test Cases =====
mtorigin = "https://moztrap.mozilla.org"
# Product Version, for downloading training data
productversion = 217  # Firefox OS v2.2
#productversion = 274  # Firefox OS v2.6

# Total number of cases, for downloading training data
# limit = 10881 #FxOS v2.6
# Total 10135
limit = 10142
#limit = 100 # for small scale testing
# limit = 5 # for small scale testing

# Show how many results, deprecated
# topCount = 5
# topCount = limit/2
# topCount = 500
# topCount = 500
# topCount = 100
