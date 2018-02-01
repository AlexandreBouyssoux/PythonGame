# -*- coding: utf-8 -*-

# import
import sys
from PyQt5.QtCore import qFatal, Qt, QTimer
from PyQt5.QtGui import QPen, QColor, QBrush, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsView,\
    QGraphicsScene, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel, \
    QTextEdit, QMenuBar, QLineEdit, QSpacerItem, QSizePolicy, QToolButton, \
    QMenu
import Controller


# errors management
import traceback


def excepthook(type_, value, traceback_):
    traceback.print_exception(type_, value, traceback_)
    qFatal('')


sys.excepthook = excepthook

# class


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OL - FCN : jeu de foot")
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
        #self.activeGame = None
        
        self.parameters = QLabel('       Paramètres')
        self.newfont = QFont("?", 14, QFont.Bold)
        self.parameters.setFont(self.newfont)
     
        self.paramPlayer1 = QPushButton('Joueur 1')
        self.paramPlayer1.clicked.connect(lambda : self.activate(1))
        self.paramPlayer1_IA_1 = QLabel('Le joueur 1 est-t-il humain ou IA ?')
        self.paramPlayer1_IA_2 = QPushButton ('Humain')
        self.paramPlayer1_IA_2.clicked.connect(lambda : self.setPlayer(1, "player"))
        self.paramPlayer1_IA_3 = QPushButton ('IA')
        self.paramPlayer1_IA_3.clicked.connect(lambda : self.setPlayer(1, "ai"))
        self.paramPlayer1Name_1 = QLabel('Nom')
        self.paramPlayer1Name_2 = QLineEdit('Joueur 1')
        self.paramPlayer1Name_3 = QPushButton ('Ok')
        self.paramPlayer1Name_3.clicked.connect(lambda : self.setPlayerName(1, \
                                                    self.paramPlayer1Name_2.text()))
        self.paramPlayer1Color_1 = QLabel('Couleur (déroulez la flèche)')
        self.paramPlayer1Color_2 = DropDownMenu(self, self.controller, \
                                                'couleur 1', ['bleu', 'rouge', \
                                                            'vert', 'jaune'])
        self.paramPlayer1Ok = QPushButton('Valider')
        self.paramPlayer1Ok.clicked.connect(lambda : self.unactivate(1))
        
        self.paramPlayer2 = QPushButton('Joueur 2')
        self.paramPlayer2.clicked.connect(lambda : self.activate(2))
        self.paramPlayer2_IA_1 = QLabel('Le joueur 2 est-t-il humain ou IA ?')
        self.paramPlayer2_IA_2 = QPushButton ('Humain')
        self.paramPlayer2_IA_2.clicked.connect(lambda : self.setPlayer(2, "player"))
        self.paramPlayer2_IA_3 = QPushButton ('IA')
        self.paramPlayer2_IA_2.clicked.connect(lambda : self.setPlayer(2, "ai"))
        self.paramPlayer2Name_1 = QLabel('Nom')
        self.paramPlayer2Name_2 = QLineEdit('Joueur 2')
        self.paramPlayer2Name_3 = QPushButton ('Ok')
        self.paramPlayer2Name_3.clicked.connect(lambda : self.setPlayerName(2, \
                                                    self.paramPlayer2Name_2.text()))
        self.paramPlayer2Color_1 = QLabel('Couleur (déroulez la flèche)')
        self.paramPlayer2Color_2 = DropDownMenu(self, self.controller, \
                                                'couleur 2', ['bleu', 'rouge', \
                                                            'vert', 'jaune'])
        self.paramPlayer2Ok = QPushButton('Valider')
        self.paramPlayer2Ok.clicked.connect(lambda : self.unactivate(2))
        
        self.paramGame = QPushButton('Paramètres du jeu')
        self.paramGame.clicked.connect(lambda : self.activate(3))
        self.paramGame_1 = QLabel ('Mode de jeu : (déroulez la flèche)')
        self.paramGame_2 = DropDownMenu(self, self.controller, \
                                                'mode', ['Au temps','Au score'])
        #self.paramGame_2 = QPushButton ('Au temps')
        #self.paramGame_2.clicked.connect(lambda : self.setGameType(1))
        #self.paramGame_3 = QPushButton ('Au score')
        #self.paramGame_3.clicked.connect(lambda : self.setGameType(0))
        
        self.design_1 = QLabel ('Fond du jeu : (déroulez la flèche)')
        self.design_2 = DropDownMenu(self, self.controller, \
                                                'fond', ['A','B'])
        self.paramGameOk = QPushButton('Valider')
        self.paramGameOk.clicked.connect(lambda : self.unactivate(3))
        
        self.score1 = QLabel('Score : ')
        self.score2 = QLineEdit('{} : {} \ {} : {}'.format(\
                                    self.controller.playerList[0].name, \
                                    self.controller.playerList[0].score, \
                                    self.controller.playerList[1].name, \
                                    self.controller.playerList[1].score))
        
        self.launch = QPushButton('Lancer une partie')
        self.launch.clicked.connect(self.launchGame)
        
        self.leave = QPushButton('Quitter')
        self.leave.clicked.connect(self.leaveGame)
        
        self.highScore = QLabel('Meilleur score {} : {}'.format(\
                                self.controller.game.gamemode, \
                                self.controller.bestScore))
        
        self.view = GraphicView(self, self.timer, self.controller)
        
        self.spacerItem1 = QSpacerItem(5, 2, QSizePolicy.Maximum, \
                                         QSizePolicy.Expanding)
        
        self.layoutVG = QVBoxLayout()
        self.layoutV1 = QVBoxLayout()
        self.layoutV2 = QVBoxLayout()
        self.layoutV3 = QVBoxLayout()
        
        self.layoutVG.addItem(self.spacerItem1)
        self.layoutVG.addWidget(self.parameters) 
        self.layoutVG.addWidget(self.paramPlayer1)
        self.layoutVG.addLayout(self.layoutV1)
        self.layoutVG.addWidget(self.paramPlayer2)
        self.layoutVG.addLayout(self.layoutV2)
        self.layoutVG.addWidget(self.paramGame)
        self.layoutVG.addLayout(self.layoutV3)
        self.layoutVG.addItem(self.spacerItem1)
        
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
        if self.activePlayer1 == True:
            self.layoutV1.addWidget(self.paramPlayer1_IA_1)
            self.underLayout1 = QHBoxLayout()
            self.underLayout1.addWidget(self.paramPlayer1_IA_2)
            self.underLayout1.addWidget(self.paramPlayer1_IA_3)
            self.layoutV1.addLayout(self.underLayout1)
            self.underLayout2 = QHBoxLayout()
            self.underLayout2.addWidget(self.paramPlayer1Name_1)
            self.underLayout2.addWidget(self.paramPlayer1Name_2)
            self.underLayout2.addWidget(self.paramPlayer1Name_3)
            self.layoutV1.addLayout(self.underLayout2)
            self.underLayout3 = QHBoxLayout()
            self.underLayout3.addWidget(self.paramPlayer1Color_1)
            self.underLayout3.addWidget(self.paramPlayer1Color_2)
            self.layoutV1.addLayout(self.underLayout3)
            self.layoutV1.addWidget(self.paramPlayer1Ok)
        elif self.activePlayer1 == False:
            self.removeLayout(self.layoutV1, self.underLayout1)
            self.removeLayout(self.layoutV1, self.underLayout2)
            self.removeLayout(self.layoutV1, self.underLayout3)
            #self.removeWidget(self.underLayout2)
            #self.removeWidget(self.underLayout3)
            #self.removeWidget(self.layoutV1)
            
        if self.activePlayer2 == True:
            self.layoutV2.addWidget(self.paramPlayer2_IA_1)
            self.underLayout4 = QHBoxLayout()
            self.underLayout4.addWidget(self.paramPlayer2_IA_2)
            self.underLayout4.addWidget(self.paramPlayer2_IA_3)
            self.layoutV2.addLayout(self.underLayout4)
            self.underLayout5 = QHBoxLayout()
            self.underLayout5.addWidget(self.paramPlayer2Name_1)
            self.underLayout5.addWidget(self.paramPlayer2Name_2)
            self.underLayout5.addWidget(self.paramPlayer2Name_3)
            self.layoutV2.addLayout(self.underLayout5)
            self.underLayout6 = QHBoxLayout()
            self.underLayout6.addWidget(self.paramPlayer2Color_1)
            self.underLayout6.addWidget(self.paramPlayer2Color_2)
            self.layoutV2.addLayout(self.underLayout6)
            self.layoutV2.addWidget(self.paramPlayer2Ok)
        elif self.activePlayer2 == False:
            self.removeWidget(self.layoutV2)
            self.removeWidget(self.underLayout4)
            self.removeWidget(self.underLayout5)
            self.removeWidget(self.underLayout6)
            
            
        if self.activeParam == True:
            self.layoutV3.addWidget(self.paramGame_1)
            self.underLayout7 = QHBoxLayout()
            self.underLayout7.addWidget(self.paramGame_2)
            #self.underLayout7.addWidget(self.paramGame_3)
            self.layoutV3.addLayout(self.underLayout7)          
            self.layoutV3.addWidget(self.design_1)
            self.underLayout8 = QHBoxLayout()
            self.underLayout8.addWidget(self.design_2)
            self.layoutV3.addLayout(self.underLayout8)
            self.layoutV3.addWidget(self.paramGameOk)
        elif self.activeParam == False:
            self.removeWidget(self.layoutV3)
            self.removeWidget(self.underLayout7)
            self.removeWidget(self.underLayout8)
            
        self.score2 = QLineEdit('{} : {} \ {} : {}'.format(\
                                    self.controller.playerList[0].name, \
                                    self.controller.playerList[0].score, \
                                    self.controller.playerList[1].name, \
                                    self.controller.playerList[1].score))
        
        # mode de jeu
            
        
        
    def activate(self, playerNum):
        if playerNum == 1:
            self.activePlayer1 = True
            print ('ok')
        if playerNum == 2:
            self.activePlayer2 = True
        if playerNum == 3:
            self.activeParam = True
        self.controller.refresh()
            
    def unactivate(self, playerNum):
        if playerNum == 1:
            self.activePlayer1 = False
        if playerNum == 2:
            self.activePlayer2 = False 
        if playerNum == 3:
            self.activeParam = False
        self.controller.refresh()
        
    def removeWidget(self, layout):
        while layout.count():
            self.item = layout.takeAt(0)
            self.widget = self.item.widget()
            if self.widget is not None:
                self.widget.deleteLater()
                
    def removeLayout(self, layout, box):
        for i in range(layout.count()):
            layout_item = layout.itemAt(i)
            if layout_item.layout() == box:
                layout.removeItem(layout_item)
        
    def setPlayer(self, playerNum, playerType):
    # définit si le joueur est un robot ou un humain (choix de l'utilisateur)
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
        self.button.setStyleSheet('border: 0px; padding: 0px;')
        self.button.setCursor(Qt.ArrowCursor)
        #self.button.setText(self.name)
        self.button.triggered.connect(lambda : self.menuActionTriggered(i))
        self.button.setPopupMode(QToolButton.InstantPopup)
        self.button.setMenu(self.menu)
        self.menuLayout.addWidget(self.button)
        self.setLayout(self.menuLayout)
        
    
    def menuActionTriggered(self, item):
        if self.name =='couleur 1':
            self.controller.setPlayerColor(1, item)
        if self.name == 'couleur 2':
            self.controller.setPlayerColor(2, item)
        if self.name == 'mode':
            self.controller.setGameType(item)
        if self.name == 'fond':
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


if __name__ == '__main__':
    main()
