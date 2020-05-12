def love_python():
    word = "Python技术"
    for char in word.split():
        allChar = []
        for y in range(12, -12, -1):
            lst = []
            lst_con = ''
            for x in range(-30, 28):
                # 心型函数实现
                formula = ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (x * 0.05) ** 2 * (y * 0.1) ** 3
                if formula <= 0:
                    lst_con += char[(x) % len(char)]
                else:
                    lst_con += ' '
            lst.append(lst_con)
            allChar += lst
        print('\n'.join(allChar))

if __name__ == '__main__':
    love_python()
