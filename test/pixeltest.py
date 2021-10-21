import board
import neopixel
import time
from random import *

pixels = neopixel.NeoPixel(board.D18, 64)

#farben = [ (50,10,20), (5,30,35), (0,0,50), (50,50,0), (0,50,50), (50,0,50)]
farben = [
	(0,0,0),		#off
	(255,200,0),	#gelb
	(255,120,0), 	#orange
	(180,0,0),		#rot
	(80,0,80),		#violett
	(20,20,80),		#blau
	(80,80,160),	#hellblau
	(180,120,255), 	#stahlblau
	(30,255,10),	#hellgrün
	(0,40,0) ]		#dunkelgrün

def zufallsfarben():
	for i in range(1000):
		for ein in range(1):
			#r = randint(0,255)
			#g = randint(0,255)
			#b = randint(0,255)
			farbe = randint(0,len(farben)-1)
			print(len(farben),farbe)
			on = randint(0,63)
			pixels[on] = (farben[farbe][0]/2, farben[farbe][1]/2, farben[farbe][2]/2)

		for aus in range(5):
			off = randint(0,63)
			pixels[off] = (0,0,0)
		
		time.sleep(0.2)

def dimmen():
	for j in range(1):
		r = randint(0,255)
		g = randint(0,255)
		b = randint(0,255)
		steps = 16
		sleep = 0.025
		for i in range(steps):
			s = i*i/256
			print(i,s)
			pixels.fill((r*s, g*s, b*s))
			time.sleep(sleep)
		for i in range(steps-1,0,-1):
			s = i*i/256
			print(i,s)
			pixels.fill((r*s, g*s, b*s))
			time.sleep(sleep/4)
		pixels.fill((0,0,0))

def alle_farben():
	print(len(farben))
	for i in range(len(farben)):
		pixels.fill( (farben[i][0]/8, farben[i][1]/8, farben[i][2]/8) )
		#pixels[28] = ( (farben[i][0]/4, farben[i][1]/4, farben[i][2]/4) )
		#pixels[28] = ( (farben[i][0]/2, farben[i][1]/2, farben[i][2]/2) )
		#pixels[28] = ( (farben[i][0], farben[i][1], farben[i][2]) )
		time.sleep(1)

	
zufallsfarben()
#dimmen()
#alle_farben()


pixels.fill((0,0,0))
