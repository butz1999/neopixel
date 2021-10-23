from http.server import BaseHTTPRequestHandler, HTTPServer
import io

class webServer:
	def __init__(self, queue):
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
		self.queue = queue
		BaseHTTPRequestHandler.__init__(self, *args)
	
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		#self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
		#self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
		#self.wfile.write(bytes("<body>", "utf-8"))
		#self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
		#self.wfile.write(bytes("</body></html>", "utf-8"))
		
		f = io.open("index.html", "r")
		content = f.read()
		self.wfile.write(bytes(content, "utf-8"))
		f.close()
		
		if (self.path != "/favicon.ico"):
			print("Sent: ", self.path)
			self.queue.put(self.path)

