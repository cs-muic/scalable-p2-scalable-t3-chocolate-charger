import ffmpy
import sys

inp = str(sys.argv[1])
target = str(sys.argv[2])

ff = ffmpy.FFmpeg(
	inputs = {inp: None},
	outputs = {sys : None})
 
ff.run