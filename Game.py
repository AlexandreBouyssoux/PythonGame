# -*- coding: utf-8 -*-

# import
import Elements as Elts
import Interactions

# constants
WINDOW_SIZE = Elts.WINDOW_SIZE
CAGE_BOX_H = 10

# class


class Game(object):
    def __init__(self):
        self.player1 = Elts.Player()
        self.player2 = Elts.Player()
        self.listPlayer = [self.player1, self.player2]
        self.ball = Elts.Base()
        self.inter = Interactions.Interactions()

        self.player1.setColor([0, 0, 255])
        self.player2.setColor([255, 0, 0])

        self.cage1 = Elts.Box(Elts.CAGE_W, Elts.CAGE_H,
                              upRightCornerPos=(Elts.WINDOW_SIZE[0],
                                                Elts.WINDOW_SIZE[-1] -
                                                Elts.CAGE_H))
        self.cage1.setColor((0, 255, 0))
        self.cage2 = Elts.Box(Elts.CAGE_W, Elts.CAGE_H,
                              upRightCornerPos=(Elts.WINDOW_SIZE[-2] -
                                                Elts.CAGE_W,
                                                Elts.WINDOW_SIZE[-1] -
                                                Elts.CAGE_H))
        self.cage2.setColor((0, 255, 0))

        self.cageBox1 = Elts.Box(Elts.CAGE_W, CAGE_BOX_H, upRightCornerPos=(
                self.cage1.upRightCorner[0], self.cage1.upRightCorner[1] -
                CAGE_BOX_H))

        self.cageBox2 = Elts.Box(Elts.CAGE_W, CAGE_BOX_H, upRightCornerPos=(
                self.cage2.upRightCorner[0], self.cage2.upRightCorner[1] -
                CAGE_BOX_H))

        self.setGame()

    def setGame(self):
        """
        put players and ball on the right position
        """
        self.player1.setPosition(Elts.WINDOW_SIZE[0],
                                 Elts.WINDOW_SIZE[0])
        self.player2.setPosition(Elts.WINDOW_SIZE[-2],
                                 Elts.WINDOW_SIZE[0])
        self.ball.setPosition(Elts.WINDOW_SIZE[-2]/2,
                              Elts.WINDOW_SIZE[0])
        self.ball.setSpeed(0, 0)

    def getElements(self):
        return(self.player1, self.player2, self.ball)

    def getStaticElements(self):
        return(self.cage1, self.cage2, self.cageBox1, self.cageBox2)

    def getBoxes(self):
        return(self.cageBox1, self.cageBox2)

    def getScore(self):
        return(self.player1.score, self.player2.score)

    def isCollisionPlayer(self, verbose=0):
        if self.inter.isCollision(self.player1, self.player2, verbose):
            if verbose > 0:
                print("collision player1 w player2")
            self.inter.playerBehaviorAfterCollision(self.player1, self.player2)

    def collisionPlayer1Ball(self, verbose=0):
        if self.inter.isCollision(self.player1, self.ball, verbose):
            if verbose > 0:
                print("collision player1 w ball")
            self.inter.ballSpeedAfterCollision(self.ball, self.player1)

    def collisionPlayer2Ball(self, verbose=0):
        if self.inter.isCollision(self.player2, self.ball, verbose):
            if verbose > 0:
                print("collision player2 w ball")
            self.inter.ballSpeedAfterCollision(self.ball, self.player2)

    def collisionWithBox(self, verbose=0):
        for box in self.getBoxes():
            for base in self.getElements():
                self.inter.collisionWithBox(box, base, verbose)

    def goal(self, verbose=0):
        if self.inter.isBallintoCage(self.cage1, self.ball):
            self.player2.scores()
            if verbose > 0:
                print("player2 scores a goal")
            self.setGame()
        if self.inter.isBallintoCage(self.cage2, self.ball):
            self.player1.scores()
            if verbose > 0:
                print("player1 scores a goal")
            self.setGame()
