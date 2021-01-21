# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 17:59:17 2020

@author: Alan Lin
"""
#Video_Processing.py
import numpy as np 
import cv2 as cv 

def video_processing(path,video_name):
    image_path = 'D:/LineBot_pic/static/'+video_name+'_video.jpg'
    video_path = 'D:/LineBot_pic/static/'+video_name+'_video.mp4'
    cap = cv.VideoCapture(path)
    # 設定擷取影像的尺寸大小
    fourcc = 0x00000021
    FPS = 24
    w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    
    # 建立 VideoWriter 物件，輸出影片至 './static/video_canny2.mp4'
    # FPS 值為 24, fourcc 為 0x00000021=>轉mp4檔案格式，w,h設定為原影片大小
    output = cv.VideoWriter(video_path,fourcc,FPS,(w,h))

    while(cap.isOpened()):
        ret, frame = cap.read()
        #以cv2.Canny()進行邊緣偵測，threshold1及threshold2可依需求調整為0-255任一數
        canny = cv.Canny(frame,80,220)
        if ret == True:
            # 寫入影格
            output.write(canny)

            # cv.imshow('canny',canny)
            cv.imwrite(image_path,canny)
            #cv2.waitKey()中的參數單位是毫秒，代表每一張圖片所停留的時間，一般設定為25
            if cv.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    return image_path , video_path
