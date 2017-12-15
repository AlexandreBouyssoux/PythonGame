# -*- coding: utf-8 -*-

# import
import Elements
import Interactions
# constant
WINDOW_SIZE = Elements.WINDOW_SIZE
# class


class Game(object):
    def __init__(self):
        self.player1 = Elements.Player()
        self.player2 = Elements.Player()
        self.listPlayer = [self.player1, self.player2]
        self.ball = Elements.Base()
        self.inter = Interactions.Interactions()

        self.player1.setPosition(Elements.WINDOW_SIZE[0],
                                 Elements.WINDOW_SIZE[0])
        self.player1.setColor([0, 0, 255])
        self.player2.setPosition(Elements.WINDOW_SIZE[-2],
                                 Elements.WINDOW_SIZE[0])
        self.player2.setColor([255, 0, 0])
        self.ball.setPosition(Elements.WINDOW_SIZE[-2]/2,
                              Elements.WINDOW_SIZE[0])

    def getElements(self):
        return(self.player1, self.player2, self.ball)

    def isCollisionPlayer(self):
        if self.inter.isCollision(self.player1, self.player2):
            print("collision joueur")
        return self.inter.isCollision(self.player1, self.player2)

    def collisionPlayer1Ball(self):
        if self.inter.isCollision(self.player1, self.ball):
            self.inter.ballSpeedAfterCollision(self.ball, self.player1)

    def collisionPlayer2Ball(self):
        if self.inter.isCollision(self.player2, self.ball):
            self.inter.ballSpeedAfterCollision(self.ball, self.player2)
