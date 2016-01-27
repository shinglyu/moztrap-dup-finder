import os, sys
sys.path.append(os.path.abspath('.')) #if run in root
sys.path.append(os.path.abspath('..')) #if run in tests/

import filters
import finddup


def test_calcDiffs():
    cvs = finddup.loadLocalCaseversions('tests/data/small_274_0.json')
    selected_pairs = finddup.genAllCombinations(cvs)[0:1]
    diffs = filters.calcDiffs(cvs, selected_pairs)
    assert(len(selected_pairs) == len(diffs))
    assert(type(diffs[0]) == type([]))
    assert(type(diffs[0][0]) == type(""))
