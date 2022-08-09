import click
from freshenv.cloud.config import view_config
from freshenv.cloud.fetch import fetch_environment
from freshenv.cloud.ls import list_environments
from freshenv.cloud.push import push_environment


@click.group(name="cloud")
def cloud() -> None:
    """Save and share your custom environments on the cloud."""


@cloud.command("ls")
@click.argument("plan", default="personal", type=click.Choice(["freshenv", "personal"]), metavar="plan")
def ls(plan: str) -> None:
    """List cloud environments."""
    list_environments(plan)

@cloud.command("push")
@click.argument("environment_name")
@click.argument("plan", default="personal",type=click.Choice(["freshenv", "personal"]),  metavar="plan")
def push(environment_name: str, plan: str) -> None:
    """Upload an environment to the cloud."""
    push_environment(environment_name, plan)

@cloud.command("fetch")
@click.argument("environment_name")
@click.argument("plan", default="personal",type=click.Choice(["freshenv", "personal"]),  metavar="plan")
def fetch(environment_name: str, plan: str) -> None:
    """Download an environment from the cloud."""
    fetch_environment(environment_name, plan)

@cloud.command("config")
@click.argument("plan", default="personal", type=click.Choice(["freshenv", "personal"]),  metavar="plan")
def config(plan: str) -> None:
    """View personal and freshenv cloud configurations."""
    view_config("cloud."+plan)
