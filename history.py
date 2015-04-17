import json
from os import listdir
from os.path import isfile, join
from pprint import pprint

#lists all files in a folder
def getFiles(path):
	files = [f for f in listdir(path) if isfile(join(path,f))]
	files.sort()
	return files

#lists the n newest files
def getLastNFiles(files, amount):
	length = len(files)
	if amount > length:
		amount = length
	return files[length - amount:length]

#list all files created from a time
def getFilesFrom(files, time):
	time = long(time)
	return [f for f in files if long(f) >= time]

#loads a file and returns a json object
def loadFile(fileName):
	with open('records/'+fileName) as jsonfile:
		data = json.load(jsonfile)
	return data

#loads a list of files and returns an array of objects
def loadJSON(files):
	return {'records':[loadFile(f) for f in files]}

#get all records in a list since time
def getRecordsSince(time):
	files = getFilesFrom(getFiles("records"), time)
	return loadJSON(files)

#get the last n records
def getNRecords(amount):
	files = getLastNFiles(getFiles("records"), amount)
	return loadJSON(files)

