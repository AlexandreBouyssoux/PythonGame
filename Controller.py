# -*- coding: utf-8 -*-

# imports
import Game
import Bot
import sys
import os
from keras.models import load_model

# constant
dictDirection = {
        Game.JUMP: 0,
        Game.LEFT: 1,
        Game.RIGHT: 2,
        }
DIRECTORY = r"C:\Users\alexa\Documents\PythonProjects\TestJeux"
# class


class ControllerBase:
    def __init__(self):
        self.listClient = []

    def add(self, client):
        self.listClient.append(client)

    def refresh(self):
        for client in self.listClient:
            client.refresh()


class Controller(ControllerBase):
    def __init__(self, generationNumber, specie):
        super().__init__()
        self.joueurList = []
        self.WINDOW_SIZE = Game.WINDOW_SIZE
        self.game = Game.Game(generationNumber, specie)
        self.playerList = self.game.getElements()
        self.cageList = self.game.getStaticElements()
        self.botList = [None, None]
        self.time = 0
        self.JUMP = Game.JUMP
        self.LEFT = Game.LEFT
        self.RIGHT = Game.RIGHT
        self.createBot()
        self.data = []
        self.model = None

    def getPlayerInformations(self, player):
        drawPoint = player.getDrawPoint()
        return(drawPoint[0], drawPoint[1], player.getSize(),
               player.getColor())

    def movePlayer(self, direction, playerNumber=0):
        """
        direction doit être jump, left ou right
        """
        player = self.playerList[playerNumber]
        if direction.lower() == self.JUMP:
            player.jump()
        elif direction.lower() == self.LEFT:
            player.moveLeft()
        elif direction.lower() == self.RIGHT:
            player.moveRight()
        else:
            print("direction must be jump, left or right")
            sys.exit()

    def isAI(self, playerNumber=0):
        """
        return True is the player is an AI
        """
        isAI = False
        player = self.playerList[playerNumber]
        if player.status == Game.AI:
            isAI = True
        return isAI

    def createBot(self):
        """
        create bot
        """
        for i, player in enumerate(self.playerList):
            if player.status == Game.AI:
                self.botList[i] = Bot.Bot(self.game, player)

    def moveAI(self, mode=0):
        for i, player in enumerate(self.playerList):
            if self.isAI(i):
                bot = self.botList[i]
                if mode == 0:
                    if self.model is None:
                        genPath = os.path.join(DIRECTORY, "GEN_" +
                                               str(player.generation))
                        os.chdir(genPath)
                        modelName = "_".join(["model", str(player.specie)])
                        self.model = load_model(modelName)
                    directionsList = bot.giveDirections2(self.model)
                elif mode == 1:
                    directionsList = bot.giveDirections()
                for direction in directionsList:
                    self.movePlayer(direction, i)

    def isGOAL(self, playerNumber=0):
        """
        return True is the player is an AI
        """
        isGOAL = False
        player = self.playerList[playerNumber]
        if player.status == Game.GOAL:
            isGOAL = True
        return isGOAL

    def placeGoal(self):
        for i, player in enumerate(self.playerList):
            if self.isGOAL(i):
                x, y = self.game.getGoalPos()
                player.setPosition(x, y)
                player.setSpeed(0, 0)

    def getPlayerList(self):
        return self.playerList

    def getPlayerPosition(self, player):
        player.updateXYPosition(verbose=0)
        drawPoint = player.getDrawPoint()
        return(drawPoint[0], drawPoint[1])

    def getCageList(self):
        return(self.cageList)

    def collisions(self):
        self.game.isCollisionPlayer(verbose=1)
        self.game.collisionPlayer1Ball(verbose=1)
        self.game.collisionPlayer2Ball(verbose=1)
        self.game.collisionWithBox(verbose=1)
        self.game.goal(verbose=1)

    def updateTime(self):
        self.time += self.game.gameTick

    def checkEndOfGame(self):
        endOfGame, winner = self.game.isGameOver(self.time)
        return endOfGame

    def saveData(self, direction):

        botInformation = Bot.Bot(self.game, self.playerList[0])
        botInformation.updateDifferenceInformations()
        goalOrientation = botInformation.goalOrientation
        xDistanceBotBall = botInformation.xDistanceBotBall
        yDistanceBotBall = botInformation.yDistanceBotBall
        xDistanceBotAdv = botInformation.xDistanceBotAdv
        yDistanceBotAdv = botInformation.yDistanceBotAdv

        self.data.append([str(goalOrientation), str(xDistanceBotBall),
                          str(yDistanceBotBall), str(xDistanceBotAdv),
                          str(yDistanceBotAdv), str(dictDirection[direction])])

        self.sendDataToGame()

    def sendDataToGame(self):
        self.game.setData(self.data)
