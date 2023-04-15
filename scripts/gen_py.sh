#! /bin/bash

jupyter nbconvert ../ipynb/*.ipynb --to python
mv ../ipynb/*.py ./
