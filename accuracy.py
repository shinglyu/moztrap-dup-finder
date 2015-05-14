import csv

groundtruth_file = "./input/ground-truth-217.csv"
output_file = "./output/full_22_vanilla_tfidf.txt"

result = []
with open(groundtruth_file, 'r') as csvfile:
    groundtruth = csv.reader(csvfile, delimiter=",", quotechar="\"")
    for row in groundtruth:
        are_dup = row[0]
        case1   = row[1]
        case2   = row[2]
        similarity = row[3]
        comment = row[4]
        result.append({"are_dup": are_dup})

invalid = filter(lambda x: x["are_dup"] == "N", result)
valid = filter(lambda x: x["are_dup"] == "Y", result)
all_marked = filter(lambda x: x["are_dup"] != "", result)

accuracy = float(len(valid))/float(len(all_marked))

print("dup: {0} \tnot dup: {1} \ttotal: \t{2}".format(len(valid), len(invalid), len(all_marked)))
print("accuracy: {0}%".format(accuracy * 100.0))
