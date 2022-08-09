from configparser import ConfigParser
from os import path
from typing import Dict
from rich import pretty, print
from freshenv.build import config_exists, create_file, key_exists, get_key_values_from_config

homedir = path.expanduser("~")
freshenv_config_location = homedir + "/.freshenv/freshenv"


def check_run(config_type: str) -> bool:
    """Check if cloud configuration is valid."""
    if not config_exists():
        print(f":card_index: No config file found. Creating an empty config at {freshenv_config_location}.")
        create_file(freshenv_config_location)
        return False
    if not key_exists(config_type):
        print(f":exclamation_mark: A [bold]{config_type}[/bold] cloud has not been configured.")
        return False
    if not mandatory_keys_exists(config_type):
        print(f":exclamation_mark: missing mandatory keys in {config_type} configuration for cloud.")
        return False
    return True


def mandatory_keys_exists(config_type: str) -> bool:
    config = ConfigParser()
    config.read(freshenv_config_location)
    if "personal" in config_type:
        if "provider" not in config[config_type]:
            return False
        if "aws_profile" not in config[config_type]:
            return False
        if "bucket" not in config[config_type]:
            return False
    elif "freshenv" in config_type:
        if "apikey" not in config[config_type]:
            return False
    else:
        return False
    return True


def get_config(config_type: str) -> Dict[str, str]:
    if not check_run(config_type):
        return {}
    cloud_config = dict(get_key_values_from_config(config_type))
    return cloud_config


def view_config(config_type: str) -> None:
    """View personal and freshenv cloud configurations."""
    cloud_config = get_config(config_type)
    if not cloud_config:
        return
    pretty.pprint(cloud_config)
