from logger import logger
import json


def get_users_from_file():
    try:
        with open('../config.json') as json_file:
            data = json.load(json_file)
            auth_users = data.get('auth_users')
        logger.debug("Allowed users: {}".format(auth_users))
    except FileNotFoundError:
        logger.debug("config.json file is missing, adding dummy user")
        auth_users = ['dummy']
        logger.debug("Allowed users: {}".format(auth_users))
    return auth_users
