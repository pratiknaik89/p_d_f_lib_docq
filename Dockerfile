FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
 

RUN pip install PyPDF2
RUN pip install fpdf
RUN pip install Pillow

COPY ./app /app
