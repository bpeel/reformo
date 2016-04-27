#!/bin/bash

set -e

svg_file="$1"

if test -z "$svg_file"; then
    echo "usage: extract-images.sh <svg_file>" >&2
    exit 1;
fi

layers=(`inkscape --query-all "$svg_file" | \
sed -n 's/^\(layer[0-9]\+\),.*/\1/p'`)

num=0

for layer in "${layers[@]}"; do
    png=`printf "layer-%04i.png" $num`

    inkscape --export-id-only --export-area-page --export-id="$layer" \
        --export-png="$png" "$svg_file"

    num=$((num+1))
done

cp layer-0000.png slide-0000.png

for ((i=0; i<${#layers[@]}; i++)); do
    dst=`printf "slide-%04i.png" $i`
    layer=`printf "layer-%04i.png" $i`

    if test $i -eq 0; then
        cp "$layer" "$dst"
    else
        prev=`printf "slide-%04i.png" $((i-1))`
        convert "$prev" "$layer" -compose over -composite "$dst"
    fi

    rm "$layer"
done
