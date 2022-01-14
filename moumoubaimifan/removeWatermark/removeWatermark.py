#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from PIL import Image
from itertools import product
import fitz
import os


def remove_img():
    image_file = input("请输入图片地址：")
    img = Image.open(image_file)
    
    width, height = img.size

    for pos in product(range(width), range(height)):
        rgb = img.getpixel(pos)[:3]
        if(sum(rgb) >= 630):
            img.putpixel(pos, (255, 255, 255))

    img.save('d:/qsy.png')


def remove_pdf():
    page_num = 0
    pdf_file = input("请输入 pdf 地址：")
    pdf = fitz.open(pdf_file);
    for page in pdf:
        pixmap = page.get_pixmap()
        for pos in product(range(pixmap.width), range(pixmap.height)):
            rgb = pixmap.pixel(pos[0], pos[1])
            if(sum(rgb) >= 630):
                pixmap.set_pixel(pos[0], pos[1], (255, 255, 255))
        pixmap.pil_save(f"d:/pdf_images/{page_num}.png")
        print(f"第{page_num}水印去除完成")
        page_num = page_num + 1

def pic2pdf():
    pic_dir = input("请输入图片文件夹路径：")
    
    pdf = fitz.open()
    img_files = sorted(os.listdir(pic_dir),key=lambda x:int(str(x).split('.')[0]))
    for img in img_files:
        print(img)
        imgdoc = fitz.open(pic_dir + '/' + img)  
        pdfbytes = imgdoc.convertToPDF()   
        imgpdf = fitz.open("pdf", pdfbytes)
        pdf.insertPDF(imgpdf)       
    pdf.save("images.pdf")         
    pdf.close()

if __name__ == "__main__":
    pic2pdf()
