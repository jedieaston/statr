#!/usr/bin/env bash

# Build script!
rm -r dist statr.pyz

pip install -r requirements.txt --target dist/
pip install shiv

cp -r statr dist

shiv --site-packages dist --compressed -p '/usr/bin/env python3' -o statr.pyz -e statr:main:cli