import filters
def drawGraph(topranks):
    import networkx as nx
    import sets
    import matplotlib.pyplot as plt
    uniqueNodes = sets.Set()
    for item in topranks:
        uniqueNodes.add(item["lhs_id"])
        uniqueNodes.add(item["rhs_id"])
    G=nx.Graph()

    G.add_nodes_from(uniqueNodes)
    for item in topranks:
        G.add_edge(item["lhs_id"], item["rhs_id"])

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

#TODO: we might not need the printOnOffPairs and printNotDup
#FIXME: inefficient loop
def printOnOffPairs(dups):
    for item in dups:
        if filters.isOnOffPairs(item['diff']):
            print("{0}\t is NOT a dup to\t {1}\t because {2}".format(
                    item["lhs_id"],
                    item["rhs_id"],
                    "They are a on/off pair"
                )),
            print("\thttp://shinglyu.github.io/moztrap-new-ui/diff.html?lhs={0}&rhs={1}".format(
                    item["lhs_id"],
                    item["rhs_id"]
                    #caseversions['objects'][item["lhs_id"]]['id'],
                    #caseversions['objects'][item["rhs_id"]]['id'])
                ))

def printNotDup(notdups, reason):
    for item in notdups:
        print("{0}\t is NOT a dup to\t {1}\t because {2}".format(
                item["lhs_id"],
                item["rhs_id"],
                reason
            )),
        print("\thttp://shinglyu.github.io/moztrap-new-ui/diff.html?lhs={0}&rhs={1}".format(
                item["lhs_id"],
                item["rhs_id"]
                #caseversions['objects'][item["lhs_id"]]['id'],
                #caseversions['objects'][item["rhs_id"]]['id'])
            ))


# TODO: printDups is the main output function for the excel file, rename and
# refactor this.
def printDups(dups):
    # TODO: add fields for user to tag answer and comments
    lines = []
    for item in dups:
        # print("{0}\t is similiar to\t {1}\t with score\t {2}".format(
        #         item["lhs_id"],
        #         item["rhs_id"],
        #         #caseversions['objects'][item["lhs_id"]]['id'],
        #         #caseversions['objects'][item["rhs_id"]]['id'],
        #         item["val"])
        #     ),
        line = ("{0}\t{1}".format(
                item["lhs_id"],
                item["rhs_id"]
            ))

        line += ("\thttp://shinglyu.github.io/moztrap-new-ui/diff.html?lhs={0}&rhs={1}".format(
                item["lhs_id"],
                item["rhs_id"]
                #caseversions['objects'][item["lhs_id"]]['id'],
                #caseversions['objects'][item["rhs_id"]]['id'])
            ))
        line += "\n"
        lines.append(line)
    print(lines)
    return lines
def formatResultCsv(results):
    dups = zip(results['ids'], results['perdictions'])
    # TODO: add fields for user to tag answer and comments
    lines = ["Dup?,Merge?,Reason,Merged in Moztrap?,Case ID 1,Case ID 2,Case 1 ,Case 2,Diff,CaseVersion ID 1,CaseVersion ID 2\n"]
    for item in dups:
        line = ""
        if item[1] == "dup":
            line += "Yes,No,"
        elif item[1] == "merge":
            line += "No,Yes,"
        else:
            line += "No,No,"

        line += ",,,,,,"
        # print("{0}\t is similiar to\t {1}\t with score\t {2}".format(
        #         item["lhs_id"],
        #         item["rhs_id"],
        #         #caseversions['objects'][item["lhs_id"]]['id'],
        #         #caseversions['objects'][item["rhs_id"]]['id'],
        #         item["val"])
        #     ),

        line += ("http://shinglyu.github.io/moztrap-new-ui/diff.html?lhs={0}&rhs={1},".format(
                item[0]["lhs_id"],
                item[0]["rhs_id"]
                #caseversions['objects'][item["lhs_id"]]['id'],
                #caseversions['objects'][item["rhs_id"]]['id'])
            ))
        line += ("{0},{1}".format(
                item[0]["lhs_id"],
                item[0]["rhs_id"]
            ))
        line += "\n"
        lines.append(line)
    return lines
