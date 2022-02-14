from PIL import Image

xin_img = Image.open('xx.png')
w ,y = xin_img.size
xin = xin_img.resize((w, w),Image.BILINEAR)

border = 15
img_new = Image.new('RGB', (w + 2 * border, w + 2 * border), (255,255,255))
img_new.paste(xin, (border, border), xin)
xin = img_new.convert('RGBA')
w, y = xin.size
xin.show()

points = [(0, 0), (w, 0), (2 * w, 0), (0, w),(w,w),(2 * w,w),(0, 2 * w),(w,2 * w),(2 * w,2 * w)]

imgs=[(6,8,9),(4,6,7,8,9),(4,7,8),(1,2,3,4,5,6,8,9),(1,2,3,4,5,6,7,8,9),(1,2,3,4,5,6,7,8),(3 , -1),(1,2,3,4,5,6,8),(1, -1)]

file_name = 0
for img in imgs:
    bgimg=Image.new("RGB",(w * 3,w * 3), (255,255,255))
    for item in img:
        if(item == -1):
            continue
        bgimg.paste(xin, points[item - 1], xin)

    file_name = file_name + 1
    bgimg.save(f"{file_name}.png")
