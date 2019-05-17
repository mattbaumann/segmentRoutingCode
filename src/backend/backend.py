#!/usr/bin/env python3

import logging
import os
from argparse import ArgumentParser
from datetime import timedelta
from pathlib import Path
from typing import List
from urllib.parse import urlparse

import requests
from ruamel.yaml import YAML
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_segment_routing_ms_cfg as sr_config
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_shellutil_oper as xr_shellutil_oper
from ydk.providers import NetconfServiceProvider
from ydk.services import CRUDService

from src.backend.model.candidatePath import CandidatePath
from src.backend.model.label import Label
from src.backend.model.policy import Policy
from src.backend.model.segmentList import SegmentList

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
    absolute_path = Path(script_path, "./Test.yaml")

    assert (absolute_path.exists() and absolute_path.is_file())

    yaml_parser = YAML(typ='safe')
    yaml = yaml_parser.load(absolute_path)

    args_parser = ArgumentParser()
    args_parser.add_argument("-c", type=str, action="append")

    args = args_parser.parse_args()

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


def read_segment_list(sr: sr_config.Sr, segment_name: str):
    segments: List[Label] = []
    for segment in sr.traffic_engineering.segments.segment:
        if segment_name == segment.path_name:
            for segmentItem in segment.segments.segment:
                segments.append(Label(segmentItem.mpls_label, segmentItem.segment_type))
    return segments


def load_data(config):
    device = urlparse(config["config"]["host"])

    logger = load_logger(config)

    # create NETCONF session
    provider = NetconfServiceProvider(address=device.hostname,
                                      port=device.port,
                                      username=device.username,
                                      password=device.password,
                                      protocol=device.scheme)

    logger.info(f"Connect to {device}")

    # create CRUD service
    crud = CRUDService()

    # create system time object
    system_time = xr_shellutil_oper.SystemTime()
    sr_config_mapping = sr_config.Sr()

    # read system time from device
    system_time = crud.read(provider, system_time)
    sr_config_mapping = crud.read(provider, sr_config_mapping)

    # Print system time
    logger.info("System uptime is " +
                str(timedelta(seconds=system_time.uptime.uptime)))

    policies: List[Policy] = []
    for policy in sr_config_mapping.traffic_engineering.policies.policy:
        paths: List[CandidatePath] = []
        for preference in policy.candidate_paths.preferences.preference:
            segments: List[SegmentList] = []
            for pathinfo in preference.path_infos.path_info:
                segments.append(SegmentList(preference.path_index.__str__(),
                                            read_segment_list(sr_config_mapping, pathinfo.segment_list_name)))
            paths.append(CandidatePath(preference.path_index, segments))
        policies.append(Policy(policy.policy_name, policy.policy_color_endpoint.color, paths))

    if len(policies) > 0:
        print(policies[0].__str__())

    requests.post("localhost:8080/policies", data=policies)


if __name__ == "__main__":
    load_data(load_config())
