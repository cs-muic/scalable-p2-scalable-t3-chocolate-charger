#!/bin/bash
INPUT=$1
OUTPUT=$2

ffmpeg -i $INPUT -vf select='eq(n\,100)+eq(n\,184)+eq(n\,213)' -vsync 0 -f image2pipe -vcodec ppm - | convert -delay 15 -loop 1 -layers Optimize - $OUTPUT