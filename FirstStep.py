from lib.TradingInfo.GetData.getCenterID import getCenterID

class FirstStep():
  def __init__(self):
    self._IDobject = getCenterID()
  
  def getID(self):
    return self._IDobject.getID()
