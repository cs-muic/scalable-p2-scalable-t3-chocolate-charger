import sys
import ffmpy

inp = str(sys.argv[1])
target = str(sys.argv[2])

print(type(inp))

ff = ffmpy.FFmpeg(
	inputs = {inp: None},
	outputs = {target : None})
 
ff.run()