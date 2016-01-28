import os, sys
sys.path.append(os.path.abspath('.')) #if run in root
sys.path.append(os.path.abspath('..')) #if run in tests/

import filters
import finddup


def test_calcDiffs():
    cvs = finddup.loadLocalCaseversions('tests/data/small_274_0.json')
    comb_it = finddup.genAllCombinations(cvs)
    selected_pairs = [next(comb_it) for i in range(2)]
    diffs = filters.calcDiffs(cvs, selected_pairs)
    assert(len(selected_pairs) == len(diffs))
    assert(type(diffs[0]) == type([]))
    assert(type(diffs[0][0]) == type(""))

def test_calcSimilarity():
    cvs = finddup.loadLocalCaseversions('tests/data/small_274_0.json')
    comb_it = finddup.genAllCombinations(cvs)
    selected_pairs = [next(comb_it) for i in range(2)]
    diffs = filters.calcSimilarity(cvs, selected_pairs)
    assert(len(selected_pairs) == len(diffs))
    #assert(type(diffs[0]) == type([]))
    #assert(type(diffs[0][0]) == type(""))
