# -*- coding: utf-8 -*-

# imports
import Game
import Bot
import sys
import os
import pickle

# constants
AI = Game.AI
PLAYER = Game.PLAYER
COLOR_LIST = ["OL", "SR", "ASSE", "FCN"]
BACKGROUND_LIST = ["Parc OL", "Roazhon Park", "Geoffroy Guichard",
                   "La Beaujoire"]
RESSOURCE = Game.RESSOURCE

JOUEUR_OL = os.path.join(RESSOURCE, 'Joueur_OL.png')
JOUEUR_SR = os.path.join(RESSOURCE, 'Joueur_SR.png')
JOUEUR_ASSE = os.path.join(RESSOURCE, 'Joueur_ASSE.png')
JOUEUR_FCN = os.path.join(RESSOURCE, 'Joueur_FCN.png')

STADE_OL = os.path.join(RESSOURCE, "Stade_OL.jpg")
STADE_SR = os.path.join(RESSOURCE, "Stade_SR.jpg")
STADE_ASSE = os.path.join(RESSOURCE, "Stade_ASSE.jpg")
STADE_FCN = os.path.join(RESSOURCE, "Stade_FCN.jpg")

DICT_TEAM = {"OL": JOUEUR_OL,
             "SR": JOUEUR_SR,
             "ASSE": JOUEUR_ASSE,
             "FCN": JOUEUR_FCN}

DICT_STADE = {"Parc OL": STADE_OL,
              "Roazhon Park": STADE_SR,
              "Geoffroy Guichard": STADE_ASSE,
              "La Beaujoire": STADE_FCN}

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
        self.run = False

    def setGame(self):
        self.run = False
        self.time = 0
        self.game.resetGame()
        self.run = True

    def pause(self):
        if self.run is True:
            self.run = False
        else:
            self.run = True

    def stop(self):
        if self.game.stop is True:
            self.run = False

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
                # directionsList = bot.giveDirections2(generation=0, specie=i)
                directionsList = bot.giveDirections()
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

    def getTime(self):
        time = self.convertTime(self.time)
        return time

    def convertTime(self, time):
        """
        return time under form: 00:00:00
        """
        nbrSecondes = time // 1000
        nbrMillisecondes = time % 1000
        nbrMinutes = nbrSecondes // 60
        nbrSecondes = nbrSecondes % 60
        listeTime = [nbrMinutes, nbrSecondes, nbrMillisecondes]

        for i, nbr in enumerate(listeTime):
            if nbr < 10:
                result = "0" + str(nbr)
            else:
                result = str(nbr)
            listeTime[i] = result

        strTime = ":".join(listeTime)
        return strTime

    def checkEndOfGame(self):
        self.game.isGameOver(self.time)
        self.stop()

    def setPlayer(self, playerNum, playerType):
        """
        définit si le joueur est un robot ou un humain (choix de
        l'utilisateur)
        """
        player = self.playerList[playerNum]
        player.setStatus(playerType)

    def setPlayerName(self, playerNum, name):
        player = self.playerList[playerNum]
        player.setName(str(name))

    def setPlayerColor(self, playerNum, couleur):
        player = self.playerList[playerNum]
        if couleur == COLOR_LIST[0]:
            player.setColor((0, 0, 255))
        elif couleur == COLOR_LIST[1]:
            player.setColor((255, 0, 0))
        elif couleur == COLOR_LIST[2]:
            player.setColor((0, 255, 0))
        elif couleur == COLOR_LIST[3]:
            player.setColor((255, 255, 0))
        self.game.updateCageColor()
        if couleur in COLOR_LIST:
            image = DICT_TEAM[couleur]
            player.setImage(image)

    def setGameType(self, num):
        print(Game.GAME_MODES[num])
        self.game.gamemode = Game.GAME_MODES[num]

    def setBackground(self, item):
        print(item)
        background = DICT_STADE[item]
        self.game.setBackground(background)

    def getHighScore(self):
        highscoreFile = os.path.join(RESSOURCE, "highscore.dat")
        dictHighscore = pickle.load(open(highscoreFile, "rb"))
        dictForDisplay = {}
        listScore_gm1 = []
        listScore_gm2 = []

        for element in dictHighscore["1"]:
            string = str(element[1]) + " : " + self.convertTime(element[0])
            listScore_gm1.append(string)
        for element in dictHighscore["2"]:
            string = str(element[1]) + " : " + str(element[0])
            listScore_gm2.append(string)
        dictForDisplay[0] = listScore_gm1
        dictForDisplay[1] = listScore_gm2

        return dictForDisplay

    def resetHighScore(self):
        highscoreFile = os.path.join(RESSOURCE, "highscore.dat")
        dictHighScore = {"1": [(999999, ""),
                               (999999, ""),
                               (999999, ""),
                               (999999, ""),
                               (999999, "")],
                         "2": [(0, ""),
                               (0, ""),
                               (0, ""),
                               (0, ""),
                               (0, "")]
                         }
        pickle.dump(dictHighScore, open(highscoreFile, "wb"))


if __name__ == "__main__":
    c = Controller()
#    c.resetHighScore()
