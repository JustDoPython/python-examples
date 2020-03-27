import PyPDF2

inputName = "input.pdf"
watermarkName = "watermark.pdf"
outputName = "output.pdf"

pdfInput = PyPDF2.PdfFileReader(inputName)
watermark = PyPDF2.PdfFileReader(watermarkName).getPage(0)

pdfWriter = PyPDF2.PdfFileWriter()

# print(pdfInput.numPages)
# print(pdfInput.getNumPages())

for i in range(pdfInput.numPages):
    page = pdfInput.getPage(i)
    page.mergePage(watermark)
    pdfWriter.addPage(page)

with open(outputName, "wb") as f:
    pdfWriter.write(f)