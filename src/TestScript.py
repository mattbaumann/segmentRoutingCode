# import providers, services and models
import logging
import os
from argparse import ArgumentParser
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlparse

from ruamel.yaml import YAML
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_shellutil_oper as xr_shellutil_oper
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


def load_config():
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", help="sets the relative path to default config",
                        default="./Test.yaml")
    # Parse parameters
    args = parser.parse_args()

    assert ("config" in args)

    # Parse config
    script_path = Path(os.path.dirname(os.path.abspath(__file__)))
    absolute_path = Path(script_path, args.config)

    assert (absolute_path.exists() and absolute_path.is_file())

    yamlParser = YAML(typ='safe')
    yaml = yamlParser.load(absolute_path)

    assert (yaml['version'] <= config_version)

    return yaml


def load_logger():
    handler = logging.StreamHandler()
    formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                   "%(levelname)s - %(message)s"))
    handler.setFormatter(formatter)

    ydk_logger = logging.getLogger("ydk")
    ydk_logger.addHandler(handler)

    app_logger = logging.getLogger("APP")
    app_logger.addHandler(handler)

    verbose = parse_bool(config["config"]["logging"]["verbose"])

    if verbose:
        ydk_logger.setLevel(logging.INFO)
        app_logger.setLevel(logging.INFO)
    else:
        ydk_logger.setLevel(logging.ERROR)
        app_logger.setLevel(logging.ERROR)
    return app_logger


if __name__ == "__main__":
    config = load_config()

    device = urlparse(config["config"]["host"])

    logger = load_logger()

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
    # read system time from device
    system_time = crud.read(provider, system_time)

    # Print system time
    print("System uptime is " +
          str(timedelta(seconds=system_time.uptime.uptime)))
