import click

from freshenv import provision


@click.group()
@click.version_option()
def cli() -> None:
    """
    A cli to provision and manag local developer environments.
    """


cli.add_command(provision.provision)
