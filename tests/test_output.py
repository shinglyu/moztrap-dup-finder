import os, sys
sys.path.append(os.path.abspath('.')) #if run in root
sys.path.append(os.path.abspath('..')) #if run in tests/

import output

def test_formatResultCsv():
    inputResult = {
        "perdictions": [
            "merge",
            "dup",
            "none",
        ],
        "ids": [
            {
                "lhs_id": 210204,
                "rhs_id": 210202
            },
            {
                "lhs_id": 210205,
                "rhs_id": 210202
            },
            {
                "lhs_id": 210204,
                "rhs_id": 210208
            },
        ]
    }


    expected = [
        "Dup?,Merge?,Reason,Merged in Moztrap?,Case ID 1,Case ID 2,Case 1 ,Case 2,Diff,CaseVersion ID 1,CaseVersion ID 2\n",
        "No,Yes,,,,,,,http://shinglyu.github.io/moztrap-new-ui/diff.html?lhs=210204&rhs=210202,210204,210202\n",
        "Yes,No,,,,,,,http://shinglyu.github.io/moztrap-new-ui/diff.html?lhs=210205&rhs=210202,210205,210202\n",
        "No,No,,,,,,,http://shinglyu.github.io/moztrap-new-ui/diff.html?lhs=210204&rhs=210208,210204,210208\n"
    ]
    #expected = [
    #"Dup?,Merge?,Reason,Merged in Moztrap?,Case ID 1,Case ID 2,Case 1 ,Case 2,Diff,CaseVersion ID 1,CaseVersion ID 2",
    #"No,Yes,,,706,707,https://moztrap.mozilla.org/manage/cases/?filter-id=706,https://moztrap.mozilla.org/manage/cases/?filter-id=707,http://shinglyu.github.io/moztrap-new-ui/diff.html?lhs=210201&rhs=210202,210204,210202",
    #"Yes,No,,,706,1696,https://moztrap.mozilla.org/manage/cases/?filter-id=706,https://moztrap.mozilla.org/manage/cases/?filter-id=1696,http://shinglyu.github.io/moztrap-new-ui/diff.html?lhs=210201&rhs=210521,210205,210202"
    #"No,No,,,706,1696,https://moztrap.mozilla.org/manage/cases/?filter-id=706,https://moztrap.mozilla.org/manage/cases/?filter-id=1696,http://shinglyu.github.io/moztrap-new-ui/diff.html?lhs=210201&rhs=210521,210204,210208"
    #]
    assert(expected == output.formatResultCsv(inputResult))

def test_formatResultCsv():
    expected = {
        "perdictions": [
            "merge",
            "dup",
            "none",
        ],
        "ids": [
            {
                "lhs_id": '210204',
                "rhs_id": '210202'
            },
            {
                "lhs_id": '210205',
                "rhs_id": '210202'
            },
            {
                "lhs_id": '210204',
                "rhs_id": '210208'
            },
        ]
    }


    inputCsv = [
        ["Dup?","Merge?","Reason","Merged in Moztrap?","Case ID 1","Case ID 2","Case 1 ","Case 2","Diff","CaseVersion ID 1","CaseVersion ID 2"],
        ["No","Yes","","","","","","","http://shinglyu.github.io/moztrap-new-ui/diff.html?lhs=210204&rhs=210202","210204","210202"],
        ["Yes","No","","","","","","","http://shinglyu.github.io/moztrap-new-ui/diff.html?lhs=210205&rhs=210202","210205","210202"],
        ["No","No","","","","","","","http://shinglyu.github.io/moztrap-new-ui/diff.html?lhs=210204&rhs=210208","210204","210208"],
    ]
    #expected = [
    #"Dup?,Merge?,Reason,Merged in Moztrap?,Case ID 1,Case ID 2,Case 1 ,Case 2,Diff,CaseVersion ID 1,CaseVersion ID 2",
    #"No,Yes,,,706,707,https://moztrap.mozilla.org/manage/cases/?filter-id=706,https://moztrap.mozilla.org/manage/cases/?filter-id=707,http://shinglyu.github.io/moztrap-new-ui/diff.html?lhs=210201&rhs=210202,210204,210202",
    #"Yes,No,,,706,1696,https://moztrap.mozilla.org/manage/cases/?filter-id=706,https://moztrap.mozilla.org/manage/cases/?filter-id=1696,http://shinglyu.github.io/moztrap-new-ui/diff.html?lhs=210201&rhs=210521,210205,210202"
    #"No,No,,,706,1696,https://moztrap.mozilla.org/manage/cases/?filter-id=706,https://moztrap.mozilla.org/manage/cases/?filter-id=1696,http://shinglyu.github.io/moztrap-new-ui/diff.html?lhs=210201&rhs=210521,210204,210208"
    #]
    assert(expected == output.parseResultCsv(inputCsv))


