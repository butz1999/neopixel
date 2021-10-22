import ledserver
import webserver
import time
import blinkled
from http.server	import BaseHTTPRequestHandler, HTTPServer
from threading		import Thread
from queue			import Queue

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


cmdQueue = Queue()

blink = blinkled.Blinker()
blinkThread = Thread(target = blink.run)
blinkThread.start()

led = ledserver.LedServer(blink)
ledThread = Thread(target = led.start, args = ("LedServer", cmdQueue))
ledThread.start()

web = webserver.webServer(cmdQueue)
webThread = Thread(target = web.run)
webThread.start()

cmdQueue.put("/led/idle")
