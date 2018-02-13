# -*- coding: utf-8 -*-

# import
import numpy as np
from Game import JUMP, LEFT, RIGHT

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
        self.xDistanceBotCage = None
        self.yDistanceBotCage = None

        self.updatePositionInformations()
        self.updateDifferenceInformations()

    def updatePositionInformations(self):
        self.botPos = (self.bot.getX(), self.bot.getY())
        self.advPos = (self.adv.getX(), self.adv.getY())
        self.ballPos = (self.ball.getX(), self.ball.getY())
        self.advCagePos = self.advCage.upRightCorner

    def updateDifferenceInformations(self):
        self.goalOrientation = np.sign(self.botPos[0] - self.advCagePos[0]) * \
            np.sign(self.botPos[0] - self.ballPos[0])

        self.xDistanceBotBall = self.botPos[0] - self.ballPos[0]
        self.yDistanceBotBall = self.botPos[1] - self.ballPos[1]
        self.xDistanceBotAdv = self.botPos[0] - self.advPos[0]
        self.yDistanceBotAdv = self.botPos[1] - self.advPos[1]
        self.xDistanceBotCage = self.botPos[0] - self.advCagePos[0]
        self.yDistanceBotCage = self.botPos[1] - self.advCagePos[1]

    def giveDirections(self, verbose=0):
        """
        return a list of direction depending on the relative position of the
        ball
        """
        directionsList = []

        if abs(self.botPos[0] - self.advCagePos[0]) > \
        abs(self.ballPos[0] - self.advCagePos[0]):
            if self.botPos[1] >= self.ballPos[1]:
                draw = np.random.randint(0, 3)
                if not draw == 0:
                    directionsList.append(JUMP)
        else:
            if self.ballPos[1] == self.botPos[1]:
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

    def relu(self, v):
        """
        non linear fonction relu for the neural network
        """
        if v > 0:
            solution = v
        else:
            solution = 0
        return solution

    def giveDirections2(self, generation=0, specie=0, verbose=0):
        """
        return a list of direction based on a pre-trained neural network
        """
        directionsList = []

        w1 = np.loadtxt(r"GEN_{}/SPE_{}/w1.txt".format(generation, specie))
        w2 = np.loadtxt(r"GEN_{}/SPE_{}/w2.txt".format(generation, specie))
        w3 = np.loadtxt(r"GEN_{}/SPE_{}/w3.txt".format(generation, specie))

        model = [w1, w2, w3]
        x = np.asarray([self.goalOrientation,
             self.xDistanceBotBall,
             self.yDistanceBotBall,
             self.xDistanceBotAdv,
             self.yDistanceBotAdv,
             self.xDistanceBotCage,
             self.yDistanceBotCage])

        a1 = np.zeros(10, dtype=float)
        a2 = np.zeros(10, dtype=float)
        a3 = np.zeros(3, dtype=float)
        a = [x, a1, a2, a3]

        for t in range(1, len(a)):
            for i in range(a[t].size):
                for j in range(a[t-1].size):
                    a[t][i] += a[t-1][j] * model[t-1][i][j]
                if not t == 3:
                    a[t][i] = self.relu(a[t][i])

        argm = np.argmax(a[-1])
        if argm == 0:
            directionsList.append(JUMP)
        elif argm == 1:
            directionsList.append(LEFT)
        elif argm == 2:
            directionsList.append(RIGHT)

        return directionsList
