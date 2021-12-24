import click
from docker import APIClient, errors
from rich import print

client = APIClient(base_url="unix://var/run/docker.sock")


@click.command("remove")
@click.option("--name","-n",required=True,help="Name of your environment to remove.")
@click.option('--force', '-f', is_flag=True, help="Force remove an environment.")
def remove(name: str, force: bool) -> None:
    """Remove a freshenv environment."""
    try:
        client.remove_container(container=name, force=force)
        print(f":boom: {name} environment removed.")
    except errors.NotFound:
        print(f":ghost: No freshenv environment called [bold]{name}[/bold] found.")
    except errors.APIError as e:
        if e.status_code == 409:
            print(f":runner: {name} is a [bold green]running[/bold green] environment. Close the session first or use the [bold blue]--force[/bold blue] flag.")
        else:
            raise Exception(e)
    except Exception as e:
        print("Unknown exception: {}".format(e))
