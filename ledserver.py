import board
import digitalio
import neopixel
import time
import sys
from random	import *
from queue	import Queue
from threading		import Thread

farben = {
	"off":      	(0,0,0),
	"white":		(255,255,255),
	"yellow":		(180,180,0),
	"orange":		(200,50,00),
	"red":			(255,0,0),
	"violet":		(180,0,180),
	"blue":			(0,0,255),
	"lightblue":	(30,160,160),
	"green":		(10,255,10),
	}

states = {
	"off":		1,
	"idle":     2,
	"user":		3,
	"setup":	4,
	"ok":		5,
	"warning":	6,
	"error":	7,
	"pos":		8,
	"neg":	    9,
	"test":		10,
	}

class LedServer():
	def __init__(self):
		print("Led server constructor called")
		self.pixels = neopixel.NeoPixel(board.D18, 64, bpp=3, brightness=1.0, auto_write=False, pixel_order=neopixel.GRB)
		self.neu = [(0,0,0)] * 64
		self.alt = [(0,0,0)] * 64
		self.state = states["off"]
		self.runner = Thread(target = self.run)
		self.runner.start()
		self.count = 16
		self.intervall = 4

	
	def run(self):
		oldstate = states["off"]
		oldtime = time.time()
		self.off()
		again = False
		while True:
			if (time.time() > oldtime + self.intervall):
				again = True
			if (self.state != oldstate or again):
				oldstate = self.state
				oldtime = time.time()
				again = False
				if (self.state == states["off"]):
					self.neu = [(0,0,0)] * 64
					self.fade()
				if (self.state == states["idle"]):
					self.zufall(self.count)
					self.fade()
				if (self.state == states["user"]):
					self.farbauswahl( farben["blue"], self.count)
					self.fade()
				if (self.state == states["setup"]):
					self.farbauswahl( farben["violet"], self.count)
					self.fade()
				if (self.state == states["ok"]):
					self.farbauswahl( farben["green"], self.count)
					self.fade()
				if (self.state == states["warning"]):
					self.farbauswahl( farben["yellow"], self.count)
					self.fade()
				if (self.state == states["error"]):
					self.farbauswahl( farben["red"], self.count)
					self.fade()
				if (self.state == states["pos"]):
					self.neu = [ farben["green"] ] * 64
					self.fade(0)
					self.state = states["ok"]
				if (self.state == states["neg"]):
					self.neu = [ farben["yellow"] ] * 64
					self.fade(0)
					self.state = states["warning"]
			time.sleep(0.01)
		
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

	def fade(self, dauer = 0.5):
		steps = 24
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
		
	def farbauswahl(self, farbe, anzahl):
		self.neu = [(0,0,0)] * 64
		gefunden = 0
		fehler = 0
		while (gefunden < anzahl):
			i = randint(0,63)
			if ((self.neu[i][0] == 0) and (self.neu[i][1] == 0) and (self.neu[i][2] == 0)):
				self.neu[i] = farbe
				gefunden += 1
			else:
				fehler += 1
				if (fehler > 1000):
					break
		self.fade()

	def zufall(self,anzahl):
		self.neu = [(0,0,0)] * 64
		gefunden = 0
		fehler = 0
		while (gefunden < anzahl):
			i = randint(0,63)
			if ((self.neu[i][0] == 0) and (self.neu[i][1] == 0) and (self.neu[i][2] == 0)):
				self.neu[i] = list(farben.values())[randint(2,len(farben)-1)]
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
		self.state = states["test"]
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
						else:
							self.farbe(farben["off"])

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
						else:
							self.single(farben["off"])
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
		if args in states:
			self.state = states[args]
		else:
			print("Fehler in 'led' argument")
			self.state = states["off"]
	
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
