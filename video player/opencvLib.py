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
     
    @staticmethod
    def video_info (path):
        videoCapture = cv2.VideoCapture(path)
        videoInfo = {}
        videoInfo["vc"] = videoCapture
        videoInfo["fps"] = videoCapture.get(cv2.CAP_PROP_FPS)
        videoInfo["width"] = int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH))
        videoInfo["height"] = int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        videoInfo["length"] = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
        return videoInfo
     
    @staticmethod
    def normalPoint_to_int(img, point):
        image_h, image_w, image_c = img.shape
        return (int(image_w*point[0]), int(image_h*point[1]))
     
    @staticmethod
    def draw_point(image, point):
        point = opencvLib.normalPoint_to_int(image, point)
        return cv2.circle(image, point, 5, (0,0,255), -1) #半徑=5,red,實心
    
    @staticmethod
    def draw_line(image, start_point, end_point):
        start_point = opencvLib.normalPoint_to_int(image, start_point)
        end_point = opencvLib.normalPoint_to_int(image, end_point)
        return cv2.line(image, start_point, end_point, (255, 0, 0), 5) #blue,寬度5
        
        
        
    
        