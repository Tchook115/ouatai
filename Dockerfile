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
RUN python -m nltk.downloader -d /usr/local/share/nltk_data all
# RUN make run_rasa &
# RUN make run_rasa_action &

# CMD uvicorn API.api:app --host 0.0.0.0 --port $PORT
