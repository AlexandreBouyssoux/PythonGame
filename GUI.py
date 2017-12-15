# -*- coding: utf-8 -*-

# import
import sys
from PyQt5.QtCore import qFatal, Qt, QTimer
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsView,\
    QGraphicsScene
import Controller


# errors management
import traceback


def excepthook(type_, value, traceback_):
    traceback.print_exception(type_, value, traceback_)
    qFatal('')


sys.excepthook = excepthook

# Constants
TIMER_REFRESH_SPEED = 60

# class


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window")
        self.timer = QTimer()
        self.controller = Controller.Controller()
        self.centralWidget = GraphicView(self, self.timer, self.controller)
        self.setCentralWidget(self.centralWidget)


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
        self.timer.start(TIMER_REFRESH_SPEED)

    def updateTimer(self):
        self.c.refresh()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.c.movePlayer("jump", 0)
            self.c.refresh()
            print(self.c.getStringPlayerPosition(0))

        elif event.key() == Qt.Key_Left:
            self.c.movePlayer("left", 0)
            self.c.refresh()
            print(self.c.getStringPlayerPosition(0))

        elif event.key() == Qt.Key_Right:
            self.c.movePlayer("right", 0)
            self.c.refresh()
            print(self.c.getStringPlayerPosition(0))

        if event.key() == Qt.Key_Z:
            self.c.movePlayer("jump", 1)
            self.c.refresh()
            print(self.c.getStringPlayerPosition(1))

        elif event.key() == Qt.Key_Q:
            self.c.movePlayer("left", 1)
            self.c.refresh()
            print(self.c.getStringPlayerPosition(1))

        elif event.key() == Qt.Key_D:
            self.c.movePlayer("right", 1)
            self.c.refresh()
            print(self.c.getStringPlayerPosition(1))

    def refresh(self):
        self.c.collisions()
        for player in self.c.getPlayerList():
            playerX, playerY = self.c.getPlayerPosition(player)
            self.dictEllipse[player].setPos(playerX, playerY)

# launch the GUI


def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
