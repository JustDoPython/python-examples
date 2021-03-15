# -*- coding: utf-8 -*-

import face_recognition
import cv2
import os
import time

pic_boss = face_recognition.load_image_file("/Users/xx/Desktop/face/0.png")
boss_face_encoding = face_recognition.face_encodings(pic_boss)[0]

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding in face_encodings:
        results = face_recognition.compare_faces([boss_face_encoding], face_encoding)
        if results[0]:
            print("boss来了，快打开其他应用")
            os.system('open /Applications/PyCharm.app')
            time.sleep(300)