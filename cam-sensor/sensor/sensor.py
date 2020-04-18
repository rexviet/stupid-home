import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import datetime
import paho.mqtt.client as mqtt
import json

class Sensor:
    def __init__(self, username, password, host="192.168.1.8", port=1883):
        self.auth = {'username': username, 'password': password}
        self.host = host
        self.port = port
        self.lastUpdated = {
            'state': None,
            'time': datetime.datetime.now()
        }
        client = mqtt.Client()
        client.username_pw_set("user", "passwd")
        client.on_connect = self.on_connect
        client.connect("192.168.1.8", 1883, 60)

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    def setState(self, state):
        now = datetime.datetime.now()
#         print('lastUpdated:', self.lastUpdated)
        seconds = (now - self.lastUpdated['time']).seconds
#         print("seconds:", seconds)
        if (state != self.lastUpdated['state'] or seconds >= 3):
            print("set state:", state)
            dict = {'occupied': state}
            print('dict:', dict)
            payload = json.dumps(dict)
            print('payload:', payload)
            publish.single(topic="cam_sensor/motion", hostname=self.host, auth=self.auth, payload = payload)
            self.lastUpdated['state'] = state
            self.lastUpdated['time'] = now
