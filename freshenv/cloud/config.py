from configparser import ConfigParser
from os import path
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
        print(f":exclamation_mark: cloud configuration does not exist.")
        return False
    if not mandatory_keys_exists(config_type):
        print(":exclamation_mark: missing mandatory keys in configuration for cloud.")
        return False
    return True
def mandatory_keys_exists(flavour: str) -> bool:
    config = ConfigParser()
    config.read(freshenv_config_location)
    if "base" not in config[flavour]:
        return False
    if "install" not in config[flavour]:
        return False
    if "cmd" not in config[flavour]:
        return False
    return True

def view_config(config_type: str) -> None:
    """View personal and freshenv cloud configurations."""
    if not check_run(config_type):
        return
    cloud_config = get_key_values_from_config(config_type)
    pretty.pprint(cloud_config)