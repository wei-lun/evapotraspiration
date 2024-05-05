"""
從 MQTT Broker 訂閱訊息
1. 收到後整理到*.CSV
"""

"""
  MQTTs at MiIoT
  Broker: "mqtts.miiot-agri.com"
  Port: 8883
  Client ID: NTU_PF306_DB
"""
import os
import paho.mqtt.client as MQTT
import ssl
import MongleDB_upload as mo


current_dir = os.path.dirname(__file__)

# ca_certs, certfile, keyfile, cert_reqs, tls_version, ciphers
ROOT_CA = "miot-ca.pem"
CLIENT_CERT = "mqtt-pub-client.crt"
CLIENT_KEY = "mqtt-pub-client.key"

root_ca_path = os.path.join(current_dir, ROOT_CA)
client_cert_path = os.path.join(current_dir, CLIENT_CERT)
client_key_path = os.path.join(current_dir, CLIENT_KEY)

# 讀取 MQTT 憑證
# with open(ROOT_CA, "r") as f:
#     ROOT_CA = f.read()
# with open(CLIENT_CERT, "r") as f:
#     CLIENT_CERT = f.read()
# with open(CLIENT_KEY, "r") as f:
#     CLIENT_KEY = f.read()

# MQTT Broker
MQTT_BROKER = "mqtts.miiot-agri.com"
MQTT_PORT = 8883
MQTT_CLIENT_ID = "NTU_PF306_DB"

# MQTT Topic
MQTT_TOPIC = "miiot"


def on_connect(client, userdata, flags, rc,mqtt_connect):
    print("Connected with result code "+str(rc))
    # 訂閱主題
    client.subscribe(MQTT_TOPIC+"/#")



def on_message(client, userdata, msg):
    print(f"[Topic]: {msg.topic}")
    _msg = None
    # try decode message
    try:
        _msg = msg.payload.decode("utf-8")
    except Exception as e:
        print(f"[ERROR]: Decode Error {e}: {_msg}")
        pass

    # try eval message
    try:
        _msg_json = eval(_msg)
        print(f"[Message]: {_msg}\r\n")

        topic_parts = msg.topic.split("/")
        collection_name = topic_parts[1]  # 假設主題格式為 "miiot/ISE000X/..."

        #print(f"[xxxxxxxxxxxxxxx]: {collection_name}\r\n")
        #db_instance = mo.MongleDB_uploading()
        if len(topic_parts) <= 2  and collection_name.startswith("ISE00"):
            db_instance.insert_data(collection_name, _msg_json)
        elif len(topic_parts) <= 2 and collection_name.startswith("ENV00"):
            db_instance.insert_data_env(collection_name, _msg_json)
        
    except Exception as e:
        print(f"[ERROR]: Eval Error {e}: {_msg}")
        pass


if __name__ == "__main__":

    db_instance = mo.MongleDB()
    # 建立一個 HTTPS 連線，並且加入憑證
    sub_client = MQTT.Client(MQTT.CallbackAPIVersion.VERSION2,MQTT_CLIENT_ID)
    sub_client.on_connect = on_connect
    sub_client.on_message = on_message

    # # 設置 STL 加密
    """sub_client.tls_set(ca_certs=ROOT_CA, certfile=CLIENT_CERT, keyfile=CLIENT_KEY,
                       cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)"""
    sub_client.tls_set(ca_certs=root_ca_path, certfile=client_cert_path, keyfile=client_key_path,
                       cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
    
    # # 設置 MQTT 服務器的地址和端口
    sub_client.connect(MQTT_BROKER, 8883, 60)  # 60為keepalive的時間間隔


    # # 保持客戶端連接
    sub_client.loop_forever()
