import click
from freshenv.cloud.config import view_config
from freshenv.cloud.fetch import fetch_environment
from freshenv.cloud.ls import list_environments
from freshenv.cloud.upload import upload_environment


@click.group(name="cloud")
def cloud() -> None:
    """Save and share your custom environments on the cloud."""


@cloud.command("ls")
@click.argument("plan",type=click.Choice(["freshenv", "personal"]))
def ls(plan: str) -> None:
    """List cloud environments."""
    list_environments(plan)

@cloud.command("upload")
@click.argument("environment_name")
def upload(environment_name: str) -> None:
    """Upload an environment to the cloud."""
    upload_environment(environment_name)

@cloud.command("fetch")
@click.argument("environment_name")
def fetch(environment_name: str) -> None:
    """Download an environment from the cloud."""
    fetch_environment(environment_name)

@cloud.command("config")
@click.argument("plan",type=click.Choice(["freshenv", "personal"]))
def config(plan: str) -> None:
    """View personal and freshenv cloud configurations."""
    view_config("cloud."+plan)
