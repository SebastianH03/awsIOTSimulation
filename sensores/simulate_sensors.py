import json
import time
import ssl
import random
from paho.mqtt import client as mqtt

# === Configuración de conexión ===
ENDPOINT = "a20fed1biem1tq-ats.iot.us-east-1.amazonaws.com"  # <-- CAMBIA ESTO
PORT = 8883
CLIENT_ID = "iot-multi-sensor-client"

# === Certificados del sensor01 ===
CA_PATH = "sensor01/AmazonRootCA1.pem"
CERT_PATH = "sensor01/sensor01.cert.pem"
KEY_PATH = "sensor01/sensor01.private.key"


# === Definición de sensores y topics ===
SENSORS = [
    {
        "id": "sensor01",
        "topic": "hogar/sala/movimiento/sensor01"
    },
    {
        "id": "sensor02",
        "topic": "hogar/entrada/contacto/sensor02"
    },
    {
        "id": "sensor03",
        "topic": "hogar/cocina/gas/sensor03"
    }
]

# === Conexión MQTT ===
def on_connect(client, userdata, flags, rc):
    print("Conectado a AWS IoT con código: " + str(rc))

client = mqtt.Client(client_id=CLIENT_ID)
client.on_connect = on_connect
client.tls_set(ca_certs=CA_PATH,
               certfile=CERT_PATH,
               keyfile=KEY_PATH,
               tls_version=ssl.PROTOCOL_TLSv1_2)

client.connect(ENDPOINT, PORT)
client.loop_start()

# === Simulación de datos ===
try:
    while True:
        for sensor in SENSORS:
            payload = {
                "sensor": sensor["id"],
                "value": random.choice([True, False]),
                "unit": "bool",
                "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            }
            client.publish(sensor["topic"], json.dumps(payload), qos=1)
            print(f"Publicado en {sensor['topic']}: {payload}")
        time.sleep(5)  # cada 5 segundos
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    print("Simulación detenida.")
