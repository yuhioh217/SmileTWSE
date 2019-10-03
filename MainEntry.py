from FirstStep import FirstStep

if __name__ == "__main__":
  # First, we should fetch all center stock ID. (I will get an array from getCenterID().getID())
  _first = FirstStep()
  _centerIDArr = _first.getID()
  _tempCenterArr = []
  for centerID in _centerIDArr:
    _tempCenterArr.append(centerID)
