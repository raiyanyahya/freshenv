import click
from docker import APIClient, errors
from rich import print

client = APIClient(base_url="unix://var/run/docker.sock")


@click.command("remove")
@click.option(
    "--name",
    required=True,
    help="Name of your environment to remove.",
)
def remove(name: str) -> None:
    """Remove a freshenv environment."""
    try:
        client.remove_container(container=name)
    except errors.NotFound:
        print(
            f":ghost: No freshenv environment called [underline  bold]{name}[/underline bold] found."
        )
    except Exception as e:
        print("Unknown exception: {}".format(e))
