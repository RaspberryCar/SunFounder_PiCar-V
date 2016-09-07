#!/usr/bin/env python
import TB6612
import filedb

class Back_Wheels(object):
	Motor_A = 23
	Motor_B = 24

	PWM_A = 4
	PWM_B = 5

	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "back_wheels.py":'


	def __init__(self):
		if self._DEBUG:
			print self._DEBUG_INFO, "Debug on"
		self.forward_A = True
		self.forward_B = True

		self.db = filedb.fileDB()

		self.forward_A = self.db.get('forward_A', default_value=True)
		self.forward_B = self.db.get('forward_B', default_value=True)

		self.left_wheel = TB6612.Motor(self.Motor_A, self.PWM_A, offset=self.forward_A)
		self.right_wheel = TB6612.Motor(self.Motor_B, self.PWM_B, offset=self.forward_B)

		if self._DEBUG:
			print self._DEBUG_INFO, 'Set left wheel to #%d, PWM channel to %d' % (self.Motor_A, self.PWM_A)
			print self._DEBUG_INFO, 'Set right wheel to #%d, PWM channel to %d' % (self.Motor_B, self.PWM_B)

	def forward(self):
		self.left_wheel.forward()
		self.right_wheel.forward()
		if self._DEBUG:
			print self._DEBUG_INFO, 'Running forward'

	def backward(self):
		self.left_wheel.backward()
		self.right_wheel.backward()
		if self._DEBUG:
			print self._DEBUG_INFO, 'Running backward'

	def stop(self):
		self.left_wheel.stop()
		self.right_wheel.stop()
		if self._DEBUG:
			print self._DEBUG_INFO, 'Stop'

	def set_speed(self, speed):
		self.left_wheel.set_speed(speed)
		self.right_wheel.set_speed(speed)
		if self._DEBUG:
			print self._DEBUG_INFO, 'Set speed to', speed

	def set_debug(self, debug):
		if debug in (True, False):
			self._DEBUG = debug
		else:
			raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

		if self._DEBUG:
			print self._DEBUG_INFO, "Set debug on"
			print self._DEBUG_INFO, "Set left wheel and right wheel debug on"
			self.left_wheel.set_debug(True)
			self.right_wheel.set_debug(True)
		else:
			print self._DEBUG_INFO, "Set debug off"
			print self._DEBUG_INFO, "Set left wheel and right wheel debug off"
			self.left_wheel.set_debug(False)
			self.right_wheel.set_debug(False)

	def ready(self):
		if self._DEBUG:
			print self._DEBUG_INFO, 'Turn to "Ready" position'
		self.left_wheel.set_offset(self.forward_A)
		self.right_wheel.set_offset(self.forward_B)
		self.stop()

	def calibration(self):
		if self._DEBUG:
			print self._DEBUG_INFO, 'Turn to "Calibration" position'
		self.set_speed(30)
		self.forward()
		self.cali_forward_A = self.forward_A
		self.cali_forward_B = self.forward_B

	def cali_left(self):
		self.cali_forward_A = not self.cali_forward_A
		self.left_wheel.set_offset(self.cali_forward_A)
		self.forward()

	def cali_right(self):
		self.cali_forward_B = not self.cali_forward_B
		self.right_wheel.set_offset(self.cali_forward_B)
		self.forward()

	def cali_ok(self):
		self.forward_A = self.cali_forward_A
		self.forward_B = self.cali_forward_B
		self.db.set('forward_A', self.forward_A)
		self.db.set('forward_B', self.forward_B)
		self.stop()

if __name__ == '__main__':
	import time
	try:
		back_wheels = Back_Wheels()
		DELAY = 0.1
		back_wheels.forward()
		for i in range(0, 100):
			back_wheels.set_speed(i)
			print "Speed =", i
			time.sleep(DELAY)
		for i in range(100, 0, -1):
			back_wheels.set_speed(i)
			print "Speed =", i
			time.sleep(DELAY)

		back_wheels.backward()
		for i in range(0, 100):
			back_wheels.set_speed(i)
			print "Speed =", i
			time.sleep(DELAY)
		for i in range(100, 0, -1):
			back_wheels.set_speed(i)
			print "Speed =", i
			time.sleep(DELAY)
	except KeyboardInterrupt:
		back_wheels.stop()
	finally:
		back_wheels.stop()