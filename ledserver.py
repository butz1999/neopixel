import board
import digitalio
import neopixel
import time
import sys
from random import *

farben = {
	"aus":      (0,0,0),
	"weiss":	(255,255,255),
	"gelb":		(255,200,0),
	"orange":	(200,50,00),
	"rot":		(255,0,0),
	"violett":	(70,0,50),
#	"blau":		(0,0,50),
	"hellblau":	(30,30,230),
#	"grün":		(0,40,0),
	"hellgrün":	(30,255,10),
	}


class LedServer():
	def __init__(self):
		print("Led server constructor called")
		self.pixels = neopixel.NeoPixel(board.D18, 64, bpp=3, brightness=1.0, auto_write=False, pixel_order=neopixel.GRB)
		self.neu = [(0,0,0)] * 64
		self.alt = [(0,0,0)] * 64
		
	def zeige(self, aktuell):
		for i in range(len(aktuell)):
			self.pixels[i] = aktuell[i]
		self.pixels.show()

	def colorstep(self, start, end, step, steps):
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

	def fade(self):
		dauer = 1
		steps = 32
		jetzt = [ (0,0,0) ] * 64
		self.zeige(self.alt)
		time.sleep(dauer/steps)
		for step in range(steps):
			for index in range(len(self.alt)):
				jetzt[index] = self.colorstep(self.alt[index], self.neu[index], step, steps)
			self.zeige(jetzt)
			time.sleep(dauer/steps)
		self.zeige(self.neu)
		self.alt = self.neu.copy()

	def zufall(self,anzahl):
		self.neu = [(0,0,0)] * 64
		gefunden = 0
		fehler = 0
		while (gefunden < anzahl):
			i = randint(0,63)
			if ((self.neu[i][0] == 0) and (self.neu[i][1] == 0) and (self.neu[i][2] == 0)):
				self.neu[i] = list(farben.values())[randint(2,len(farben)-2)]
				gefunden += 1
			else:
				fehler += 1
				if (fehler > 1000):
					break
		self.fade()

	def off(self):
		self.neu = [(0,0,0)] * 64
		self.fade()

	def farbe(self,farbe):
		self.neu = [farbe] * 64
		self.fade()
	
	def single(self,farbe):
		self.neu = [(0,0,0)] * 64
		self.neu[35] = farbe
		self.fade()
	
	def test(self, args):
		print("test: ", args)
		if (args.find("off") != -1):
			self.off()
		else:
			sub = args.split("/",1)
			if (len(sub) == 2):
				if (sub[0] == "color"):
					colors = sub[1].split(",")
					if (len(colors) == 3):
						r = int(colors[0])
						g = int(colors[1])
						b = int(colors[2])
						self.farbe((r,g,b))
					else:
						color = int(sub[1])
						if (color < len(farben)):
							self.farbe(list(farben.values())[color])

				elif (sub[0] == "single"):
					colors = sub[1].split(",")
					if (len(colors) == 3):
						r = int(colors[0])
						g = int(colors[1])
						b = int(colors[2])
						self.single((r,g,b))
					else:
						color = int(sub[1])
						if (color < len(farben)):
							self.single(list(farben.values())[color])
				elif (sub[0] == "zufall"):
					anzahl = int(sub[1])
					self.zufall(anzahl)
				elif (sub[0] == "off"):
					self.off()
				else:
					print("test: wrong subcommand")
			else:
				print("test: wrong arguments")
				
		
	def led(self, args):
		print("led: ", args)
	
	def parse(self, url):
		if (url[:1] == "/"):
			url = url[1:]
		print("Trimmed: ", url)
		cmd = url.split("/", 1)
		if (len(cmd) == 2):
			print("Cmd: ", cmd[0])
			print("Arg: ", cmd[1])
			
			if (cmd[0] == "test"):
				self.test(cmd[1])
			if (cmd[0] == "led"):
				self.led(cmd[1])
			
		else:
			print("Wrong command syntax!")
		
		

	def start(self, name, cmdQueue):
		print("LedServer started")
		while True:
			url = cmdQueue.get()
			self.parse(url)
			print("Received: ", url)
