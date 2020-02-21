from tkinter import *
from tkinter import filedialog

root = Tk()

file_path = filedialog.askopenfilename()

# List of Lists
invoice_number = input('What is the invoice number? ')
nominal = input('What is the nominal? ')

data = [
    ['Invoice No.', str(invoice_number), 'Nominal', str(nominal)],
    ['1st Approver', '                    ', '2nd Approver', '                    '],
    ['Date', '', 'Date', ''],
]

fileName = 'pdfTable.pdf'

from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter

pdf = SimpleDocTemplate(
    fileName,
    pagesize=letter
)

from reportlab.platypus import Table
table = Table(data)

# add style
from reportlab.platypus import TableStyle
from reportlab.lib import colors

style = TableStyle([
    ('BACKGROUND', (0,0), (3,0), colors.white),
    ('TEXTCOLOR',(0,0),(-1,0),colors.black),

    ('ALIGN',(0,0),(-1,-1),'LEFT'),

    ('BOTTOMPADDING', (0,0), (-1,0), 5),

#    ('BACKGROUND',(0,1),(-1,-1),colors.beige),
])
table.setStyle(style)

# 2) Alternate backgroud color
#rowNumb = len(data)
#for i in range(1, rowNumb):
#    if i % 2 == 0:
#        bc = colors.burlywood
#    else:
#        bc = colors.beige
#
#    ts = TableStyle(
#        [('BACKGROUND', (0,i),(-1,i), bc)]
#    )
#    table.setStyle(ts)

# 3) Add borders
ts = TableStyle(
    [
    ('BOX',(0,0),(-1,-1),2,colors.black),

    ('LINEBEFORE',(2,1),(2,-1),2,colors.red),
    ('LINEABOVE',(0,2),(-1,2),2,colors.green),

    ('GRID',(0,0),(-1,-1),2,colors.black),
    ]
)
table.setStyle(ts)

elems = []
elems.append(table)

pdf.build(elems)



from PyPDF4 import PdfFileWriter, PdfFileReader


def create_watermark(input_pdf, output, watermark):
    watermark_obj = PdfFileReader(watermark)
    watermark_page = watermark_obj.getPage(0)

    pdf_reader = PdfFileReader(input_pdf)
    pdf_writer = PdfFileWriter()

    # Watermark all the pages
    for page in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page)
        page.mergePage(watermark_page)
        pdf_writer.addPage(page)

    with open(output, 'wb') as out:
        pdf_writer.write(out)


if __name__ == '__main__':
    create_watermark(
        input_pdf=(file_path),
        output=(file_path),
        watermark=r'C:\Users\james.cran\PycharmProjects\TestProject\pdfTable.pdf')

root.quit()
