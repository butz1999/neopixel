import board
import digitalio
import neopixel
import time
import sys
from random import *

#farben = {
#	(0,0,0),		# 0: off
#	(255,200,0),	# 1: gelb
#	(200,50,00), 	# 2: orange
#	(255,0,0),		# 3: rot
#	(70,0,50),		# 4: violett
#	(0,0,50),		# 5: blau
#	(30,30,230),	# 6: hellblau
#	(255,255,255), 	# 7: weiss
#	(30,255,10),	# 8: hellgrün
#	(0,40,0)		# 9: dunkelgrün
#	}

farben = {
	"aus":      (0,0,0),
	"weiss":	(255,255,255),
	"gelb":		(255,200,0),
	"orange":	(200,50,00),
	"rot":		(255,0,0),
	"violett":	(70,0,50),
	"blau":		(0,0,50),
	"hellblau":	(30,30,230),
	"grün":		(0,40,0),
	"hellgrün":	(30,255,10),
	}


pixels = neopixel.NeoPixel(board.D18, 64, bpp=3, brightness=1.2, auto_write=False, pixel_order=neopixel.GRB)

def colorstep(start, end, step, steps):
	start_r = start[0]
	start_g = start[1]
	start_b = start[2]
	
	end_r = end[0]
	end_g = end[1]
	end_b = end[2]
	
	step_r = int((end_r - start_r) / steps * step)
	step_g = int((end_g - start_g) / steps * step)
	step_b = int((end_b - start_b) / steps * step)
	
	return (start_r+step_r, start_g+step_g, start_b+step_b)

def zeige(aktuell):
	for i in range(len(aktuell)):
		pixels[i] = aktuell[i]
	pixels.show()

def fade(von, bis, dauer):
	steps = 32
	jetzt = [ (0,0,0) ] * 64
	zeige(von)
	time.sleep(dauer/steps)
	for step in range(steps):
		for index in range(len(von)):
			jetzt[index] = colorstep(von[index], bis[index], step, steps)
		zeige(jetzt)
		time.sleep(dauer/steps)
	zeige(bis)
		

def zufall_aus(liste, anzahl):
	gefunden = 0
	fehler = 0
	while (gefunden < anzahl):
		index = randint(0,len(liste)-1)
		if ((liste[index][0] != 0) or (liste[index][1] != 0) or (liste[index][2] != 0)):
			liste[index] = (0,0,0)
			gefunden += 1
		else:
			fehler += 1
			if (fehler > 1000):
				#print("Fehler: zu wenige helle LEDs")
				return

def zufall_ein(liste, anzahl, farbe):
	gefunden = 0
	fehler = 0
	while (gefunden < anzahl):
		index = randint(0,len(liste)-1)
		if ((liste[index][0] == 0) and (liste[index][1] == 0) and (liste[index][2] == 0)):
			if ((farbe == "zufall") or (not farbe)):
				liste[index] = list(farben.values())[randint(2,len(farben)-2)]
			else:
				liste[index] = farben[farbe]
			gefunden += 1
		else:
			fehler += 1
			if (fehler > 1000):
				#print("Fehler: zu wenige dunkle LEDs")
				break


def rainbow(liste):
	for i in range(16):
		liste[i] = (i*16, 0, 0)
	for i in range(16):
		liste[i+16] = (255-i*16, i*16, 0)
	for i in range(16):
		liste[i+32] = (0, 255-i*16, i*16)
	for i in range(16):
		liste[i+48] = (0, 0, 255-i*16)


blank = [ (0,0,0) ] * 64	
von = [ (0,0,0) ] * 64
bis = [ (0,0,0) ] * 64

wartezeit = 0.5
fadezeit = .75

rainbow(von)
fade(blank,von,fadezeit)
time.sleep(wartezeit)
fade(von,blank,fadezeit)

von = [ (0,0,0) ] * 64
bis = [ (0,0,0) ] * 64



while True:
	# zufälliges Muster
	von = [ (0,0,0) ] * 64
	bis = [ (0,0,0) ] * 64
	zufall_ein(von, 16, "zufall")
	zufall_ein(bis, 16, "zufall")
	fade(blank,von,fadezeit)
	time.sleep(wartezeit)
	for i in range(5):
		fade(von, bis, fadezeit)
		von = bis.copy()
		zufall_aus(bis,randint(10,30))
		zufall_ein(bis,randint(10,30), "zufall" )
		time.sleep(wartezeit)
		
	fade(von,blank,fadezeit)
	time.sleep(wartezeit)
	
	# zufällige Farbe
	color = list(farben)[randint(2, len(farben)-2)]
	von = [ (0,0,0) ] * 64
	bis = [ (0,0,0) ] * 64
	zufall_ein(von, 16, color)
	zufall_ein(bis, 16, color)
	fade(blank,von,fadezeit)
	time.sleep(wartezeit)
	for i in range(5):
		fade(von, bis, fadezeit)
		von = bis.copy()
		zufall_ein(bis, randint(10,30), color)
		zufall_aus(bis, randint(10,30))
		time.sleep(wartezeit)
	
	fade(von,blank,fadezeit)
	time.sleep(wartezeit)

	# zufällige Farbübergänge
	color = list(farben)[randint(2, len(farben)-2)]
	von = [ (0,0,0) ] * 64
	bis = [ (0,0,0) ] * 64
	zufall_ein(von, 16, color)
	zufall_ein(bis, 16, color)
	fade(blank,von,fadezeit)
	time.sleep(wartezeit)
	for i in range(5):
		color = list(farben)[randint(2, len(farben)-2)]
		fade(von, bis, fadezeit)
		von = bis.copy()
		bis = [ (0,0,0) ] * 64
		zufall_ein(bis, 16, color)
		time.sleep(wartezeit)
	
	fade(von,blank,fadezeit)
	time.sleep(wartezeit)
