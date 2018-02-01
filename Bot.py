# -*- coding: utf-8 -*-

# import
import numpy as np
from Game import JUMP, LEFT, RIGHT
import Elements as Elts
# class


class Bot(object):
    def __init__(self, game, player):
        self.game = game
        for i, p in enumerate(self.game.getElements()[:-1]):
            if p == player:
                self.bot = p
                self.botCage = self.game.getStaticElements()[i]
            else:
                self.adv = p
                self.advCage = self.game.getStaticElements()[i]
        self.ball = self.game.getElements()[-1]

        # Position informations
        self.botPos = None
        self.advPos = None
        self.ballPos = None
        self.advCagePos = None

        # difference informations
        self.goalOrientation = None  # 1 if the ball is between player and adv
        # goal, -1 otherwise
        self.xDistanceBotBall = None
        self.yDistanceBotBall = None
        self.xDistanceBotAdv = None
        self.yDistanceBotAdv = None
        self.xRelativeballSpeed = None
        self.yBallSpeed = None

        self.updatePositionInformations()
        self.updateDifferenceInformations()

    def updatePositionInformations(self):
        self.botPos = (self.bot.getX(), self.bot.getY())
        self.advPos = (self.adv.getX(), self.adv.getY())
        self.ballPos = (self.ball.getX(), self.ball.getY())
        self.advCagePos = self.advCage.upRightCorner
        self.xBallSpeed, self.yBallSpeed = self.ball.getSpeed()

    def updateDifferenceInformations(self):
        self.goalOrientation = np.sign(self.botPos[0] - self.advCagePos[0]) * \
            np.sign(self.botPos[0] - self.ballPos[0])

        self.xDistanceBotBall = (self.botPos[0] - self.ballPos[0]) / \
            Elts.WINDOW_SIZE[2]
        self.yDistanceBotBall = (self.botPos[1] - self.ballPos[1]) / \
            Elts.WINDOW_SIZE[3]
        self.xDistanceBotAdv = (self.botPos[0] - self.advPos[0]) / \
            Elts.WINDOW_SIZE[2]
        self.yDistanceBotAdv = (self.botPos[1] - self.advPos[1]) / \
            Elts.WINDOW_SIZE[3]

    def giveDirections(self, verbose=0):
        """
        return a list of direction depending on the relative position of the
        ball
        """
        directionsList = []

        if self.botPos[1] >= self.ballPos[1]:
            draw = np.random.randint(0, 3)
            if not draw == 0:
                directionsList.append(JUMP)

        if self.botPos[0] < self.ballPos[0]:
            draw = np.random.randint(0, 3)
            if not draw == 0:
                directionsList.append(RIGHT)

        elif self.botPos[0] > self.ballPos[0]:
            draw = np.random.randint(0, 3)
            if not draw == 0:
                directionsList.append(LEFT)

        if verbose > 0:
            print("boty = {} | bally = {}".format(self.botPos[1],
                  self.ballPos[1]))
            print("botx = {} | ballx = {}".format(self.botPos[0],
                  self.ballPos[0]))

        self.updatePositionInformations()
        return directionsList

    def giveDirections2(self, model):
        directionList = []

        self.updatePositionInformations()
        self.updateDifferenceInformations()

        x = np.asarray([self.goalOrientation,
                        self.xDistanceBotBall,
                        self.yDistanceBotBall,
                        self.xDistanceBotAdv,
                        self.yDistanceBotAdv,
                        self.xBallSpeed,
                        self.yBallSpeed])

        modelOutput = model.predict(np.expand_dims(x, axis=0))[0]
        if modelOutput[0] > 0.5:
            directionList.append(JUMP)
        if modelOutput[1] > 0.5:
            directionList.append(RIGHT)
        if modelOutput[2] > 0.5:
            directionList.append(LEFT)

        return directionList
