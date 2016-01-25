read -r -p "Are you sure about installing of gfortran, libblas-dev, liblapack-dev, numpy, scipy, scikit-learn,  and networkx? [y/N] " response
if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]
then
  sudo apt-get install gfortran libblas-dev liblapack-dev
  sudo pip install numpy scipy scikit-learn networkx
else
  echo "Thank you for trying moztrap-dup-finder. We will stop this installation right away."
  exit 1
fi
