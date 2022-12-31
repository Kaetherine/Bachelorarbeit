import subprocess
import random
import requests

def ip_creator(interface_id):

    position_1 = random.randint(0,255)
    position_2 = random.randint(0,255)

    ip = f'192.168.{position_1}.{position_2}'
    command = f'sudo ifconfig {interface_id} {ip} up'
    subprocess.call(command, shell = True)

    try:
        response = requests.get('https://ipinfo.io/json')
    except:
        response = 'error'
    return response, ip

ip_creator('ens33')

