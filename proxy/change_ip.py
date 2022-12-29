import subprocess
import random
import requests
import time

def ip_creator(interface_id):

    # position_1 = random.randint(0,255)
    position_2 = random.randint(0,255)
    position_1 = '73'

    ip = f'192.168.{position_1}.{position_2}'
    command = f'sudo ifconfig {interface_id} {ip} up'
    subprocess.call(command, shell = True)

    try:
        response = requests.get('https://ipinfo.io/json', timeout=2)
        print(response.status_code)
    except:
        response = 'error'
        print(ip)
    return response, ip

ip_creator('ens33')

