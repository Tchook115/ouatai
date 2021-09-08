FROM python:3.8.6-buster

COPY API /API
COPY ouatai /ouatai
COPY rasa_ouatai /rasa_ouatai
COPY raw_data /raw_data
COPY scripts /scripts
COPY sketchrnn_ouatai /sketchrnn_ouatai
COPY Makefile /Makefile
COPY requirements.txt /requirements.txt
COPY setup.py /setup.py

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn api.simple:app --host 0.0.0.0 --port $PORT