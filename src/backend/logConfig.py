import logging
import os
from pathlib import Path


def load_logger(config):
    script_path = Path(os.path.dirname(os.path.abspath(__file__)))
    absolute_path = Path(script_path, config["config"]["logging"]["filename"])
    handler = logging.FileHandler(filename=absolute_path)

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
