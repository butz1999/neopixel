import board
import digitalio
import time

class Blinker():
	def __init__(self):
		print("Blinker constructor called")
		self.state = False
		self.led  = digitalio.DigitalInOut(board.D23)
		self.led.direction = digitalio.Direction.OUTPUT
		
	def run(self):
		while True:
			self.state = not self.state
			self.led.value = self.state
			time.sleep(0.5)
