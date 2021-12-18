#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""


import numpy as np
import cv2
import dlib
import PySimpleGUI as sg
import os.path


# 给img中的人头像加上圣诞帽，人脸最好为正脸
def add_hat(imgPath):
    # 读取头像图
    img = cv2.imread(imgPath)
    #print(img)
    # 读取帽子图，第二个参数-1表示读取为rgba通道，否则为rgb通道
    hat_img = cv2.imread("hat2.png",-1)

    # 分离rgba通道，合成rgb三通道帽子图，a通道后面做mask用
    r,g,b,a = cv2.split(hat_img)
    rgb_hat = cv2.merge((r,g,b))

    cv2.imwrite("hat_alpha.jpg",a)

    # dlib人脸关键点检测器
    predictor_path = "shape_predictor_5_face_landmarks.dat"
    predictor = dlib.shape_predictor(predictor_path)

    # dlib正脸检测器
    detector = dlib.get_frontal_face_detector()

    # 正脸检测
    dets = detector(img, 1)

    # 如果检测到人脸
    if len(dets)>0:
        for d in dets:
            x,y,w,h = d.left(),d.top(), d.right()-d.left(), d.bottom()-d.top()
            
            # 关键点检测，5个关键点
            shape = predictor(img, d)

            # 选取左右眼眼角的点
            point1 = shape.part(0)
            point2 = shape.part(2)

            # 求两点中心
            eyes_center = ((point1.x+point2.x)//2,(point1.y+point2.y)//2)

            #  根据人脸大小调整帽子大小
            factor = 1.5
            resized_hat_h = int(round(rgb_hat.shape[0]*w/rgb_hat.shape[1]*factor))
            resized_hat_w = int(round(rgb_hat.shape[1]*w/rgb_hat.shape[1]*factor))

            if resized_hat_h > y:
                resized_hat_h = y-1

            # 根据人脸大小调整帽子大小
            resized_hat = cv2.resize(rgb_hat,(resized_hat_w,resized_hat_h))

            # 用alpha通道作为mask
            mask = cv2.resize(a,(resized_hat_w,resized_hat_h))
            mask_inv =  cv2.bitwise_not(mask)

            # 帽子相对与人脸框上线的偏移量
            dh = 0
            dw = 0
            # 原图ROI
            # bg_roi = img[y+dh-resized_hat_h:y+dh, x+dw:x+dw+resized_hat_w]
            bg_roi = img[y+dh-resized_hat_h:y+dh,(eyes_center[0]-resized_hat_w//3):(eyes_center[0]+resized_hat_w//3*2)]

            # 原图ROI中提取放帽子的区域
            bg_roi = bg_roi.astype(float)
            mask_inv = cv2.merge((mask_inv,mask_inv,mask_inv))
            alpha = mask_inv.astype(float)/255

            # 相乘之前保证两者大小一致（可能会由于四舍五入原因不一致）
            alpha = cv2.resize(alpha,(bg_roi.shape[1],bg_roi.shape[0]))
            # print("alpha size: ",alpha.shape)
            # print("bg_roi size: ",bg_roi.shape)
            bg = cv2.multiply(alpha, bg_roi)
            bg = bg.astype('uint8')

            cv2.imwrite("bg.jpg",bg)
            # cv2.imshow("image",img)
            # cv2.waitKey()

            # 提取帽子区域
            hat = cv2.bitwise_and(resized_hat,resized_hat,mask = mask)
            cv2.imwrite("hat.jpg",hat)

            # cv2.imshow("hat",hat)
            # cv2.imshow("bg",bg)

            # print("bg size: ",bg.shape)
            # print("hat size: ",hat.shape)

            # 相加之前保证两者大小一致（可能会由于四舍五入原因不一致）
            hat = cv2.resize(hat,(bg_roi.shape[1],bg_roi.shape[0]))
            # 两个ROI区域相加
            add_hat = cv2.add(bg,hat)
            # cv2.imshow("add_hat",add_hat)

            # 把添加好帽子的区域放回原图
            img[y+dh-resized_hat_h:y+dh,(eyes_center[0]-resized_hat_w//3):(eyes_center[0]+resized_hat_w//3*2)] = add_hat

            # 展示效果
            # cv2.imshow("img",img )
            # cv2.waitKey(0)

            return img







file_list_column = [
    [sg.Submit('生成', key='Go',size=(15, 1)), sg.Cancel('退出',key='Cancel', size=(15, 1))],
    [
        sg.Text("图片位置（选择文件夹）"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse('浏览'),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ]
]
image_viewer_column = [
    [sg.Text("从左边图片列表中选择一张图片:")],
    [sg.Image(key="-IMAGE-")]
]
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]
window = sg.Window("人像添加圣诞帽软件", layout)
filename = ''
while True:
    event, values = window.read()
    if event == "Cancel" or event == sg.WIN_CLOSED:
        break
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
               and f.lower().endswith((".jpg", ".png"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":
        try:
            filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])
            if filename.endswith('.jpg'):
                im = cv2.imread(filename)
                cv2.imwrite(filename.replace('jpg', 'png'), im)
            window["-IMAGE-"].update(filename=filename.replace('jpg', 'png'))
        except Exception as e:
            print(e)
    elif event== "Go" :
        try:
            output = add_hat(filename)
            #print(output)
            # 展示效果
            #cv2.imshow("output",output)
            #cv2.waitKey(0)
            print(os.path.join(folder, "output.png"))
            cv2.imwrite(os.path.join(folder, "output.png"),output)
            #print(output)
            window["-IMAGE-"].update(filename=os.path.join(folder, "output.png"))
        except:
            print('OMG！添加失败了！')

        cv2.destroyAllWindows()




