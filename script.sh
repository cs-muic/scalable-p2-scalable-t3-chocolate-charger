#!/bin/bash
INPUT=$1
OUTPUT=$2

<<<<<<< HEAD
ffmpeg -i $INPUT -vf select='eq(n\,100)+eq(n\,184)+eq(n\,213)' -vsync 0 -f image2pipe -vcodec ppm - | convert -delay 15 -loop 1 -layers Optimize - $OUTPUT
=======

dur=$(ffprobe -i footages/imagine.mp4 -v quiet -show_entries format=duration -hide_banner -of default=noprint_wrappers=1:nokey=1)
num=3
dur=${dur%.*}

one_por=$(( dur / num ))

start=$(( one_por * 2 ))


#echo $start_min

#ffmpeg -i $INPUT -vf select='eq(n\,1000)+eq(n\,1020)+eq(n\,1060)+eq(n\,1065)+eq(n\,1090)' -vsync 0 -f image2pipe -vcodec ppm - | convert -delay 15 -loop 1 -layers Optimize - $OUTPUT
ffmpeg -i $INPUT -ss $start -t $start.2 -vf select='not(mod(n\,10))' -vframes 300 -c:v pam -f image2pipe - | convert -delay 3 - -loop 0 -layers optimize $OUTPUT
>>>>>>> c19528bf1eadda397ab9bc29423c66b54e8ba567
