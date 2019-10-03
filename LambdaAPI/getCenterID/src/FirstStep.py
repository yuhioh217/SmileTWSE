from src.getCenterID import getCenterID

class FirstStep():
  def __init__(self):
    self._IDobject = getCenterID()
  
  def getID(self):
    return self._IDobject.getID()

  def getName(self):
    return self._IDobject.getName()

  def getType(self):
    return self._IDobject.getType()
