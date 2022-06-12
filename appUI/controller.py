from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QCursor, QColor
from PyQt5.QtWidgets import QFileDialog,QColorDialog,QMainWindow, QApplication
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import time
from UI import Ui_MainWindow
from imageController import Image_controller

class threadTask(QThread):
    qThread_single = pyqtSignal(int)
    
    def start_Process(self):
        max_value = 100
        for i in range(max_value):
            time.sleep(0.05)
            #print("ok")
            self.qThread_single.emit(i+1)


class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()
        
    def setup_control(self):
        
        # button count
        self.ui.pushButton.setText('click count')
        self.click_count = 0
        self.ui.pushButton.clicked.connect(self.buttonClick_count)
        
        # button show line edit
        self.ui.pushButton_line_edit.setText('click show line')
        self.ui.pushButton_line_edit.clicked.connect(self.buttonClick_showLineEdit)
        
        # button show color plane
        self.ui.label_showColorPlane.setText('show color')
        self.ui.pushButton_colorPlane.clicked.connect(self.color_select)
        
        
        #image process
        self.img_path = '' 
        self.Image_controller = Image_controller(img_path = self.img_path, 
                                                 ui = self.ui
                                                 )
        # open image file
        self.ui.pushButton_open_file.setText('open file')
        self.ui.pushButton_open_file.clicked.connect(self.buttonClick_openFilePath)
        
        # image zoom in&zoom out
        self.ui.pushButton_roomIn.setText('Room In')
        self.ui.pushButton_roomIn.clicked.connect(self.Image_controller.image_roomIn)
        self.ui.pushButton_roomOut.setText('Room Out')
        self.ui.pushButton_roomOut.clicked.connect(self.Image_controller.image_roomOut)
        
        # slider bar
        self.ui.label_silder.setText('50')
        self.ui.horizontalSlider.valueChanged.connect(self.getSliderVlaue)
        
        
        #timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_run)
        self.timer.start(1)
        self.time_count = 0
        
        # process bar
        self.ui.progressBar.setMaximum(100)
        self.ui.pushButton_goProcess.clicked.connect(self.click_event)
        
        # get image current color
        image_update_timer = QTimer(self)
        image_update_timer.timeout.connect(self.Image_controller.get_imageCurrentColor)
        image_update_timer.start(20)
        


    #------------------------------------------------------------#
    def buttonClick_count(self):
        self.click_count = self.click_count + 1
        self.ui.show_output_label.setText(f"you clicked {self.click_count} times")
        
    
    def buttonClick_showLineEdit(self):
        message = self.ui.lineEdit.text()
        self.ui.show_line_edit.setText(message)

    def color_select(self):
        color = QColorDialog.getColor()
        
        r,g,b = color.red(),color.green(),color.blue()
        stringRGB = ('{:3d}, {:3d}, {:3d}'.format(r,g,b)) #{:3d} => 長度為3的十進制參數
        self.ui.label_showColorPlane.setStyleSheet('background-color:rgb({});'.format(stringRGB))
    
        
    #-----------------------------------------------------------#    
    def buttonClick_openFilePath(self):
        fileName, fileType= QFileDialog.getOpenFileName(self, "Open file", "./")
        self.Image_controller.get_path(fileName)
   
    def getSliderVlaue(self):  
        self.Image_controller.set_rate_value(self.ui.horizontalSlider.value()+1)
        
        
    #-----------------------------------------------------------#  
    def timer_run(self):
        self.ui.label_timer.setText(str(self.timer_format_convert(self.time_count)))
        self.time_count = self.time_count + 1
        
    def timer_format_convert(self,time_count):
        sec = max(0, time_count // 1000)%60
        minute = max(0, time_count // (1000*60))%60
        hour = max(0, time_count // (1000*60*60))
        return f"Timer:{hour}:{minute}:{sec}" 
    
    #-----------------------------------------------------------# 
    
    def click_event(self):
        self.qthread = threadTask()
        self.qthread.qThread_single.connect(self.process_value_change)
        self.qthread.start_Process()
        
    def process_value_change(self,value):
        self.ui.progressBar.setValue(value)
        

        
     