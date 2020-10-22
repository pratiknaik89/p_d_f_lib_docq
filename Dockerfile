FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
 

RUN pip3 install PyPDF2
RUN pip3 install fpdf
RUN pip3 install Pillow
RUN pip3 install boto3
RUN pip3 install requests


COPY ./app /app
