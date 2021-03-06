from http.server import BaseHTTPRequestHandler, HTTPServer
import io
import logging
import json

log = logging.getLogger("webserver")

class webServer:
	def __init__(self, cmdQueue, datQueue):
		log.info("WebServer constructor called")
		self.serverPort = 8080
		self.hostName = ""
		def handler(*args):
			webHandler(cmdQueue, datQueue, *args)
		self.server = HTTPServer((self.hostName, self.serverPort), handler)

	def run(self):
		self.server.serve_forever()
		
class webHandler(BaseHTTPRequestHandler):
	queue = None
	
	def __init__(self, cmdQueue, datQueue, *args):
		log.info("WebHandler constructor called")
		self.cmdQueue = cmdQueue
		self.datQueue = datQueue
		BaseHTTPRequestHandler.__init__(self, *args)
	
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

		f = io.open("/home/pi/git/neopixel/index.html", "r")
		content = f.read()
		self.wfile.write(bytes(content, "utf-8"))
		f.close()
		
		if (self.path != "/favicon.ico"):
			log.info("Sending: " + self.path)
			self.cmdQueue.put(self.path)

	def do_POST(self):
		path = self.path
		length = int(self.headers["content-length"])
		
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		data = self.rfile.read(length)
		self.cmdQueue.put(self.path)
		self.datQueue.put(data)
		print(data)
