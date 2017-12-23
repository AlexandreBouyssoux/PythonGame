# -*- coding: utf-8 -*-

# import

# Constants
WINDOW_SIZE = (0, 0, 1000, 600)
BALL_SIZE = 50
PLAYER_SIZE = 75
SPEED_INCREASE = 10
SPEED_DECREASE = 1
GRAVITY_BALL = 5
GRAVITY_PLAYER = 8
JUMP_HEIGHT = - 30
COEF_REBOND = 0.5
CAGE_W = 100
CAGE_H = 250
CAGE_BOX_H = 30
# Class


class Base(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = BALL_SIZE
        self.drawPoint = (self.x - self.size/2, self.y - self.size/2)
        self.color = (0, 0, 0)
        self.xSpeed = 0
        self.ySpeed = 0
        self.gravity = GRAVITY_BALL
        self.speedIncrease = SPEED_INCREASE
        self.speedDecrease = SPEED_DECREASE
        self.rebond = True
        self.debug = True

    def _applyGravity(self):
        applyGravity = True
        if self.y == WINDOW_SIZE[-1] - self.size/2:
            applyGravity = False
        if self.y == WINDOW_SIZE[-1] - CAGE_H - CAGE_BOX_H - self.size/2:
            if self.x <= CAGE_W:
                applyGravity = False
            elif self.x >= WINDOW_SIZE[-2] - CAGE_W:
                applyGravity = False
        return applyGravity

    def _speedUpdate(self):
        if self._applyGravity():
            self.ySpeed += self.gravity

        if abs(self.xSpeed) >= SPEED_DECREASE:
            if self.xSpeed > 0:
                self.xSpeed -= self.speedDecrease
            elif self.xSpeed < 0:
                self.xSpeed += self.speedDecrease
        else:
            self.xSpeed = 0

    def rebondY(self, verbose=0):
        if self.debug and verbose > 0:
            print("speed before Ybounce: {}".format(self.ySpeed))
        if self.rebond and self.ySpeed > 0.5*self.size:
            self.ySpeed = - COEF_REBOND*self.ySpeed
        else:
            self.ySpeed = 0

    def rebondX(self, verbose=0):
        if self.debug and verbose > 0:
            print("speed before Xbounce: {}".format(self.xSpeed))
        if self.rebond:
            self.xSpeed = - COEF_REBOND*self.xSpeed
        else:
            self.xSpeed = 0

    def updateXYPosition(self, verbose=0):
        """
        we update the base position based on the speed of the object
        """
        if self.debug and verbose > 0:
            print("x: {} | y: {}".format(self.x, self.y))
            print("xSpeed: {} | ySpeed: {}".format(self.xSpeed, self.ySpeed))
            print("---")
        self.y += self.ySpeed
        self.x += self.xSpeed

        if self.y <= self.size/2:
            if self.debug and verbose > 1:
                print("ceiling collision")
            self.y = self.size/2
            self.ySpeed = 0

        if self.y >= WINDOW_SIZE[-1] - self.size/2:
            if self.debug and verbose > 1:
                print("floor collision")
            self.y = WINDOW_SIZE[-1] - self.size/2
            self.rebondY()

        if self.x <= self.size/2:
            self.x = self.size/2
            self.rebondX()

        if self.x >= WINDOW_SIZE[-2] - self.size/2:
            self.x = WINDOW_SIZE[-2] - self.size/2
            self.rebondX()

        if self.debug and verbose > 1:
            print("correct pos | x: {} | y: {}".format(self.x, self.y))
            print("correct speed | xSpeed: {} | ySpeed: {}".format(self.xSpeed,
                  self.ySpeed))
            print("---")

        self._speedUpdate()
        if self.debug and verbose > 1:
            print("pos update | x: {} | y: {}".format(self.x, self.y))
            print("speed update | xSpeed: {} | ySpeed: {}".format(self.xSpeed,
                  self.ySpeed))
            print("||||||||||||||||||||||||||||||||||||||||")

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def setColor(self, tupleColor):
        """
        tupleColor must be like: (x, y, z)
        with x, y, z between 0 and 255
        """
        self.color = tupleColor

    def setSpeed(self, xSpeed, ySpeed):
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getDrawPoint(self):
        self.drawPoint = (self.x - self.size/2, self.y - self.size/2)
        return(self.drawPoint)

    def getSize(self):
        return self.size

    def getColor(self):
        return self.color

    def getSpeed(self):
        return(self.xSpeed, self.ySpeed)


class Player(Base):
    def __init__(self):
        super().__init__()
        self.gravity = GRAVITY_PLAYER
        self.jumpHeight = JUMP_HEIGHT
        self.size = PLAYER_SIZE
        self.score = 0
        self.rebond = False
        self.debug = False

    def moveLeft(self):
            self.xSpeed -= self.speedIncrease

    def moveRight(self):
            self.xSpeed += self.speedIncrease

    def jump(self):
        self.ySpeed = self.jumpHeight

    def scores(self):
        self.score += 1

    def getScore(self):
        return(self.score)


class Box(object):
    def __init__(self, w, h, upRightCornerPos=(0, 0), color=(0, 0, 0)):
        self.upRightCorner = upRightCornerPos
        self.h = h
        self.w = w
        self.color = (0, 0, 0)

    def setPosition(self, x, y):
        self.upRightCorner = (x, y)

    def setW(self, w):
        self.w = w

    def setH(self, h):
        self.h = h

    def setColor(self, colorTuple):
        self.color = colorTuple
