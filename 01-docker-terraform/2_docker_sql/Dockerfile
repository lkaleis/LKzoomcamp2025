FROM python:3.9

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2 

WORKDIR /app

COPY ingest_multiple_datasets.py ingest_multiple_datasets.py

ENTRYPOINT [ "python", "ingest_multiple_datasets.py" ]