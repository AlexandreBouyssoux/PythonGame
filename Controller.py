# -*- coding: utf-8 -*-

# imports
import Elements
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
        self.WINDOW_SIZE = Elements.WINDOW_SIZE

    def createJoueur(self):
        newJoueur = Elements.Player()
        self.joueurList.append(newJoueur)
        return(newJoueur)

    def getJoueurInformations(self, joueurNumber=0):
        joueur = self.joueurList[joueurNumber]
        return(joueur.getX(), joueur.getY(), joueur.getSize(),
               joueur.getColor())

    def moveJoueur(self, direction, joueurNumber=0):
        """
        direction doit être jump, left ou right
        """
        joueur = self.joueurList[joueurNumber]
        if direction.lower() == "jump":
            joueur.jump()
        elif direction.lower() == "left":
            joueur.moveLeft()
        elif direction.lower() == "right":
            joueur.moveRight()
        else:
            print("direction must be jump, left or right")
            sys.exit()

    def getJoueurPosition(self, joueurNumber=0):
        joueur = self.joueurList[joueurNumber]
        joueur.updateYPosition()
        return(joueur.getX(), joueur.getY())

    def getStringJoueurPosition(self, joueurNumber=0):
        joueur = self.joueurList[joueurNumber]
        return joueur.getPosition()
