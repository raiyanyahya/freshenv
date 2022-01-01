import click
from docker import APIClient, errors
import dockerpty
from rich import print




@click.command("start")
@click.argument("name")
def start(name: str) -> None:
    """Resume working in an environment."""
    try:
        client = APIClient(base_url="unix://var/run/docker.sock")
        containers = client.containers(all=True, filters={"name": name})
        if containers:
            dockerpty.start(client, containers[0])
        else:
            print(f":ghost: No freshenv environment called [bold]{name}[/bold] found.")
    except errors.DockerException:
        print(":cross_mark_button: Docker not installed or running. ")
    except Exception as e:
        print("Unknown exception: {}".format(e))
