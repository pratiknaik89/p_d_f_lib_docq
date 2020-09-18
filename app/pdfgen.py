

from pydantic import BaseModel
import io

import fpdf
from PyPDF2 import PdfFileWriter, PdfFileReader
from controls import Controls


class Payload(BaseModel):
    url: str
    doc: object
    value: object

    class Config:
        arbitrary_types_allowed = True


class PdfGen(object):
    def __init__(self, payload):
        self.doc = payload.doc
        self.value = payload.value
        self.pdf = fpdf.FPDF(format='A4', unit='mm', )
        # self.pdf.set_margins(0,0)
        self.pdf.set_top_margin(55)
        self.pdf.set_auto_page_break(False)
        self.pages = []

    def generate(self):
        self.gencontrol = Controls(self.pdf)
        for page in self.doc:
            self.pdf.add_page()
            print("adding page")
            self.pages.append(int(page) - 1)
            for control in self.doc[page]:
                ctrl = self.doc[page][control]
                self.writeonpage(ctrl)

        self.finalizePdf()

    def finalizePdf(self):
        pdf_template_file_name = 'doc.pdf'
        result_pdf_file_name = 'final_PDF.pdf'
        d = self.pdf.output(None, 'S')
        self.pdf.close()

        # Take the PDF you created above and overlay it on your template PDF
        # Open your template PDFpdf_template_file_name
        pdf_template = PdfFileReader(open(pdf_template_file_name, 'rb'))
        numpages = pdf_template.getNumPages()
        overlay_pdf = None
        # with io.BytesIO(d) as open_pdf_file:
        overlay_pdf = PdfFileReader(io.BytesIO(d.encode("latin1")))
        page = -1
        output_pdf = PdfFileWriter()
        overlaypagecount = -1
       
        while page < numpages - 1:
            page = page + 1         
            # Get the first page from the template
            
            # Open your overlay PDF that was created earlier
            #overlay_pdf = PdfFileReader(open(overlay_pdf_file_name, 'rb'))
            # Merge the overlay page onto the template page
            if page in self.pages:
                overlaypagecount = overlaypagecount + 1
                template_page = pdf_template.getPage(page)
                template_page.mergePage(overlay_pdf.getPage(overlaypagecount))
            # Write the result to a new PDF file
            
        output_pdf.appendPagesFromReader(pdf_template)
        output_pdf.write(open(result_pdf_file_name, "wb"))

    def writeonpage(self, control):
        getattr(self.gencontrol, control['type'])(control)

    


