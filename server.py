#CONSTANTS
FETCH_RATE = 5
MONITOR_RATE = 15
STATE_OFF = 0
STATE_SCHEDULE = 1
STATE_RUNNING = 2
STATE_DONE = 3

#IMPORTS
import thread
import time
import raspcom
import monitor
import api
import environment
import push
#BODY

def startServer():
	global state
	print "starting main server"
	state = STATE_OFF
	setState (STATE_OFF)
	init()
	
	try:
		thread.start_new_thread(api.startAPIServer, ())
	except:
		print "Couldn't start API thread"

	serverLoop()
	
def serverLoop():
	global state
	global startTime
	global useWind

	while True:
		if state == STATE_OFF:
			data = raspcom.fetchData()
			monitor.logic(data[1], False)
			for x in range (0, MONITOR_RATE):
				if state == STATE_OFF:
					time.sleep(1)
		elif state == STATE_SCHEDULE:
			data = raspcom.fetchData()
			monitor.logic(data[1], False)
			
			for x in range (0, MONITOR_RATE):
				if state == STATE_SCHEDULE:	
					currentMillis = int(round(time.time() * 1000))
					if currentMillis > startTime:
						print "Starting the device by schedule"
						raspcom.startDevice()
						setState(STATE_RUNNING)
					elif useWind and environment.isWind():
						print "Starting the device early with wind"
						raspcom.startDevice()
						setState(STATE_RUNNING)
				time.sleep(1)	
		elif state == STATE_RUNNING:
			data = raspcom.fetchData()
			raspcom.createEnergyPoint(data, FETCH_RATE)
			monitor.logic(data[1], True)
			for x in range (0, FETCH_RATE):
				if state == STATE_RUNNING:
					time.sleep(1)
		elif state == STATE_DONE: 
			time.sleep(1)

def setState(newState):
	global state
	if state == STATE_OFF:
		if newState == STATE_DONE:
			return error(state, newState)
	elif state == STATE_SCHEDULE:
		if newState == STATE_DONE:
			return error(state, newState)
	elif state == STATE_RUNNING:
		if newState == STATE_SCHEDULE:
			return error(state, newState)
	elif state == STATE_DONE:
		if newState != STATE_OFF:
			return error(state, newState)

	if newState == STATE_RUNNING and state != newState:
		printProgram()
		raspcom.startRecording()
	if newState == STATE_DONE and state != newState:
		raspcom.stopRecording()
	if state == STATE_RUNNING and newState == STATE_OFF:
		raspcom.stopRecording()
	
	state = newState
	print "Changed state to", getNameOf(state)
	return True

def getState():
	global state
	return state

def error(state, newState):
	print "Can't change from %s to %s" %(getNameOf(state),getNameOf(newState))
	return False

def getNameOf(state):
	return ["OFF", "SCHEDULE", "RUNNING", "DONE"][state]

def stopDevice():
	if getState() == STATE_RUNNING and setState(STATE_OFF):
		raspcom.stopDevice()
		return True
	if getState() == STATE_SCHEDULE and setState(STATE_OFF):
		return True
	return False

def scheduleWith(scheduleTime, washTime, wind, price, name, degree):
	global startTime
	global useWind
	global useLowPrice
	global programName
	global programDegree
	global doneTime
	global programTime


	programTime = washTime/1000/60
	currentMillis = int(round(time.time() * 1000))
	if scheduleTime < currentMillis:
		scheduleTime = currentMillis
	startTime = scheduleTime
	doneTime = startTime + washTime
	useWind = wind
	useLowPrice = price
	programName = name
	programDegree = degree

	return setState(STATE_SCHEDULE)
	

def startDeviceWithinTime(time, washTime, name, degree):
	global startTime
       	status = scheduleWith(time, washTime, False, False, name, degree)	
	return [startTime, environment.getPriceAt(startTime), status]
	
def startDeviceAtLowestPrice(time, washTime, name, degree):
	data = environment.startAtCheapest(time)
	status = scheduleWith(data[0], washTime, False, True, name, degree)
	data.append(status)
	return data

def startDeviceWithWind(time, washTime, name, degree):
	global startTime
        status = scheduleWith(time, washTime, True, False, name, degree)
	return [startTime, environment.getPriceAt(startTime),status]

def printProgram():
	global programTime

	info = getProgramInfo()
	print "Starting washer!"
	print "Program name:", info['name']
	print "Degrees:", info['degree']
	print "Estimated run time: %d minutes" %programTime
	print "Using wind?", info['wind']
	print "Low price?", info['lowPrice']

def pingDone():
	status = setState(STATE_OFF)
	return status

def getProgramInfo():
	global startTime
	global useWind
	global useLowPrice
	global programName
	global programDegree
	global doneTime
	
	return {'startTime':startTime,'wind':useWind,'lowPrice':useLowPrice,'name':programName,'degree':programDegree,'endTime':doneTime};

def getLiveData():
	global state

	return {'state':state,'energy':raspcom.getLatestEnergy(),'programInfo':getProgramInfo()}


def init():
	global startTime
	global useWind
	global useLowPrice
	global programName
	global programDegree
	global doneTime
	global programTime
		
	startTime = 0
	useWind = False
	useLowPrice = False
	programName = "No Name"
	programDegree = "0"
	doneTime = 0
	programTime = 0

	raspcom.init()
