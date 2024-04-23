from flask import Flask, render_template,jsonify
import paho.mqtt.client as mqtt
import json
import random
import ssl
import threading
app = Flask(__name__)

# MQTT 連接設定
mqtt_broker = "mqtts.miiot-agri.com"
mqtt_port = 8883
mqtt_topic = "miiot/ENV0001"
ca_cert = "miot-ca.pem"
certfile="mqtt-pub-client.crt"
keyfile="mqtt-pub-client.key"
mqtt_data = {}
mqtt_connected = False  # MQTT 連接狀態


def connect_mqtt():
    def on_connect(client, userdata, flags, rc,mqtt_connect):
        global mqtt_connected
        if rc == 0:
            print("Connected to MQTT Broker!")
            mqtt_connected = True
        else:
            print("Failed to connect, return code %d\n", rc)
            mqtt_connected = False
    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id)
    client.tls_set(ca_certs=ca_cert,certfile=certfile,keyfile=keyfile,cert_reqs=ssl.CERT_REQUIRED,tls_version=ssl.PROTOCOL_TLS)
    client.on_connect = on_connect
    client.connect(mqtt_broker, mqtt_port)
    return client

def subscribe(client: mqtt):
    def on_message(client, userdata, message):
        global mqtt_data
        mqtt_playload = json.loads(message.payload.decode())
        mqtt_data = mqtt_playload.get("data", {})

    client.subscribe(mqtt_topic)
    client.on_message = on_message

def update_data():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    #threading.Timer(60, update_data).start()
    return mqtt_data

update_data()



@app.route('/')
def index():
    #mqtt_data = update_data()
    global mqtt_data
    return render_template('index.html',data=mqtt_data)

@app.route('/get_new_data', methods=['GET'])
def send_new_data():
    new_data = mqtt_data
    return jsonify(new_data)

def auto_update():
    while True:
        update_data()
        threading.Timer(60, auto_update).start()  # 每 60 秒執行一次

if __name__ == '__main__':
    #global mqtt_data
    #update_data()
    app.run(debug=True, port=2000, host="0.0.0.0")