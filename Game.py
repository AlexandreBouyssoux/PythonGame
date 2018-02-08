# -*- coding: utf-8 -*-

# import
import sys
import os
import pickle
import Elements as Elts
import Interactions

# constants
WINDOW_SIZE = Elts.WINDOW_SIZE
CAGE_BOX_H = Elts.CAGE_BOX_H
GAME_TIME = 2*60000
GAME_TICK = 60
GAME_MODES = ["Premier à 10 (standard)", "Au temps en 2 min (standard)", 
              "Meilleur au score choisi", "Meilleur au temps choisi"]
DEFAULT_GAME_MODE = GAME_MODES[0]
AI = Elts.AI
PLAYER = Elts.PLAYER
JUMP = "jump"
LEFT = "left"
RIGHT = "right"
DIRECTORY = os.getcwd()
RESSOURCE = os.path.join(DIRECTORY, "Ressources")
# class


class Game(object):
    def __init__(self):
        self.stop = False
        self.player1 = Elts.Player()
        self.player1.setName("Player1")
        self.player2 = Elts.Player()
        self.player2.setName("Player2")
        self.listPlayer = [self.player1, self.player2]
        self.ball = Elts.Base()
        self.inter = Interactions.Interactions()
        self.gameTick = GAME_TICK
        self.gamemode = DEFAULT_GAME_MODE
        print("gamemode: {}".format(self.gamemode))
        self.limitTime = GAME_TIME
        self.limitScore = 10
        self.background = None

        self.player1.setColor([0, 0, 255])
        self.player2.setColor([255, 0, 0])

        self.cage1 = Elts.Box(Elts.CAGE_W, Elts.CAGE_H,
                              upRightCornerPos=(Elts.WINDOW_SIZE[0],
                                                Elts.WINDOW_SIZE[-1] -
                                                Elts.CAGE_H))
        self.cage1.setColor(self.player1.getColor())
        self.cage2 = Elts.Box(Elts.CAGE_W, Elts.CAGE_H,
                              upRightCornerPos=(Elts.WINDOW_SIZE[-2] -
                                                Elts.CAGE_W,
                                                Elts.WINDOW_SIZE[-1] -
                                                Elts.CAGE_H))
        self.cage2.setColor(self.player2.getColor())

        self.cageBox1 = Elts.Box(Elts.CAGE_W, CAGE_BOX_H, upRightCornerPos=(
                self.cage1.upRightCorner[0], self.cage1.upRightCorner[1] -
                CAGE_BOX_H))

        self.cageBox2 = Elts.Box(Elts.CAGE_W, CAGE_BOX_H, upRightCornerPos=(
                self.cage2.upRightCorner[0], self.cage2.upRightCorner[1] -
                CAGE_BOX_H))

        self.selectPlayerStatus(Elts.AI, Elts.AI)
        self.setGame()

    def setBackground(self, background):
        self.background = background

    def selectPlayerStatus(self, status1, status2):
        self.player1.setStatus(status1)
        self.player2.setStatus(status2)

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

    def resetGame(self):
        self.player1.score = 0
        self.player2.score = 0
        self.setGame()

    def getElements(self):
        return(self.player1, self.player2, self.ball)

    def getStaticElements(self):
        return(self.cage1, self.cage2, self.cageBox1, self.cageBox2)

    def getBoxes(self):
        return(self.cageBox1, self.cageBox2)

    def getScore(self, verbose=0):
        if verbose > 0:
            print("player1: {} | player2: {}".format(self.player1.score,
                  self.player2.score))
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
                print("player1 scores a goal {}".format(self.player1.score))
            self.setGame()

    def updateCageColor(self):
        self.cage1.setColor(self.player1.getColor())
        self.cage2.setColor(self.player2.getColor())

    def isGameOver(self, time):
        gamemode = self.gamemode
        score1, score2 = self.getScore()

        if gamemode == GAME_MODES[0]:
            # First player to score 10 goals win the game
            if score1 >= 10:
                self.setBestPerformance(self.player1, time)
                self.updateHighScore()
                self.gameOver(self.player1.name)
            elif score2 >= 10:
                self.setBestPerformance(self.player2, time)
                self.updateHighScore()
                self.gameOver(self.player2.name)
        elif gamemode == GAME_MODES[1]:
            # player with max score win
            if time >= GAME_TIME:
                if score1 > score2:
                    self.setBestPerformance(self.player1, score1)
                    self.updateHighScore()
                    self.gameOver(self.player1.name)
                elif score2 > score1:
                    self.setBestPerformance(self.player2, score2)
                    self.updateHighScore()
                    self.gameOver(self.player2.name)
                else:
                    self.gameOver(None)
        if gamemode == GAME_MODES[2]:
            # First player to score x goals win the game
            if score1 >= self.limitScore:
                self.gameOver(self.player1.name)
            elif score2 >= self.limitScore:
                self.gameOver(self.player2.name)
        elif gamemode == GAME_MODES[3]:
            # player with max score win
            if time >= self.limitTime:
                if score1 > score2:
                    self.gameOver(self.player1.name)
                elif score2 > score1:
                    self.gameOver(self.player2.name)
                else:
                    self.gameOver(None)

    def gameOver(self, winner):
        _, _ = self.getScore(verbose=1)
        self.stop = True
        if winner:
            print("Game over, Winner: {}".format(winner))
            print("||||||||||||||||||END|||||||||||||||||||")
        else:
            print("Game over, It's a draw")
            print("||||||||||||||||||END|||||||||||||||||||")
        self.resetGame()

    def setBestPerformance(self, player, perf):
        self.performance = (player.name, perf)

    def getBestPerformance(self):
        return self.performance

    def updateHighScore(self):
        highscoreFile = os.path.join(RESSOURCE, "highscore.dat")
        playerName, perf = self.getBestPerformance()
        dictHighscore = pickle.load(open(highscoreFile, "rb"))
        updateList = []
        if self.gamemode == GAME_MODES[0]:
            scoresList = dictHighscore["1"]
            scoresList.append((perf, playerName))
            scoresList.sort()
            updateList = scoresList[:5]
            dictHighscore["1"] = updateList

        elif self.gamemode == GAME_MODES[1]:
            scoresList = dictHighscore["2"]
            scoresList.append((perf, playerName))
            scoresList.sort(reverse=True)
            updateList = scoresList[:5]
            dictHighscore["2"] = updateList

        else:
            print("wrong gamemode detected, please verify")
            sys.exit()

        pickle.dump(dictHighscore, open(highscoreFile, "wb"))
