#!/usr/bin/python
import json

files = [
"full_274_0.json",
"full_274_500.json",
"full_274_1000.json",
"full_274_1500.json",
"full_274_2000.json",
"full_274_2500.json",
"full_274_3000.json",
"full_274_3500.json",
"full_274_4000.json",
"full_274_4500.json",
"full_274_5000.json",
"full_274_5500.json",
"full_274_6000.json",
"full_274_6500.json",
"full_274_7000.json",
"full_274_7500.json",
"full_274_8000.json",
"full_274_8500.json",
"full_274_9000.json",
"full_274_9500.json",
"full_274_10000.json",
"full_274_10500.json"
]

outfilename = "full_274.json"

fulljson = {'meta':{}, 'objects':[]}

for f in files:
  with open(f, 'r') as fp:
    cases = json.load(fp)
    fulljson['meta'] = cases['meta']
    fulljson['objects'] += cases['objects']

with open(outfilename, 'w') as ofp:
    json.dump(fulljson, ofp)
