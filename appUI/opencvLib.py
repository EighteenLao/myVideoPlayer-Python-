# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 15:12:43 2021

@author: USER
"""

import cv2

class opencvLib(object):
    
    @staticmethod
    def read_image(file_path):
        return cv2.imread(file_path)
    
    @staticmethod
    def point_floatToint(point):
        return (int(point[0]), int(point[1]))
    
    @staticmethod
    def draw_circle(img,point):
        point = opencvLib.point_floatToint(point)
        size = 8
        color = (0, 0, 255)
        return cv2.circle(img, point, size, color, 4)

        
    
        