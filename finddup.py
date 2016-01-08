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

logging.basicConfig(level=logging.INFO)

from config import *
import output

def downloadCaseversions():
    # query = query.replace(" ", "\%20")
    # baseurl = "https://developer.mozilla.org/en-US/search?format=json&q="
    url = mtorigin + "/api/v1/caseversion/"
    #url = baseURL + str(cid) + "/"
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
    are_dups = []
    with open(filename, 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=",", quotechar="\"")
        for row in rows:
            if row[0] == "Y":
                are_dup = True
            elif row[0] == "N":
                are_dup = False
            else:
                continue # SKIP Not labeled!
                #are_dup = None
            case1   = row[1]
            case2   = row[2]
            # similarity = row[3]
            # comment = row[4]
            ids.append({
                "lhs_id": case1,
                "rhs_id": case2,
            })
            are_dups.append(are_dup)
    return {'ids': ids, 'targets': are_dups}

#caseversions = downloadCaseversions()
#print json.dumps(caseversions['objects'][0])

def prepare_training_data(caseversions):

    #print(caseversions['meta'])
    caseversions_sorted_by_id = sorted(caseversions['objects'], key=lambda x: x['id'])
    #idx_from_caseversion_id = dict((d['id'], dict(d, index=i)) for (i, d) in enumerate(x))
    idx_from_caseversion_id = dict((str(d['id']), i) for (i, d) in enumerate(caseversions_sorted_by_id))
    #TODO: can we reduce the number of cases here?
    #TODO: find the intersection between the groundtruth and the caseversions
    caseversion_texts = map(lambda x: json.dumps(x), caseversions_sorted_by_id)

    vect = TfidfVectorizer(min_df=1)
    tfidf = vect.fit_transform(caseversion_texts)
    pairwise_similarity = tfidf * tfidf.T

    groundtruth = loadGroundTruth(groundtruth_filename)
    #print(pairwise_similarity.shape)
    features = []
    #case_ids= []
    #pdb.set_trace()
    p = ProgressBar(len(list(itertools.combinations(range(len(caseversion_texts)),2))))

#        item['diff'] = filters.calcDiff(item['r'], item['c'], caseversions)
# #        if filters.isOnOffPairs(item['diff']):
#            topranks[i]['are_dup']= False
#            topranks[i]['reason']= "onoff"
#
#        if filters.isDifferentModule(item['diff']):
#            topranks[i]['are_dup']= False
#            topranks[i]['reason']= "diffmodule"
    counter = 0
    for pair in groundtruth['ids']:
        # TODO: handle if groundtruth is not in the small set
        #Extract similarity
        try:
            r = idx_from_caseversion_id[pair['lhs_id']]
            c = idx_from_caseversion_id[pair['rhs_id']]
            similarity = pairwise_similarity[r, c] #"tfidf_diff": tfidf[i] - tfidf[j]

            diff  = filters.calcDiff(caseversion_texts[r], caseversion_texts[c])
            isonoff = filters.isOnOffPairs(diff)
            isdiffmodule = filters.isDifferentModule(diff)

        except KeyError:
            similarity = 0 # Is this good?
            isonoff = False
            isdiffmodule = False
            continue

        features.append({
            "similarity": similarity,
            "isonoff": isonoff,
            "isdiffmodule": isdiffmodule
        })
        p.update(counter)
        counter += 1
    #for i, j in itertools.combinations(range(len(caseversion_texts)),2):
        #print([i,j])
        #case_ids.append({
        #    'lhs_id':caseversions_sorted_by_id[i]['id'],
        #    'rhs_id':caseversions_sorted_by_id[j]['id']
        #})
        #features.append({
        #    "similarity": pairwise_similarity[i, j],
        #    #"tfidf_diff": tfidf[i] - tfidf[j]
        #})

    #print(json.dumps(features, indent=2))

    vec = DictVectorizer()
    vectorized_features = vec.fit_transform(features)

    p.done()
    return (vectorized_features, groundtruth['targets'])

def fit(vectorized_features, targets):
    #vectorized_features, targets = prepare_training_data(caseversions)
    #TODO: load groundtruth to target
    #print(features)
    #naive_target = map(lambda x: x['similarity'] > 0.8, features)
    #print(naive_target.count(True))
    #print(naive_target.count(False))
    #>>> feature = [[0, 0], [1, 1]]
    #>>> target = [0, 1]
    clf = tree.DecisionTreeClassifier(max_depth=3)
    #clf = clf.fit(vectorized_features, groundtruth['targets'])
    clf = clf.fit(vectorized_features, targets)
    return clf

def perdict(caseversions, model):

    #print(caseversions['meta'])
    caseversions_sorted_by_id = sorted(caseversions['objects'], key=lambda x: x['id'])
    caseversion_texts = map(lambda x: json.dumps(x), caseversions_sorted_by_id)

    vect = TfidfVectorizer(min_df=1)
    tfidf = vect.fit_transform(caseversion_texts)
    pairwise_similarity = tfidf * tfidf.T

    #print(pairwise_similarity.shape)
    features = []
    case_ids= []
    #pdb.set_trace()
    p = ProgressBar(len(list(itertools.combinations(range(len(caseversion_texts)),2))))

    #sorting by similarity
    #reindex = np.argsort(-pairwise_similarity.A.flatten())
    #r, c = divmod(reindex, pairwise_similarity.shape[1])
    #dups = filter(lambda (ri,ci): ri < ci, zip(r,c))

    counter = 0
    for i, j in itertools.combinations(range(len(caseversion_texts)),2):
        try:
            p.update(counter)
            counter += 1
            #print([i,j])
            case_ids.append({
                'lhs_id':caseversions_sorted_by_id[i]['id'],
                'rhs_id':caseversions_sorted_by_id[j]['id']
            })
            diff  = filters.calcDiff(
                json.dumps(caseversions_sorted_by_id[i]),
                json.dumps(caseversions_sorted_by_id[j])
            )
            features.append({
                "similarity": pairwise_similarity[i, j],
                "isonoff": filters.isOnOffPairs(diff),
                "isdiffmodule": filters.isDifferentModule(diff)
                #"tfidf_diff": tfidf[i] - tfidf[j]
            })
        except KeyboardInterrupt:
            if len(case_ids) != len(features):
                old_len = min(len(case_ids), len(features))
                case_ids = case_ids[:old_len]
                features = features[:old_len]
            break


    vec = DictVectorizer()
    vectorized_features = vec.fit_transform(features)
    p.done()

    return {'ids': case_ids, 'perdictions':model.predict(vectorized_features)}

    #print(features)

    #print pairwise_similarity.A

    #sorting by similarity
    #reindex = np.argsort(-pairwise_similarity.A.flatten())
    #r, c = divmod(reindex, pairwise_similarity.shape[1])

    #topranks = []
    # Only use the lower half of the similarity matrix
    #dups = filter(lambda (ri,ci): ri < ci, zip(r,c))

    #for ri, ci in dups:
    #    if ri < ci:
    #        topranks.append({
    #            #"r": ri,
    #            #"c": ci,
    #            #"lhs_id": caseversions['objects'][ri]['id'], #FIXME: rename to rhs/lhs
    #            #"rhs_id": caseversions['objects'][ci]['id'],
    #            "similarity": pairwise_similarity[ri, ci],
                #"are_dup" : False,
    #            #"reason" : ""
    #            #"diff": filters.calcDiff(ri, ci, caseversions)
    #        })
#
#    for i in range(0, topCount):
#        item = topranks[i]
#        item['are_dup']=True
#        item['diff'] = filters.calcDiff(item['r'], item['c'], caseversions)
#
#        if filters.isOnOffPairs(item['diff']):
#            topranks[i]['are_dup']= False
#            topranks[i]['reason']= "onoff"
#
#        if filters.isDifferentModule(item['diff']):
#            topranks[i]['are_dup']= False
#            topranks[i]['reason']= "diffmodule"

    #topranks = topranks[:topCount] # Only get the top

    #for item in topranks:
    #    item['diff'] = filters.calcDiff(item['r'], item['c'], caseversions)

    #onoffs_indexes = [i for i, val in enumerate(topranks) if
                      #val['diff'] and
                      #filters.isOnOffPairs(val['diff'])]
    #diffmodules_indexes = [i for i, val in enumerate(topranks) if filters.isDifferentModule(val['diff'])]
#
    #for i in onoffs_indexes:
        #topranks[i]['are_dup']= False
        #topranks[i]['reason']= "onoff"
#
    #for i in diffmodules_indexes:
        #topranks[i]['are_dup']= False
        #topranks[i]['reason']= "diffmodule"


    #output.printNotDup(onoffs, "is an on/off pair")
#    return topranks

#onoffs = filter(lambda x: filters.isOnOffPairs(x['diff']), topranks)
#output.printNotDup(onoffs, "is an on/off pair")
#
#diffModules = filter(lambda x: filters.isDifferentModule(x['diff']), topranks)
#output.printNotDup(diffModules, "belong to different module")
#
#topranks = filter(lambda x: not filters.isOnOffPairs(x['diff']), topranks)
#topranks = filter(lambda x: not filters.isDifferentModule(x['diff']), topranks)

#
#output.drawGraph(realdups)
#
def main(args):
    if args.mode == 'fit':
        main_fit()
    elif args.mode == 'cross-validate':
        main_cross_validate()
    elif args.mode == 'perdict':
        main_perdict()

def main_fit():
    caseversions = loadLocalCaseversions(trainLocalJson)
    vectorized_features, targets = prepare_training_data(caseversions)
    model = fit(vectorized_features, targets)


    #Drawing decision tree
    #sudo apt-get install graphviz
    #dot -Tpdf iris.dot -o iris.pdf
    #from sklearn.externals.six import StringIO
    with open("output/model.dot", 'w') as f:
        f = tree.export_graphviz(model, out_file=f)

    model_filename = "output/latest_model.pkl"
    with open(model_filename, 'w') as f:
        pickle.dump(model, f)

    logging.info("Model saved to " + model_filename)

def main_cross_validate():
    caseversions = loadLocalCaseversions(trainLocalJson)
    vectorized_features, targets = prepare_training_data(caseversions)
    model = fit(vectorized_features, targets)

    predicted = cross_validation.cross_val_predict(model, vectorized_features, targets, cv=3)
    print(metrics.accuracy_score(targets, predicted))
    print(metrics.classification_report(targets, predicted))

def main_perdict():
    # TODO: load existing model if provided
    caseversions = loadLocalCaseversions(trainLocalJson)
    vectorized_features, targets = prepare_training_data(caseversions)
    model = fit(vectorized_features, targets)


    #Drawing decision tree
    #sudo apt-get install graphviz
    #dot -Tpdf iris.dot -o iris.pdf
    #from sklearn.externals.six import StringIO
    with open("output/model.dot", 'w') as f:
        f = tree.export_graphviz(model, out_file=f)

    model_filename = "output/latest_model.pkl"
    with open(model_filename, 'w') as f:
        pickle.dump(model, f)
    logging.info("Model saved to " + model_filename)

    predictCaseversions = loadLocalCaseversions(perdictLocalJson)
    topranks = perdict(predictCaseversions, model) # This can be interrupted by Ctrl+C

    print("preparing data for saving to file")
    topranks['perdictions'] = topranks['perdictions'].tolist()
    print("saving to file")
    outputFilename = 'output/latest_output.json'
    with open(outputFilename , 'w') as f:
        json.dump(topranks, f, indent=2)
    print(outputFilename + " created")

    dups = zip(topranks['ids'], topranks['perdictions'])
    dups = filter(lambda x: x[1], dups)
    dups = map(lambda x: x[0], dups)

    print(output.printDups(dups))

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('mode', choices=['fit', 'cross-validate', 'perdict'],
                        help='The mode you want to learn')

    args = parser.parse_args()

    main(args)
