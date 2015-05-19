import csv
import json
import sys

groundtruth_file = "./input/ground-truth-217.csv"
output_file = "./output/latest_output.json"

print "Checking {0} against {1}".format(output_file, groundtruth_file)

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

match = 0
mismatch = 0
nomatch = 0
print len(groundtruth)
for idx, truth_entry in enumerate(groundtruth):

    progress = float(idx)/float(len(groundtruth)) * 100
    sys.stdout.write("\rProgress: [{0}{1}] {2:0.2f}%".format('='*int(round(progress/10)), ' '*int(round((100-progress)/10)), progress))
    sys.stdout.flush()

    for answer_entry in myanswer:
    #for answer_entry in myanswer[:10000]: #speedup
        if truth_entry['lhs_id'] == str(answer_entry['lhs_id']) and truth_entry['rhs_id'] == str(answer_entry['rhs_id']):
            #print truth_entry['are_dup']
            #print answer_entry['are_dup']
            if truth_entry['are_dup'] is None:
                continue
            if truth_entry['are_dup'] == answer_entry['are_dup']:
                match += 1
            else:
                mismatch += 1

nomatch = len(myanswer) - match - mismatch


print('\n')
print("correct: {0} \tincorrect: {1} \tnot in groundtruth:\t {2}\ttotal: \t{3}".format(match, mismatch, nomatch, len(myanswer)))
accuracy = float(match)/float(match + mismatch)
print("accuracy: {0:0.3f}%".format(accuracy * 100.0))

#invalid = filter(lambda x: x["are_dup"] == "N", result)
#valid = filter(lambda x: x["are_dup"] == "Y", result)
#all_marked = filter(lambda x: x["are_dup"] != "", result)

#accuracy = float(len(valid))/float(len(all_marked))

#print("dup: {0} \tnot dup: {1} \ttotal: \t{2}".format(len(valid), len(invalid), len(all_marked)))
#print("accuracy: {0}%".format(accuracy * 100.0))
