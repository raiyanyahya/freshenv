import click
from freshenv import provision, view, start, remove, check


@click.group()
@click.version_option()
def cli() -> None:
    """A cli to provision and manage local developer environments."""


cli.add_command(provision.provision)
cli.add_command(view.view)
cli.add_command(start.start)
cli.add_command(remove.remove)
cli.add_command(check.check)