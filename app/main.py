from typing import Optional

from fastapi import FastAPI

import json
import io 
from pdfgen import Payload, PdfGen

#from urllib2 import Request, urlopen

overlay_pdf_file_name = 'tuto1.pdf'
pdf_template_file_name = 'doc.pdf'
result_pdf_file_name = 'final_PDF.pdf'


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World 11533"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}




@app.post("/pdf/generate")
async def pdf_generate(payload: Payload):
    pdfGen = PdfGen(payload)
    pdfGen.generate()
    return {"item_id": payload}


