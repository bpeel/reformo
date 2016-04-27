#!/usr/bin/env python3

import sys
import re
import subprocess

FRAME_RATE = 30
MILLISECONDS_PER_FRAME = 1000 / FRAME_RATE

if sys.stdout.isatty():
    sys.stderr.write('stdout is a tty\n')
    sys.exit(1)

reg = re.compile(r'^([0-9]+) (.*)$')

videos = []

line_num = 1
for line in sys.stdin:
    line = line.rstrip()
    match = reg.match(line)
    if not match:
        sys.stderr.write('invalid line {}\n'.format(line_num))
        sys.exit(1)

    videos.append((int(match.group(1)), match.group(2)))

    line_num += 1

if len(videos) <= 0:
    sys.stderr.write('No videos\n')
    sys.exit(1)

videos[0] = (0, videos[0][1])

frame_num = 0

while True:
    video_num = 0
    frame_time = frame_num * MILLISECONDS_PER_FRAME
    for video_num in range(0, len(videos)):
        if videos[video_num][0] > frame_time:
            break
    else:
        break
    video_num -= 1

    res = subprocess.call(["convert", videos[video_num][1], "rgb:-"])
    if res != 0:
        sys.stderr.write('convert failed\n')
        sys.exit(1)

    frame_num += 1
