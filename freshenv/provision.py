from typing import Dict, List
import click
from docker import APIClient, errors
import dockerpty
from freshenv.util import PythonLiteralOption
from freshenv.view import count_environents
from rich import print
from requests import exceptions
from freshenv.console import console
from os import getcwd, path

client: APIClient = None
dir = getcwd()
folder = path.basename(dir)
local_mount_binds = [f"{dir}:/home/devuser/{folder}:delegated"]
google_dns = ["8.8.8.8"]

def get_port_bindings(ports: List[str]) -> Dict:
    port_bindings = {}
    for port in ports:
        port_bindings[port] = port
    return port_bindings


def create_environment(flavour: str, command: str, ports: List[str], name: str, client: APIClient, tty: bool=True, stdin_open: bool=True) -> Dict:
    if name == "index":
        name = str(count_environents() + 1)
    container = client.create_container(
        name=f"freshenv_{name}",
        image=f"ghcr.io/raiyanyahya/{flavour}/{flavour}",
        stdin_open=stdin_open,
        tty=tty,
        command=command,
        volumes=["/home/devuser"],
        ports=ports,
        use_config_proxy=False,
        host_config=client.create_host_config(port_bindings=get_port_bindings(ports),userns_mode="host",privileged=True,dns=google_dns,binds=local_mount_binds))
    return container


def pull_and_try_again(flavour: str, command: str, ports: List[str], name: str, client: APIClient):
    try:
        with console.status("Flavour doesnt exist locally. Fetching flavour...", spinner="arrow2"):
            client.pull(f"ghcr.io/raiyanyahya/{flavour}/{flavour}")
        container = create_environment(flavour, command, ports, name, client)
        dockerpty.start(client, container)
    except (errors.ImageNotFound, exceptions.HTTPError):
        print(":x: flavour doesnt exist")


@click.command("provision")
@click.option("--flavour","-f",default="base", help="The flavour of the environment.",show_default=True)
@click.option("--command","-c",default="zsh", help="The command to execute at startup of environment.",show_default=True)
@click.option("--ports","-p", default='["3000","4000"]', cls=PythonLiteralOption, help="String list of ports to forward.", show_default=True)
@click.option("--name","-n", default="index", help="Name of your environment.", show_default=False)
def provision(flavour: str, command: str, ports: List[str], name: str) -> None:
    """Provision a developer environment."""
    try:
        client = APIClient(base_url="unix://var/run/docker.sock")
        container = create_environment(flavour, command, ports, name, client)
        dockerpty.start(client, container)
    except (exceptions.HTTPError, errors.NotFound):
        pull_and_try_again(flavour, command, ports, name,client)
    except errors.DockerException:
        print(":cross_mark_button: Docker not installed or running. ")
    except Exception as e:
        print("Unknown exception: {}".format(e))
