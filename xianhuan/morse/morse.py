#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 闲欢
"""

# 表示摩斯密码图的字典
MORSE_CODE_DICT = {
                   'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..',
                   '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....',
                   '7': '--...', '8': '---..', '9': '----.', '0': '-----',
                   ', ': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-',
                   '(': '-.--.', ')': '-.--.-'
                   }


# 根据摩斯密码图对字符串进行加密的函数
def encrypt(message):
    cipher = ''
    for letter in message:
        if letter != ' ':
            # 查字典并添加对应的摩斯密码
            # 用空格分隔不同字符的摩斯密码
            cipher += MORSE_CODE_DICT[letter] + ' '
        else:
            # 1个空格表示不同的字符
            # 2表示不同的词
            cipher += ' '
    return cipher


# 将字符串从摩斯解密为英文的函数
def decrypt(message):
    # 在末尾添加额外空间以访问最后一个摩斯密码
    message += ' '
    decipher = ''
    citext = ''
    global i
    for letter in message:
        # 检查空间
        if letter != ' ':
            i = 0
            # 在空格的情况下
            citext += letter
        # 在空间的情况下
        else:
            # 如果 i = 1 表示一个新字符
            i += 1
            # 如果 i = 2 表示一个新单词
            if i == 2:
                # 添加空格来分隔单词
                decipher += ' '
            else:
                # 使用它们的值访问密钥（加密的反向）
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
                citext = ''
    return decipher



def main():
    message = "I LOVE YOU"
    result = encrypt(message.upper())
    print(result)

    message = "..  .-.. --- ...- .  -.-- --- ..-"
    result = decrypt(message)
    print(result)


# 执行主函数
if __name__ == '__main__':
    main()
