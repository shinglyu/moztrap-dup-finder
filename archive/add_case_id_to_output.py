import json

# TODO: integrate this into the output.py
with open('./input/full_274.json') as f:
    caseversions = json.load(f)

cvid_to_cid = {}
for caseversion in caseversions['objects']:
    cvid_to_cid[str(caseversion['id'])] =  caseversion['case']

with open ('./output/result.csv') as f:
    lines = f.readlines()

newlines = []
for line in lines:
    fields = line.split(' ')
    cid1 = cvid_to_cid[fields[0]]
    cid2 = cvid_to_cid[fields[1]]

    cid1 = cid1[13:-1] #strip the "/api/v1/case/" and the last "/"
    cid2 = cid2[13:-1]

    base_url = "https://moztrap.mozilla.org/manage/cases/?filter-id="
    fields[:0] = ([cid1, cid2] + [base_url + cid1, base_url + cid2])
    newlines.append(fields)

for line in newlines:
    print(','.join(line)),

