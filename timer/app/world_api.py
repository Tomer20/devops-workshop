from logger import logger
import requests
import json


def get_datetime(continental, capital):
    response = requests.get(
        'http://worldtimeapi.org/api/timezone/{}/{}'.format(
            continental, capital))
    logger.debug("response: {}".format(response.text))
    return json.loads(response.text)['datetime']


def get_epochtime(continental, capital):
    response = requests.get(
        'http://worldtimeapi.org/api/timezone/{}/{}'.format(
            continental, capital))
    logger.debug("response: {}".format(response.text))
    return json.loads(response.text)['unixtime']
