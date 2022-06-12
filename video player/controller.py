#from PyQt5 import QtWidgets
#from PyQt5.QtGui import QImage, QPixmap, QCursor, QColor
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QMainWindow
#from PyQt5.QtCore import QTimer, QThread, pyqtSignal
#import time
from UI import Ui_MainWindow
from videoController import video_controller


class MainWindow_controller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()
        
    def setup_control(self):
        
        # button open file
        self.ui.pushButton_fileSelect.clicked.connect(self.openFile)
        
    def openFile(self):
        fileName, fileType= QFileDialog.getOpenFileName(self, "Open file", "./", "Video Files(*.mp4 *.avi)")
        self.videoCtroller = video_controller(img_path = fileName, ui = self.ui)
        
        self.ui.pushButton_stop.clicked.connect(self.videoCtroller.video_stop)
        self.ui.pushButton_play.clicked.connect(self.videoCtroller.video_play)
        self.ui.pushButton_pause.clicked.connect(self.videoCtroller.video_pause)
        
        


   
        

        
     