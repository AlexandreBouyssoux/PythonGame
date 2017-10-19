# -*- coding: utf-8 -*-

# import
import Elements
# import Interactions
# constant
WINDOW_SIZE = Elements.WINDOW_SIZE
# class


class Game(object):
    def __init__(self):
        self.player1 = Elements.Player()
        self.player2 = Elements.Player()
        self.listPlayer = [self.player1, self.player2]
        self.ball = Elements.Base()

    def getElements(self):
        return(self.player1, self.player2, self.ball)
