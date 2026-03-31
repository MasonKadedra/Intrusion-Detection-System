import os

def send_alert(message):
    os.system(f'notify-send "HIDS Alert" "{message}"')
