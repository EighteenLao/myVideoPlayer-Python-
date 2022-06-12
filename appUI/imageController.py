# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 10:24:28 2021

@author: USER
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QCursor, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication
from opencvLib import opencvLib

class Image_controller(object):
    def __init__(self, img_path, ui):
        self.img_path = img_path
        self.ui = ui
        self.scale_value = 50
        self.read_file()        
        
    def get_path(self, img_path):
        self.img_path = img_path
        self.read_file()
        
    def read_file(self):
        # tru catch
        try:
            self.ori_img = opencvLib.read_image(self.img_path)
            self.ori_height, self.ori_width, self.ori_channel = self.ori_img.shape
        except:
            self.ori_img = opencvLib.read_image('Screenshot.jpg')
            self.ori_height, self.ori_width, self.ori_channel = self.ori_img.shape
         
        self.display_img = self.ori_img 
        self.scale_value = 50
        self.update_img()
        
    def update_img(self):
        # QImage:適合用在讀取圖像、單次修改圖像、更改圖像像素
        # QPixmap:適合用在多次操作相同的圖像
        # fromImage: QImage convert to QPixmap
        bytesPerline = 3* self.ori_width
        qImg = QImage(self.display_img, self.ori_width, self.ori_height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.qpixmap = QPixmap.fromImage(qImg) 
        self.update_imgScale()
        
        self.ui.label.setPixmap(self.qpixmap)
        self.ui.label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.ui.label.mousePressEvent = self.get_click_pos
        
        # show mouse move event
        self.ui.label.mouseMoveEvent = self.show_move_pos
        self.ui.label.mouseReleaseEvent = self.show_mouse_release
    
    def update_imgScale(self):
        self.scale_rate = pow(10, (self.scale_value - 50)/50)
        qpixmap_height = self.ori_height * self.scale_rate
        self.qpixmap = self.qpixmap.scaledToHeight(qpixmap_height)
        self.showImg_rateValue()
        
    def showImg_rateValue(self):
        self.ui.label_silder.setText(f"{self.scale_value}")
      
    def image_roomIn(self):
        self.scale_value = max(0, self.scale_value-1)
        self.update_img()
        
    def image_roomOut(self):
        self.scale_value = min(100, self.scale_value+1)
        self.update_img()
        
    def set_rate_value(self,scaleValue):
        self.scale_value = scaleValue
        self.update_img()
        
    def get_click_pos(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.norm_x = x / self.qpixmap.width()
        self.norm_y = y / self.qpixmap.height()
        self.draw_point((self.norm_x,self.norm_y))
        self.display_pos(x,y)
        
    def display_pos(self,x,y):
        self.ui.label_click_pos.setText(f"click pos:{x},{y}")
        self.ui.label_norm_pos.setText(f"norm pos:{self.norm_x:.3f},{self.norm_y:.3f}")
        self.ui.label_real_pos.setText(f"real pos:{int(self.norm_x*self.ori_width)},{int(self.norm_y*self.ori_height)}")
        
    def draw_point(self, point):
        real_image_x = point[0]*self.ori_width
        real_image_y = point[1]*self.ori_height
        self.display_img = opencvLib.draw_circle(self.display_img,(real_image_x,real_image_y))
        self.update_img()
        
    def show_move_pos(self,event):
        print(f"mouse move: {event.x()=},{event.y()=},{event.button()=}")
        
    def show_mouse_release(self,event):
        print(f"release move: {event.x()=},{event.y()=},{event.button()=}")
        
    def get_imageCurrentColor(self):
        x = QCursor.pos().x()
        y = QCursor.pos().y()
        self.ui.textEdit_pos.setText(f"X:{x:4d},Y:{y:4d}")
        pixmap = QApplication.primaryScreen().grabWindow(QApplication.desktop().winId(),x,y,1,1)
        image = pixmap.toImage()
        color = QColor(image.pixel(0,0))
        self.image_color_select(color)
        
    def image_color_select(self, color):
        r,g,b = color.red(),color.green(),color.blue()
        stringRGB = ('{:3d}, {:3d}, {:3d}'.format(r,g,b)) #{:3d} => 長度為3的十進制參數
        self.ui.label_showColorPlane.setStyleSheet('background-color:rgb({});'.format(stringRGB))
        self.ui.textEdit_RGBValue.setText(f"{stringRGB}")
        self.ui.textEdit_hexValue.setText(color.name().upper())
        
    