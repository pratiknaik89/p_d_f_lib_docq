from typing import Optional

from fastapi import FastAPI

import json
import io
from pdfgen import Payload, PdfGen
from deps import sqs
import threading
import os
from conf import config
from model import envmodel
import requests
#from urllib2 import Request, urlopen


def getEnv():
    url = config.API_URL_MAIN + '/getenv'
    x = requests.get(url, headers={'Content-Type': 'application/json'})
    jtext = x.json()
    _respayload = envmodel.EnvResp(**jtext['resultValue'])
    config.ACCESS_KEY =  _respayload.AWS_ACCESS_KEY_ID
    config.bucket =  _respayload.AWS_BUCKET_PREFIX+'cmp'
    config.REGION =  _respayload.AWS_SQS_REGION
    config.SECRET_KEY =  _respayload.AWS_SECRET_ACCESS_KEY
    config.QUEUE_URL = _respayload.AWS_SQS_URL
    




def create_temp_folder(folder):
    try:
        os.makedirs(folder)
    except OSError as e:
        print(e)
        pass
    
getEnv()
create_temp_folder(config.temp_folder)

# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World 11533"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}


# @app.post("/pdf/generate")
# async def pdf_generate(payload: Payload):
#     pdfGen = PdfGen(payload)
#     return pdfGen.generate()


try:
    sq = sqs.Sqs()
    th = threading.Thread(target=sq.start_que)
    th.start()

except:
    print ("Error: unable to start thread")
