from http.server import BaseHTTPRequestHandler, HTTPServer
import io
import logging

log = logging.getLogger("webserver")

class webServer:
	def __init__(self, queue):
		log.info("WebServer constructor called")
		self.serverPort = 8080
		self.hostName = ""
		def handler(*args):
			webHandler(queue, *args)
		self.server = HTTPServer((self.hostName, self.serverPort), handler)

	def run(self):
		self.server.serve_forever()
		
class webHandler(BaseHTTPRequestHandler):
	queue = None
	
	def __init__(self, queue, *args):
		log.info("WebHandler constructor called")
		self.queue = queue
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
			self.queue.put(self.path)

