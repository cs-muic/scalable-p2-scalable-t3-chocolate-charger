import sys
import ffmpeg
from wand.image import Image
import numpy as np

inp = str(sys.argv[1])
target = str(sys.argv[2])

ff, err = ffmpeg.input(inp).filter('fps', fps=5, round='up').output('pipe:', format='gif', pix_fmt='rgb24').run()

frames = np.frombuffer(ff, np.uint8)
for i in ff:
	print(i)
