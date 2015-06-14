import time
import server
import push

LOW_ENERGY_THRESHOLD = 2
HIGH_ENERGY_THRESHOLD = 5

START_TIME_THRESHOLD = 5000
STOP_TIME_THRESHOLD = 45000

startTime = 0
timing = False

currentTime = lambda: int(round(time.time()*1000))

def timePassed(amount):
	global startTime
	return currentTime() - startTime >= amount

def logic(currentW, running):
	global timing
	global LOW_ENERGY_THRESHOLD
	global HIGH_ENERGY_THRESHOLD
	global START_TIME_THRESHOLD
	global STOP_TIME_THRESHOLD
	if running:
		if currentW < LOW_ENERGY_THRESHOLD:
			if timing:
				if timePassed(STOP_TIME_THRESHOLD):
					server.setState(server.STATE_DONE)
					push.deviceStopped()
			else:
				timing = True
				startTime = currentTime()	
		else:
			timing = False
	else:
		if currentW > HIGH_ENERGY_THRESHOLD:
			if timing:
				if timePassed(START_TIME_THRESHOLD):
					server.setState(server.STATE_RUNNING)
					push.reset()
			else:
				timing = True
				startTime = currentTime()
		else:
			timing = False
