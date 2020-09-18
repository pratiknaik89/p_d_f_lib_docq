import io

import fpdf
from PyPDF2 import PdfFileWriter, PdfFileReader
#from urllib2 import Request, urlopen

overlay_pdf_file_name = 'tuto1.pdf'
pdf_template_file_name = 'doc.pdf'
result_pdf_file_name = 'final_PDF.pdf'

# This section creates a PDF containing the information you want to enter in the fields
# on your base PDF.
pdf = fpdf.FPDF(format='letter', unit='pt', )
pdf.add_page()
pdf_style = 'B'
pdf.set_font("Arial", style=pdf_style, size=10)
pdf.set_xy(0, 0)
pdf.cell(0, 10, txt='THIS IS THE TEXT THAT IS GOING IN YOUR FIELD', ln=0)


pdf.image('qqq.png',60,30,90,0,'', link = '')



d = pdf.output(overlay_pdf_file_name,'S')
pdf.close()

# Take the PDF you created above and overlay it on your template PDF
# Open your template PDFpdf_template_file_name
pdf_template = PdfFileReader(open(pdf_template_file_name, 'rb'))

# Get the first page from the template
template_page = pdf_template.getPage(0)
# Open your overlay PDF that was created earlier
overlay_pdf = None
# with io.BytesIO(d) as open_pdf_file:
overlay_pdf = PdfFileReader(io.BytesIO(d.encode("latin1")))
#overlay_pdf = PdfFileReader(open(overlay_pdf_file_name, 'rb'))
# Merge the overlay page onto the template page
template_page.mergePage(overlay_pdf.getPage(0))
# Write the result to a new PDF file
output_pdf = PdfFileWriter()
output_pdf.addPage(template_page)
output_pdf.write(open(result_pdf_file_name, "wb"))

