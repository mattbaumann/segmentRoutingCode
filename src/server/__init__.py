
import os
from pathlib import Path
from flask import Flask

from ruamel.yaml import YAML

from src.server.controller import IndexView, LoadConfigView, StoreConfigView

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
    absolute_path = Path(script_path, "../Test.yaml")

    assert (absolute_path.exists() and absolute_path.is_file())

    yaml_parser = YAML(typ='safe')
    yaml = yaml_parser.load(absolute_path)

    assert (yaml['version'] <= config_version)

    convert_bool(yaml)

    return yaml


def create_app(test_config=None):
    """Create and configure Flusk Server Component"""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            # a default secret that should be overridden by instance config
            SECRET_KEY='dev'
        )
        global_config = load_config()
        app.config.update(global_config['config']['flask'])
        config = global_config
    else:
        app.app_config = test_config
        app.config.update(test_config)
        config = test_config

    # Add Components
    app.add_url_rule("/", view_func=IndexView.as_view('index', config))
    app.add_url_rule("/configs", view_func=LoadConfigView.as_view('loadConfig', config))
    app.add_url_rule("/store", view_func=StoreConfigView.as_view('storeConfig', config))

    return app


if __name__ == "__main__":
    create_app().run()
