# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 10:36:58 2021

@author: USER
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from controller  import MainWindow_controller

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    sys.exit(app.exec_())