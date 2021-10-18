import board
import digitalio
import neopixel
import time

led = digitalio.DigitalInOut(board.D23)
led.direction = digitalio.Direction.OUTPUT

pixels = neopixel.NeoPixel(board.D18, 64)

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
	time.sleep(duration/steps)


fade(pixels, (0,0,0), (255,0,0) , 0.5)
fade(pixels, (255,0,0), (0,0,0), 0.5)

#for i in range(64):
#	on(pixels, i, (255,255,255) )
	#time.sleep(0.1)
#for i in range(64):
#	off(pixels,i)

#pixels.fill((1,0,0))

while True:
	led.value = True
	pixels.fill((10,0,0))
	time.sleep(0.5)
	led.value = False
	pixels.fill((0,0,0))
	time.sleep(0.5)
