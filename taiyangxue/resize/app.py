from PIL import Image, ImageDraw, ImageFont
import os
import time

def process(imgPath, destPath=None, size=(800,600), text=""):
    destPath = destPath if destPath else os.path.join(imgPath,'out','')
    if not os.path.isdir(destPath):
        os.makedirs(destPath)

    files = [x for x in os.listdir(imgPath) if os.path.isfile(imgPath + x)]
    print("待处理文件个数:", len(files))
    start = time.time()
    print("开始处理 ", start)
    for f in files:
        fext = os.path.splitext(f)[1]   # 扩展名
        if fext in ['.png', '.jpg', '.bmp', '.jpeg']:
            img = Image.open(os.path.join(imgPath, f))
            img = resize(img, size)
            img = waterMark(img, text)
            img.save(os.path.join(destPath,f))
    end = time.time()
    print("完成处理 %d, 耗时: %s秒" % (end, int(end-start)))


def resize(img, size):
    nsize = scale(img.size, size)
    return img.resize(nsize, Image.ANTIALIAS)
    
def waterMark(image, text, font=None):
    font = font if font else ImageFont.truetype(r"C:\Windows\Fonts\STHUPO.TTF", 24)
    mode = image.mode
    if mode != 'RGBA':
        rgba_image = image.convert('RGBA')
    else:
        rgba_image = image

    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    
    text_size_x, text_size_y = image_draw.textsize(text, font=font)
    # 设置文本文字位置
    text_xy = (rgba_image.size[0] - text_size_x - 10, rgba_image.size[1] - text_size_y - 10)
    # 设置文本颜色和透明度
    image_draw.text(text_xy, text, font=font, fill=(255, 255, 255, 100))
    
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)
    
    if mode != image_with_text.mode:
        image_with_text = image_with_text.convert(mode)

    return image_with_text

def scale(size, lsize):
    nsize = (size[0], size[1])
    if nsize[0] > lsize[0]:
        nsize = (lsize[0], int(lsize[0]*nsize[1]/nsize[0]))
    if nsize[1] > lsize[1]:
        nsize = (int(lsize[1]*nsize[0]/nsize[1]), lsize[1])
    return nsize

if __name__ == "__main__":
    process("D:\\images\\", text="@python技术")
    