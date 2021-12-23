from typing import Dict, List, ValuesView
import click
from docker import APIClient
from freshenv.console import console
from rich.table import Table
from rich import box

client = APIClient(base_url="unix://var/run/docker.sock")


def count_environents() -> int:
    return len(get_list_environments())


def get_list_environments() -> List[Dict]:
    environment_list = []
    try:
        environment_list = client.containers(
            all=True,
            filters={
                "label": "maintainer=Raiyan Yahya <raiyanyahyadeveloper@gmail.com>"
            },
        )
    except Exception as error:
        print("Unknown exception: {}".format(error))
    return environment_list


@click.command("view")
def view() -> None:
    """View local freshenv managed environments."""
    container_list = get_list_environments()
    table = Table(title="LOCAL FRESHENV ENVIRONMENTS", leading=1, box=box.ROUNDED)
    table.add_column("FLAVOUR", justify="center", style="blue")
    table.add_column("NAME", justify="center", style="magenta")
    table.add_column("STATUS", justify="center", style="cyan")
    table.add_column("STATE", justify="center", style="green")
    for container in container_list:
        table.add_row(
            container.get("Image").split("/")[-1],
            container.get("Names")[0],
            container.get("Status"),
            container.get("State"),
        )
    console.print(table)
