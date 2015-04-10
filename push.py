import json
import time
import thread

currentTime = lambda: int(round(time.time()*1000))

	
#call if user should not be reminded
def reset():
	global hasPushed
	hasPushed = True

def deviceStopped():
	global hasPushed
	hasPushed = False
	data = loadSettings()
	if data['push']:
		sendPush('done')
		remindTime = data['reminderTime']
		if remindTime > 0:
			print "Reminding user in %d minutes" % remindTime
			pushTime = currentTime() + remindTime*60*1000
			
			try:
				thread.start_new_thread(waitToRemind, (pushTime,))
			except:
				print "Couldn't start reminder thread"
				

def sendPush(message):

	print "Sent Push: ", message


def shouldPush():
	global hasPushed
	data = loadSettings()
	return data['push'] and not hasPushed

def remindTime():
	data = loadSettings()
	return data['reminderTime']

def loadSettings():
	with open('settings/settings') as jsonfile:
		data = json.load(jsonfile)
	return data


def waitToRemind(pushTime):
	while (currentTime() < pushTime):
		time.sleep(1)
	
	if shouldPush():
		sendPush('reminder')


reset()
