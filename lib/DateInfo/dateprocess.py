from dataclasses import dataclass

@dataclass
class DateItem:
  dateStr:str
  year:str
  yearAD:str
  month:str
  day:str

class DateProcess():
  '''
    Class for processing date string
    @parameter dateStr string
  '''
  def __init__(self, dateStr):
    self.dateStr = dateStr
    self.latestdateStr = ''
    self.processDate()

  def processDate(self):
    tempYear = ''
    tempMonth= ''
    tempDay  = ''

    if (self.dateStr.count('/') == 2):
      tempYear = (self.dateStr).split('/')[0]
      tempMonth = (self.dateStr).split('/')[1]
      tempDay = (self.dateStr).split('/')[2]
    elif (self.dateStr.count('-') == 2):
      tempYear = (self.dateStr).split('-')[0]
      tempMonth = (self.dateStr).split('-')[1]
      tempDay = (self.dateStr).split('-')[2]

    if (len(tempYear) == 4):
      self.latestdateStr = DateItem(self.dateStr, tempYear ,str(int(tempYear)-1911), tempMonth, tempDay)
    elif (len(tempYear) == 3):
      self.latestdateStr = DateItem(self.dateStr, str(int(tempYear)+1911), tempYear, tempMonth, tempDay)

  def getDate(self):
    return self.latestdateStr

if __name__ == "__main__":
  a = DateProcess('108/02/18')
  print(a.getDate().year)