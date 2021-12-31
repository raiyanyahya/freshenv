import click
from docker import APIClient
import dockerpty
from rich import print




@click.command("start")
@click.option("--name", "-n",required=True,help="Name of your environment to resume.")
def start(name: str) -> None:
    """Resume working in an environment."""
    client = APIClient(base_url="unix://var/run/docker.sock")
    containers = client.containers(all=True, filters={"name": name})
    if containers:
        dockerpty.start(client, containers[0])
    else:
        print(f":ghost: No freshenv environment called [bold]{name}[/bold] found.")
