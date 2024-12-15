
#esptool.py --port /dev/ttyUSB0 flash_id
#esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 ~/ESP32_GENERIC-20241129-v1.24.1.bin 
#ampy --port /dev/ttyUSB0 put esp32code.py

import network
import urequests
from umqtt.simple import MQTTClient
import _thread
import time
import ssl
import gc

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
while not wifi.isconnected():
    wifi.connect("TPLINKCDA", "0004Passw#")

client = 0
client_hivemq = 0

def mqqt_local_message(topic, msg):
    fields = {}
    lines = msg.decode().split("\n")

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
    urequests.get("https://api.thingspeak.com/update?api_key=JGKQ6GQ0WPMH80Y4" + ''.join([f'&{key}={value}' for key, value in fields.items()]))
    gc.collect()

def mqqt_local_client():
    global client
    
    client = MQTTClient("id_one", "192.168.0.78", 1883)
    client.set_callback(mqqt_local_message)

    try:
        client.connect()
        client.subscribe(b"info")

        while True:
            client.wait_msg()
            time.sleep(0.5)
    except Exception as e:
        print('Eroare pe partea de client ', e)
        client.disconnect()

def mqtt_hivemq_message(topic, msg):
    command = msg.decode()
    global client
    if command == "turn_off_airp":
        client.publish("ventsCommand".encode(), "./scripts/power/turn_off_airp.sh".encode())
    elif command == "turn_on_airp":
        client.publish("ventsCommand".encode(), "./scripts/power/turn_on_airp.sh".encode())
    elif command == "set_auto_mode":
        client.publish("ventsCommand".encode(), "./scripts/set_mode/set_auto_mode.sh".encode())
    elif command == "set_fan_mode":
        client.publish("ventsCommand".encode(), "./scripts/set_mode/set_fan_mode.sh".encode())
    elif command == "set_favorite_mode":
        client.publish("ventsCommand".encode(), "scripts/set_mode/set_favorite_mode.sh".encode())
    elif command == "set_silent_mode":
        client.publish("ventsCommand".encode(), "./scripts/set_mode/set_silent_mode.sh".encode())
    elif command == "set_anion_off":
        client.publish("ventsCommand".encode(), "./scripts/set_things/set_anion_off.sh".encode())
    elif command == "set_child_lock":
        client.publish("ventsCommand".encode(), "./scripts/set_things/set_child_lock.sh".encode())
    elif command == "set_anion":
        client.publish("ventsCommand", "./scripts/set_things/set_anion.sh".encode())
    elif command == "set_child_lock_off":
        client.publish("ventsCommand".encode(), "scripts/set_things/set_child_lock_off.sh".encode())
    gc.collect()

def mqtt_hivemq_client():
    global client_hivemq

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_NONE
    client_hivemq = MQTTClient("pico", "379c82a6c6934b6db7eb23e46479c875.s1.eu.hivemq.cloud", 8883, "sebii", "Sebi1406", ssl=context)
    client_hivemq.set_callback(mqtt_hivemq_message)

    try:
        client_hivemq.connect()
        client_hivemq.subscribe(b"commands")

        while True:
            client_hivemq.wait_msg()
            time.sleep(0.5)
    
    except Exception as e:
        print('Exceptie client hivemq ', e)
        client_hivemq.disconnect()

_thread.start_new_thread(mqqt_local_client, ())
mqtt_hivemq_client()