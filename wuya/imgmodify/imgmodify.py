import cv2
import numpy as np
import os

def modify_image(img_path, target_dir):
    # 读取全部图片
    pic = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    # 将图片修改为HSV
    pichsv = cv2.cvtColor(pic, cv2.COLOR_BGR2HSV)
    # 提取饱和度和明度
    H,S,V = cv2.split(pichsv)
    # S为饱和度，V为明度
    new_pic = cv2.merge([np.uint8(H), np.uint8(S*1.4), np.uint8(V*0.9)])
    # 将合并后的图片重置为RGB
    pictar = cv2.cvtColor(new_pic, cv2.COLOR_HSV2BGR)
    # 获取原文件名
    file_name = img_path.split("/")[-1]
    # 将图片写入目录
    cv2.imwrite(os.path.join(target_dir, file_name), pictar)

root, dirs, files = next(os.walk("./test/"))

for item in files:
    img_path = os.path.join(root,item)
    process_image(img_path, "./target/")