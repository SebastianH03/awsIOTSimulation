import json
import time
import ssl
import random
from paho.mqtt import client as mqtt

ENDPOINT = "a20fed1biem1tq-ats.iot.us-east-1.amazonaws.com"
PORT = 8883
CLIENT_ID = "sensor03"
TOPIC = "hogar/cocina/gas/sensor03"

CA_PATH = "../amazon_root/AmazonRootCA1.pem"
CERT_PATH = "sensor03.cert.pem"
KEY_PATH = "sensor03.private.key"

def on_connect(client, userdata, flags, rc):
    print("Conectado sensor03 con código:", rc)

client = mqtt.Client(client_id=CLIENT_ID)
client.on_connect = on_connect
client.tls_set(ca_certs=CA_PATH, certfile=CERT_PATH, keyfile=KEY_PATH, tls_version=ssl.PROTOCOL_TLSv1_2)
client.connect(ENDPOINT, PORT)
client.loop_start()

try:
    while True:
        payload = {
            "sensor": CLIENT_ID,
            "value": random.choice([True, False]),
            "unit": "bool",
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        }
        client.publish(TOPIC, json.dumps(payload), qos=1)
        print(f"[sensor01] Publicado en {TOPIC}: {payload}")
        time.sleep(5)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    print("Sensor01 detenido.")
