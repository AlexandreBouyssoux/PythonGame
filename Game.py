# -*- coding: utf-8 -*-

# import
import os
import Elements as Elts
import Interactions
import numpy as np

# constants
WINDOW_SIZE = Elts.WINDOW_SIZE
CAGE_BOX_H = Elts.CAGE_BOX_H
GAME_TIME = 5000
GAME_TICK = 60
GAME_MODES = ["First to 10", "Best in 2 min"]
DEFAULT_GAME_MODE = GAME_MODES[1]
PLAYER = Elts.PLAYER
AI = Elts.AI
GOAL = Elts.GOAL
JUMP = "jump"
LEFT = "left"
RIGHT = "right"
STATUS_PLAYER_1 = GOAL
STATUS_PLAYER_2 = AI
# class


class Game(object):
    def __init__(self, generationNumber, specie):
        self.player1 = Elts.Player()
        self.player1.setName("Player1")
        self.player2 = Elts.Player()
        self.player2.setName("Player2")
        self.listPlayer = [self.player1, self.player2]
        self.ball = Elts.Base()
        self.inter = Interactions.Interactions()
        self.gameTick = GAME_TICK
        self.gamemode = DEFAULT_GAME_MODE
        self.data = None
        self.goalPos = None

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

        self.selectPlayerStatus(STATUS_PLAYER_1, STATUS_PLAYER_2)
        self.player1.generation = generationNumber
        self.player2.generation = generationNumber
        self.player1.specie = specie
        self.player2.specie = specie
        self.setGame()

    def selectPlayerStatus(self, status1, status2):
        self.player1.setStatus(status1)
        self.player2.setStatus(status2)

    def setGame(self):
        """
        put players and ball on the right position
        """
        self.player1.setPosition(WINDOW_SIZE[0],
                                 WINDOW_SIZE[0])
        self.player2.setPosition(WINDOW_SIZE[-2],
                                 WINDOW_SIZE[0])
        self.ball.setPosition(WINDOW_SIZE[-2]/2,
                              WINDOW_SIZE[0])
        ballxSpeed = np.random.randint(-20, 20)
        self.ball.setSpeed(ballxSpeed, 0)
        self.goalPos = self.setGoalPos()

    def setGoalPos(self):
        x = np.random.randint(WINDOW_SIZE[2]/2,
                              WINDOW_SIZE[2])
        x = np.random.randint(0, WINDOW_SIZE[2]/2)
        b = np.random.randint(1)
        if b == 0:
            y = np.random.randint(WINDOW_SIZE[3]/2,
                                  WINDOW_SIZE[3])
        else:
            y = WINDOW_SIZE[3]
        goalPos = (x, y)

        return goalPos

    def getGoalPos(self):
        return self.goalPos

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
            self.player1.addHit()
            if verbose > 0:
                print("collision player1 w ball")
            self.inter.ballSpeedAfterCollision(self.ball, self.player1)

    def collisionPlayer2Ball(self, verbose=0):
        if self.inter.isCollision(self.player2, self.ball, verbose):
            self.player2.addHit()
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

    def computeFitness(self):
        """
        fitness is computed for player1
        """
        score1, score2 = self.getScore()
        hit = self.player2.getHit()

        if hit == 0:
            fitness = - 50
        else:
            fitness = hit + score2*10 - score1*5
        return fitness

    def isGameOver(self, time):
        endOfGame = False
        winner = None
        gamemode = self.gamemode
        score1, score2 = self.getScore()
        if gamemode == GAME_MODES[0]:
            # First player to score 10 goals win the game
            if score1 == 10:
                endOfGame = True
                winner = self.player1
                self.gameOver(winner)
            elif score2 == 10:
                endOfGame = True
                winner = self.player2
                self.gameOver(winner)
        elif gamemode == GAME_MODES[1]:
            # player with max score win
            if time >= GAME_TIME:
                endOfGame = True
                if score1 > score2:
                    winner = self.player1
                    self.gameOver(winner)
                elif score2 > score1:
                    winner = self.player2
                    self.gameOver(winner)
                else:
                    self.gameOver(None)
        return endOfGame, winner

    def gameOver(self, winner):
        _, _ = self.getScore(verbose=1)
        directory = r"C:\Users\alexa\Documents\PythonProjects\TestJeux"
        fitness = self.computeFitness()
        with open(os.path.join(directory, "fitness.txt"), "w") as file:
                file.write(str(fitness))
        if winner:
            print("Game over, Winner: {}".format(winner))

            if self.data is not None:
                filePath = os.path.join(directory, "data.txt")
                print(filePath)
                with open(filePath, "a") as f:
                    for dat in self.data:
                        f.write(" ".join(dat) + "\n")
        else:
            print("Game over, It's a draw")

    def setData(self, data):
        self.data = data
