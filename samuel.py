import board
import digitalio
import neopixel
import time
from random import *

pixels = neopixel.NeoPixel(board.D18, 64)
#pixels = neopixel.NeoPixel(board.D18, 64, bpp=3, brightness=1.2, auto_write=False, pixel_order=neopixel.RGB)

#pixels[0] = (255,0,0)
#pixels[1] = (0,255,0)
#pixels[2] = (0,0,255)

for index in range(0):
	#pixels[index] = (index,index,index)
	pixels[index] = (255,0,0)
	#pixels.fill( (randint(0,255),randint(0,255),randint(0,255)) )
	if (((index+1) % 8) == 0):
		pixels.show()
		time.sleep(1)
	
print(time.time())
for i in range(0):
	pixels.fill( (randint(0,255),randint(0,255),randint(0,255)) )
print(time.time())

pixels.fill( (0,40,0) )
