FROM eclipse-mosquitto

RUN mkdir -p /auth
COPY mqttauth.txt /auth
COPY mosquitto.conf /

RUN mosquitto_passwd -U /auth/mqttauth.txt