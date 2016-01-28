import os, sys
sys.path.append(os.path.abspath('.')) #if run in root
sys.path.append(os.path.abspath('..')) #if run in tests/

import finddup
#def test_loadLocalCaseversion():
    #finddup.loadLocalCaseversions('tests/data/full_217.json', 'tests/data/full_217_groundtruth.csv')

def test_loadGroundTruth():
    groundtruth = finddup.loadGroundTruth('tests/data/groundtruth-274.csv')
    expected = {
        "perdictions": [
            "merge",
            "dup",
            "none"
        ],
        "ids": [
            {
                "lhs_id": "210201",
                "rhs_id": "210202"
            },
            {
                "lhs_id": "210201",
                "rhs_id": "210521"
            },
            {
                "lhs_id": "210201",
                "rhs_id": "211079"
            }
        ]
    }

    assert(groundtruth == expected)

def test_loadGroundTruth_empty():
    groundtruth = finddup.loadGroundTruth('tests/data/groundtruth-274-empty.csv')
    expected = {
        "perdictions": [
            "none"
        ],
        "ids": [
            {
                "lhs_id": "210201",
                "rhs_id": "210202"
            },
        ]
    }

    assert(groundtruth == expected)

def test_loadGroundTruth_filter_by_csv():
    cvs = finddup.loadLocalCaseversions('tests/data/small_274_0_key_error.json')
    groundtruth = finddup.loadGroundTruth('tests/data/groundtruth-274.csv', cvs['objects'])
    expected = {
        "perdictions": [
            "merge",
            "none"
        ],
        "ids": [
            {
                "lhs_id": "210201",
                "rhs_id": "210202"
            }, # 210521 does not exist in csv
            {
                "lhs_id": "210201",
                "rhs_id": "211079"
            }
        ]
    }

    assert(groundtruth == expected)

def test_extractFeatures_select():
    cvs = finddup.loadLocalCaseversions('tests/data/small_274_0.json')
    gt = finddup.loadGroundTruth('tests/data/groundtruth-274.csv')
    features = finddup.extractFeatures(cvs, gt['ids'])

    assert(features.shape[0] == len(gt['perdictions']))
    #TODO: test feature #
    #assert(targets == gt['perdictions'])

def test_extractFeatures_keyerror():
    # Test when some groundtruth are not in the local caseversion file
    cvs = finddup.loadLocalCaseversions('tests/data/small_274_0_key_error.json')
    gt = finddup.loadGroundTruth('tests/data/groundtruth-274.csv', cvs['objects'])
    features = finddup.extractFeatures(cvs, gt['ids'])

    assert(features.shape[0] == len(gt['perdictions']))
    #TODO: test feature #
    #assert(targets == gt['perdictions'])

def test_extractFeatures_default():
    cvs = finddup.loadLocalCaseversions('tests/data/small_274_0.json')
    #gt = finddup.loadGroundTruth('tests/data/groundtruth-274.csv')
    comb = [x for x in finddup.genAllCombinations(cvs)] #FIXME: remove this dependency
    features = finddup.extractFeatures(cvs, comb)

    print(len(cvs['objects']))
    pairs_count = len(cvs['objects']) * (len(cvs['objects']) - 1) / 2
    assert(features.shape[0] == pairs_count)
    #TODO: test feature #
    #assert(targets == gt['perdictions'])

def test_genAllCombinations():
    caseversions = {
        "objects":[
            {
                'id': 12345
            },
            {
                'id': 12346
            },
            {
                'id': 12347
            }
        ]
    }
    expected = [
        {
            'lhs_id': '12345',
            'rhs_id': '12346',
        },
        {
            'lhs_id': '12345',
            'rhs_id': '12347',
        },
        {
            'lhs_id': '12346',
            'rhs_id': '12347',
        }
    ]
    comb_it = finddup.genAllCombinations(caseversions)
    combinations = [next(comb_it) for i in range(3)]
    #gt = finddup.loadGroundTruth('tests/data/groundtruth-274.csv')
    assert(expected == combinations)
    #TODO: test feature #
    #assert(targets == gt['perdictions'])

def test_getCombinationSlice():
    caseversions = {
        "objects":[
            {
                'id': 12345
            },
            {
                'id': 12346
            },
            {
                'id': 12347
            },
            {
                'id': 12348
            }
        ]
    }
    comb_it = finddup.genAllCombinations(caseversions)

    count = 0
    for s in finddup.getCombinationSlice(3, comb_it):
        assert(3 == len(s))
        count += 1
    assert(2 == count)

def test_getCombinationSlice_step():
    caseversions = {
        "objects":[
            {
                'id': 12345
            },
            {
                'id': 12346
            },
            {
                'id': 12347
            },
            {
                'id': 12348
            },
            {
                'id': 12349
            }
        ]
    }
    comb_it = finddup.genAllCombinations(caseversions)

    count = 0
    for s in finddup.getCombinationSlice(3, comb_it, step=3):
        count += 1
        if (count == 2):
            assert(1 == len(s))
        else:
            assert(3 == len(s))
        print(s)
    assert(2 == count)
def test_loadGroundTruth():
    groundtruth = finddup.loadGroundTruth('tests/data/groundtruth-274.csv')
    expected = {
        "perdictions": [
            "merge",
            "dup",
            "none"
        ],
        "ids": [
            {
                "lhs_id": "210201",
                "rhs_id": "210202"
            },
            {
                "lhs_id": "210201",
                "rhs_id": "210521"
            },
            {
                "lhs_id": "210201",
                "rhs_id": "211079"
            }
        ]
    }

    assert(groundtruth == expected)

def test_transformTargetLabels():
    inputLabels = [
            "merge",
            "dup",
            "none"
        ]
    inputLabelClasses = [
            "merge",
            "dup",
            "none"
        ]
    expectedNums = [1,0,2]
    expectedClasses = ["dup", "merge", "none"]
    transformed_label, classes = finddup.transformTargetLabels(inputLabels, inputLabelClasses)

    print(transformed_label)
    print(classes)
    for i in range(len(expectedNums)):
        assert(expectedNums[i] == transformed_label[i])
    for i in range(len(expectedClasses)):
        assert(expectedClasses[i] == classes[i])
