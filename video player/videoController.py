# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 10:24:28 2021

@author: USER
"""

from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QSlider
from opencvLib import opencvLib

class video_controller(object):
    def __init__(self, img_path, ui):
        self.img_path = img_path
        self.ui = ui
        self.frame_width = 800
        self.frame_height = 450
        self.frame_current_no = 0
        self.frame_current_state = "pause"
        self.listPoints = []
        
        self.video_Info()
        self.video_player()
        
    def video_Info(self):
        videoCapture = opencvLib.video_info(self.img_path)
        self.vc = videoCapture["vc"]
        self.video_width = videoCapture["width"]
        self.video_height = videoCapture["height"]
        self.video_fps = videoCapture["fps"]
        self.video_fps_count = videoCapture["length"]
        
        self.ui.horizontalSlider.setRange(0, self.video_fps_count-1)
        self.ui.horizontalSlider.valueChanged.connect(self.getSliderVlaue)
        self.ui.label_progress.setText(f"0/{self.video_fps_count}")
        
        
    def video_player(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_run_do)
        #self.timer.start(1)
        self.timer.start(1000//self.video_fps)
        
        self.ui.label_videoPlayer.mousePressEvent = self.mouse_Press_Event
        self.ui.pushButton_clearPoint.clicked.connect(self.clearPoints)
        
        
    def video_play(self):
        self.frame_current_state = "play"
           
    def video_stop(self):
        self.frame_current_state = "stop"
            
    def video_pause(self):
        self.frame_current_state = "pause"
        
    def get_frame_current_no(self, frame_no):
        # set(1, frame) => 1: CV_CAP_PROP_POS_FRAMES, frame: current frame
        self.vc.set(1, frame_no)
    
    def get_frame_next_no(self):
        # ret: boolen value , flame: 3-dim array flame image
        ret, frame = self.vc.read()
        self.ui.label_progress.setText(f"{self.ui.horizontalSlider.value()}/{self.video_fps_count}")
        self.setSliderVlaue(self.frame_current_no)
        return frame
    
    def update_label_frame(self, frame):
        bytesPerline = 3* self.video_width
        frame = self.update_points_onScreen(frame)
        qImg = QImage(frame, self.video_width, self.video_height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.qpixmap = QPixmap.fromImage(qImg) 
        
        if self.qpixmap.width()/16 >= self.qpixmap.height()/9:
            self.qpixmap = self.qpixmap.scaledToWidth(self.frame_width)
        else:
            self.qpixmap = self.qpixmap.scaledToHeight(self.frame_width)
        
        self.ui.label_videoPlayer.setPixmap(self.qpixmap)
        self.ui.label_videoPlayer.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        

    def timer_run_do(self):
        if (self.frame_current_state == "play"):
            if self.frame_current_no >= self.video_fps_count-1: #if video end play => restart play
                self.frame_current_no = 0
                self.get_frame_current_no(self.frame_current_no)
            else:      
                self.frame_current_no = self.frame_current_no + 1
            
            
        if (self.frame_current_state == "stop"):
            self.frame_current_no = 0
            self.get_frame_current_no(self.frame_current_no)
            
        if (self.frame_current_state == "pause"):
            self.frame_current_no = self.frame_current_no
            self.get_frame_current_no(self.frame_current_no)
        
        self.ui.label_state.setText(f"{self.frame_current_state}")
        frame = self.get_frame_next_no()
        self.update_label_frame(frame)   
            
    def getSliderVlaue(self):  
        self.frame_current_no = self.ui.horizontalSlider.value()
        self.get_frame_current_no(self.frame_current_no)
        
    def setSliderVlaue(self, value):
        self.ui.horizontalSlider.setValue(value)
        
    #----------------------------------------------------------------#
    def mouse_Press_Event(self, event):
        x = event.x()
        y = event.y()
        norm_x = x / self.qpixmap.width()
        norm_y = y / self.qpixmap.height()
        
        if event.button() == 2: #end press => press mouse right
            self.listPoints.append(self.listPoints[0])
            print("you press right")
        elif event.button() == 1: #press mouse left
            self.listPoints.append((norm_x, norm_y))
            print("you press left")
            
    def clearPoints(self):
        self.listPoints = []
    
    def update_points_onScreen(self, frame):
        if len(self.listPoints) == 0:
            pass
        else:
            frame = opencvLib.draw_point(frame, self.listPoints[0])
            for i in range(1, len(self.listPoints)):
                frame = opencvLib.draw_point(frame, self.listPoints[i])
                frame = opencvLib.draw_line(frame, self.listPoints[i-1], self.listPoints[i])
        return frame
        