import paho.mqtt.client as mqtt
import threading
import time
import subprocess

def on_connect(client, userdata, flags, rc):
    print(f'Conexiune stabilita cu codul {rc}')
    client.subscribe("ventsCommand")

def on_message(client, userdata, msg):
    result = subprocess.run(["./" + msg.payload.decode()], capture_output=True, text=True)

def periodic_task(client):
    while True:
        result = subprocess.run(["./scripts/get_status/get_status.sh"], capture_output=True, text=True)
        
        payload = result.stdout
        topic = "info"
        client.publish(topic, payload)
        
        time.sleep(2)

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