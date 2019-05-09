#!/usr/bin/env python3
# import providers, services and models
import logging
import os
from argparse import ArgumentParser
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlparse

from ruamel.yaml import YAML
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_shellutil_oper as xr_shellutil_oper
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_crypto_ssh_oper as ssh_oper
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_segment_routing_ms_oper as sr_oper
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_segment_routing_ms_cfg as sr_config
from ydk.providers import NetconfServiceProvider
from ydk.services import CRUDService

boolean_dict = {
    "true": True,
    "false": False,
    "yes": True,
    "no": True,
    "on": True,
    "off": False
}
config_version = 1


def parse_bool(value_string):
    if isinstance(value_string, bool):
        return value_string
    else:
        return boolean_dict[value_string.lower()]


def convert_bool(config_dict):
    for key, value in config_dict.items():
        if isinstance(value, str) and value.lower() in boolean_dict:
            config_dict[key] = parse_bool(value)
        if isinstance(value, dict):
            convert_bool(value)


def load_config():
    # Parse config
    script_path = Path(os.path.dirname(os.path.abspath(__file__)))
    absolute_path = Path(script_path, "../../Test.yaml")

    assert (absolute_path.exists() and absolute_path.is_file())

    yaml_parser = YAML(typ='safe')
    yaml = yaml_parser.load(absolute_path)

    assert (yaml['version'] <= config_version)

    convert_bool(yaml)

    return yaml


def load_logger(config):
    handler = logging.StreamHandler()
    formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                   "%(levelname)s - %(message)s"))
    handler.setFormatter(formatter)

    ydk_logger = logging.getLogger("ydk")
    ydk_logger.addHandler(handler)

    app_logger = logging.getLogger("APP")
    app_logger.addHandler(handler)

    verbose = config["config"]["logging"]["verbose"]

    if verbose:
        ydk_logger.setLevel(logging.INFO)
        app_logger.setLevel(logging.INFO)
    else:
        ydk_logger.setLevel(logging.ERROR)
        app_logger.setLevel(logging.ERROR)
    return app_logger


def load_data(config):

    device = urlparse(config["config"]["host"])

    logger = load_logger(config)

    # create NETCONF session
    provider = NetconfServiceProvider(address=device.hostname,
                                      port=device.port,
                                      username=device.username,
                                      password=device.password,
                                      protocol=device.scheme)

    logger.info(f"Connnect to {device}")

    # create CRUD service
    crud = CRUDService()

    # create system time object
    system_time = xr_shellutil_oper.SystemTime()
    sr_config_mapping = sr_config.Sr()

    # read system time from device
    system_time = crud.read(provider, system_time)
    logger.info(crud.read(provider, sr_config_mapping))

    # Print system time
    logger.info("System uptime is " +
          str(timedelta(seconds=system_time.uptime.uptime)))

    titles = []
    for item in sr_config_mapping.traffic_engineering.policies:
        titles.append(item.policy_name)

    return titles


if __name__ == "__main__":
    load_data(load_config())
