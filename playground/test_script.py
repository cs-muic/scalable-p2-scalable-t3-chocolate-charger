import ffmpy
ff = ffmpy.FFmpeg(
	inputs = {"cash.mp4" : None},
	outputs = {"cash.gif" : None})
 
ff.run