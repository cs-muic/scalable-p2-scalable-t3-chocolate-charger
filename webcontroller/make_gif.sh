#!/bin/bash
INPUT=$1
OUTPUT=$2

convert -delay 20 -loop 0 $INPUT/*.jpeg $OUTPUT
