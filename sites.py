from config import *
class Sites:
    def  __init__(self,name):
        self.name = name
        self.landArray = []
        self.objArray = []
        for x in range(GRID_SIZE):
            self.landArray.append([15 for x in range(GRID_SIZE)])
            self.objArray.append([])
        print(self.landArray, self.objArray)
    
    def addObject(self, icon, pos):
        self.objArray[pos[0]].append(icon)
    