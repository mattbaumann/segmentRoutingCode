import logging
from enum import IntEnum
from typing import List

import requests

from src.backend.model.policy import Policy


class Commands(IntEnum):
    """ The possible commands sent by the command server """
    READ = 1
    WRITE = 2


def send_answer(policies: List[Policy], config: dict, logger: logging.Logger):
    """ Sends the answer of a read """
    string = "[" + ",".join(policy.json() for policy in policies) + "]"
    logger.info("Send response: " + string)
    requests.post(config["config"]["server"] + "update", json=string).raise_for_status()


def receive_command(config: dict):
    """ Questions the server which command should be executed """
    base = config["config"]["server"]

    url = base + "command"
    response = requests.post(url, data=config["version"].__str__())
    response.raise_for_status()
    if response.status_code == 204:
        return Commands.READ, None
    else:
        return Commands.WRITE, parse_json(response)


def parse_json(response: requests.Response):
    """ Parses the JSON transfer format into classes """
    json = response.json()
    if json is None:
        return None

    policies: List[Policy] = []
    policies.extend(map(lambda obj: Policy.parse_json(obj), json))
    return policies
