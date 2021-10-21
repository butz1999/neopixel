from http.server import BaseHTTPRequestHandler, HTTPServer

class WebServer(HTTPServer):
	def start(self, name):
		self.name = name
		print(name)
		serve_forever()

class WebHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
		self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
		self.wfile.write(bytes("<body>", "utf-8"))
		self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
		self.wfile.write(bytes("</body></html>", "utf-8"))
		self.queue.put(self.path)

	def setQueue(self, queue):
		self.queue = queue

