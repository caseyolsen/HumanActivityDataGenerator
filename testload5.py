#!/usr/bin/env python

import yaml
import random
import sys
import os
import shutil
import time

with open('importdoc5.yaml', 'r') as f:
  doc = yaml.load(f)
numberTests = doc["numberOfTests"]
folder = doc["folderName"]

try:
  os.mkdir(folder)
except OSError:
  pass
shutil.copy2('importdoc5.yaml', folder + '/input.yaml')

filesPath = "./activity_data"
activityLabels = doc["activityTable"]

STime = doc["startTime"]
if STime == 'now':
  STime = int(round(time.time() *1000))

seglength = 0
addtime = 0
for n in range(1, numberTests+1):
  dictcall = "Test" + str(n)
  dictname = doc[dictcall]
  print dictcall
  activities = dictname["activities"]
  persons = dictname["persons"]
  segments = dictname["numberSegments"]
  signals = dictname["sensor"]
  v2percent = dictname["partialverification"]
  seglength = segments * len(activities) * 5000
  startTime = STime
  startTime += addtime
  addtime += seglength

  usedDataPath = "dataUsed" + str(n) +".csv"
  newfilePath = "source" + str(n) + ".csv"
  verifFilePath = "verification-activity"+ str(n) + ".csv" 
  verifFilePath2 = "verification2-activity" + str(n) + ".csv"

  segmentations = []
  for n in range (0, segments):
    value = str(random.randrange(1, 61, 1))
    if len(value) == 1:
      value = "0" + value
    value = "s" + value
    segmentations.append(value)

  if(persons == ['all']):
    persons = []
    for x in range(1,9):
      persons.append('p'+ str(x))

  if(activities == ['all']):
    activities = []
    for x in range(1, 20):
      activities.append('a' + str("{0:0=2d}".format(x)))

  if(segmentations == ['all']):
    segmentations = [];
    for x in range(1, 61):
      segmentations.append('s' + str("{0:0=2d}".format(x)))

  if(signals == ['all']):
    signals = []
    for x in range(1,46):
      signals.append('q' + str("{0:0=2d}".format(x)))

  fileMap = {};
  for p in persons:
    allSegs = [];
    for a in activities:
      for s in segmentations:
        allSegs.append(a + ',' + s)
        random.shuffle(allSegs)

    fileMap[p] = allSegs
  newFile = open(folder + "/" + newfilePath, "w")
  newFile.write("time,activity,person,"
              + str(",".join(signals)) + "\n")

  sensor = {"T_xacc":0, "T_yacc":1, "T_zacc":2, "T_xgyro":3, "T_ygyro":4, "T_zgyro":5, "T_xmag":6, "T_ymag":7, "T_zmag":8, "RA_xacc":9, "RA_yacc":10, "RA_zacc":11, "RA_xgyro":12, "RA_ygyro":13, "RA_zgyro":14, "RA_xmag":15, "RA_ymag":16, "RA_zmag":17, "LA_xacc":18, "LA_yacc":19, "LA_zacc":20, "LA_xgyro":21, "LA_ygyro":22, "LA_zgyro":23, "LA_xmag":24, "LA_ymag":25, "LA_zmag":26, "RL_xacc":27, "RL_yacc":28, "RL_zacc":29, "RL_xgyro":30, "RL_ygyro":31, "RL_zgyro":32, "RL_xmag":33, "RL_ymag":34, "RL_zmag":35, "LL_xacc":36, "LL_yacc":37, "LL_zacc":38, "LL_xgyro":39, "LL_ygyro":40, "LL_zgyro":41, "LL_xmag":42, "LL_ymag":43, "LL_zmag\n":44}

  sigs = []
  for n in signals:
    if n in sensor:
      sigs.append(sensor[n])

  verifFile = open(folder + "/" + verifFilePath, "w")
  verifFile.write("time,activity,person,end\n")
  verifFile2 = open(folder + "/" + verifFilePath2, "w")
  verifFile2.write("time,activity,person,end\n")
  usedData = open(folder + "/" + usedDataPath, "w")

  activitiesUsed = []
  for x in range(0, len(activities) * len(segmentations)):
    segTime = long(startTime) + x * 5000
    for p in persons:
      seg = fileMap[p][x]
      route = seg.split(",")
      activity = route[0]
      segment = route[1]
      path = filesPath + "/" + activity + "/" + p + "/" + segment + ".txt"
      print path
      usedData.write(path + "\n")
      filein = open(path)
      first = filein.readlines()
      for line in range(0,125):
        newlist = []
        lines = first[line]
        lines = lines.split(",")
        for key in range(0, len(sigs)):
          newlist.append(lines[sigs[key]]) 
        time = segTime + line * 40
        newlist = ",".join(newlist)
        Line = str(time) + "," + activityLabels[activity] + "," + p + "," + str(newlist) + "\n"
        newFile.write(Line)
      Line2 = str(segTime) + "," + activityLabels[activity] + "," + p + "," + str(segTime + 5000) + "\n"
      verifFile.write(Line2)
      if random.randrange(1,101,1) <= v2percent:
        verifFile2.write(Line2)
        activitiesUsed.append(activity)

 # Makes sure each activity is used at least once in verification2

  for n in range(0, len(activities)):
     if activities[n] not in activitiesUsed:
       segUsed = segmentations[random.randrange(0, len(segmentations))]
       perUsed = persons[random.randrange(0, len(persons))]
       new = filesPath + "/" + activities[n] + "/" + perUsed + "/" +  segUsed + ".txt"
       name = activities[n] + "," + segUsed
       number = fileMap[perUsed].index(name)
       time1 = startTime + 5000 * number
       time2 = time1 + 5000
       newline = str(time1) + "," + activityLabels[activities[n]] + "," + perUsed + "," + str(time2) + "\n"
       verifFile2.write(newline)
