#!/usr/bin/env python
import argparse
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import urllib2
import json
import itertools
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
from sklearn import cross_validation, metrics
import csv
import pdb
import pickle
import logging
import os

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

def loadGroundTruth(filename, caseversions=[]):
    existing_case_ids = map(lambda x:str(x['id']), caseversions)

    # TODO: move this parsing part to output.py
    with open(filename, 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=",", quotechar="\"")
        gt = output.parseResultCsv(rows)

    ids = []
    targets = [] # answers
    if len(existing_case_ids) > 0:
        for idx in range(len(gt['ids'])):
            case1 = gt['ids'][idx]['lhs_id']
            case2 = gt['ids'][idx]['rhs_id']

            if (case1 in existing_case_ids and case2 in existing_case_ids):
                targets.append(gt['perdictions'][idx])
                ids.append(gt['ids'][idx])
    else:
        ids = gt['ids']
        targets = gt['perdictions']

    return {'ids': ids, 'perdictions': targets}

def transformTargetLabels(labels, classes):
    le = LabelEncoder()
    le.fit(classes)
    return le.transform(labels), le.classes_

def genAllCombinations(caseversions):
    cvs_count = len(caseversions['objects'])
    logging.info("Found " + str(cvs_count) + " caseversions")
    comb = ({'lhs_id': str(caseversions['objects'][i]['id']), 'rhs_id': str(caseversions['objects'][j]['id']) } for i, j in itertools.combinations(range(len(caseversions['objects'])),2))
    logging.info("Generated " + str(cvs_count * (cvs_count - 1 )/2) + " pairs")
    return comb

def getCombinationSlice(n, combination_iter, step=1):
    logging.info("Getting " + str(n) + " pairs with sampling step of " + str(step))
    it = iter(combination_iter)
    while True:
        chunk = list(itertools.islice(it, 0, n*step, step))
        if not chunk:
            return
        yield chunk

def extractFeatures(caseversions, selected_pairs):
    #caseversions_sorted_by_id = sorted(caseversions['objects'], key=lambda x: x['id'])
    #print(caseversions_sorted_by_id)
    #idx_from_caseversion_id = dict((str(d['id']), i) for (i, d) in enumerate(caseversions_sorted_by_id))
    #TODO: can we reduce the number of cases here?
    #TODO: find the intersection between the groundtruth and the caseversions
    #caseversion_texts = map(lambda x: json.dumps(x), caseversions_sorted_by_id)

    logging.info("Prepare to extract features from " + str(len(selected_pairs)) + " pairs")


    counter = 0

    # Extracting similarity related features
    p = ProgressBar(3)
    p.update(1)
    #similarities = filters.calcSimilarity(caseversions, selected_pairs)
    #TODO enable similarity
    #vect = TfidfVectorizer(min_df=1)
    #tfidf = vect.fit_transform(caseversion_texts)
    #pairwise_similarity = tfidf * tfidf.T

    #p = ProgressBar(len(selected_pairs))
    # Extracting diff related features
    diffs = filters.calcDiffs(caseversions, selected_pairs)

    p.update(2)
    isonoffs = map(filters.isOnOffPairs, diffs)
    p.update(3)
    isdiffmodules = map(filters.isDifferentModule, diffs)
            #isdiffmodule = filters.isDifferentModule(diff)

    # Feature re-formatting
    def toDict(fields):
        return {
            "isonoff": fields[0],
            "isdiffmodule": fields[1],
            #"similarity": fields[2]
        }

    #features = map(toDict, zip(isonoffs, isdiffmodules, similarities))
    features = map(toDict, zip(isonoffs, isdiffmodules))
    vec = DictVectorizer()
    vectorized_features = vec.fit_transform(features)
    p.done()

    #p.done()
    return vectorized_features


def fit(vectorized_features, targets):
    #TODO: move this depth to config
    clf = tree.DecisionTreeClassifier(max_depth=3)
    clf = clf.fit(vectorized_features, targets)
    return clf

def perdict(vectorized_features, model):
    return model.predict(vectorized_features)

def main_fit(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)


    caseversions = loadLocalCaseversions(config['trainLocalJson'])
    groundtruth = loadGroundTruth(config['groundtruth_filename'], caseversions['objects'])
    vectorized_features = extractFeatures(caseversions, groundtruth['ids'])
    labels = ['dup', 'merge', 'none'] #TODO:Move to config
    transformed_labels, classes = transformTargetLabels(groundtruth['perdictions'],labels)
    #print(transformed_labels)
    #print(classes)
    model = fit(vectorized_features, transformed_labels)


    #Drawing decision tree
    #sudo apt-get install graphviz
    #dot -Tpdf iris.dot -o iris.pdf
    #from sklearn.externals.six import StringIO
    with open(config['model_filename'] + ".dot", 'w') as f:
        f = tree.export_graphviz(model, out_file=f,
                                 feature_names=['isonoff', 'isdiffmodule', 'similarity'], #TODO: move this to config, and let extractFeature read this
                                 class_names=classes
                                 )
        #os.system("dot -Tpdf {infile} -o {outfile}".format(
        #    infile = config['model_filename'] + ".dot",
        #    outfile = config['model_filename'] + ".pdf",
        #))

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

    logging.info("Extracting features")
    predictCaseversions = loadLocalCaseversions(config['perdictLocalJson'])
    comb_it = genAllCombinations(predictCaseversions)
    # TODO: extract the slice size to config

    labels = ['dup', 'merge', 'none'] #TODO:Move to config
    # TODO: this does not align with the fit function
    le = LabelEncoder()
    le.fit(labels)
    slice_num = 1
    for combinations in getCombinationSlice(config['slice_size'],comb_it, step=config.get('sample_step', 1)):
        vectorized_features = extractFeatures(predictCaseversions, combinations)
        logging.info("Making perdictions")
        perdictions = perdict(vectorized_features, model) # This can be interrupted by Ctrl+C

        answer = {'ids': combinations, 'perdictions': perdictions}

        logging.info("preparing data for saving to file")
        answer['perdictions'] = le.inverse_transform(answer['perdictions']).tolist()
        logging.info("saving to file")
        rawJson = "{perdiction_filename}_{slice_num}.raw.json".format(
            perdiction_filename = config['perdiction_filename'],
            slice_num = str(slice_num)
        )
        with open(rawJson, 'w') as f:
            json.dump(answer, f, indent=2)
        logging.info(rawJson+ " created")

        outputCsv = output.formatResultCsv(answer)

        csv_filename = "{perdiction_filename}_{slice_num}.csv".format(
            perdiction_filename = config['perdiction_filename'],
            slice_num = str(slice_num)
        )
        with open(csv_filename, 'w') as f:
            f.writelines(outputCsv)
        logging.info(csv_filename+ " created")

        slice_num += 1

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
