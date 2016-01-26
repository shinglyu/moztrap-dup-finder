#!/usr/bin/env python
import argparse
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import urllib2
import json
import itertools
from sklearn.feature_extraction import DictVectorizer
from sklearn import tree
from sklearn import cross_validation, metrics
import csv
import pdb
import pickle
import logging

import filters
from progressbar import ProgressBar


from config import *
import output

logging.basicConfig(level=logging.INFO)

#TODO: we should probably do this in the shell script, not here, too slow
def downloadCaseversions():
    url = mtorigin + "/api/v1/caseversion/"
    url = url + "?format=json"
    url = url + "&limit=" + str(limit)
    url = url + "&productversion=" + str(productversion)
    data = urllib2.urlopen(url).read()
    return json.loads(data)

def loadLocalCaseversions(filename):
    with open(filename, "r") as f:
        return json.load(f)

def loadGroundTruth(filename):
    ids = []
    targets = [] # answers
    with open(filename, 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=",", quotechar="\"")
        for row in rows: # has title row
            if row[0] == "Dup?":
                continue # title row
            if row[0][0] == "Y" or row[0][0] == "y":
                target = "dup"
            elif row[1][0] == "Y" or row[1][0] == "y":
                target = "merge"
            else:
                target = "none"

            case1   = row[9]
            case2   = row[10]
            ids.append({
                "lhs_id": case1,
                "rhs_id": case2,
            })
            targets.append(target) #TODO: change to X/Dup/Merge tags
    return {'ids': ids, 'perdictions': targets}


def genAllCombinations(caseversions):
    return [{'lhs_id': caseversions['objects'][i]['id'], 'rhs_id': caseversions['objects'][j]['id'] } for i, j in itertools.combinations(range(len(caseversions['objects'])),2)]

def extractFeatures(caseversions, selected_pairs):
    caseversions_sorted_by_id = sorted(caseversions['objects'], key=lambda x: x['id'])
    #print(caseversions_sorted_by_id)
    idx_from_caseversion_id = dict((str(d['id']), i) for (i, d) in enumerate(caseversions_sorted_by_id))
    #TODO: can we reduce the number of cases here?
    #TODO: find the intersection between the groundtruth and the caseversions
    caseversion_texts = map(lambda x: json.dumps(x), caseversions_sorted_by_id)

    features = []

    counter = 0

    #TODO enable similarity
    #vect = TfidfVectorizer(min_df=1)
    #tfidf = vect.fit_transform(caseversion_texts)
    #pairwise_similarity = tfidf * tfidf.T

    p = ProgressBar(len(selected_pairs))
    for pair in selected_pairs:
        # TODO: handle if groundtruth is not in the small set
        #Extract similarity
        try:
            r = idx_from_caseversion_id[str(pair['lhs_id'])]
            c = idx_from_caseversion_id[str(pair['rhs_id'])]
            #similarity = pairwise_similarity[r, c] #"tfidf_diff": tfidf[i] - tfidf[j]

            diff  = filters.calcDiff(caseversion_texts[r], caseversion_texts[c])
            isonoff = filters.isOnOffPairs(diff)
            #isdiffmodule = filters.isDifferentModule(diff)

        except KeyError:
            #similarity = 0 # Is this good?
            isonoff = False
            #isdiffmodule = False
            continue

        features.append({
            #"similarity": similarity,
            "isonoff": isonoff,
            #"isdiffmodule": isdiffmodule
        })
        p.update(counter)
        counter += 1

    vec = DictVectorizer()
    vectorized_features = vec.fit_transform(features)

    p.done()
    return vectorized_features


def fit(vectorized_features, targets):
    clf = tree.DecisionTreeClassifier(max_depth=3)
    clf = clf.fit(vectorized_features, targets)
    return clf

def perdict(vectorized_features, model):
    return model.predict(vectorized_features)

def main_fit(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)


    caseversions = loadLocalCaseversions(config['trainLocalJson'])
    groundtruth = loadGroundTruth(config['groundtruth_filename'])
    vectorized_features= extractFeatures(caseversions, groundtruth['ids'])
    model = fit(vectorized_features, groundtruth['perdictions'])


    #Drawing decision tree
    #sudo apt-get install graphviz
    #dot -Tpdf iris.dot -o iris.pdf
    #from sklearn.externals.six import StringIO
    with open("output/model.dot", 'w') as f:
        f = tree.export_graphviz(model, out_file=f)

    with open(config['model_filename'], 'w') as f:
        pickle.dump(model, f)

    logging.info("Model saved to " + config['model_filename'])

def main_cross_validate():
    caseversions = loadLocalCaseversions(trainLocalJson)
    vectorized_features, targets = prepare_training_data(caseversions)
    model = fit(vectorized_features, targets)

    predicted = cross_validation.cross_val_predict(model, vectorized_features, targets, cv=3)
    print(metrics.accuracy_score(targets, predicted))
    print(metrics.classification_report(targets, predicted))

def main_perdict(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)

    with open(config['model_filename'], 'r') as f:
        model = pickle.load(f)

    logging.info("Loaded model " + config['model_filename'])

    predictCaseversions = loadLocalCaseversions(config['perdictLocalJson'])
    combinations = genAllCombinations(predictCaseversions)
    vectorized_features = extractFeatures(predictCaseversions, combinations)
    perdictions = perdict(vectorized_features, model) # This can be interrupted by Ctrl+C

    answer = {'ids': combinations, 'perdictions': perdictions}

    print("preparing data for saving to file")
    answer['perdictions'] = answer['perdictions'].tolist()
    print("saving to file")
    rawJson = config['perdiction_filename'] + ".raw.json"
    with open(rawJson, 'w') as f:
        json.dump(answer, f, indent=2)
    logging.info(rawJson+ " created")

    dups = zip(answer['ids'], answer['perdictions'])
    dups = filter(lambda x: x[1], dups)
    dups = map(lambda x: x[0], dups)

    outputCsv = output.printDups(dups)

    csv_filename = config['perdiction_filename'] + ".csv"
    with open(csv_filename, 'w') as f:
        f.writelines(outputCsv)
    logging.info(csv_filename+ " created")

def main():

    parser = argparse.ArgumentParser(description='Finding duplicates or mergeable cases in MozTrap.')
    subparsers = parser.add_subparsers(dest="action",
                                       help="use \"[command] -h\" to see help message for individual command")

    parser_fit = subparsers.add_parser('fit')
    parser_fit.add_argument('config_file', type=str
                              ,help="Config File JSON")

    parser_perdict = subparsers.add_parser('perdict')
    parser_perdict.add_argument('config_file', type=str
                              ,help="Config File JSON")
    args = parser.parse_args()
    # TODO: split this into three files

    if args.action == 'fit':
        main_fit(args.config_file)
    elif args.action == 'cross-validate':
        main_cross_validate()
    elif args.action == 'perdict':
        main_perdict(args.config_file)

if __name__ == '__main__':
    main()
