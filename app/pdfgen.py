

from pydantic import BaseModel
from typing import Optional
from urllib.request import urlretrieve
import io
import os
import fpdf
from PyPDF2 import PdfFileWriter, PdfFileReader
from controls import Controls
from deps import s3
import uuid
from conf import config
from pathlib import Path
import requests
from datetime import datetime


class ResPayload(BaseModel):
    url: Optional[str] = None
    docdata: Optional[object] = None
    valuedata: Optional[object] = None
    bucket: Optional[str] = None
    completiondate: Optional[object] = None

    class Config:
        arbitrary_types_allowed = True


class Payload(BaseModel):
    url: Optional[str] = None
    doc: Optional[object] = None
    value: Optional[object] = None
    completiondate: Optional[object] = None

    class Config:
        arbitrary_types_allowed = True


class SQSPayload(BaseModel):
    drid: str
    dmid: str
    cmpid: int

    class Config:
        arbitrary_types_allowed = True


class PdfGen(object):
    def __init__(self, payload):
        if payload != None:
            self.template_url = payload.url
            self.doc = payload.doc
            self.value = payload.value
        self.pdf = fpdf.FPDF(format='A4', unit='mm', )
        # self.pdf.set_margins(0,0)
        self.pdf.set_top_margin(55)
        self.pdf.set_auto_page_break(False)
        self.pages = []

    def setPayload(self, payload):
        self.template_url = payload.url
        self.doc = payload.doc
        self.value = payload.value
        self.completiondate = payload.completiondate
        self.pages = []

    def generate(self, cmp):
        self.gencontrol = Controls(self.pdf)
        for page in self.doc:
            self.pdf.add_page()
            print("page", page)
            self.pages.append(int(page) - 1)
            for control in self.doc[page]:
                ctrl = self.doc[page][control]
                try:
                    recipient = self.extractRecipientName(ctrl)
                    if ctrl['type'] == 'signdate':
                        ctrl['val'] = self.getSigndate(recipient, ctrl)
                    else:
                        ctrl['val'] = self.value[ctrl['id']]['val']
                    self.writeonpage(ctrl)
                except Exception as e:
                    print("exception in writing control ",  e)

        return self.finalizePdf(cmp)

    def download_pdf_locally(self, url):
        file_name = config.temp_folder + \
            '/live_' + str(uuid.uuid4()) + '.pdf'
        urlretrieve(url, file_name)
        return file_name

    def finalizePdf(self, cmp):

        result_pdf_file_name = config.temp_folder + \
            '/' + str(uuid.uuid4()) + '.pdf'
        d = self.pdf.output(None, 'S')
        self.pdf.close()

        # Take the PDF you created above and overlay it on your template PDF
        # Open your template PDFpdf_template_file_name
        live_temp_template_path = self.download_pdf_locally(self.template_url)
        pdf_template = PdfFileReader(open(live_temp_template_path, 'rb'))
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
            # overlay_pdf = PdfFileReader(open(overlay_pdf_file_name, 'rb'))
            # Merge the overlay page onto the template page
            if page in self.pages:
                overlaypagecount = overlaypagecount + 1
                template_page = pdf_template.getPage(page)
                template_page.mergePage(overlay_pdf.getPage(overlaypagecount))
            # Write the result to a new PDF file

        output_pdf.appendPagesFromReader(pdf_template)
        output_pdf.write(open(result_pdf_file_name, "wb"))
        s3_bucket_file_name = 'finaldoc/'+Path(result_pdf_file_name).name
        bucket_name = config.bucket + str(cmp)
        if config.debug == False:
            s3.upload_to_aws(result_pdf_file_name,
                             bucket_name, s3_bucket_file_name)
            self.remove_temp_file(result_pdf_file_name)
            self.remove_temp_file(live_temp_template_path)

        return s3_bucket_file_name

    def remove_temp_file(self, file_name):
        os.remove(file_name)

    def writeonpage(self, control):
        getattr(self.gencontrol, control['type'])(control)

    def extractRecipientName(self, ctrl):
        if 'extras' in ctrl:
            if 'recipient' in ctrl['extras']:
                if 'val' in ctrl['extras']['recipient']:
                    return ctrl['extras']['recipient']['val']
        return ""

    def getSigndate(self, recipeint_key, control):
        if recipeint_key in self.completiondate:
            try:
                print("sign date", control)
                ds = control['dataset']
                format = '%m-%d-%Y'
                if 'dateFormat' in ds:
                    if control['dataset']['dateFormat'] == 'mm-dd-yyyy':
                        format = '%m-%d-%Y'
                    elif control['dataset']['dateFormat'] == 'yyyy-mm-dd':
                        format = '%Y-%m-%d'
                    elif control['dataset']['dateFormat'] == 'dd-mm-yyyy':
                        format = '%d-%m-%Y'
                print("format ->>", format)
                tmstr = self.completiondate[recipeint_key]
                if ":" == tmstr[-3]:
                    tmstr = tmstr[:-3]+tmstr[-2:]
                tm = datetime.strptime(
                    tmstr, '%Y-%m-%dT%H:%M:%S.%f%z')
                date = tm.strftime(format)
                print(self.completiondate,"<<- completion date" ,date, "<<- converted date")
                return date
            except Exception as e:
                print(e)
                return ""
