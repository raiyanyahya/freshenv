from typing import Dict, List
import click
from docker import APIClient, errors
import dockerpty
from freshenv.util import PythonLiteralOption
from freshenv.view import count_environents
from rich import print
from requests import exceptions
from freshenv.console import console
from os import getcwd, path, environ

client: APIClient = None
dir = getcwd()
folder = path.basename(dir)
local_mount_binds = [
        f"{dir}:/home/devuser/{folder}:delegated",
        "/home/$USER/.gitconfig:/root/.gitconfig:ro",
        "/home/$USER/.ssh:/root/.ssh:ro",
        "/var/run/docker.sock:/var/run/docker.sock"
    ]
test_mount_binds = [
        f"{dir}:/home/devuser/{folder}:delegated",
        "/var/run/docker.sock:/var/run/docker.sock"
    ]
google_dns = ["8.8.8.8"]
def create_environment(flavour: str, command: str, ports: List[str], name: str, client: APIClient, tty: bool=True, stdin_open: bool=True) -> Dict:
    if name == "index":
        name = str(count_environents() + 1)
    container = client.create_container(
        name=f"freshenv_{name}",
        image=f"ghcr.io/raiyanyahya/{flavour}/{flavour}",
        stdin_open=stdin_open,
        tty=tty,
        command=command,
        ports=ports,
        volumes=["/home/devuser"],
        host_config=client.create_host_config(dns=google_dns,binds=test_mount_binds if environ.get('GITHUB_ACTIONS') else local_mount_binds))
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
@click.option("--flavour","-f",default="devenv", help="The flavour of the environment.",show_default=True)
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
