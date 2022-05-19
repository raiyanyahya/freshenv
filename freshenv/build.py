from io import BytesIO
from os import makedirs, path
from configparser import ConfigParser
from rich import print
from jinja2 import Environment, FileSystemLoader
import click
from docker import APIClient
from freshenv.console import console



homedir = path.expanduser("~")
freshenv_config_location = homedir + "/.freshenv/freshenv"


def create_dockerfile(base: str, install: str) -> str:
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('simple')
    build_template = template.render(base=base, install=install)
    return build_template


def config_exists() -> bool:
    if not path.isfile(freshenv_config_location):
        return False
    return True


def get_key_values_from_config(cenv: str) -> dict:
    config = ConfigParser()
    config.read(freshenv_config_location)
    return config[cenv]


def env_exists(cenv: str) -> bool:
    config = ConfigParser()
    config.read(freshenv_config_location)
    if cenv not in config.sections():
        return False
    return True


def mandatory_keys_exists(cenv: str) -> bool:
    config = ConfigParser()
    config.read(freshenv_config_location)
    if "BASE" not in config[cenv]:
        return False
    if "INSTALL" not in config[cenv]:
        return False
    return True


def create_file(location: str) -> None:
    makedirs(path.dirname(location), exist_ok=True)
    open(location, "w", encoding="utf8").close()


@click.command("build")
@click.argument("cenv")
def build(cenv: str) -> None:
    """Build a custom freshenv environment."""
    if not config_exists():
        print(
            f":card_index: No config file found. Creating an empty config at {freshenv_config_location}.")
        create_file(freshenv_config_location)
        return
    if not env_exists(cenv):
        print(
            f":exclamation_mark: configuration for custom environment {cenv} does not exist.")
        return
    if not mandatory_keys_exists(cenv):
        print(
            ":exclamation_mark: missing mandatory keys in configuration for custom environment {cenv}.")
        return
    cenv_config = get_key_values_from_config(cenv)
    cenv_dockerfile = create_dockerfile(
        cenv_config["BASE"], cenv_config["INSTALL"])
    client = APIClient(base_url="unix://var/run/docker.sock")
    with console.status("Building custom flavour...", spinner="dots8Bit"):
        [line for line in client.build(fileobj=BytesIO(cenv_dockerfile.encode('utf-8')), tag=f"raiyanyahya/{cenv}/{cenv}", rm=True, pull=True, decode=True)]  # pylint: disable=expression-not-assigned
