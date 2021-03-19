class Velocity:
    def __init__(self, vx=0, vy=0, gravity=0):
        self.vx = vx
        self.vy = vy
        self.gravity = gravity

    def getvx(self):
        return self.vx

    def getvy(self):
        return self.vy

    def setvx(self, vx):
        self.vx = vx

    def setvy(self, vy):
        self.vy = vy

    def reversevx(self):
        self.vx = -self.vx

    def reversevy(self):
        self.vy = -self.vy