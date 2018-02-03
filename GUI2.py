# -*- coding: utf-8 -*-

# import
import sys
from PyQt5.QtCore import qFatal, Qt, QTimer
from PyQt5.QtGui import QPen, QColor, QBrush, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsView,\
    QGraphicsScene, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel, \
    QTextEdit, QMenuBar, QLineEdit, QSpacerItem, QSizePolicy, QToolButton, \
    QMenu, QFrame
import Controller


# errors management
import traceback


def excepthook(type_, value, traceback_):
    traceback.print_exception(type_, value, traceback_)
    qFatal("")


sys.excepthook = excepthook

# CONSTANT
TITLE = "OL - FCN : jeu de foot"
COLOR_LIST = ["bleu", "rouge", "vert", "jaune"]

# class


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(TITLE)
        self.timer = QTimer()
        self.controller = Controller.Controller()
        self.centralWidget = Welcome(self, self.controller)
        self.setCentralWidget(self.centralWidget)


class Welcome(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.add(self)
        self.timer = QTimer()
        self.activePlayer1 = None
        self.activePlayer2 = None
        self.activeParam = None
        # self.activeGame = None

        # # #
        # # # Definition du layout Vertical Gauche
        # # #
        self.layoutVG = QVBoxLayout()
        self.spacerItem1 = QSpacerItem(5, 2, QSizePolicy.Maximum,
                                       QSizePolicy.Expanding)
        self.layoutVG.addItem(self.spacerItem1)

        # titre paramètre en gras
        self.parameters = QLabel("Paramètres")
        self.parameters.setFont(QFont("?", 14, QFont.Bold))
        self.layoutVG.addWidget(self.parameters)

        # fonctions clikables
        self.player1_human = lambda: self.setPlayer(1, "player")
        self.player1_robot = lambda: self.setPlayer(1, "ai")
        self.player2_human = lambda: self.setPlayer(2, "player")
        self.player2_robot = lambda: self.setPlayer(2, "ai")

        self.setPlayer1Name = lambda: self.setPlayerName(1,
                                            self.paramPlayer1NameEdit.text())
        self.setPlayer2Name = lambda: self.setPlayerName(2,
                                            self.paramPlayer2NameEdit.text())

        self.activateFrame1 = lambda: self.activate(1)
        self.activateFrame2 = lambda: self.activate(2)
        self.activateFrame3 = lambda: self.activate(3)
        self.unactivateFrame1 = lambda: self.unactivate(1)
        self.unactivateFrame2 = lambda: self.unactivate(2)
        self.unactivateFrame3 = lambda: self.unactivate(3)

        # paramètre joueurs
        self.paramPlayer_status = QLabel("Le joueur 1 est-t-il humain ou IA ?")

        self.paramPlayer1_human = QPushButton("Humain")
        self.paramPlayer1_human.clicked.connect(self.player1_human)
        self.paramPlayer1_robot = QPushButton("IA")
        self.paramPlayer1_robot.clicked.connect(self.player1_robot)

        self.paramPlayer2_human = QPushButton("Humain")
        self.paramPlayer2_human.clicked.connect(self.player2_human)
        self.paramPlayer2_robot = QPushButton("IA")
        self.paramPlayer2_robot.clicked.connect(self.player2_robot)

        self.paramPlayerName = QLabel("Nom")

        self.paramPlayer1NameEdit = QLineEdit("Joueur 1")
        self.paramPlayer1NameConfirm = QPushButton("Ok")
        self.paramPlayer1NameConfirm.clicked.connect(self.setPlayer1Name)

        self.paramPlayer2NameEdit = QLineEdit("Joueur 2")
        self.paramPlayer2NameConfirm = QPushButton("Ok")
        self.paramPlayer2NameConfirm.clicked.connect(self.setPlayer2Name)

        self.paramPlayerColorTitle = QLabel("Couleur (déroulez la flèche)")
        self.paramPlayer1Color = DropDownMenu(self, self.controller,
                                              "couleur", COLOR_LIST)
        self.paramPlayer2Color = DropDownMenu(self, self.controller,
                                              "couleur", COLOR_LIST)

        self.paramPlayer1_Ok = QPushButton("Valider")
        self.paramPlayer1_Ok.clicked.connect(self.unactivateFrame1)
        self.paramPlayer2_Ok = QPushButton("Valider")
        self.paramPlayer2_Ok.clicked.connect(self.unactivateFrame2)

        # bouton Joueur 1
        self.paramPlayer1 = QPushButton("Joueur 1")
        self.paramPlayer1.clicked.connect(self.activateFrame1)
        self.layoutVG.addWidget(self.paramPlayer1)

        # layer paramètre joueur 1
        self.frame1 = QFrame()
        self.layoutV1 = QVBoxLayout()
        self.frame1.setLayout(self.layoutV1)
        self.layoutV1.addWidget(self.paramPlayer_status)
        # under-layout: select player status
        self.underLayout1 = QHBoxLayout()
        self.underLayout1.addWidget(self.paramPlayer1_human)
        self.underLayout1.addWidget(self.paramPlayer1_robot)
        self.layoutV1.addLayout(self.underLayout1)
        # under-layout: select player name
        self.underLayout2 = QHBoxLayout()
        self.underLayout2.addWidget(self.paramPlayerName)
        self.underLayout2.addWidget(self.paramPlayer1NameEdit)
        self.underLayout2.addWidget(self.paramPlayer1NameConfirm)
        self.layoutV1.addLayout(self.underLayout2)
        # under-layout: select player color
        self.underLayout3 = QHBoxLayout()
        self.underLayout3.addWidget(self.paramPlayerColorTitle)
        self.underLayout3.addWidget(self.paramPlayer1Color)
        self.layoutV1.addLayout(self.underLayout3)

        self.layoutV1.addWidget(self.paramPlayer1_Ok)
        self.frame1.hide()
        self.layoutVG.addWidget(self.frame1)

        # bouton Joueur 2
        self.paramPlayer2 = QPushButton("Joueur 2")
        self.paramPlayer2.clicked.connect(self.activateFrame2)
        self.layoutVG.addWidget(self.paramPlayer2)

        # layer paramètre joueur 2
        self.frame2 = QFrame()
        self.layoutV2 = QVBoxLayout()
        self.frame2.setLayout(self.layoutV2)
        self.layoutV2.addWidget(self.paramPlayer_status)
        # under-layout: select player status
        self.underLayout1 = QHBoxLayout()
        self.underLayout1.addWidget(self.paramPlayer2_human)
        self.underLayout1.addWidget(self.paramPlayer2_robot)
        self.layoutV2.addLayout(self.underLayout1)
        # under-layout: select player name
        self.underLayout2 = QHBoxLayout()
        self.underLayout2.addWidget(self.paramPlayerName)
        self.underLayout2.addWidget(self.paramPlayer2NameEdit)
        self.underLayout2.addWidget(self.paramPlayer2NameConfirm)
        self.layoutV2.addLayout(self.underLayout2)
        # under-layout: select player color
        self.underLayout3 = QHBoxLayout()
        self.underLayout3.addWidget(self.paramPlayerColorTitle)
        self.underLayout3.addWidget(self.paramPlayer2Color)
        self.layoutV2.addLayout(self.underLayout3)

        self.layoutV2.addWidget(self.paramPlayer2_Ok)
        self.frame2.hide()
        self.layoutVG.addWidget(self.frame2)

        # bouton paramètre game
        self.paramGame = QPushButton("Paramètres du jeu")
        self.paramGame.clicked.connect(self.activateFrame3)
        self.layoutVG.addWidget(self.paramGame)

        # paramètre game
        self.paramGame_title = QLabel("Mode de jeu : (déroulez la flèche)")
        self.paramGame_menu = DropDownMenu(self, self.controller,
                                           "mode", ["Au temps", "Au score"])

        self.design_title = QLabel("Fond du jeu : (déroulez la flèche)")
        self.design_menu = DropDownMenu(self, self.controller,
                                        "fond", ["A", "B"])

        self.paramGame_Ok = QPushButton("Valider")
        self.paramGame_Ok.clicked.connect(self.unactivateFrame3)

        # layout paramètre game
        self.frame3 = QFrame()
        self.layoutV3 = QVBoxLayout()
        self.frame3.setLayout(self.layoutV3)
        self.layoutV3.addWidget(self.paramGame)
        self.layoutV3.addWidget(self.paramGame_title)
        self.layoutV3.addWidget(self.paramGame_menu)
        self.layoutV3.addWidget(self.design_title)
        self.layoutV3.addWidget(self.design_menu)
        self.layoutV3.addWidget(self.paramGame_Ok)

        self.frame3.hide()
        self.layoutVG.addWidget(self.frame3)

        self.layoutVG.addItem(self.spacerItem1)

        self.score1 = QLabel("Score : ")
        self.score2 = QLineEdit("{} : {} \ {} : {}".format(
                                    self.controller.playerList[0].name,
                                    self.controller.playerList[0].score,
                                    self.controller.playerList[1].name,
                                    self.controller.playerList[1].score))

        self.launch = QPushButton("Lancer une partie")
        self.launch.clicked.connect(self.launchGame)

        self.leave = QPushButton("Quitter")
        self.leave.clicked.connect(self.leaveGame)

        self.highScore = QLabel("Meilleur score {} : {}".format(
                                self.controller.game.gamemode,
                                self.controller.bestScore))

        self.view = GraphicView(self, self.timer, self.controller)

        layoutH1 = QHBoxLayout()
        layoutH1.addWidget(self.launch)
        layoutH1.addWidget(self.leave)
        layoutH1.addWidget(self.highScore)

        layoutH2 = QHBoxLayout()
        layoutH2.addWidget(self.score1)
        layoutH2.addWidget(self.score2)

        layoutVD = QVBoxLayout()
        layoutVD.addLayout(layoutH1)
        layoutVD.addWidget(self.view)
        layoutVD.addLayout(layoutH2)
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.layoutVG)
        self.mainLayout.addLayout(layoutVD)
        self.setLayout(self.mainLayout)

        self.controller.refresh()

    def refresh(self):
        self.score2 = QLineEdit("{} : {} \ {} : {}".format(
                                    self.controller.playerList[0].name,
                                    self.controller.playerList[0].score,
                                    self.controller.playerList[1].name,
                                    self.controller.playerList[1].score))

    # mode de jeu
    def activate(self, number):
        if number == 1:
            self.frame1.show()
        elif number == 2:
            self.frame2.show()
        elif number == 3:
            self.frame3.show()

    def unactivate(self, number):
        if number == 1:
            self.frame1.hide()
        elif number == 2:
            self.frame2.hide()
        elif number == 3:
            self.frame3.hide()

    def setPlayer(self, playerNum, playerType):
        """
        define if player is robot or human (user choice)
        """
        self.controller.setPlayer(playerNum, playerType)
        self.controller.refresh()

    def setPlayerName(self, playerNum, name):
        self.controller.setPlayerName(playerNum, name)
        self.controller.refresh()

    def setGameType(self, num):
        self.controller.setGameType(self, num)
        self.controller.upDateBest(self, num)
        self.controller.refresh()

    def showScores(self):
        pass

    def launchGame(self):
        self.removeWidget(self.layoutVG)

    def leaveGame(self):
        pass


class DropDownMenu(QWidget):
    def __init__(self, parent, controller, name, items=[]):
        super().__init__(parent)
        self.name = name
        self.menuLayout = QVBoxLayout()
        self.menu = QMenu()
        self.controller = controller
        self.controller.add(self)

        for i in items:
            self.menu.addAction(i)

        self.button = QToolButton(self)
        self.button.setStyleSheet("border: 0px; padding: 0px;")
        self.button.setCursor(Qt.ArrowCursor)
        # self.button.setText(self.name)
        self.button.triggered.connect(lambda: self.menuActionTriggered(i))
        self.button.setPopupMode(QToolButton.InstantPopup)
        self.button.setMenu(self.menu)
        self.menuLayout.addWidget(self.button)
        self.setLayout(self.menuLayout)

    def menuActionTriggered(self, item):
        if self.name == "couleur 1":
            self.controller.setPlayerColor(1, item)
        if self.name == "couleur 2":
            self.controller.setPlayerColor(2, item)
        if self.name == "mode":
            self.controller.setGameType(item)
        if self.name == "fond":
            self.controller.setBackground(item)

    def refresh(self):
        pass


class GraphicView(QGraphicsView):
    def __init__(self, parent, timer, controller):
        super().__init__(parent)
        self.mainScene = GraphicScene(self, timer, controller)
        self.setScene(self.mainScene)


class GraphicScene(QGraphicsScene):
    def __init__(self, parent, timer, controller):
        super().__init__(parent)
        self.c = controller
        self.c.add(self)
        self.timer = timer
        self.setSceneRect(*self.c.WINDOW_SIZE)

        for cage in self.c.getCageList():
            pen = QPen(QColor(0, 0, 0), 1, Qt.DotLine)
            brush = QBrush(QColor(*cage.color), Qt.SolidPattern)
            self.addRect(*cage.upRightCorner, cage.w, cage.h, pen, brush)

        self.dictEllipse = {}
        for player in self.c.getPlayerList():
            playerX, playerY, playerSize, playerColor = \
                self.c.getPlayerInformations(player)
            pen = QPen(QColor(*playerColor), 1, Qt.SolidLine)
            brush = QBrush(QColor(*playerColor), Qt.SolidPattern)
            self.dictEllipse[player] = (self.addEllipse(0, 0, playerSize,
                                                        playerSize, pen,
                                                        brush))

        self.c.refresh()
        self.timer.timeout.connect(self.updateTimer)
        self.timer.start(self.c.game.gameTick)

    def updateTimer(self):
        self.c.refresh()

    def keyPressEvent(self, event):
        if not self.c.isAI(0):
            if event.key() == Qt.Key_Up:
                self.c.movePlayer(self.c.JUMP, 0)
                self.c.refresh()

            if event.key() == Qt.Key_Left:
                self.c.movePlayer(self.c.LEFT, 0)
                self.c.refresh()

            if event.key() == Qt.Key_Right:
                self.c.movePlayer(self.c.RIGHT, 0)
                self.c.refresh()

        if not self.c.isAI(1):
            if event.key() == Qt.Key_Z:
                self.c.movePlayer(self.c.JUMP, 1)
                self.c.refresh()

            if event.key() == Qt.Key_Q:
                self.c.movePlayer(self.c.LEFT, 1)
                self.c.refresh()

            if event.key() == Qt.Key_D:
                self.c.movePlayer(self.c.RIGHT, 1)
                self.c.refresh()

    def refresh(self):
        self.c.moveAI()
        self.c.collisions()
        for player in self.c.getPlayerList():
            playerX, playerY = self.c.getPlayerPosition(player)
            self.dictEllipse[player].setPos(playerX, playerY)
        self.c.updateTime()
        self.c.checkEndOfGame()


# launch the GUI


def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
