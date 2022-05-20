from io import BytesIO
from os import makedirs, path
from configparser import ConfigParser, SectionProxy
from rich import print
from jinja2 import Environment, FileSystemLoader
import click
from docker import APIClient
from freshenv.console import console



homedir = path.expanduser("~")
freshenv_config_location = homedir + "/.freshenv/freshenv"


def create_dockerfile(base: str, install: str, cmd: str) -> str:
    env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
    template = env.get_template('simple')
    build_template = template.render(base=base, install=install, cmd=cmd)
    return build_template


def config_exists() -> bool:
    if not path.isfile(freshenv_config_location):
        return False
    return True


def get_key_values_from_config(flavour: str) -> SectionProxy:
    config = ConfigParser()
    config.read(freshenv_config_location)
    return config[flavour]


def env_exists(flavour: str) -> bool:
    config = ConfigParser()
    config.read(freshenv_config_location)
    if flavour not in config.sections():
        return False
    return True


def mandatory_keys_exists(flavour: str) -> bool:
    config = ConfigParser()
    config.read(freshenv_config_location)
    if "BASE" not in config[flavour]:
        return False
    if "INSTALL" not in config[flavour]:
        return False
    if "CMD" not in config[flavour]:
        return False
    return True


def create_file(location: str) -> None:
    makedirs(path.dirname(location), exist_ok=True)
    open(location, "w", encoding="utf8").close()


def run_checks(flavour: str) -> bool:
    if not config_exists():
        print(f":card_index: No config file found. Creating an empty config at {freshenv_config_location}.")
        create_file(freshenv_config_location)
        return False
    if not env_exists(flavour):
        print(f":exclamation_mark:configuration for custom flavour {flavour} does not exist.")
        return False
    if not mandatory_keys_exists(flavour):
        print(":exclamation_mark: missing mandatory keys in configuration for custom environment {flavour}.")
        return False
    return True

@click.command("build")
@click.argument("flavour")
@click.option('--logs', '-l', is_flag=True, help="Show build logs")
def build(flavour: str, logs: bool) -> None:
    """Build a custom freshenv flavour."""
    if not run_checks(flavour):
        return

    flavour_config = get_key_values_from_config(flavour)
    flavour_dockerfile = create_dockerfile(flavour_config["base"], flavour_config["install"], flavour_config["cmd"])
    client = APIClient(base_url="unix://var/run/docker.sock")
    with console.status("Building custom flavour...", spinner="point"):
        for line in client.build(fileobj=BytesIO(flavour_dockerfile.encode('utf-8')), tag=f"raiyanyahya/{flavour}/{flavour}", rm=True, pull=True, decode=True):
            if logs:
                print(line)
    print(f":party_popper: Successfully built custom flavour {flavour}. You can provision it by running [bold]freshenv -provision -f {flavour}[/bold].")