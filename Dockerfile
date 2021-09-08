FROM python:3.8.6-buster

COPY API /API
COPY ouatai /ouatai
COPY rasa-ouatai /rasa-ouatai
COPY raw_data /raw_data
COPY scripts /scripts
COPY sketchrnn_ouatai /sketchrnn_ouatai
COPY Makefile /Makefile
COPY requirements.txt /requirements.txt
COPY setup.py /setup.py

RUN pip install --upgrade pip
#RUN pip install -r requirements.txt
RUN pip install .
RUN: rasa shell

CMD: make run_local_illustration
