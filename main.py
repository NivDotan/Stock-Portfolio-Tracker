from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFrame, QDialog, QMessageBox, QApplication, QHeaderView
from PyQt5.QtCore import pyqtSignal, QFile, QTextStream, Qt
import sys
import qdarkstyle
from HomeWindoow import HomeWindoowClass


def main(): 
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5()) #Set the style as dark theme
    a_window = HomeWindoowClass()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()