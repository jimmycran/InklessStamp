from tkinter import *
from tkinter import filedialog

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, Paragraph, Table
from reportlab.lib import colors

import os

root = Tk()

# This opens a dialog box to select the Invoice that you wish to stamp.
file_path = filedialog.askopenfilename()

c = canvas.Canvas('BayWaStamp.pdf', pagesize=A4)  # alternatively use bottomup=False
width, height = A4

invoice_number = input('What is the invoice number? ')
nominal = input('What is the nominal? ')


data = [
    ['Invoice No.', str(invoice_number), 'Nominal', str(nominal)],
    ['1st Approver', '                    ', '2nd Approver', '                    '],
    ['Date', '', 'Date', ''],
]

table = Table(data, colWidths=30*mm)
table.setStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                ('BACKGROUND', (0,0), (-1,-1), colors.whitesmoke),
                ("ALIGN", (0,0), (-1,-1), "CENTER"),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                ('BOX', (0,0), (-1,-1), 0.25, colors.black)])

table.wrapOn(c, width, height)
table.drawOn(c, 30*mm, 270*mm)

styles = getSampleStyleSheet()
ptext = " "
p = Paragraph(ptext, style=styles["Normal"])
p.wrapOn(c, 50*mm, 50*mm)  # size of 'textbox' for linebreaks etc.
p.drawOn(c, 0*mm, 0*mm)    # position of text / where to draw

c.save()


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
        watermark=r'C:\Users\james.cran\PycharmProjects\TestProject\BayWaStamp.pdf')

os.startfile(file_path)

root.quit()
