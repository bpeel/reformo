#!/bin/bash

set -xe

cd $(dirname "$0")

./generate-png.sh
./timedvideo.sh < timing.txt
ffmpeg -i presentation.webm -i reformo.flac -c:v copy -c:a libvorbis -aq 4 reformo.webm
