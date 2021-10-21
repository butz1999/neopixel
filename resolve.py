import ledserver
import time

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

serverPort = 8080
hostName = "localhost"

cmdQueue = Queue()

class WebServer(BaseHTTPRequestHandler):

	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
		self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
		self.wfile.write(bytes("<body>", "utf-8"))
		self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
		self.wfile.write(bytes("</body></html>", "utf-8"))
		if (self.path != "/favicon.ico"):
			print("Sent: ", self.path)
			cmdQueue.put(self.path)
        

led = ledserver.LedServer()
ledThread = Thread(target = led.start, args = ("LedServer", cmdQueue))
ledThread.start()

web = HTTPServer((hostName, serverPort), WebServer)
webThread = Thread(target = web.serve_forever)
webThread.start()
