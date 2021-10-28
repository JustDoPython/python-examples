from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont

img = Image.open('cat.jpg')
print(F'图片大小为 {img.format}, 格式为 {img.size}, 模式为 {img.mode}')

# img.show()

# img.save("cat.png")

# 剪裁
#point = (1500, 800, 3000, 2300)
#img_crop = img.crop(point)
#img_crop.show()

# 覆盖
#img.paste(img_crop, (0, 0), None)
#img.show()

# 缩略图
# thumb_size = (345, 345)
# img.thumbnail(thumb_size)
# img.show()

# 旋转
# img_rotate = img.transpose(Image.ROTATE_90)
# img_rotate.show()

# 滤镜
# 高斯模糊
# img_gaussianblur = img.filter(ImageFilter.GaussianBlur(30))
# img_gaussianblur.show()

# 轮廓
# img_contour = img.filter(ImageFilter.CONTOUR)
# img_contour.show()

# 增强
#color = ImageEnhance.Color(img)
#img_color = color.enhance(1.5)
#img_color.show()

# draw = ImageDraw.Draw(img)

# 画线
# draw.line((0, 0) + img.size, fill=20, width=3)
# draw.line((0, img.size[1], img.size[0], 0), fill=200, width=3)

# 写字
# font = ImageFont.truetype('AliPuHui-Bold.ttf', 200)
# text = 'This is a cat!'
# drawing text size
# draw.text((450, 450), text, font=font, fill='pink', align="left")
# img.show()