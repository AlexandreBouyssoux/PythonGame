# -*- coding: utf-8 -*-

# import

# Constants
WINDOW_SIZE = (0, 0, 300, 300)
BALL_SIZE = 20
PLAYER_SIZE = 50
STEP = 20
GRAVITY_BALL = 5
GRAVITY_PLAYER = 8
JUMP_HEIGHT = - 30
# Class


class Base(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = BALL_SIZE
        self.color = (0, 0, 0)
        self.xSpeed = 0
        self.ySpeed = 0
        self.gravity = GRAVITY_BALL
        self.step = STEP
        self.rebond = True

    def _gravityEffect(self):
        self.ySpeed += self.gravity

    def _rebond(self, coeffRebond):
        if self.rebond and self.y >= WINDOW_SIZE[-1] - self.size:
            self.ySpeed = - coeffRebond*self.ySpeed
            if abs(self.ySpeed) < 0.6*self.size:
                self.ySpeed = 0

    def updateXYPosition(self):
        self._gravityEffect()
        self._rebond()
        self.y += self.ySpeed
        if self.y < 0:
            self.y = 0
        elif self.y > WINDOW_SIZE[-1] - self.size:
            self.y = WINDOW_SIZE[-1] - self.size
        if self.x < 0:
            self.x = 0
        elif self.x > WINDOW_SIZE[-2] - self.size:
            self.x = WINDOW_SIZE[-2] - self.size

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

    def getSize(self):
        return self.size

    def getColor(self):
        return self.color

    def getSpeed(self):
        return(self.xSpeed, self.ySpeed)

    def getPosition(self):
        return("x: {} y: {} xspeed: {} yspeed: {}".format(self.x, self.y,
               self.xSpeed, self.ySpeed))


class Player(Base):
    def __init__(self):
        super().__init__()
        self.gravity = GRAVITY_PLAYER
        self.jumpHeight = JUMP_HEIGHT
        self.size = PLAYER_SIZE
        self.rebond = False

    def moveLeft(self):
        if self.x > 0:
            self.x -= self.step

    def moveRight(self):
        if self.x < WINDOW_SIZE[-1] - self.size:
            self.x += self.step

    def jump(self):
        self.ySpeed = self.jumpHeight
        self.y += self.ySpeed
        if self.y <= 0:
            self.ySpeed = 0
