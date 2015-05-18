import filters
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
    #plt.show()

#FIXME: inefficient loop
def printOnOffPairs(dups):
    for item in dups:
        if filters.isOnOffPairs(item['diff']):
            print("{0}\t is NOT a dup to\t {1}\t because {2}".format(
                    item['r'],
                    item['c'],
                    "They are a on/off pair"
                )),
            print("\thttp://shinglyu.github.io/moztrap-new-ui/diff.html?lhs={0}&rhs={1}".format(
                    item['r'],
                    item['c']
                    #caseversions['objects'][item['r']]['id'],
                    #caseversions['objects'][item['c']]['id'])
                ))

def printDups(dups):
    for item in dups:
        print("{0}\t is similiar to\t {1}\t with score\t {2}".format(
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
