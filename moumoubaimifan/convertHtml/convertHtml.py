import pypandoc
import pdfkit

# web to pdf
pdfkit.from_url(['www.baidu.com','www.bing.com'],'search.pdf')

# html to pdf
pdfkit.from_file('/Users/xx/Desktop/html/baidu.html', 'html2pdf.pdf')

# html to word
output = pypandoc.convert_file('/Users/xx/Desktop/html/baidu.html', 'docx', outputfile="baidu.doc")