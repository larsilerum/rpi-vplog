import RPi.GPIO as GPIO
import datetime
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)


class Korr:
  global arraySize
  arraySize = 8

def updateValues(prognos):
  print "korr.updateValues : prognos= " + str(prognos.temp) + ", " + str(prognos.symbol)
  return getAndCommitCorrection(prognos, 0)    # getKaminKorr())

def printLists():
  print "TempList"
  for temp in prognosTempList:
    print temp
  print "SymbolList"
  for symbol in prognosSymbolList:
    print symbol
    
def getAndCommitCorrection(prognos, kaminKorr):
  print "kaminKorr = " + str(kaminKorr)
  corr = kaminKorr
  now = datetime.datetime.now()
  if now.hour > 17:
    corr = corr - 1
  sumDiffs = sumOfDiffs(prognos.temp)
  print "sumDiffs = " + str(sumDiffs)
  if now.hour > 4 and now.hour < 15 and now.month > 2 and now.month < 11:
    symbolsum = sum(prognos.symbol)
    if symbolsum >= 9 and symbolsum < 12:
      corr = corr + 1
      print "sumbolsum mellan 9 och 12"
    if symbolsum < 9:
      corr = corr + 2
      print "symbolsum mindre an 9"
  if sumDiffs >= 4 and sumDiffs < 7:
    corr = corr + 1
    print "sumofdiffs mellan 4 och 7"
  if sumDiffs >= 7:
    corr = corr + 2
    print "sumofdiffs mer an 7"
  if sumDiffs <= -4 and sumDiffs > -7:
    corr = corr - 1
    print "sumofdiffs mellan -4 och -7"
  if sumDiffs <= -7:
    corr = corr - 2
    print "sumofdiffs mindre an -7"
  if corr > 3:
    corr = 3
  if corr < -3:
     corr = -3
  actualCorrection = commitCorr(corr)
  print "New correction calculated: " + str(actualCorrection)
  return actualCorrection

def sumOfDiffs(templist):
  sum = 0
  for i in range(1, arraySize):
    sum = sum + templist[i - 1] - templist[i]
  return -sum

def commitCorr(corr):
  if corr < -2:
    GPIO.output(10,True)
    GPIO.output(12,True)
    GPIO.output(16,False)
    GPIO.output(18,False)
    return -2.8
  if corr == -2:
    GPIO.output(10,False)
    GPIO.output(12,True)
    GPIO.output(16,False)
    GPIO.output(18,False)
    return -1.8
  if corr == -1:
    GPIO.output(10,True)
    GPIO.output(12,False)
    GPIO.output(16,False)
    GPIO.output(18,False)
    return -1.0
  if corr == 0:
    GPIO.output(10,False)
    GPIO.output(12,False)
    GPIO.output(16,False)
    GPIO.output(18,False)
    return 0
  if corr == 1:
    GPIO.output(10,False)
    GPIO.output(12,False)
    GPIO.output(16,True)
    GPIO.output(18,False)
    return 1.0
  if corr == 2:
    GPIO.output(10,False)
    GPIO.output(12,False)
    GPIO.output(16,False)
    GPIO.output(18,True)
    return 1.8
  if corr > 2:
    GPIO.output(10,False)
    GPIO.output(12,False)
    GPIO.output(16,True)
    GPIO.output(18,True)
    return 2.8

def getKaminKorr():
  f = open('kamin.txt', 'r+')
  start = int(f.readline())
  print "startKamin = " + str(start)
  end = int(f.readline())
  print "endKamin = " + str(end)
  now = int(time.time())
  print "now = " + str(now)
  if (now - start < 3600):
    return -1
  if (now - end > 0):
    return 0
  return -1
