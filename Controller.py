# -*- coding: utf-8 -*-

# imports
import Game
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

    def getPlayerInformations(self, player):
        return(player.getX(), player.getY(), player.getSize(),
               player.getColor())

    def movePlayer(self, direction, playerNumber=0):
        """
        direction doit être jump, left ou right
        """
        player = self.playerList[playerNumber]
        if direction.lower() == "jump":
            player.jump()
        elif direction.lower() == "left":
            player.moveLeft()
        elif direction.lower() == "right":
            player.moveRight()
        else:
            print("direction must be jump, left or right")
            sys.exit()

    def getPlayerList(self):
        return self.playerList

    def getPlayerPosition(self, player):
        player.updateXYPosition(verbose=0)
        return(player.getX(), player.getY())

    def getStringPlayerPosition(self, playerNumber=0):
        player = self.playerList[playerNumber]
        return player.getPosition()

    def getCageList(self):
        return(self.cageList)

    def collisions(self):
        self.game.isCollisionPlayer(verbose=1)
        self.game.collisionPlayer1Ball(verbose=1)
        self.game.collisionPlayer2Ball(verbose=1)
        self.game.collisionWithBox(verbose=1)
        self.game.goal(verbose=1)
