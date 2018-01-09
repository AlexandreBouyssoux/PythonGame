# -*- coding: utf-8 -*-

# import
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

        self.botPos = None
        self.advPos = None
        self.ballPos = None
        self.advCagePos = None

        self.updateInformations()

    def updateInformations(self):
        self.botPos = (self.bot.getX(), self.bot.getY())
        self.advPos = (self.adv.getX(), self.adv.getY())
        self.ballPos = (self.ball.getX(), self.ball.getY())
        self.advCagePos = self.advCage.upRightCorner

    def giveDirections(self, verbose=0):
        """
        return a list of direction depending on the relative position of the
        ball
        """
        directionsList = []
        if self.botPos[1] >= self.ballPos[1]:
            directionsList.append(JUMP)
        if self.botPos[0] < self.ballPos[0]:
            directionsList.append(RIGHT)
        elif self.botPos[0] > self.ballPos[0]:
            directionsList.append(LEFT)

        if verbose > 0:
            print("boty = {} | bally = {}".format(self.botPos[1],
                  self.ballPos[1]))
            print("botx = {} | ballx = {}".format(self.botPos[0],
                  self.ballPos[0]))

        self.updateInformations()
        return directionsList
