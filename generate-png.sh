#!/bin/bash

set -xe

num=0
mkdir -p slides-png

for x in slides/*.svg; do
    rm -f slide-????.png
    ./extract-images.sh "$x"
    for y in slide-????.png; do
        mv "$y" slides-png/slide-$(printf %04i $num).png
        ((num++)) || true
    done
done
