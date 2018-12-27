from random import randint
import time

class Car:
    def __init__(self,i,xi,yi,max_age):
        self.i=i
        self.x=xi
        self.y=yi
        self.done=False
        self.age=0
        self.max_age=max_age

    def getX(self):  #for x coordinate
        return self.x

    def getY(self):  #for y coordinate
        return self.y

    def updateCoords(self, xn, yn):
        self.age = 0
        self.x = xn
        self.y = yn

    def setDone(self):
        self.done = True

    def timedOut(self):
        return self.done

    def age_one(self):
        self.age+=1
        if self.age>self.max_age:
            self.done=True
        return  True
