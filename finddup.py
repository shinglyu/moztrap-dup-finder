from sklearn.feature_extraction.text import TfidfVectorizer
import urllib2
import json
import numpy as np

import output
import filters

mtorigin = "https://moztrap.mozilla.org"
# Total 10135
# limit = 10135
limit = 100 # for small scale testing
# limit = 5 # for small scale testing
# topCount = 5
# topCount = limit/2
# topCount = 500
#topCount = 500
topCount = 100
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

caseversion_texts = map(lambda x: json.dumps(x), caseversions['objects'])

vect = TfidfVectorizer(min_df=1)
tfidf = vect.fit_transform(caseversion_texts)
pairwise_similarity = tfidf * tfidf.T
#print pairwise_similarity.A

#sorting
reindex = np.argsort(-pairwise_similarity.A.flatten())
r, c = divmod(reindex, pairwise_similarity.shape[1])

topranks = []
#counter = 0
#while len(topranks) < topCount:
#    if r[counter] < c[counter]:
#        topranks.append({
#            "r": caseversions['objects'][r[counter]]['id'],
#            "c": caseversions['objects'][c[counter]]['id'],
#            "val": pairwise_similarity[r[counter], c[counter]],
#            "diff": filters.calcDiff(r[counter], c[counter], caseversions)
#        })
#    counter += 1

#allPairs = zip(r,c)
dups = filter(lambda (ri,ci): ri < ci, zip(r,c))

dups = dups[:topCount] # Only get the top

for ri, ci in dups:
    if ri < ci:
        topranks.append({
            "r": caseversions['objects'][ri]['id'], #FIXME: rename to rhs/lhs
            "c": caseversions['objects'][ci]['id'],
            "val": pairwise_similarity[ri, ci],
            "diff": filters.calcDiff(ri, ci, caseversions)
        })

#topranks = filters.getTopN(topCount, topranks)

output.printOnOffPairs(topranks)

topranks = filter(lambda x: not filters.isOnOffPairs(x['diff']), topranks)

output.printDups(topranks)

output.drawGraph(topranks)
