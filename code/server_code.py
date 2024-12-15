import paho.mqtt.client as mqtt
import threading
import time
import subprocess
import random

def on_connect(client, userdata, flags, rc):
    print(f'Conexiune stabilita cu codul {rc}')
    client.subscribe("ventsCommand")

def on_message(client, userdata, msg):
    result = subprocess.run(["./" + msg.payload.decode()], capture_output=True, text=True)

def periodic_task(client):
    while True:
        result = subprocess.run(["./scripts/get_status/get_status.sh"], capture_output=True, text=True)
        
        payload = result.stdout
        message_send = ""
        lines = payload.split("\n")
        number = random.choice([1, 2, 3])
        if number == 1:
            for line in lines:
                if ':' in line:
                    key_val = line.split(":")
                    if key_val[0] == 'Motor speed':
                        message_send += "Motor speed:" + key_val[1] + "\n"
                    elif key_val[0] == 'Purify volume':
                        message_send += "Purify volume:" + key_val[1] + "\n"
                    elif key_val[0] == 'Child lock':
                        message_send += "Child lock:" + key_val[1] + "\n"
        else:
            for line in lines:
                if ':' in line:
                    key_val = line.split(":")
                    if key_val[0] == 'Temperature':
                        message_send += "Temperature:" + key_val[1] + "\n"
                    elif key_val[0] == 'AQI':
                        message_send += "AQI:" + key_val[1] + "\n"
                    elif key_val[0] == 'Filter left time':
                        message_send += "Filter left time:" + key_val[1] + "\n"
                    elif key_val[0] == 'Humidity':
                        message_send += "Humidity:" + key_val[1] + "\n"
                    elif key_val[0] == 'Filter life remaining':
                        message_send += "Filter life remaining:" + key_val[1] + "\n"
        topic = "info"
        client.publish(topic, message_send)
        
        time.sleep(1)

client = mqtt.Client(client_id="LocalServer")

client.on_connect = on_connect
client.on_message = on_message

broker = "localhost"
port = 1883

client.connect(broker, port)

task_thread = threading.Thread(target=periodic_task, args=(client,))
task_thread.daemon = True
task_thread.start()

client.loop_forever()