import pdfplumber
import pyttsx3


def read_from_pdf():
    with pdfplumber.open("欺骗的艺术.pdf") as pdf:
        print('总页数 = ' + str(len(pdf.pages)))
        print('#' * 30)
        page = pdf.pages[3]
        text = page.extract_text()
        print('第四页内容如下：')
        print('#' * 30)
        print(text)
        read_by_mp3(text)


def read_by_mp3(text):
    engine = pyttsx3.init()  # 初始化语音引擎
    text = text.replace('\n', '')  # 去掉换行符
    engine.say(text)  # 读文本
    engine.runAndWait()

    # 保存文件
    # engine.save_to_file(text, 'test.mp3')
    # engine.runAndWait()


if __name__ == '__main__':
    read_from_pdf()
