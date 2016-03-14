import time
import serial
import datetime
import yr
import korr
import requests

def readlineCR(port):
  while True:
    line = port.readline()
    if len(line) >0:
      return line

def getSunTemp():
  try:
    tfile1 = open("/sys/bus/w1/devices/28-00000504cc47/w1_slave")
    text1 = tfile1.read()
    temperaturedata1 = text1.split("\n")[1].split(" ")[9]
    temp1 = float(temperaturedata1[2:]) / 1000
    print "Soltemp=" + str(temp1)
    return temp1
  except:
    return 0

def logtoinflux(name, value) :
  payload = name + " value=" + str(value)
  print payload
  r = requests.post("http://influxdb:8086/write?db=vplog", data=payload)

print "vplog started"
port = serial.Serial("/dev/ttyUSB0", 
  baudrate=9600, 
  parity=serial.PARITY_NONE, 
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)

minuter = 1
prognos = yr.Prognos()

while True:
  try :
    print "vantar"
    textRow = readlineCR(port)
    print textRow
    print "length" + str(len(textRow))
    if len(textRow) != 99 :
      print "skipping last update"
      continue 
    list = textRow.split("\t")
    setTemp = float(list[1])
    setVV = float(list[2])
    innetemp = float(list[3])
    varmvatten = float(list[4])
    if varmvatten == 0: 
      varmvatten = 80
    avluft=float(list[5])
    retur=float(list[6])
    kod1=list[7]
    print "kod1" + str(kod1)
    elpatron = int(kod1[3:5], 2)
    kod2=list[8]
    print "kod2" + str(kod2)
    frekv=float(list[9])
    print "frekvens" + str(frekv)
    minuter = minuter - 1
    if minuter == 0:
      korrektion = 0
      minuter = 60
      nyPrognos = yr.getPrognosFromYr()
      if nyPrognos.valid == True:
        prognos = nyPrognos
    
    korrektion = korr.updateValues(prognos)
    sunTemp = getSunTemp()
    logtoinflux('innetemp', innetemp-korrektion)
    logtoinflux('sim_innetemp', innetemp)
    logtoinflux('varmvatten', varmvatten)
    logtoinflux('innebv', setTemp)
    logtoinflux('prognostemp', prognos.temp[7])
    logtoinflux('prognossymbol', prognos.symbol[7])
    logtoinflux('avluft', avluft)
    logtoinflux('retur', retur)
    logtoinflux('frekvens', frekv)
    logtoinflux('elpatron', elpatron)
    logtoinflux('soltemp', sunTemp )
    updateText = str(int(time.time())) + ":" + str(innetemp) + ":" + str(varmvatten) + ":" + str(setTemp) + ":" + str(prognos.temp[7]) + ":" + str(prognos.symbol[7])+ ":" + str(avluft) + ":" + str(retur) + ":" + str(float(frekv)) + ":" + str(korrektion)  + ":" + str(elpatron) + ":" + str(sunTemp)
    #print updateText
    os.system('rrdtool update vp.rrd ' + updateText)
    time.sleep(5)
  except Exception as inst:
    print inst
