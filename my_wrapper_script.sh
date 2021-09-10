#!/bin/bash

(cd ./rasa_ouatai && rasa run -m models --enable-api &)
sleep 1m
(cd ./rasa_ouatai && rasa run actions &)
sleep 1m
uvicorn API.api:app --host 0.0.0.0 --port $PORT

# Start the first process
#make run_rasa


# Start the second process
#make run_rasa_action


# Start the third process
#uvicorn API.api:app --host 0.0.0.0 --port 8000


# Naive check runs checks once a minute to see if either of the processes exited.
# This illustrates part of the heavy lifting you need to do if you want to run
# more than one service in a container. The container exits with an error
# if it detects that either of the processes has exited.
# Otherwise it loops forever, waking up every 60 seconds


