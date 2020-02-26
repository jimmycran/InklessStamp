from tkinter import *
from tkinter import filedialog

root = Tk()

# This opens a dialog box to select the Invoice that you wish to stamp.
file_path = filedialog.askopenfilename()

# The below the user input for the Invoice number and Nominal to be stamped
invoice_number = input('What is the invoice number? ')
nominal = input('What is the nominal? ')

# This is the dataframe that populates the stamp
data = [
    ['Invoice No.', str(invoice_number), 'Nominal', str(nominal)],
    ['1st Approver', '                    ', '2nd Approver', '                    '],
    ['Date', '', 'Date', ''],
]

fileName = 'pdfTable.pdf'

# Reportlab module is used to create the stamp file
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter

pdf = SimpleDocTemplate(
    fileName,
    pagesize=letter
)

from reportlab.platypus import Table
from reportlab.lib.enums import TA_LEFT
table = Table(data, vAlign=TA_LEFT)

elems = []
elems.append(table)

# add style
from reportlab.platypus import TableStyle
from reportlab.lib import colors

# Yet to figure out how to move the table up to the top of the page
style = TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.whitesmoke),
    ('TEXTCOLOR',(0,0),(-1,-1),colors.black),

    ('ALIGN',(0,0),(-1,-1),'LEFT'),
    ('BOX', (0, 0), (-1, -1), 2, colors.black),

    ('GRID', (0, 0), (-1, -1), 2, colors.black),

    ('BOTTOMPADDING', (0,0), (-1,0), 5),
])
table.setStyle(style)


pdf.build(elems)


# PyPDF4 is used to merge the stamp to the invoice file
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
