class Velocity:
    def __init__(self, vx=0, vy=0, ax=0, ay=0):
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay

    def getvx(self):
        return self.vx

    def getvy(self):
        return self.vy

    def getax(self):
        return self.ax

    def getay(self):
        return self.ay    

    def setvx(self, vx):
        self.vx = vx

    def setvy(self, vy):
        self.vy = vy

    def setax(self, ax):
        self.ax = ax

    def setay(self, ay):
        self.ay = ay
        
