if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <productversion id> <number of test cases>"
  echo "    <productversion id>     id of product version"
  echo "    <number of test cases>  number of test cases you want to download, default = 20"
  exit 1
fi

OUTPUT_FILE="input/full_$1.json"



wget "https://moztrap.mozilla.org/api/v1/caseversion/?format=json&productversion=$1&limit=$2" -O $OUTPUT_FILE

echo "$OUTPUT_FILE downloaded"




