#!/bin/bash
INPUT=$1
OUTPUT=$2


dur=$(ffprobe -i footages/imagine.mp4 -v quiet -show_entries format=duration -hide_banner -of default=noprint_wrappers=1:nokey=1)
num=3
dur=${dur%.*}

one_por=$(( dur / num ))

start=$(( one_por * 2 ))

temp=$(( 10 / 3 ))

echo $temp
#echo $start_min

#ffmpeg -i $INPUT -vf select='eq(n\,1000)+eq(n\,1020)+eq(n\,1060)+eq(n\,1065)+eq(n\,1090)' -vsync 0 -f image2pipe -vcodec ppm - | convert -delay 15 -loop 1 -layers Optimize - $OUTPUT
ffmpeg -i $INPUT -ss $start -t $start.2 -vf select='not(mod(n\,10))' -vframes 200 -c:v pam -f image2pipe - | convert -delay 3 - -loop 0 -layers optimize temp1.gif
ffmpeg -i $INPUT -ss $one_por -t $one_por.2 -vf select='not(mod(n\,10))' -vframes 200 -c:v pam -f image2pipe - | convert -delay 3 - -loop 0 -layers optimize temp2.gif
convert temp1.gif temp2.gif $OUTPUT
rm temp1.gif
rm temp2.gif
