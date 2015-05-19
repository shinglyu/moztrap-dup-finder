from sklearn.feature_extraction.text import TfidfVectorizer
import urllib2
import json
import numpy as np

import output
import filters

mtorigin = "https://moztrap.mozilla.org"
# Total 10135
limit = 10135
#limit = 100 # for small scale testing
# limit = 5 # for small scale testing
# topCount = 5
# topCount = limit/2
# topCount = 500
topCount = 500
#topCount = 100
productversion=217 #Firefox OS v.22.
#https://moztrap.mozilla.org/api/v1/caseversion/?format=json&productversion=217
#localJson="./mid_217.json"
localJson="./input/full_217.json"


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


#caseversions = downloadCaseversions()
caseversions = loadLocalCaseversions(localJson)
#print json.dumps(caseversions['objects'][0])

def finddup(caseversions):

    caseversion_texts = map(lambda x: json.dumps(x), caseversions['objects'])

    vect = TfidfVectorizer(min_df=1)
    tfidf = vect.fit_transform(caseversion_texts)
    pairwise_similarity = tfidf * tfidf.T
#print pairwise_similarity.A

#sorting
    reindex = np.argsort(-pairwise_similarity.A.flatten())
    r, c = divmod(reindex, pairwise_similarity.shape[1])

    topranks = []
#    counter = 0
#    while len(topranks) < topCount:
#        if r[counter] < c[counter]:
#            topranks.append({
#                "r": r[counter],
#                "c": c[counter],
#                "lhs_id": caseversions['objects'][r[counter]]['id'],
#                "rhs_id": caseversions['objects'][c[counter]]['id'],
#                "val": pairwise_similarity[r[counter], c[counter]],
#            "diff": filters.calcDiff(r[counter], c[counter], caseversions)
#            })
#        counter += 1
#
#allPairs = zip(r,c)
    dups = filter(lambda (ri,ci): ri < ci, zip(r,c))

    for ri, ci in dups:
        if ri < ci:
            topranks.append({
                "r": ri,
                "c": ci,
                "lhs_id": caseversions['objects'][ri]['id'], #FIXME: rename to rhs/lhs
                "rhs_id": caseversions['objects'][ci]['id'],
                "val": pairwise_similarity[ri, ci],
                "are_dup" : False,
                "reason" : ""
                #"diff": filters.calcDiff(ri, ci, caseversions)
            })

    for i in range(0, topCount):
        item = topranks[i]
        item['are_dup']=True
        item['diff'] = filters.calcDiff(item['r'], item['c'], caseversions)

        if filters.isOnOffPairs(item['diff']):
            topranks[i]['are_dup']= False
            topranks[i]['reason']= "onoff"

        if filters.isDifferentModule(item['diff']):
            topranks[i]['are_dup']= False
            topranks[i]['reason']= "diffmodule"
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
    return topranks

#onoffs = filter(lambda x: filters.isOnOffPairs(x['diff']), topranks)
#output.printNotDup(onoffs, "is an on/off pair")
#
#diffModules = filter(lambda x: filters.isDifferentModule(x['diff']), topranks)
#output.printNotDup(diffModules, "belong to different module")
#
#topranks = filter(lambda x: not filters.isOnOffPairs(x['diff']), topranks)
#topranks = filter(lambda x: not filters.isDifferentModule(x['diff']), topranks)

topranks = finddup(caseversions)

realdups = filter(lambda x: x['are_dup'], topranks)

output.printDups(realdups)

onoffs = filter(lambda x: not x['are_dup'] and x['reason'] == "onoff", topranks)
output.printNotDup(onoffs, "is an on/off pair")

diffModules = filter(lambda x: not x['are_dup'] and x['reason'] == "diffmodule", topranks)
output.printNotDup(diffModules, "belong to different module")

output.drawGraph(realdups)
