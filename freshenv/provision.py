from typing import Dict, List
import click
from docker import APIClient, errors
import dockerpty
from freshenv.view import count_environents
from rich import print
from requests import exceptions
from freshenv.console import console
from os import getcwd, path

client = APIClient(base_url="unix://var/run/docker.sock")
dir = getcwd()
folder = path.basename(dir)

def create_environment(flavour: str, command: str, ports: List[int], name: str) -> Dict:
    if name == "index":
        name = str(count_environents() + 1)
    
    container = client.create_container(
        name=f"freshenv_{name}",
        image=f"ghcr.io/raiyanyahya/{flavour}/{flavour}",
        stdin_open=True,
        tty=True,
        command=command,
        ports=ports,
        volumes=["/home/devuser"],
        host_config=client.create_host_config(binds=[
        f"{dir}:/home/devuser/{folder}:delegated",
        "/home/$USER/.gitconfig:/root/.gitconfig:ro",
        "/home/$USER/.ssh:/root/.ssh:ro",
        "/var/run/docker.sock:/var/run/docker.sock"
    ])
    )
    return container


def pull_and_try_again(flavour, command, ports, name):
    try:
        with console.status("Flavour doesnt exist locally. Fetching flavour...", spinner="arrow2"):
            client.pull(f"ghcr.io/raiyanyahya/{flavour}/{flavour}")
        container = create_environment(flavour, command, ports, name)
        dockerpty.start(client, container)
    except (errors.ImageNotFound, exceptions.HTTPError):
        print(":x: flavour doesnt exist")


@click.command("provision")
@click.option("--flavour","-f",default="devenv",help="The flavour of the environment.",show_default=True)
@click.option("--command","-c",default="zsh",help="The command to execute at startup of environment.",show_default=True)
@click.option("--ports","-p", default=[3000], help="List of ports to forward.", show_default=True)
@click.option("--name","-n", default="index", help="Name of your environment.", show_default=False)
def provision(flavour: str, command: str, ports: List[int], name: str) -> None:
    """Provision a developer environment."""
    try:
        container = create_environment(flavour, command, ports, name)
        dockerpty.start(client, container)
    except (exceptions.HTTPError, errors.NotFound):
        pull_and_try_again(flavour, command, ports, name)
    except Exception as e:
        print("Unknown exception: {}".format(e))
