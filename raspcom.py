import urllib2
import json
import time 
energypoints = []
currentTime = lambda: int(round(time.time()*1000))

startTime = currentTime()
totalEnergy = 0.0
latestEnergy = 0.0
isRunning = False
timeLeft = 43

#Get's the Live data from RaZBerry
def fetchData():
	url = "http://192.168.1.5:8083/ZWaveAPI/Run/devices[2].instances[0].commandClasses.Meter"
	data = urllib2.urlopen(url).read()

	jdata = json.loads(data)

	currentKwh = jdata["data"]["0"]["val"]["value"]

	currentW = jdata["data"]["2"]["val"]["value"]

	
	return [currentKwh, currentW, currentTime()]


#Creates energypoints
def createEnergyPoint(data, rate):
	global totalEnergy
	totalEnergy += (data[1] * rate)
	global latestEnergy
	latestEnergy = data[1]
	newPoint = {'time':data[2], 'value':data[1]}
	global energypoints
	energypoints.append(newPoint)

	

#Creates washrecords
def createWashRecord():
	global energypoints
	global startTime
	washRecord = {'startTime':startTime, 'endTime':currentTime(), "totalEnergy":totalEnergy, "points":energypoints}	

	washRecord = json.dumps(washRecord)


	fo = open("records/"+str(startTime), "w")
	fo.write(washRecord)
	fo.close()



#Reset global variables before recording
def startRecording():
	global totalEnergy
	totalEnergy = 0.0
	global energypoints
	energypoints = []
	global startTime
	startTime = 0


#get live data: status, time left, current energy
def getLiveData():
	global latestEnergy

	returnValue = {'isRunning':isRunning, 'timeLeft':timeLeft, 'energy':latestEnergy}
	return returnValue
	

getLiveData()
createWashRecord()

