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
TIMER_REFRESH_SPEED = 50

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
        self.joueur = self.c.createJoueur()
        self.timer = timer
        self.setSceneRect(*self.c.WINDOW_SIZE)
        joueurX, joueurY, joueurSize, joueurColor = \
            self.c.getJoueurInformations()
        pen = QPen(QColor(*joueurColor), 1, Qt.SolidLine)
        brush = QBrush(QColor(*joueurColor), Qt.SolidPattern)
        self.ellipse = self.addEllipse(0, 0, joueurSize, joueurSize, pen,
                                       brush)
        self.c.refresh()
        self.timer.timeout.connect(self.updateTimer)
        self.timer.start(TIMER_REFRESH_SPEED)

    def updateTimer(self):
        self.c.refresh()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.c.moveJoueur("jump")
            self.c.refresh()
            print(self.c.getStringJoueurPosition())

        elif event.key() == Qt.Key_Left:
            self.c.moveJoueur("left")
            self.c.refresh()
            print(self.c.getStringJoueurPosition())

        elif event.key() == Qt.Key_Right:
            self.c.moveJoueur("right")
            self.c.refresh()
            print(self.c.getStringJoueurPosition())

    def refresh(self):
        joueurX, joueurY = self.c.getJoueurPosition()
        self.ellipse.setPos(joueurX, joueurY)

# launch the GUI


def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
