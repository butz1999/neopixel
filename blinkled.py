import board
import digitalio
import time

class Blinker():
	def __init__(self):
		print("Blinker constructor called")
		self.state = False
		self.led  = digitalio.DigitalInOut(board.D17)
		self.lock1 = digitalio.DigitalInOut(board.D22)
		self.lock2 = digitalio.DigitalInOut(board.D23)
		self.drawer1 = digitalio.DigitalInOut(board.D24)
		self.drawer2 = digitalio.DigitalInOut(board.D25)
		self.led.direction  = digitalio.Direction.OUTPUT
		self.lock1.direction = digitalio.Direction.OUTPUT
		self.lock2.direction = digitalio.Direction.OUTPUT
		self.drawer1.direction = digitalio.Direction.OUTPUT
		self.drawer2.direction = digitalio.Direction.OUTPUT
		
	def run(self):
		while True:
			self.state = not self.state
			self.led.value = self.state
			#self.lock1.value = self.state
			#self.lock2.value = self.state
			#self.drawer1.value = self.state
			#self.drawer2.value = self.state
			time.sleep(0.5)

	def setLock1(self, value):
		self.lock1.value = value
	
	def setLock2(self, value):
		self.lock2.value = value
	
	def setDrawer1(self, value):
		self.drawer1.value = value
		
	def setDrawer2(self, value):
		self.drawer2.value = value
