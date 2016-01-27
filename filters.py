import json
import difflib

# TODO: make tfidf a filter too
def calcDiffs(cvs, selected_pairs):
    print(selected_pairs)
    cv_texts = { str(x['id']): json.dumps(x) for x in cvs['objects'] }#map(lambda x:{x['id']: json.dumps(x)}, cvs['objects'])
    print(map(lambda x:x['id'], cvs['objects']))
    #from pprint import pprint
    #pprint(cv_texts)
    def calcPairwiseDiff(pair):
        txt1 = cv_texts[pair['lhs_id']]
        txt2 = cv_texts[pair['rhs_id']]
        return calcDiff(txt1, txt2)
    return map(calcPairwiseDiff, selected_pairs)

def calcDiff(lhs_text, rhs_text):
    lhs = lhs_text.split(' ')
    rhs = rhs_text.split(' ')
    d = difflib.Differ()
    diff = list(d.compare(lhs, rhs))
    #print(json.dumps(diff, indent=2))
    #diffwords = [i[2:] if i[:1] == '+' else None for i in diff if not i[:1] in '-?']
    diffwords = [i[2:] if (i[:1] == '+' or i[:1] == "-") else None for i in diff if not i[:1] in '?']
    diffwords = filter(lambda x: x != None, diffwords)
    noisewords = [",", "\"", "\'", "}", "{", ")", "("]
    for word in noisewords:
        diffwords = map(lambda x: x.strip(word).lower(), diffwords)
    #print(json.dumps(diffwords, indent=2))
    #print(diffwords)
    #print(isOnOffPairs(diffwords))
    return diffwords

def isOnOffPairs(diff):
    keywords = [
        ("on", "off"),
        ("correct", "incorrect"),
        ("enable", "disable"),
        ("correct", "wrong"),
    ]
    for keyword in keywords:
        if keyword[0].lower() in diff and keyword[1].lower() in diff:
            return True
    return False

def isDifferentModule(diff):
    keywords = [
        ("wifi", "bluetooth"),
    ]
    for keyword in keywords:
        if keyword[0].lower() in diff and keyword[1].lower() in diff:
            return True
    return False

#def getTopN(n, dups):
    #return dups[:n]

