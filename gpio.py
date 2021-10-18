import board
import digitalio
import neopixel
import time
from random import *

led = digitalio.DigitalInOut(board.D23)
led.direction = digitalio.Direction.OUTPUT

pixels = neopixel.NeoPixel(board.D18, 64)

farben = [
	(0,0,0),		# 0: off
	(255,200,0),	# 1: gelb
	(255,120,0), 	# 2: orange
	(180,0,0),		# 3: rot
	(80,0,80),		# 4: violett
	(20,20,80),		# 5: blau
	(80,80,160),	# 6: hellblau
	(180,120,255), 	# 7: stahlblau
	(30,255,10),	# 8: hellgrün
	(0,40,0) ]		# 9: dunkelgrün

def on(pixels, index, color):
	pixels[index] = color

def off(pixels, index):
	pixels[index] = 0,0,0

def colorstep(start, end, step, steps):
	print(steps, step)
	
	start_r = start[0]
	start_g = start[1]
	start_b = start[2]
	
	print(start_r, start_g, start_b)
	
	end_r = end[0]
	end_g = end[1]
	end_b = end[2]
	
	print(end_r, end_g, end_b)
	
	step_r = int((end_r - start_r) / steps * step)
	step_g = int((end_g - start_g) / steps * step)
	step_b = int((end_b - start_b) / steps * step)
	
	return (start_r+step_r, start_g+step_g, start_b+step_b)

def fade(pixels, start, end, duration):
	steps = 16
	pixels.fill(start)
	time.sleep(duration/steps)
	for step in range(1,steps-1):
		col = colorstep(start, end, step, steps)
		print(col)
		pixels.fill(col)
		time.sleep(duration/steps)
	pixels.fill(end)
	#time.sleep(duration/steps)
	#time.sleep(0)

def blink():
	while True:
		led.value = True
		pixels.fill((10,0,0))
		time.sleep(0.5)
		led.value = False
		pixels.fill((0,0,0))
		time.sleep(0.5)

von = farben[randint(1,len(farben)-1)]
bis = farben[randint(1,len(farben)-1)]
off = farben[0]

fade(pixels, off, von , 0.25)
time.sleep(1)
fade(pixels, von, off, 0.25)
fade(pixels, off, bis, 0.25)
time.sleep(1)
fade(pixels, bis, (0,0,0), 0.25)
#time.sleep(1)
#fade(pixels, (255,0,0), (0,255,0), 0.5)
#fade(pixels, (0,255,0), (0,0,255), 0.5)
#fade(pixels, (0,0,255), (0,0,0), 0.5)

#for i in range(64):
#	on(pixels, i, (255,255,255) )
	#time.sleep(0.1)
#for i in range(64):
#	off(pixels,i)

#pixels.fill((1,0,0))

#blink()

print (len(farben))
