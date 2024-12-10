import paho.mqtt.client as mqtt
import requests

headers = {
    "Content-Type": "application/json"
}

def on_connect(client, userdata, flags, rc):
    print(f'Conexiune stabilita cu codul {rc}')
    client.subscribe("info")

def on_message(client, userdata, msg):
    lines = msg.payload.decode().split("\n")
    basic_url = "https://api.thingspeak.com/update?api_key=JGKQ6GQ0WPMH80Y4"

    # Inițializăm un dicționar pentru a salva valorile câmpurilor
    fields = {}

    for line in lines:
        if ':' in line:
            key_val = line.split(":")
            if key_val[0] == 'Temperature':
                fields['field1'] = key_val[1]
            elif key_val[0] == 'AQI':
                fields['field2'] = key_val[1]
            elif key_val[0] == 'Filter left time':
                fields['field3'] = key_val[1]
            elif key_val[0] == 'Humidity':
                fields['field4'] = key_val[1]
            elif key_val[0] == 'Filter life remaining':
                fields['field5'] = key_val[1]
            elif key_val[0] == 'Motor speed':
                fields['field6'] = key_val[1]
            elif key_val[0] == 'Purify volume':
                fields['field7'] = key_val[1]
            elif key_val[0] == 'Child lock':
                fields['field8'] = key_val[1]

    # Construim URL-ul pentru cererea GET cu toate câmpurile
    url = basic_url + ''.join([f'&{key}={value}' for key, value in fields.items()])

    # Trimitem cererea GET cu toate câmpurile într-o singură cerere
    requests.get(url)

def on_connect1(client, userdata, flags, rc):
    print(f'Conexiune client1 stabilita cu codul {rc}')
    client.subscribe("commands")

def on_disconnect(client, packet_from_broker, v1_rc):
    print(f"{packet_from_broker} {v1_rc}")

def on_message1(client1, userdata, msg):
    command = msg.payload.decode()
    if command == "turn_off_airp":
        client.publish("ventsCommand", "./scripts/power/turn_off_airp.sh")
    elif command == "turn_on_airp":
        client.publish("ventsCommand", "./scripts/power/turn_on_airp.sh")
    elif command == "set_auto_mode":
        client.publish("ventsCommand", "./scripts/set_mode/set_auto_mode.sh")
    elif command == "set_fan_mode":
        client.publish("ventsCommand", "./scripts/set_mode/set_fan_mode.sh")
    elif command == "set_favorite_mode":
        client.publish("ventsCommand", "scripts/set_mode/set_favorite_mode.sh")
    elif command == "set_silent_mode":
        client.publish("ventsCommand", "./scripts/set_mode/set_silent_mode.sh")
    elif command == "set_anion_off":
        client.publish("ventsCommand", "./scripts/set_things/set_anion_off.sh")
    elif command == "set_child_lock":
        client.publish("ventsCommand", "./scripts/set_things/set_child_lock.sh")
    elif command == "set_anion":
        client.publish("ventsCommand", "./scripts/set_things/set_anion.sh")
    elif command == "set_child_lock_off":
        client.publish("ventsCommand", "scripts/set_things/set_child_lock_off.sh")

client = mqtt.Client(client_id="pi")

client.on_connect = on_connect
client.on_message = on_message

broker = "localhost"
port = 1883

client.connect(broker, port)

client1 = mqtt.Client(client_id="pico")
client1.on_connect = on_connect1
client1.on_message = on_message1
client1.on_disconnect = on_disconnect
client1.username_pw_set("sebii", "Sebi1406")
port1 = 8883
client1.tls_set()

broker1 = "379c82a6c6934b6db7eb23e46479c875.s1.eu.hivemq.cloud"

client1.connect(broker1, port=port1)



client1.loop_start()
client.loop_start()
while True:
    pass