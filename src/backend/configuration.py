import os
from argparse import ArgumentParser
from pathlib import Path

from ruamel.yaml import YAML

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
    args_parser.add_argument("-s", type=str)

    args = args_parser.parse_args()

    assert (yaml['version'] <= config_version)

    convert_bool(yaml)

    return yaml, args.s
