import click

from freshenv import provision, view, start


@click.group()
@click.version_option()
def cli() -> None:
    """
    A cli to provision and manag local developer environments.
    """


cli.add_command(provision.provision)
cli.add_command(view.view)
cli.add_command(start.start)
