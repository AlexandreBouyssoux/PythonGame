# -*- coding: utf-8 -*-

# imports
import Game
import Bot
import sys

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
    def __init__(self):
        super().__init__()
        self.joueurList = []
        self.WINDOW_SIZE = Game.WINDOW_SIZE
        self.game = Game.Game()
        self.playerList = self.game.getElements()
        self.cageList = self.game.getStaticElements()
        self.botList = [None, None]
        self.time = 0
        self.JUMP = Game.JUMP
        self.LEFT = Game.LEFT
        self.RIGHT = Game.RIGHT
        self.createBot()

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

    def moveAI(self):
        for i, player in enumerate(self.playerList):
            if self.isAI(i):
                bot = self.botList[i]
                directionsList = bot.giveDirections(verbose=1)
                print(directionsList)
                for direction in directionsList:
                    self.movePlayer(direction, i)

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
        self.game.isGameOver(self.time)
