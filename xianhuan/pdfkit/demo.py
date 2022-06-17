import pdfkit


path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

pdfkit.from_url(r'https://zhuanlan.zhihu.com/p/421726412', 'studypython.pdf', configuration=config)

pdfkit.from_file(r'C:\Users\cxhuan\Downloads\ttest\test.html','html.pdf', configuration=config)

pdfkit.from_string('talk is cheap, show me your code!','str.pdf', configuration=config)
 
