# -*- coding: utf-8 -*-

# import
import Elements
from Interactions import Interactions
# constant
WINDOW_SIZE = Elements.WINDOW_SIZE
# class


class Game(object):
    def __init__(self):
        self.player1 = Elements.Player()
        self.player2 = Elements.Player()
        self.listPlayer = [self.player1, self.player2]
        self.ball = Elements.Base()

        self.player1.setPosition(Elements.WINDOW_SIZE[0],
                                 Elements.WINDOW_SIZE[0])
        self.player2.setPosition(Elements.WINDOW_SIZE[-2],
                                 Elements.WINDOW_SIZE[0])
        self.ball.setPosition(Elements.WINDOW_SIZE[-2]/2,
                              Elements.WINDOW_SIZE[0])

    def getElements(self):
        return(self.player1, self.player2, self.ball)

    def isCollisionPlayer(self):
        if Interactions.isCollision(self.player1, self.player2):
            print("collision joueur")
        return Interactions.isCollision(self.player1, self.player2)

    def collisionPlayer1Ball(self):
        if Interactions.isCollision(self.player1, self.ball):
            Interactions.ballSpeedAfterCollision(self.ball, self.player1)

    def collisionPlayer2Ball(self):
        if Interactions.isCollision(self.player2, self.ball):
            Interactions.ballSpeedAfterCollision(self.ball, self.player2)
