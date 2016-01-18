import csv
import json
import sys
from sklearn import metrics

#TODO: What is this file for?
#TODO: make these cmd parameters
groundtruth_file = "./input/ground-truth-217.csv"
#output_file = "./output/latest_output.json"
#output_file = "./output/full_22_tfidf_remove_onoff_and_diffmodule.json"
output_file = "./output/full_22_tfidf_naive.json"

print "Checking {0} against {1}".format(output_file, groundtruth_file)

#Loading files
groundtruth = []
with open(groundtruth_file, 'r') as csvfile:
    rows = csv.reader(csvfile, delimiter=",", quotechar="\"")
    for row in rows:
        if row[0] == "Y":
            are_dup = True
        elif row[0] == "N":
            are_dup = False
        else:
            are_dup = None
        case1   = row[1]
        case2   = row[2]
        similarity = row[3]
        comment = row[4]
        groundtruth.append({
            "lhs_id": case1,
            "rhs_id": case2,
            "are_dup": are_dup
        })

groundtruth = filter(lambda x: x['are_dup'] is not None, groundtruth)

myanswer = []
with open(output_file, 'r') as f:
    myanswer = json.load(f)

# Preparing result
#TODO: use some more functional way for this nested for
target = []
predicted = []
for idx, truth_entry in enumerate(groundtruth):

    progress = float(idx)/float(len(groundtruth)) * 100
    sys.stdout.write("\rProgress: [{0}{1}] {2:0.2f}%".format('='*int(round(progress/10)), ' '*int(round((100-progress)/10)), progress))
    sys.stdout.flush()

    for answer_entry in myanswer:
    #for answer_entry in myanswer[:10000]: #speedup
        if truth_entry['lhs_id'] == str(answer_entry['lhs_id']) and truth_entry['rhs_id'] == str(answer_entry['rhs_id']):
            target.append(truth_entry['are_dup'])
            predicted.append(answer_entry['are_dup'])

assert(len(target) == len(predicted))

print("\n")
print(metrics.classification_report(target, predicted))
