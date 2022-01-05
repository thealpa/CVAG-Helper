#!/usr/local/bin/python
# coding: utf-8

import json

cvag = open('cvag.json', encoding='utf8')
data = json.load(cvag)

stops = []
length = 0

with open('stops.txt', encoding='utf8') as file:
	for line in file:
		temp = line.rstrip()
		line_items = temp.split("\",\"")
		temp_items = []
		for item in line_items:
			item = item.replace('\"', '')
			temp_items.append(item)
		stops.append(temp_items)
		length = length + 1

no_matches = []
finalList = []

for station in data['stations']:
	number = station['number']
	displayName = station['displayName']
	
	if displayName.endswith('.'):
		displayName = displayName[:-1]
	if "str." in displayName:
		displayName = displayName.replace('str.', 'str')
	if "Mülsen St. Jacob" in displayName:
		displayName = displayName.replace('Mülsen St. Jacob', 'Mülsen St Jacob')
	
	# Edge Cases that have to be handled in the future:
	#
	# Mülsen St. Jacob -> Mülsen St Jacob
	# Riemenschneiderstr -> Riemenschneiderstraße
	# Haltepunkt -> Hp
	# Bahnhof -> Bf
	# Ortseingang Draisdorf -> Draisdorf, Ortseingang
	# Wittgensdorf Chemnitztalstr -> Wittgensdorf, Chemnitztalstr
	# Marktsteig Wittgensdorf -> Wittgensdorf, Marktsteig
	# Oberer Bahnhof Wittgensdorf -> Wittgensdorf, Oberer Bahnhof
	
	i = 1
	matches = 0
	lat = []
	lon = []
	while i < length and matches == 0:
		if stops[i][1].endswith(displayName):
			foundMatch = 1
			lat = stops[i][2]
			lon = stops[i][3]
			matches = matches + 1
		i = i + 1
	if matches == 0:
		no_matches.append(displayName)
	if matches >= 1:
		entry = {'id': number, 'name': station['displayName'], 'latitude': float(lat), 'longitude': float(lon)}
		finalList.append(entry)	

# Uncomment to find more edge cases
#for item in no_matches:
	#print(item)

with open('Stops.json', 'w', encoding='utf-8') as f:
	json.dump(finalList, f, ensure_ascii=False, indent=4)