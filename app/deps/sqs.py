import boto3
from conf import config
from signal import signal, SIGINT, SIGTERM
from pdfgen import ResPayload, Payload, PdfGen, SQSPayload
import json

import requests
# Create SQS client


# class SignalHandler:
#     def __init__(self):
#         self.received_signal = False
#         signal(SIGINT, self._signal_handler)
#         signal(SIGTERM, self._signal_handler)

#     def _signal_handler(self, signal, frame):
#         print(f"handling signal {signal}, exiting gracefully")
#         self.received_signal = True

class Sqs:

    
    # sqs_queue = _sqs.GET(QueueName=config.QUEUE_URL)

    def start_que(self):
        self.sqs_client = boto3.client('sqs', aws_access_key_id=config.ACCESS_KEY,
                              aws_secret_access_key=config.SECRET_KEY,
                              region_name=config.REGION)
        if config.debug == True:
            data_set = {"Body":'{"cmpid":2,"drid":"27e6ed73-cf12-43d1-97b4-ea9e23e854c9", "dmid":"22df6ef0-14a8-4fa5-9c65-f5598e7cdb4b"}'}
            json_dump = json.dumps(data_set)
            message =  json.loads(json_dump)
            self.process_message(message)
            return
        while 1:
            response = self.sqs_client.receive_message(
                AttributeNames=[
                    'SentTimestamp'
                ],
                QueueUrl=config.QUEUE_URL,
                MessageAttributeNames=[
                    'All'
                ],
                WaitTimeSeconds=10,
                MaxNumberOfMessages=2
            )
            if 'Messages' not in response:
                print('waiting for message')
                continue

            for message in response['Messages']:
                try:
                    self.process_message(message)
                    receipt_handle = message['ReceiptHandle']
                    self.sqs_client.delete_message(
                        QueueUrl=config.QUEUE_URL,
                        ReceiptHandle=receipt_handle
                    )
                except Exception as e:
                    print(f"exception while processing message: {repr(e)}")
                    continue

            # Delete received message from queue

    def process_message(self, message):
        print(message['Body'])
        try:
            payload_dict = json.loads(message['Body'])
            sqspayload = SQSPayload(**payload_dict)
            self.pdfGen = PdfGen(None)
            self.callDocumentData(sqspayload)
            # print(payload)
            # self.pdfGen.setPayload(payload)
            # self.pdfGen.generate()
        except Exception as e:
            print(e)

    def callDocumentData(self, sqspayload: SQSPayload):
        url = config.getAPIURL(sqspayload.cmpid)
        url = url + '/document/getdoclinkbyid?drid='+sqspayload.drid
        x = requests.get(url, headers={'Content-Type': 'application/json'})
        jtext = x.json()

        _respayload = ResPayload(**jtext['resultValue'][0])

        url = json.loads(_respayload.url)

        _payload = Payload()
        _payload.doc = json.loads(_respayload.docdata)
        _payload.value = json.loads(_respayload.valuedata)
        _payload.url = _respayload.bucket+url['doc']
        _payload.completiondate = json.loads(_respayload.completiondate)

        self.pdfGen.setPayload(_payload)
        res_url = self.pdfGen.generate(sqspayload.cmpid)
        if config.debug == False:
            self.upload_Status_to_server(
               sqspayload.cmpid, res_url, sqspayload.drid, sqspayload.dmid)

    def upload_Status_to_server(self, cmpid, _url, _drid, _dmid):
        url = config.getAPIURL(cmpid)
        url = url + '/document/savefinaldocurl'

        x = requests.post(url, data={
            "finaldocurl": _url,
            "drid": _drid,
            "dmid": _dmid
        })
        print(x.text)
        jtext = x.json()
        _respayload = ResPayload(**jtext['resultValue'][0])
