import board
import digitalio
import neopixel
import blinkled
import time
import sys
import logging
import json
from random	import *
from queue	import Queue
from threading		import Thread

#log = logging.getLogger("webserver")

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
	def __init__(self, cmdQueue, datQueue, blinker):
		#log.info("LedServer constructor called")
		self.cmdQueue = cmdQueue
		self.datQueue = datQueue
		self.blinker = blinker

		self.leds = 64
		self.pixels = neopixel.NeoPixel(board.D18, self.leds, bpp=3, brightness=1.0, auto_write=False, pixel_order=neopixel.GRB)
		self.neu = [(0,0,0)] * self.leds
		self.alt = [(0,0,0)] * self.leds
		self.state = states["off"]
		self.runner = Thread(target = self.run)
		self.runner.start()
		self.normal = 16
		self.intense = 48
		self.intervall = 4
		self.pulsesteps = 10
		self.pulsetime  = 0.1
		self.blinker.setLock1(False)
		self.blinker.setLock2(False)
		
	def run(self):
		oldstate = states["off"]
		oldtime = time.time()
		intervall = 0
		again = False
		while True:
			if ((self.state != oldstate) or (time.time() > oldtime + intervall)):
				#log.info("oldstate: " + str(oldstate) + " newstate: " + str(self.state))
				oldstate = self.state
				if (oldstate != self.state):
					oldtime = time.time()
				if (self.state == states["off"]):
					self.neu = [(0,0,0)] * self.leds
					self.fade()
					intervall = 3600
				elif (self.state == states["idle"]):
					self.zufall(self.normal)
					self.fade()
					intervall = 4
				elif (self.state == states["user"]):
					self.farbauswahl( farben["blue"], self.intense)
					self.fade(self.pulsetime,self.pulsesteps)
					self.farbauswahl( farben["blue"], self.normal)
					self.fade(self.pulsetime,self.pulsesteps)
					intervall = 2
				elif (self.state == states["setup"]):
					self.farbauswahl( farben["violet"], self.normal)
					self.fade()
					intervall = 4
				elif (self.state == states["ok"]):
					self.farbauswahl( farben["green"], self.normal)
					self.fade()
					intervall = 4
				elif (self.state == states["warning"]):
					self.farbauswahl( farben["yellow"], self.normal)
					self.fade()
					intervall = 4
				elif (self.state == states["error"]):
					self.farbauswahl( farben["red"], self.intense)
					self.fade(self.pulsetime,self.pulsesteps)
					self.farbauswahl( farben["red"], self.normal)
					self.fade(self.pulsetime,self.pulsesteps)
					intervall = 2
				elif (self.state == states["pos"]):
					self.farbauswahl( farben["green"], self.intense)
					self.fade(self.pulsetime,self.pulsesteps)
					self.farbauswahl( farben["green"], self.normal)
					self.fade(self.pulsetime,self.pulsesteps)
					oldstate = states["ok"]
					self.state = states["ok"]
				elif (self.state == states["neg"]):
					self.farbauswahl( farben["yellow"], self.intense)
					self.fade(self.pulsetime,self.pulsesteps)
					self.farbauswahl( farben["yellow"], self.normal)
					self.fade(self.pulsetime,self.pulsesteps)
					oldstate = states["warning"]
					self.state = states["warning"]
				elif (self.state == states["test"]):
					intervall = 3600
				else:
					"""
					#log.warning("ledserver: wrong state detected!")
					"""
				oldtime = time.time()
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

	def fade(self, dauer = 0.5, steps = 24):
		#log.info("Dauer: " + str(dauer) + " Steps: " + str(steps))
		jetzt = [ (0,0,0) ] * self.leds
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
		self.neu = [(0,0,0)] * self.leds
		gefunden = 0
		fehler = 0
		while (gefunden < anzahl):
			i = randint(0,self.leds-1)
			if ((self.neu[i][0] == 0) and (self.neu[i][1] == 0) and (self.neu[i][2] == 0)):
				self.neu[i] = farbe
				gefunden += 1
			else:
				fehler += 1
				if (fehler > 1000):
					break

	def zufall(self,anzahl):
		self.neu = [(0,0,0)] * self.leds
		gefunden = 0
		fehler = 0
		while (gefunden < anzahl):
			i = randint(0,self.leds-1)
			if ((self.neu[i][0] == 0) and (self.neu[i][1] == 0) and (self.neu[i][2] == 0)):
				self.neu[i] = list(farben.values())[randint(2,len(farben)-1)]
				gefunden += 1
			else:
				fehler += 1
				if (fehler > 1000):
					break

	def off(self):
		self.neu = [(0,0,0)] * self.leds
		self.fade()

	def farbe(self,farbe):
		self.neu = [farbe] * self.leds
	
	def single(self,farbe):
		self.neu = [(0,0,0)] * self.leds
		self.neu[35] = farbe
		
	def linearisieren(self, bild):
		linear = [(0,0,0)] * self.leds
		
		index=0
		for x in range(8):
			for y in range(8):
				if ((x % 2) == 0):
					#gerade spalte
					linear[index] = bild[y][x]
				else:
					#ungerade spalte
					linear[index] = bild[7-y][x]
				index += 1
		return linear
	
	def ch(self):
		rt = (128,0,0)
		ws = (128,128,128)
		
		flagge = [ 
			[rt,rt,rt,rt,rt,rt,rt,rt],
			[rt,rt,rt,ws,ws,rt,rt,rt],
			[rt,rt,rt,ws,ws,rt,rt,rt],
			[rt,ws,ws,ws,ws,ws,ws,rt],
			[rt,ws,ws,ws,ws,ws,ws,rt],
			[rt,rt,rt,ws,ws,rt,rt,rt],
			[rt,rt,rt,ws,ws,rt,rt,rt],
			[rt,rt,rt,rt,rt,rt,rt,rt]
			]
			
		self.neu = self.linearisieren(flagge)
		self.fade()
		
	def de(self):
		rt = (128,0,0)
		rg = (128,32,0)
		ge = (110,64,0)
		sw = (0,0,0)
		sr = (30,0,0)
		
		flagge = [
			[sw,sw,sw,sw,sw,sw,sw,sw],
			[sw,sw,sw,sw,sw,sw,sw,sw],
			[sr,sr,sr,sr,sr,sr,sr,sr],
			[rt,rt,rt,rt,rt,rt,rt,rt],
			[rt,rt,rt,rt,rt,rt,rt,rt],
			[rg,rg,rg,rg,rg,rg,rg,rg],
			[ge,ge,ge,ge,ge,ge,ge,ge],
			[ge,ge,ge,ge,ge,ge,ge,ge],
			]
		self.neu = self.linearisieren(flagge)
		self.fade()
		
	def us(self):
		rt = (128,0,0)
		ws = (128,128,128)
		bl = (0,0,128)
		
		flagge = [
			[bl,bl,bl,bl,ws,ws,ws,ws],
			[bl,bl,bl,bl,rt,rt,rt,rt],
			[bl,bl,bl,bl,ws,ws,ws,ws],
			[bl,bl,bl,bl,rt,rt,rt,rt],
			[ws,ws,ws,ws,ws,ws,ws,ws],
			[rt,rt,rt,rt,rt,rt,rt,rt],
			[ws,ws,ws,ws,ws,ws,ws,ws],
			[rt,rt,rt,rt,rt,rt,rt,rt],
		]
		self.neu = self.linearisieren(flagge)
		self.fade()
		
			
	def resolve(self):
		rt = (255,0,0)
		dr = (30,0,0)
		bk = (0,0,0)
		bl = (0,0,255)

		logo = [
			[bk,bk,bk,bk,bk,bk,bk,bk],
			[bk,bk,bk,bk,bk,bk,bk,bk],
			[rt,rt,rt,bk,rt,rt,bk,bk],
			[rt,bk,bk,rt,bk,bk,rt,bk],
			[rt,bk,bk,rt,rt,rt,rt,bk],
			[rt,bk,bk,rt,bk,bk,bk,bk],
			[rt,bk,bk,bk,rt,rt,rt,bk],
			[bk,bk,bk,bk,bk,bk,bk,bk],
		]
		
		self.neu = self.linearisieren(logo)
		self.fade()
	
	def test(self, args):
		self.state = states["test"]
		if (args.find("off") != -1):
			self.off()
		elif (args.find("ch") != -1):
			self.ch()
		elif (args.find("de") != -1):
			self.de()
		elif (args.find("us") != -1):
			self.us()
		elif (args.find("resolve") != -1):
			self.resolve()
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
					self.fade()

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
					self.fade()
					
				elif (sub[0] == "random"):
					anzahl = int(sub[1])
					self.zufall(anzahl)
					self.fade()
				elif (sub[0] == "off"):
					self.off()
				else:
					"""
					#log.warning("test: wrong subcommand")
					"""
			else:
				"""
				#log.warning("test: wrong arguments")
				"""

	def jsonToBitmap(self, jdata):
		data = json.loads(jdata)
		bmp = []
		for i in range(8):
			line = []
			for j in range(8):
				line.append(tuple(data[i][j]))
			bmp.append(line)
		return bmp

		
	def led(self, args):
		#log.info("led: " + args)
		if args in states:
			self.state = states[args]
		else:
			#log.warning("led: Wrong argument:", args)
			self.state = states["off"]
			
	def lock(self, args):
		#log.info("lock: " + args)
		arg = args.split("/")
		sensor = arg[0]
		state  = arg[1]
		if (sensor == "waste"):
			if (state == "release"):
				self.blinker.wasteRelease()
			elif (state == "off"):
				self.blinker.wasteOff()
			else:
				self.blinker.wasteOff()
		elif (sensor == "reagent"):
			if (state == "release"):
				self.blinker.reagentRelease()
			elif (state == "off"):
				self.blinker.reagentOff()
			else:
				self.blinker.reagentOff()
	
	def drawer(self, args):
		#log.info("drawer:" + args)
		if (args == "in"):
			self.blinker.drawerIn()
		elif (args == "out"):
			self.blinker.drawerOut()
		elif (args == "off"):
			self.blinker.drawerOff()
		else:
			#log.warning("drawer: wrong argument:", args)
			self.blinker.drawerOff()
	
	def img(self, args):
		#log.info("img:" + args)
		if (args == "img"):
			jsonData = self.datQueue.get()
			imgData = self.jsonToBitmap(jsonData)
			print(imgData)
			self.neu = self.linearisieren(imgData)
			self.fade()
	
	def parse(self, url):
		if (url[:1] == "/"):
			url = url[1:]
		#log.info("Trimmed: " + url)
		cmd = url.split("/", 1)
		if (len(cmd) == 2):
			#log.info("Cmd: " + cmd[0] + " Arg: " + cmd[1])
			
			if (cmd[0] == "test"):
				self.test(cmd[1])
			elif (cmd[0] == "led"):
				self.led(cmd[1])
			elif (cmd[0] == "lock"):
				self.lock(cmd[1])
			elif (cmd[0] == "drawer"):
				self.drawer(cmd[1])
			elif (cmd[0] == "data"):
				self.img(cmd[1])
			else:
				"""
				#log.warning("parse: Wrong command:", cmd[0])
				"""
			
		else:
			"""
			#log.warning("parse: Wrong command syntax!")
			"""
		
		

	def start(self):
		#log.info("LedServer message handler started")
		while True:
			url = self.cmdQueue.get()
			#log.info("Received: " + url)
			self.parse(url)
