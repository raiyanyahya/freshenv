import click
from docker import APIClient
import dockerpty
from rich import print

client = APIClient(base_url="unix://var/run/docker.sock")


@click.command("start")
@click.option("--name", "-n",required=True,help="Name of your environment to resume.")
def start(name: str) -> None:
    """Resume working in an environment."""
    containers = client.containers(all=True, filters={"name": name})
    if containers:
        dockerpty.start(client, containers[0])
    else:
        print(f":ghost: No freshenv environment called [bold]{name}[/bold] found.")
