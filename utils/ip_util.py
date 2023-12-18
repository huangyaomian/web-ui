import socket
import requests

from utils.mysql import db_get_email


def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


def get_public_ip_address():
    url = 'https://httpbin.org/ip'
    response = requests.get(url)
    data = response.json()
    ip_address = data['origin']
    return ip_address


if __name__ == '__main__':
    print(get_ip_address())
    db_get_email()
    print(get_public_ip_address())
