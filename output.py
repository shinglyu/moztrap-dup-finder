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
    return lines
def formatResultCsv(results):
    dups = zip(results['ids'], results['perdictions'])
    # TODO: add fields for user to tag answer and comments
    lines = ["Dup?,Merge?,Reason,Merged in Moztrap?,Case ID 1,Case ID 2,Case 1 ,Case 2,Diff,CaseVersion ID 1,CaseVersion ID 2\n"]
    for item in dups:
        dup_or_merge = ""
        if item[1] == "dup":
            dup_or_merge = "Yes,No"
        elif item[1] == "merge":
            dup_or_merge = "No,Yes"
        else:
            dup_or_merge = "No,No"

        diff_link = ("http://shinglyu.github.io/moztrap-new-ui/diff.html?lhs={0}&rhs={1}".format(
                item[0]["lhs_id"],
                item[0]["rhs_id"]
            ))
        line = "{dup_or_merge},{reason},{merged},{cid_lhs},{cid_rhs},{cid_rhs_link},{cid_lhs_link},{diff_link},{cvid_lhs},{cvid_rhs}\n".format(
            dup_or_merge = dup_or_merge,
            reason = "",
            merged = "",
            cid_lhs = "", #TODO
            cid_rhs = "", #TODO
            cid_rhs_link = "", #TODO
            cid_lhs_link = "", #TODO
            diff_link = diff_link,
            cvid_lhs = item[0]["lhs_id"],
            cvid_rhs = item[0]["rhs_id"],
        )
        lines.append(line)
    return lines
def parseResultCsv(lines):
    ids = []
    targets = [] # answers
    for row in lines: # has title row
        if row[0] == "Dup?":
            continue # title row
        if len(row[0]) > 0  and (row[0][0] == "Y" or row[0][0] == "y"):
            target = "dup"
        elif len(row[1]) > 0  and (row[1][0] == "Y" or row[1][0] == "y"):
            target = "merge"
        else:
            target = "none"

        case1   = row[9]
        case2   = row[10]
        # pdb.set_trace()
        ids.append({
            "lhs_id": case1,
            "rhs_id": case2,
        })
        targets.append(target) #TODO: change to X/Dup/Merge tags

    return {'ids': ids, 'perdictions': targets}
