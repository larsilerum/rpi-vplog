import urllib2
from lxml import objectify

class Prognos:
  def __init__(self):
    self.temp = [0,0,0,0,0,0,0,0]
    self.symbol = [0,0,0,0,0,0,0,0]
    self.valid = False

def getPrognosFromYr():
  prognos = Prognos()
  try:
    xml=objectify.parse("http://www.yr.no/place/Sweden/V%C3%A4stra_G%C3%B6taland/Lerum/forecast_hour_by_hour.xml")
    weatherdata = xml.getroot()
    for i in xrange(8):
      nextTime = weatherdata.forecast.tabular.time[i]
      print nextTime.temperature.get("value")
      prognos.temp[i]=int(nextTime.temperature.get("value"))
      prognos.symbol[i]=int(nextTime.symbol.get("number"))
    prognos.valid = True
  except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    prognos.valid = False
  print prognos
  return prognos
