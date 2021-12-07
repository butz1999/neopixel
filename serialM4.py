import serial
import logging

port = "/dev/ttyUSB0"
baud = 115200

#log = logging.getLogger("serialM4")

class serialM4():
	def __init__(self):
		#log.info("SerialM4 constructor called")
		self.com = serial.Serial(port, 115200)
		
	def run(self):
		#log.info("Receive thread started")
		while True:
			self.state = self.com.read(1)
			print(self.state)

	def cmd(self, char):
		#log.info("Serial command: '" + char + "'")
		self.com.write(str.encode(char))

	def open(self):
		self.cmd("o")
		
	def close(self):
		self.cmd("c")
	
	def stop(self):
		self.cmd("s")
