import cv2
import numpy as np
from PIL import Image
from wordcloud import WordCloud

img = cv2.imread('test.png')
mask = np.zeros(img.shape[:2], np.uint8)
size = (1, 65)
bgd = np.zeros(size, np.float64)
fgd = np.zeros(size, np.float64)
rect = (1, 1, img.shape[1], img.shape[0])
cv2.grabCut(img, mask, rect, bgd, fgd, 10, cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask == 2) | (mask == 0), 1, 255)
img = img.astype(np.int32)
img *= mask2[:, :, np.newaxis]
img[img>255] = 255
img =img.astype(np.uint8)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = Image.fromarray(img, 'RGB')
img.save('test1.jpg')
fp = open(r"word.txt", "r", encoding="utf-8")
text = fp.read()
mask_pic=np.array(Image.open(r"test1.jpg"))
wordcloud = WordCloud(font_path='hyr3gjm.ttf',mask=mask_pic,max_words=200).generate(text)
image=wordcloud.to_image()
image.save("wordcloud2.png")
cloud_data = np.array(image)
alpha = np.copy(cloud_data[:,:,0])
alpha[alpha>0] = 255
new_image = Image.fromarray(np.dstack((cloud_data, alpha)))
card = Image.open("test.png")
card = card.convert("RGBA")
card.paste(new_image, (0,0), mask=new_image)
card.save("card.png")