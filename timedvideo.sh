#!/bin/bash

set -e

IN_ARGS="-f rawvideo -pixel_format rgb24 -video_size 1920x1080 -framerate 30"
OUT_ARGS="-c:v libvpx -b:v 3M"

./timedvideo.py | ffmpeg $IN_ARGS -i - $OUT_ARGS presentation.webm
