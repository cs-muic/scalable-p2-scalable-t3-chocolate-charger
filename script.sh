#!/bin/bash
INPUT=$1
OUTPUT=$2


dur=$(ffprobe -i $INPUT -v quiet -show_entries format=duration -hide_banner -of default=noprint_wrappers=1:nokey=1)
num=3
dur=${dur%.*}

one_por=$(( dur / num ))

start=$(( one_por * 2 ))

width=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of default=nw=1:nk=1 $INPUT)
height=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of default=nw=1:nk=1 $INPUT)

default_width=480
default_height=360


ffmpeg -i $INPUT -ss $start -t $start.2 -vf "select='not(mod(n\,10))',scale='if(lt(iw,480),480)':'if(lt(ih,360),360)'" -vframes 200 -c:v pam -f image2pipe - | convert -delay 3 - -loop 0 -layers optimize temp1.gif
ffmpeg -i $INPUT -ss $one_por -t $one_por.2 -vf "select='not(mod(n\,10))',scale='if(lt(iw,480),480)':'if(lt(ih,360),360)'" -vframes 200 -c:v pam -f image2pipe - | convert -delay 3 - -loop 0 -layers optimize temp2.gif
convert temp1.gif temp2.gif $OUTPUT
rm temp1.gif
rm temp2.gif
