import cv2
import os

image_base_path = "D:\\video\\images\\";

def get_images(video_path):
    frame_times = 0;
    fileName = video_path.split("\\")[-1:][0].split('.')[0]
    image_out_path = image_base_path + fileName
    if not os.path.exists(image_out_path):
        os.makedirs(image_out_path) 

    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        frame_times = frame_times + 1
        success, frame = cap.read()
        
        if not success:
            break;

        cv2.imencode('.jpg', frame)[1].tofile(image_out_path + "\\" + str(frame_times) + ".jpg")

if __name__ == '__main__':
    get_images('D:\\video\\只予你的晴天【三杞】.mp4')
