# moztrap-dup-finder
Finding duplicated test cases in MozTrap https://moztrap.mozilla.org

#Installation 

Run `install.sh` (for Ubuntu)

# Usage

Run `python finddup.py`, a list of potential duplications will be printed to `stdout`, also a network graph will be created.

# Tips

If you don't want to call the MozTrap API everytime, use `wget`/`curl` to download the this url: https://moztrap.mozilla.org/api/v1/caseversion/?format=json&productversion=217 as json file. And set the `localJson` variable to its filename. Then change `downloadCasevesions()` call to `loadLocalCaseversion(localJson)`.

# TODO
* Define what is a duplication
* Create manully marked groundtruth data
* Tune the features and parameters
* Prettify the network graph

# Contribute
Open a pull request for review. Or submit ideas to `slyu@mozilla.org`
