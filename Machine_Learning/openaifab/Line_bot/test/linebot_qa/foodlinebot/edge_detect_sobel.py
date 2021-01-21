# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 16:26:44 2020

@author: Alan Lin
"""
import cv2
import numpy as np

#正規化圖片
def normlize(img):
    imgOri = img.astype(np.double)
    imgOri = imgOri / 255
    return imgOri
#二值化圖片
def Binarization(img, threshold):
    h, w = img.shape
    for i in range(h):
        for j in range(w):
            if img[i][j] > threshold:
                img[i][j] = 255
            else:
                img[i][j] = 0
    return img
#照片邊緣檢測(浮雕)
def edge_detect_Relief(img,state):    
    h, w = img.shape   
    img_pad = img.copy()
    #製作檢測點上下左右各擴增一格之filter(1*1 >> 3*3)
    img_filter_range = np.pad(array=img,pad_width=((1,1),(1,1)), mode='reflect')  
    if state == 0:
        #垂直濾波濾鏡(0:增強垂直線條)
        vertical_sobel = np.array([[-1, 0, 1],
                                   [-2, 0, 2],
                                   [-1, 0, 1]])           
        for i in range(h):
            for j in range(w):
                #目標filter 由左至右、由上到下掃過，與濾鏡做點對點相乘
                Ver_tem = np.sum(np.multiply(img_filter_range[i:i+3, j:j+3], vertical_sobel)) 
                img_pad[i][j] = Ver_tem
        print('vertical_sobel')
    else:        
        #水平濾波濾鏡(1:增強水平線條)
        horizontal_sobel = np.array([[-1,-2,-1],
                                     [0,0,0],
                                     [1,2,1]])               
        for i in range(h):
            for j in range(w):
                #目標filter 由左至右、由上到下掃過，與濾鏡做點對點相乘
                Hor_tem = np.sum(np.multiply(img_filter_range[i:i+3, j:j+3], horizontal_sobel))
                img_pad[i][j] = Hor_tem
        print('horizontal_sobel')
    return img_pad
# 照片邊緣檢測(輪廓)
def edge_detect_contour(imgOri):    
    #4~6.邊緣檢測(浮雕 0:水平特徵，1:垂直特徵)
    img_H = edge_detect_Relief(imgOri,0)*255 #水平處理
    img_bh = img_H + 0.5*255
    # cv2.imwrite('./result/HW1_01/Relief_v.jpg', img_bh)
    # cv2.imshow("Relief_h", img_bh)
    img_V = edge_detect_Relief(imgOri,1)*255 #垂直處理
    img_bv = img_V + 0.5*255
    # cv2.imwrite('./result/HW1_01/Relief_h.jpg', img_bv)
    # cv2.imshow("Relief_v", img_bv)   
    img_contour = abs(img_V)+abs(img_H) #各自取絕對值後直接相加
    # img_contour = cv2.bitwise_or(img_V,img_H) #用 bitwise_or (效果較不好)
    img_contour = Binarization(img_contour, 180) #二值化
    print('edge_detect_contour')
    return img_contour
def edge_detection(path):
    #1.讀取圖片
    img = cv2.imread(path, 0)   
    #2.顯示原圖
    # cv2.imwrite('./result/HW1_01/Original.jpg', img)
    #3.將影像轉換成 double 格式，數值範圍在[0 1]之間。
    imgOri = normlize(img)    
    #7.邊緣檢測(輪廓)
    img_c = edge_detect_contour(imgOri)
    img_c = img_c.astype(np.uint8) #轉8bit格式
    cv2.imwrite(path, img_c)
    return path 
def detection(path):
    img = cv2.imread(path, 0)
    canny = cv2.Canny(img,80,220)
    cv2.imwrite(path,canny)    
    return path
