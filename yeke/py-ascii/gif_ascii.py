import os, imageio
from PIL import Image, ImageDraw, ImageFont

# 拆分 gif 将每一帧处理成字符画
def gif2pic(file, ascii_chars, isgray, font, scale):
    '''
    file: gif 文件
    ascii_chars: 灰度值对应的字符串
    isgray: 是否黑白
    font: ImageFont 对象
    scale: 缩放比例
    '''
    im = Image.open(file)
    path = os.getcwd()
    if(not os.path.exists(path+"/tmp")):
        os.mkdir(path+"/tmp")
    os.chdir(path+"/tmp")
    # 清空 tmp 目录下内容
    for f in os.listdir(path+"/tmp"):
        os.remove(f)
    try:
        while 1:
            current = im.tell()
            name = file.split('.')[0]+'_tmp_'+str(current)+'.png'
            # 保存每一帧图片
            im.save(name)
            # 将每一帧处理为字符画
            img2ascii(name, ascii_chars, isgray, font, scale)
            # 继续处理下一帧
            im.seek(current+1)
    except:
        os.chdir(path)

# 将不同的灰度值映射为 ASCII 字符
def get_char(ascii_chars, r, g, b):
    length = len(ascii_chars)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    return ascii_chars[int(gray/(256/length))]


# 将图片处理成字符画
def img2ascii(img, ascii_chars, isgray, font, scale):
    scale = scale
    # 将图片转换为 RGB 模式
    im = Image.open(img).convert('RGB')
    # 设定处理后的字符画大小
    raw_width = int(im.width * scale)
    raw_height = int(im.height * scale)
    # 获取设定的字体的尺寸
    font_x, font_y = font.getsize(' ')
    # 确定单元的大小
    block_x = int(font_x * scale)
    block_y = int(font_y * scale)
    # 确定长宽各有几个单元
    w = int(raw_width/block_x)
    h = int(raw_height/block_y)
    # 将每个单元缩小为一个像素
    im = im.resize((w, h), Image.NEAREST)
    # txts 和 colors 分别存储对应块的 ASCII 字符和 RGB 值
    txts = []
    colors = []
    for i in range(h):
        line = ''
        lineColor = []
        for j in range(w):
            pixel = im.getpixel((j, i))
            lineColor.append((pixel[0], pixel[1], pixel[2]))
            line += get_char(ascii_chars, pixel[0], pixel[1], pixel[2])
        txts.append(line)
        colors.append(lineColor)
    # 创建新画布
    img_txt = Image.new('RGB', (raw_width, raw_height), (255, 255, 255))
    # 创建 ImageDraw 对象以写入 ASCII
    draw = ImageDraw.Draw(img_txt)
    for j in range(len(txts)):
        for i in range(len(txts[0])):
            if isgray:
                draw.text((i * block_x, j * block_y), txts[j][i], (119,136,153))
            else:
                draw.text((i * block_x, j * block_y), txts[j][i], colors[j][i])
    img_txt.save(img)

# 读取 tmp 目录下文件合成 gif
def pic2gif(dir_name, out_name, duration):
    path = os.getcwd()
    os.chdir(dir_name)
    dirs = os.listdir()
    images = []
    num = 0
    for d in dirs:
        images.append(imageio.imread(d))
        num += 1
    os.chdir(path)
    imageio.mimsave(out_name + '_ascii.gif',images,duration = duration)


if __name__ == "__main__":
    ascii_chars = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
    fname = 'g2'
    font = ImageFont.truetype('Courier-New.ttf', size=int(6))
    gif2pic(fname + '.gif', ascii_chars, False, font, 1)
    pic2gif('tmp', fname, 0.2)
