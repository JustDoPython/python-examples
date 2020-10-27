import cv2
import random
import numpy as np

def img2strimg(frame, K=5):   
    if type(frame) != np.ndarray:
        frame = np.array(frame)
    height, width, *_ = frame.shape  
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_array = np.float32(frame_gray.reshape(-1))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    # 得到 labels(类别)、centroids(矩心)
    compactness, labels, centroids = cv2.kmeans(frame_array, K, None, criteria, 10, flags)
    centroids = np.uint8(centroids)
    # labels 的数个矩心以随机顺序排列，所以需要简单处理矩心
    centroids = centroids.flatten()
    centroids_sorted = sorted(centroids)
    # 获得不同 centroids 的明暗程度，0 为最暗
    centroids_index = np.array([centroids_sorted.index(value) for value in centroids])
    bright = [abs((3 * i - 2 * K) / (3 * K)) for i in range(1, 1 + K)]
    bright_bound = bright.index(np.min(bright))
    shadow = [abs((3 * i - K) / (3 * K)) for i in range(1, 1 + K)]
    shadow_bound = shadow.index(np.min(shadow))
    labels = labels.flatten()
    # 将 labels 转变为实际的明暗程度列表
    labels = centroids_index[labels]
    # 解析列表
    labels_picked = [labels[rows * width:(rows + 1) * width:2] for rows in range(0, height, 2)]
    canvas = np.zeros((3 * height, 3 * width, 3), np.uint8)
	# 创建长宽为原图三倍的白色画布
    canvas.fill(255)
    y = 8
    for rows in labels_picked:
        x = 0
        for cols in rows:
            if cols <= shadow_bound:
                cv2.putText(canvas, str(random.randint(2, 9)),
                            (x, y), cv2.FONT_HERSHEY_PLAIN, 0.45, 1)
            elif cols <= bright_bound:
                cv2.putText(canvas, "-", (x, y),
                            cv2.FONT_HERSHEY_PLAIN, 0.4, 0, 1)
            x += 6
        y += 6
    return canvas

if __name__ == '__main__':
    fp = r"static/static.jpg"
    img = cv2.imread(fp)
    str_img = img2strimg(img)
    cv2.imwrite("static/static_ascii.jpg", str_img)