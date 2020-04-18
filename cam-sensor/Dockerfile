FROM python:3.6

RUN mkdir -p /app
WORKDIR /app
VOLUME /app

RUN pip -V && \
    pip install opencv-python paho-mqtt imutils

CMD python /app/main.py