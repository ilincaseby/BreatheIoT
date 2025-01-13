import paho.mqtt.client as mqtt
import threading
import time
import subprocess
import random
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(aqi: int):
    fromMy = 'ilinca_sebastian@yahoo.com' # fun-fact: "from" is a keyword in python, you can't use it as variable.. did anyone check if this code even works?
    to  = 'ilincasebastian1406@gmail.com'
    subj='AQI too high'
    date='1/1/2025'
    message_text='AQI too high'

    msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % ( fromMy, to, subj, date, message_text )
    
    username = str('ilinca_sebastian@yahoo.com')  
    password = str('blmtwkbbejfywapq')  
    
    try :
        server = smtplib.SMTP("smtp.mail.yahoo.com",587)
        server.starttls()
        server.login(username,password)
        server.sendmail(fromMy, to,msg)
        server.quit()
    except Exception as e:
        print (f'can\'t send the Email{e}')

def on_connect(client, userdata, flags, rc):
    print(f'Conexiune stabilita cu codul {rc}')
    client.subscribe("ventsCommand")

def on_message(client, userdata, msg):
    print(f"buna, am primit o comanda{msg.payload.decode()}")
    result = subprocess.run(["./" + msg.payload.decode()], capture_output=True, text=True)

def periodic_task(client):
    notified_bad_air = False
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
                        message_send += "Motor speed:" + key_val[1].split(" ")[0] + "%20" + key_val[1].split(" ")[1] + "\n"
                    elif key_val[0] == 'Purify volume':
                        message_send += "Purify volume:" + key_val[1].split(" ")[1] + "%20metri%20cubi\n"
                    elif key_val[0] == 'Child lock':
                        message_send += "Child lock:" + key_val[1].split(" ")[1] + "\n"
        else:
            for line in lines:
                if ':' in line:
                    key_val = line.split(":")
                    if key_val[0] == 'Temperature':
                        message_send += "Temperature:" + key_val[1].split(" ")[1] + "%20grade%20Celsius\n"
                    elif key_val[0] == 'AQI':
                        if key_val[1].split(" ")[1] == 'None':
                            continue
                        message_send += "AQI:" + key_val[1].split(" ")[1] + "%20micrograme\n"
                        print(key_val[1])
                        print(int(key_val[1].split(" ")[1]))
                        aux = int(key_val[1].split(" ")[1])
                        if aux > 100 and notified_bad_air is False:
                            notified_bad_air = True
                            send_email(aux)
                        if aux < 80 and notified_bad_air is True:
                            notified_bad_air = False
                    elif key_val[0] == 'Filter left time':
                        message_send += "Filter left time:" + key_val[1].split(" ")[0] + "%20days\n"
                    elif key_val[0] == 'Humidity':
                        message_send += "Humidity:" + key_val[1].split(" ")[1] + "%25\n"
                    elif key_val[0] == 'Filter life remaining':
                        message_send += "Filter life remaining:" + key_val[1].split(" ")[1] + "%25\n"
        topic = "info"
        client.publish(topic, message_send)
        print(f'Am trimis asa:')
        print(f'{message_send}')
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