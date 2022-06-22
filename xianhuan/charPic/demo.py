#!/usr/bin/python3
#coding: utf-8

from PIL import Image

ascii_char = list('M3NB6Q#OC?7>!:–;. ')

def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ' '
    
    grey = (2126 * r + 7152 * g + 722 * b) / 10000
    
    char_idx = int((grey / (alpha + 1.0)) * len(ascii_char))
    return ascii_char[char_idx]

def write_file(out_file_name, content):
    with open(out_file_name, 'w') as f:
        f.write(content)

def main(file_name="input.jpg", width=100, height=80, out_file_name='output.txt'):
    text = ''
    im = Image.open(file_name)
    im = im.resize((width, height), Image.NEAREST)
    for i in range(height):
        for j in range(width):
            text += get_char(*im.getpixel((j, i)))
        text += '\n'
    print(text)
    write_file(out_file_name, text)

if __name__ == '__main__':
    main('dance.png')

