from typing import Dict, List
import click
from docker import APIClient
from rich import print

client = APIClient(base_url="unix://var/run/docker.sock")


def count_environents() -> int:
    return len(get_list_environments())


def get_list_environments() -> List[Dict]:
    environment_list = []
    try:
        environment_list = client.containers(all=True,filters={"label": "maintainer=Raiyan Yahya <raiyanyahyadeveloper@gmail.com>"})
    except Exception as error:
        print("Unknown exception: {}".format(error))
    return environment_list


@click.command("view")
def view() -> None:
    """View local freshenv managed environments."""
    container_list = get_list_environments()
    if not container_list:
        print(":computer: No freshenv environments found.")
    for container in container_list:
        if "Exited" in container.get("Status"):  # type: ignore
            img = ":arrow_down_small: "
        else:
            img = ":arrow_up_small: "
        print(
            img,
            "Name: [bold blue]" + container.get("Names")[0] + "[/bold blue]",  # type: ignore
            "| Flavour: [bold blue]" + container.get("Image").split("/")[-1] + "[/bold blue]",  # type: ignore
            "| State: [bold blue]" + container.get("Status") + "[/bold blue]",  # type: ignore
        )
