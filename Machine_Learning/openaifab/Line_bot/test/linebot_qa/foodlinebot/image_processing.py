# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 18:17:40 2020

@author: Alan Lin
"""

#image_processing.py

import cv2 as cv
import numpy as np

def image_processing_1(image_name,image_path):
    #讀取照片原圖
    img = cv.imread(image_path)
    
    #將原圖轉為灰階圖
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    
    #將灰階圖進行二值化處理
    ret,binary=cv.threshold(gray,127,255,cv.THRESH_BINARY)
    
    #將灰階圖與二值化處理圖存為實體檔案
    gray_path = 'D:/LineBot_pic/static/gray_'+image_name
    binary_path = 'D:/LineBot_pic/static/binary_'+image_name
    cv.imwrite(gray_path,gray)
    cv.imwrite(binary_path,binary)

    return gray_path, binary_path
def edge (path,image_name):
    path_out = 'D:/LineBot_pic/static/'+image_name+'_edge.jpg'
    image = cv.imread(path)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    canny = cv.Canny(blurred, 80, 100)
    cv.imwrite(path_out,canny)
    return path_out
