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

COPY my_wrapper_script.sh /my_wrapper_script.sh

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m nltk.downloader -d /usr/local/share/nltk_data all
RUN chmod -R 755 ./my_wrapper_script.sh

CMD ./my_wrapper_script.sh
# RUN make run_rasa &
# RUN make run_rasa_action &

#CMD make run_rasa & make run_rasa_action & uvicorn API.api:app --host 0.0.0.0 --port $PORT
