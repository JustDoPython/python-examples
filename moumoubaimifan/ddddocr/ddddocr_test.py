import ddddocr
import cv2


def hk():
    det = ddddocr.DdddOcr(det=False, ocr=False)

    with open('hycdn.png', 'rb') as f:
            target_bytes = f.read()
        
    with open('background.jpg', 'rb') as f:
        background_bytes = f.read()

    res = det.slide_match(target_bytes, background_bytes, simple_target=True)

    print(res)



def dx():
    det = ddddocr.DdddOcr(det=True)

    with open("eb.jpg", 'rb') as f:
        image = f.read()

    poses = det.detection(image)
    print(poses)

    im = cv2.imread("eb.jpg")

    for box in poses:
        x1, y1, x2, y2 = box
        im = cv2.rectangle(im, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)

    cv2.imwrite("result.jpg", im)

def zm():

    ocr = ddddocr.DdddOcr(old=True)
    for i in ['z1.jpg', 'z2.jpg']:
        with open(i, 'rb') as f:
            image = f.read()

        res = ocr.classification(image)
        print(res)
