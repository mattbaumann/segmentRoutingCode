from enum import IntEnum
from typing import List

import requests

from src.backend.model.policy import Policy


class Commands(IntEnum):
    """ The possible commands sent by the command server """
    READ = 1
    WRITE = 2


def send_answer(policies: List[Policy], config: dict):
    """ Sends the answer of a read """
    string = "[" + ",".join(policy.json() for policy in policies) + "]"
    requests.post(config["config"]["server"] + "/update", data=string).raise_for_status()


def receive_command(config: dict):
    """ Questions the server which command should be executed """
    response = requests.post(config["config"]["server"] + "/command", data=config["version"])
    response.raise_for_status()
    if response.status_code == 240:
        return Commands.READ, None
    else:
        return Commands.WRITE, parse_json(response)


def parse_json(response: requests.Response):
    """ Parses the JSON transfer format into classes """
    json = response.json()
    policies: List[Policy] = []
    policies.extend(map(lambda obj: Policy.parse_json(obj), json))
    return policies
