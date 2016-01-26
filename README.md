# moztrap-dup-finder
Finding duplicated test cases in MozTrap https://moztrap.mozilla.org

#Installation 

Run `install.sh` (for Ubuntu)

# Usage
##Updated:##
Read `tests/test_smoke.sh` for usage

* Download test cases from Moztrap using `download_sample.sh`
* Manually mark the duplications as in `input/ground-truth-217.csv`
* Edit the `config.py` to add your new training data and perdict data files
* Run `python finddup.py fit` to generate a model (only use `trainLocalJson`)
* Run `python finddup.py cross-val` to do cross validation on feature and model parameters (only use `trainLocalJson`)
* Run `python finddup.py perdict` to create a model using `trainLocalJson` + `groundtruth_filename` and use that model to make perdictions on `perdictLocalJson`.
* If you need case ID and links, run `add_case_id_to_output.py`, remember to modify the output file path in the script.

# Tips

If you don't want to call the MozTrap API everytime, use `wget`/`curl` to download the this url: https://moztrap.mozilla.org/api/v1/caseversion/?format=json&productversion=217 as json file. And set the `localJson` variable to its filename. Then change `downloadCasevesions()` call to `loadLocalCaseversion(localJson)`.

# TODO
* Define what is a duplication
* Create manully marked groundtruth data
* Tune the features and parameters
* Prettify the network graph

# Contribute
Open a pull request for review. Or submit ideas to `slyu@mozilla.org`
