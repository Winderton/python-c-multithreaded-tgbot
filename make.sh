# !/bin/bash

[! -e "nogil.c" ] || rm "nogil.c"
find . -name "*.so" -type f -delete

python3 setup.py build_ext -b build

mv bot/*.c bot/lowlevel/