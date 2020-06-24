import os
import requests
import json


def send_to_timer(timetype, continental, capital):
    timer_host = os.getenv('TIMER_HOST', '0.0.0.0')
    timer_port = os.getenv('TIMER_PORT', '8080')
    resp = requests.get('http://{}:{}/{}/{}/{}'.format(
        timer_host, timer_port, timetype, continental, capital))
    return json.loads(resp.text)
