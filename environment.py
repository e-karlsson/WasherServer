import urllib, urllib2, cookielib, datetime, time, math, json
currentTime = lambda: int(round(time.time()*1000))

#Returns millis until start at cheapest price
def startAtCheapest(maxWait):
	cookie_jar = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
	urllib2.install_opener(opener)

	now = datetime.datetime.now()
	
	# do POST
	url_2 = 'http://www.elskling.se/timpriser'
	currentDate = now.strftime("%Y-%m-%d")
	values = dict(timpriser=currentDate, seomr='se0123')
	data = urllib.urlencode(values)
	req = urllib2.Request(url_2, data)
	rsp = urllib2.urlopen(req)
	content = rsp.read()


	#Parse content
	startIndex = content.index("se1Arr")
	newContent = content[startIndex:]
	endIndex = newContent.index(";")
	if endIndex < 20:
		print "Couldn't find the prices for %s" % currentDate
		return [currentTime(), -1]

	startValues = newContent.index("(")
	valueString = newContent[startValues+1:]
	endValues = valueString.index(")")
	valueString = valueString[:endValues]

	splittedString = valueString.split(",")

	floats = [float(f) for f in splittedString]

	#Get the current hour
	currentHour = now.hour + 2

	#convert maxWait to hours
	millisLeft = maxWait - currentTime()
	hoursLeft = math.ceil(millisLeft/(1000*60*60))
 	maxWait = int(hoursLeft)+1

	#Get the minumum price
	minValue = floats[currentHour]
	minIndex = currentHour
	for x in range(1,maxWait):
		index = (currentHour + x)%24
		if (floats[index] < minValue):
			minValue = floats[index]
			minIndex = index

	

	#Convert to millis left until start
	hoursLeft = (minIndex - currentHour) % 24
	hoursMilli = (hoursLeft-1) * 3600000
	minutesLeft = 60 - now.minute
	minutesMilli = minutesLeft * 60000
	timeLeft = hoursMilli + minutesMilli

	startAt = currentTime() + timeLeft
	#return how many millis is left	
	return [startAt, minValue]


def isWind():
	with open('settings/wind') as jsonfile:
		data = json.load(jsonfile)
	return data['isWind']>0

def getPriceAt(time):
	return 12.5
