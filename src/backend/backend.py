#!/usr/bin/env python3

from datetime import timedelta
from urllib.parse import urlparse

import requests
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_segment_routing_ms_cfg as sr_config
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_shellutil_oper as xr_shellutil_oper
from ydk.providers import NetconfServiceProvider
from ydk.services import CRUDService

from src.backend.configuration import load_config
from src.backend.logging import load_logger
from src.backend.parser import parse_policy


def load_data():
    config, server = load_config()
    device = urlparse(config["config"]["host"])

    logger = load_logger(config)
    logger.info(f"Connect to {device}")

    # create NETCONF session
    provider = NetconfServiceProvider(address=device.hostname,
                                      port=device.port,
                                      username=device.username,
                                      password=device.password,
                                      protocol=device.scheme)

    # create CRUD service
    crud = CRUDService()
    logger.info("System uptime is " + str(read_system_time(crud, provider)))
    policies = parse_policy(read_policy(crud, provider))

    if len(policies) > 0:
        print(policies[0].__str__())

    if server is None or server == "":
        server = "http://localhost:5000"

    string = "[" + ",".join(policy.json() for policy in policies) + "]"
    requests.post(server + "/update", data=string)


def read_policy(service: CRUDService, provider: NetconfServiceProvider):
    sr_config_mapping = sr_config.Sr()
    sr_config_mapping = service.read(provider, sr_config_mapping)
    return sr_config_mapping


def read_system_time(service: CRUDService, provider: NetconfServiceProvider):
    system_time = xr_shellutil_oper.SystemTime()
    system_time = service.read(provider, system_time)
    return timedelta(seconds=system_time.uptime.uptime)


if __name__ == "__main__":
    load_data()
