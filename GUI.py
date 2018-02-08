# -*- coding: utf-8 -*-

# import
import sys
from PyQt5.QtCore import qFatal, Qt, QTimer
from PyQt5.QtGui import QPen, QColor, QBrush, QFont, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsView,\
    QGraphicsScene, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel, \
    QTextEdit, QMenuBar, QLineEdit, QSpacerItem, QSizePolicy, QToolButton, \
    QMenu, QFrame, QComboBox, QSlider
import Controller


# errors management
import traceback


def excepthook(type_, value, traceback_):
    traceback.print_exception(type_, value, traceback_)
    qFatal("")


sys.excepthook = excepthook

# CONSTANT
TITLE = "OL - FCN : jeu de foot"
COLOR_LIST = Controller.COLOR_LIST
GAMEMODES = Controller.GAME_MODES
BACKGROUND_LIST = Controller.BACKGROUND_LIST

# class


class mainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.setWindowTitle(TITLE)
        self.timer = QTimer()
        self.controller = Controller.Controller()
        self.centralWidget = Welcome(self, self.controller, app)
        self.setCentralWidget(self.centralWidget)


class Welcome(QWidget):
    def __init__(self, parent, controller, app):
        super().__init__(parent)
        self.controller = controller
        self.controller.add(self)
        self.timer = QTimer()
        self.app = app
        self.activeHighScore = False

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

        # fonctions cliquables
        self.player1_human = lambda: self.setPlayer(0, Controller.PLAYER)
        self.player1_robot = lambda: self.setPlayer(0, Controller.AI)
        self.player2_human = lambda: self.setPlayer(1, Controller.PLAYER)
        self.player2_robot = lambda: self.setPlayer(1, Controller.AI)

        self.setPlayer1Name = lambda: self.setPlayerName(0,
                                            self.paramPlayer1NameEdit.text())
        self.setPlayer2Name = lambda: self.setPlayerName(1,
                                            self.paramPlayer2NameEdit.text())

        self.activateFrame1 = lambda: self.activate(1)
        self.activateFrame2 = lambda: self.activate(2)
        self.activateFrame3 = lambda: self.activate(3)
        self.unactivateFrame1 = lambda: self.unactivate(1)
        self.unactivateFrame2 = lambda: self.unactivate(2)
        self.unactivateFrame3 = lambda: self.unactivate(3)

        # paramètre joueurs
        self.paramPlayer1_stat = QLabel("Le joueur 1 est-t-il humain ou IA ?")
        self.paramPlayer2_stat = QLabel("Le joueur 2 est-t-il humain ou IA ?")

        self.paramPlayer1_human = QPushButton("Humain")
        self.paramPlayer1_human.clicked.connect(self.player1_human)
        self.paramPlayer1_robot = QPushButton("IA")
        self.paramPlayer1_robot.clicked.connect(self.player1_robot)

        self.paramPlayer2_human = QPushButton("Humain")
        self.paramPlayer2_human.clicked.connect(self.player2_human)
        self.paramPlayer2_robot = QPushButton("IA")
        self.paramPlayer2_robot.clicked.connect(self.player2_robot)

        self.paramPlayer1Name = QLabel("Nom")
        self.paramPlayer2Name = QLabel("Nom")

        self.paramPlayer1NameEdit = QLineEdit("Joueur 1")
        self.paramPlayer1NameConfirm = QPushButton("Ok")
        self.paramPlayer1NameConfirm.clicked.connect(self.setPlayer1Name)

        self.paramPlayer2NameEdit = QLineEdit("Joueur 2")
        self.paramPlayer2NameConfirm = QPushButton("Ok")
        self.paramPlayer2NameConfirm.clicked.connect(self.setPlayer2Name)

        self.paramPlayer1ColorTitle = QLabel("Couleur")
        self.paramPlayer2ColorTitle = QLabel("Couleur")

        self.paramPlayer1Color = DropDownMenu(self, self.controller,
                                              "couleur 1", COLOR_LIST)
        self.paramPlayer2Color = DropDownMenu(self, self.controller,
                                              "couleur 2", COLOR_LIST)

        self.paramPlayer1_Ok = QPushButton("Valider")
        self.paramPlayer1_Ok.clicked.connect(self.unactivateFrame1)
        self.paramPlayer2_Ok = QPushButton("Valider")
        self.paramPlayer2_Ok.clicked.connect(self.unactivateFrame2)
        
        self.player1Buttons = QLabel("Utiliser les flèches pour jouer")
        self.player2Buttons = QLabel("Utliser les touches Z Q S D pour jouer")

        # bouton Joueur 1
        self.paramPlayer1 = QPushButton("Joueur 1")
        self.paramPlayer1.clicked.connect(self.activateFrame1)
        self.layoutVG.addWidget(self.paramPlayer1)

        # layer paramètre joueur 1
        self.frame1 = QFrame()
        self.layoutV1 = QVBoxLayout()
        self.frame1.setLayout(self.layoutV1)
        self.layoutV1.addWidget(self.paramPlayer1_stat)
        # under-layout: select player status
        self.underLayout1 = QHBoxLayout()
        self.underLayout1.addWidget(self.paramPlayer1_human)
        self.underLayout1.addWidget(self.paramPlayer1_robot)
        self.layoutV1.addLayout(self.underLayout1)
        # under-layout: select player name
        self.underLayout2 = QHBoxLayout()
        self.underLayout2.addWidget(self.paramPlayer1Name)
        self.underLayout2.addWidget(self.paramPlayer1NameEdit)
        self.underLayout2.addWidget(self.paramPlayer1NameConfirm)
        self.layoutV1.addLayout(self.underLayout2)
        # under-layout: select player color
        self.underLayout3 = QHBoxLayout()
        self.underLayout3.addWidget(self.paramPlayer1ColorTitle)
        self.underLayout3.addWidget(self.paramPlayer1Color)
        self.layoutV1.addLayout(self.underLayout3)

        self.layoutV1.addWidget(self.paramPlayer1_Ok)
        self.frame1.hide()
        self.layoutVG.addWidget(self.frame1)
        
        self.frame1_1 = QFrame()
        self.underLayout4 = QHBoxLayout()
        self.frame1_1.setLayout(self.underLayout4)
        self.underLayout4.addWidget(self.player1Buttons)
        self.frame1_1.hide()
        self.layoutVG.addWidget(self.frame1_1)

        # bouton Joueur 2
        self.paramPlayer2 = QPushButton("Joueur 2")
        self.paramPlayer2.clicked.connect(self.activateFrame2)
        self.layoutVG.addWidget(self.paramPlayer2)

        # layer paramètre joueur 2
        self.frame2 = QFrame()
        self.layoutV2 = QVBoxLayout()
        self.frame2.setLayout(self.layoutV2)
        self.layoutV2.addWidget(self.paramPlayer2_stat)
        # under-layout: select player status
        self.underLayout1 = QHBoxLayout()
        self.underLayout1.addWidget(self.paramPlayer2_human)
        self.underLayout1.addWidget(self.paramPlayer2_robot)
        self.layoutV2.addLayout(self.underLayout1)
        # under-layout: select player name
        self.underLayout2 = QHBoxLayout()
        self.underLayout2.addWidget(self.paramPlayer2Name)
        self.underLayout2.addWidget(self.paramPlayer2NameEdit)
        self.underLayout2.addWidget(self.paramPlayer2NameConfirm)
        self.layoutV2.addLayout(self.underLayout2)
        # under-layout: select player color
        self.underLayout3 = QHBoxLayout()
        self.underLayout3.addWidget(self.paramPlayer2ColorTitle)
        self.underLayout3.addWidget(self.paramPlayer2Color)
        self.layoutV2.addLayout(self.underLayout3)

        self.layoutV2.addWidget(self.paramPlayer2_Ok)
        self.frame2.hide()
        self.layoutVG.addWidget(self.frame2)
        
        self.frame2_1 = QFrame()
        self.underLayout4 = QHBoxLayout()
        self.frame2_1.setLayout(self.underLayout4)
        self.underLayout4.addWidget(self.player2Buttons)
        self.frame2_1.hide()
        self.layoutVG.addWidget(self.frame2_1)

        # bouton paramètre game
        self.paramGame = QPushButton("Paramètres du jeu")
        self.paramGame.clicked.connect(self.activateFrame3)
        self.layoutVG.addWidget(self.paramGame)

        # paramètre game
        self.paramGame_title = QLabel("Mode de jeu :")
        self.paramGame_menu = DropDownMenu(self, self.controller,
                                           "mode", GAMEMODES)
        
        self.paramGame_time = QSlider(Qt.Horizontal)
        self.paramGame_time.setMinimum(15)
        self.paramGame_time.setMaximum(300)
        self.paramGame_time.setValue(120)
        self.paramGame_time.setTickInterval(10)
        self.paramGame_time.valueChanged.connect(self.setLimitTime)
        self.paramGame_timeTitle = QLabel("{} secondes".format(\
                                          self.paramGame_time.value()))
        
        self.paramGame_score = QSlider(Qt.Horizontal)
        self.paramGame_score.setMinimum(2)
        self.paramGame_score.setMaximum(30)
        self.paramGame_score.setValue(10)
        self.paramGame_score.setTickInterval(1)
        self.paramGame_score.valueChanged.connect(self.setLimitScore)
        self.paramGame_scoreTitle = QLabel(" Choisir le score : {} points"\
                                          .format(self.paramGame_score.value()))

        self.design_title = QLabel("Fond du jeu :")
        self.design_menu = DropDownMenu(self, self.controller,
                                        "fond", BACKGROUND_LIST)

        self.paramGame_Ok = QPushButton("Valider")
        self.paramGame_Ok.clicked.connect(self.unactivateFrame3)

        # layout paramètre game
        self.frame3 = QFrame()
        self.layoutV3 = QVBoxLayout()
        self.frame3.setLayout(self.layoutV3)
        self.layoutV3.addWidget(self.paramGame)
        self.layoutV3.addWidget(self.paramGame_title)
        self.layoutV3.addWidget(self.paramGame_menu)
        
        self.frame3_1 = QFrame()
        self.underLayout1 = QVBoxLayout()
        self.frame3_1.setLayout(self.underLayout1)
        self.underLayout1.addWidget(self.paramGame_timeTitle)
        self.underLayout1.addWidget(self.paramGame_time)
        self.frame3_1.hide()
        self.layoutV3.addWidget(self.frame3_1)
        
        self.frame3_2 = QFrame()
        self.underLayout3 = QVBoxLayout()
        self.frame3_2.setLayout(self.underLayout3)
        self.underLayout3.addWidget(self.paramGame_scoreTitle)
        self.underLayout3.addWidget(self.paramGame_score)
        self.frame3_2.hide()
        self.layoutV3.addWidget(self.frame3_2)
        
        self.layoutV3.addWidget(self.design_title)
        self.layoutV3.addWidget(self.design_menu)
        self.layoutV3.addWidget(self.paramGame_Ok)

        self.frame3.hide()
        self.layoutVG.addWidget(self.frame3)

        self.layoutVG.addItem(self.spacerItem1)

        self.score1 = QLabel("Score : ")
        self.score2 = QLabel("{} : {} \ {} : {}".format(
                                    self.controller.playerList[0].name,
                                    self.controller.playerList[0].score,
                                    self.controller.playerList[1].name,
                                    self.controller.playerList[1].score))
        
        self.score2.setFont(QFont("?", 16, QFont.Bold))
        self.chrono = QLabel("00:00:00") 
        self.chrono.setFont(QFont("?", 16, QFont.Bold))

        self.launch = QPushButton("Lancer une partie")
        self.launch.clicked.connect(self.launchGame)

        self.leave = QPushButton("Quitter")
        self.leave.clicked.connect(self.leaveGame)

        self.highScore = QPushButton("Highscores")
        self.highScore.clicked.connect(self.showHighScore)
        
        self.pause = QLabel("Appuyer sur la touche P pour mettre la partie en"\
                            " pause")

        self.view = GraphicView(self, self.timer, self.controller)

        layoutH1 = QHBoxLayout()
        layoutH1.addWidget(self.launch)
        layoutH1.addWidget(self.leave)
        layoutH1.addWidget(self.highScore)
        
        layoutH3 = QHBoxLayout()
        layoutH3.addSpacing(150)
        layoutH3.addWidget(self.pause)

        layoutH2 = QHBoxLayout()
        layoutH2.addSpacing(150)
        layoutH2.addWidget(self.score2)
        layoutH2.addWidget(self.chrono)

        layoutVC = QVBoxLayout()
        layoutVC.addLayout(layoutH1)
        layoutVC.addLayout(layoutH3)
        layoutVC.addWidget(self.view)
        layoutVC.addLayout(layoutH2)

        self.frameD = QFrame()
        self.frameD.hide()
        layoutVD = QHBoxLayout()
        self.frameD.setLayout(layoutVD)
        layoutV_gamemode1 = QVBoxLayout()
        layoutV_gamemode2 = QVBoxLayout()
        layoutVD.addLayout(layoutV_gamemode1)
        layoutVD.addSpacing(20)
        layoutVD.addLayout(layoutV_gamemode2)

        highScoreTitle1 = QLabel("Best time")
        highScoreTitle1.setFont(QFont("?", 12, QFont.Bold))
        highScoreSubtitle1 = QLabel("score 10 goals")
        highScoreSubtitle1.setFont(QFont("?", 12, QFont.Bold))
        gm1_score1 = QLabel()
        gm1_score2 = QLabel()
        gm1_score3 = QLabel()
        gm1_score4 = QLabel()
        gm1_score5 = QLabel()

        highScoreTitle2 = QLabel("Number of goals")
        highScoreTitle2.setFont(QFont("?", 12, QFont.Bold))
        highScoreSubtitle2 = QLabel("in 2 min")
        highScoreSubtitle2.setFont(QFont("?", 12, QFont.Bold))
        gm2_score1 = QLabel()
        gm2_score2 = QLabel()
        gm2_score3 = QLabel()
        gm2_score4 = QLabel()
        gm2_score5 = QLabel()

        self.highscore_gm1 = [gm1_score1, gm1_score2, gm1_score3, gm1_score4,
                              gm1_score5]
        self.highscore_gm2 = [gm2_score1, gm2_score2, gm2_score3, gm2_score4,
                              gm2_score5]

        layoutV_gamemode1.addSpacing(100)
        layoutV_gamemode1.addWidget(highScoreTitle1)
        layoutV_gamemode1.addWidget(highScoreSubtitle1)
        layoutV_gamemode1.addSpacing(50)

        layoutV_gamemode2.addSpacing(100)
        layoutV_gamemode2.addWidget(highScoreTitle2)
        layoutV_gamemode2.addWidget(highScoreSubtitle2)
        layoutV_gamemode2.addSpacing(50)

        for qlabel in self.highscore_gm1:
            layoutV_gamemode1.addWidget(qlabel)
        for qlabel in self.highscore_gm2:
            layoutV_gamemode2.addWidget(qlabel)

        layoutV_gamemode1.addSpacing(400)
        layoutV_gamemode2.addSpacing(400)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.layoutVG)
        self.mainLayout.addLayout(layoutVC)
        self.mainLayout.addWidget(self.frameD)
        self.setLayout(self.mainLayout)
        
        self.window = Popup(self, self.controller)
        self.window.setGeometry(100, 100, 400, 200)
        self.window.hide()

        self.controller.refresh()

    def refresh(self):
        self.score2.setText(("{} : {} | {} : {}".format(
                             self.controller.playerList[0].name,
                             self.controller.playerList[0].score,
                             self.controller.playerList[1].name,
                             self.controller.playerList[1].score)))
        self.chrono.setText(self.controller.getTime())
        self.paramGame_scoreTitle.setText("Choisir le score : {} \
                                          points".format(\
                                          self.paramGame_score.value()))
        self.paramGame_timeTitle.setText("Choisir le temps : {} \
                                         secondes".format(\
                                          self.paramGame_time.value()))
        self.activateFrame()
        self.openPopUp()

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
        
        if playerNum == 0:
            if playerType == Controller.PLAYER:
                self.frame1_1.show()
            elif playerType == Controller.AI:
                self.frame1_1.hide()
                
        if playerNum == 1:
            if playerType == Controller.PLAYER:
                self.frame2_1.show()
            elif playerType == Controller.AI:
                self.frame2_1.hide()
                
        self.controller.refresh()

    def setPlayerName(self, playerNum, name):
        self.controller.setPlayerName(playerNum, name)
        self.controller.refresh()
    
    def activateFrame(self):
        if self.controller.game.gamemode == GAMEMODES[2]:
            self.frame3_2.show()
        else:
            self.frame3_2.hide()
        if self.controller.game.gamemode == GAMEMODES[3]:
            self.frame3_1.show()
        else:
            self.frame3_1.hide()
        
    def setLimitTime(self):
        self.controller.setLimitTime(self.paramGame_time.value())
        
    def setLimitScore(self):
        self.controller.setLimitScore(self.paramGame_score.value())

    def launchGame(self):
        self.controller.setGame()
        
    def openPopUp(self):
        if self.controller.game.stop:
            self.window.show()
        #else:
         #   self.window.hide()

    def leaveGame(self):
        self.app.quit()

    def showHighScore(self):
        highscore = self.controller.getHighScore()
        if self.activeHighScore is False:
            self.activeHighScore = True
            self.frameD.show()
            for indice, liste in enumerate([self.highscore_gm1,
                                            self.highscore_gm2]):
                h = highscore[indice]
                for i, qlabel in enumerate(liste):
                    string = h[i]
                    qlabel.setText("{}. {}".format(i+1, string))
        else:
            self.activeHighScore = False
            self.frameD.hide()


class DropDownMenu(QWidget):
    def __init__(self, parent, controller, name, items=[]):
        super().__init__(parent)
        self.name = name
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.controller = controller
        self.comboBox = QComboBox(self)
        self.layout.addWidget(self.comboBox)

        for item in items:
            self.comboBox.addItem(item)

        self.comboBox.activated[str].connect(self.menuActionTriggered)
        self.show()

    def menuActionTriggered(self, item):
        if self.name == "couleur 1":
            self.controller.setPlayerColor(0, item)
        if self.name == "couleur 2":
            self.controller.setPlayerColor(1, item)
        if self.name == "mode":
            num = GAMEMODES.index(item)
            self.controller.setGameType(num)
        if self.name == "fond":
            self.controller.setBackground(item)


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
        self.run = self.c.run

        imageBack = QPixmap(self.c.game.background)
        imageBackResized = imageBack.scaled(*self.c.WINDOW_SIZE[2:])
        self.background = self.addPixmap(imageBackResized)

        self.dictCage = {}
        for cage in self.c.getCageList()[:2]:
            pen = QPen(QColor(0, 0, 0), 1, Qt.SolidLine)
            brush = QBrush(QColor(*cage.color), Qt.CrossPattern)
            self.dictCage[cage] = self.addRect(*cage.upRightCorner, cage.w,
                                               cage.h, pen, brush)
        for cage in self.c.getCageList()[2:]:
            pen = QPen(QColor(0, 0, 0), 1, Qt.SolidLine)
            brush = QBrush(QColor(*cage.color), Qt.SolidPattern)
            self.addRect(*cage.upRightCorner, cage.w, cage.h, pen, brush)

        self.dictEllipse = {}
        self.dictImage = {}
        for player in self.c.getPlayerList():
            playerX, playerY, playerSize, playerColor = \
                self.c.getPlayerInformations(player)
            pen = QPen(QColor(255, 255, 255), 1, Qt.SolidLine)
            brush = QBrush(QColor(*playerColor), Qt.SolidPattern)
            self.dictEllipse[player] = (self.addEllipse(0, 0,
                                        playerSize, playerSize, pen, brush))
            self.dictEllipse[player].setPos(playerX, playerY)

            imagePlayer = QPixmap(player.image)
            imagePlayerResized = imagePlayer.scaled(player.size, player.size,
                                                    Qt.KeepAspectRatio)
            self.dictImage[player] = self.addPixmap(imagePlayerResized)
            self.dictImage[player].setPos(playerX, playerY)

        self.c.refresh()
        self.timer.timeout.connect(self.updateTimer)
        self.timer.start(self.c.game.gameTick)

    def updateTimer(self):
        self.run = self.c.run
        self.c.refresh()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_P:
            self.c.pause()

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

        imageBack = QPixmap(self.c.game.background)
        imageBackResized = imageBack.scaled(*self.c.WINDOW_SIZE[2:])
        self.background.setPixmap(imageBackResized)

        for player in self.c.getPlayerList():
            playerColor = player.getColor()
            brush = QBrush(QColor(*playerColor), Qt.SolidPattern)
            self.dictEllipse[player].setBrush(brush)

            imagePlayer = QPixmap(player.image)
            imagePlayerResized = imagePlayer.scaled(player.size,
                                                    player.size,
                                                    Qt.KeepAspectRatio)
            self.dictImage[player].setPixmap(imagePlayerResized)

        for cage in self.c.getCageList()[:2]:
            brush = QBrush(QColor(*cage.color), Qt.CrossPattern)
            self.dictCage[cage].setBrush(brush)

        if self.run is True:
            self.c.moveAI()
            self.c.collisions()
            for player in self.c.getPlayerList():
                playerX, playerY = self.c.getPlayerPosition(player)
                self.dictEllipse[player].setPos(playerX, playerY)
                self.dictImage[player].setPos(playerX, playerY)
            self.c.updateTime()
            self.c.checkEndOfGame()

class Popup(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.add(self)
        self.winnerLabel = QLabel()
        self.scoreLabel = QLabel()
        self.timeLabel = QLabel()
        
        self.layoutV = QVBoxLayout()
        self.layoutV.addWidget(self.winnerLabel)
        self.layoutV.addWidget(self.scoreLabel)
        self.layoutV.addWidget(self.timeLabel)
        self.setLayout(self.layoutV)

    def writeEvent(self):
        winner = self.controller.game.winner
        score = self.controller.game.getScore()
        time = self.controller.time
        convertedTime = self.controller.convertTime(time)
        
        if winner:
            self.winnerLabel.setText("Le joueur {} a gagné".format(winner))
            self.scoreLabel.setText("sur le score de {}".format(score))
            self.timeLabel.setText("en {}".format(convertedTime))
        else:
            self.winnerLabel.setText("Match nul")
            
    def refresh(self):
        self.writeEvent()
        

# launch the GUI


def main():
    app = QApplication(sys.argv)
    window = mainWindow(app)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
