from sklearn.feature_extraction.text import TfidfVectorizer
import urllib2
import json
import numpy as np

mtorigin = "https://moztrap.mozilla.org"
# Total 10135
# limit = 10135
limit = 100 # for small scale testing
# topCount = 5
topCount = limit/2
# topCount = 500
productversion=217 #Firefox OS v.22.
#https://moztrap.mozilla.org/api/v1/caseversion/?format=json&productversion=217
#localJson="./mid_217.json"
localJson="./full_217.json"


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

# main
caseversions = downloadCaseversions()
#caseversions = loadLocalCaseversions(localJson)
#print json.dumps(caseversions['objects'][0])

caseversion_texts = map(lambda x: json.dumps(x), caseversions['objects'])

vect = TfidfVectorizer(min_df=1)
tfidf = vect.fit_transform(caseversion_texts)
#tfidf = vect.fit_transform(["I'd like an apple",
                            #"I'd like an apples",
                            #"An apple a day keeps the doctor away",
                            #"Never compare an apple to an orange",
                            #"I prefer scikit-learn to Orange"])
#documents = [open(f) for f in text_files]
#tfidf = TfidfVectorizer().fit_transform(documents)
# no need to normalize, since Vectorizer will return normalized tf-idf
pairwise_similarity = tfidf * tfidf.T
#print pairwise_similarity.A

#sorting
reindex = np.argsort(-pairwise_similarity.A.flatten())
r, c = divmod(reindex, pairwise_similarity.shape[1])

topranks = []
counter = 0
while len(topranks) < topCount:
    if r[counter] < c[counter]:
        topransk = topranks.append({
            "r": caseversions['objects'][r[counter]]['id'],
            "c": caseversions['objects'][c[counter]]['id'],
            "val": pairwise_similarity[r[counter], c[counter]]
        })
    counter += 1

#print str(r[i]) + "," + str(c[i]) + " " + str(pairwise_similarity[r[i], c[i]])

for item in topranks:
    print("{0}\t is similiar to {1}\t with socre {2}".format(
            item['r'],
            item['c'],
            #caseversions['objects'][item['r']]['id'],
            #caseversions['objects'][item['c']]['id'],
            item["val"])
         ),
    print("\thttp://shinglyu.github.io/moztrap-new-ui/diff.html?lhs={0}&rhs={1}".format(
            item['r'],
            item['c']
            #caseversions['objects'][item['r']]['id'],
            #caseversions['objects'][item['c']]['id'])
         ))

#similar_pairs =
def drawGraph(topranks):
    import networkx as nx
    import sets
    import matplotlib.pyplot as plt
    uniqueNodes = sets.Set()
    for item in topranks:
        uniqueNodes.add(item["r"])
        uniqueNodes.add(item["c"])
    G=nx.Graph()

    G.add_nodes_from(uniqueNodes)
    for item in topranks:
        G.add_edge(item["r"], item["c"])

    #https://networkx.github.io/documentation/latest/examples/drawing/labels_and_colors.html
    #pos = nx.spring_layout(G)
    pos = nx.circular_layout(G)
    #pos = nx.random_layout(G)
    #pos = nx.spectral_layout(G)
    #pos = nx.shell_layout(G)
    nx.draw_networkx_labels(G, pos)
    nx.draw(G,pos)
    plt.axis('off')
    plt.savefig("similarity.png") # save as png
    plt.show()


drawGraph(topranks)
