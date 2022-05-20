import click
from rich import pretty, print
from urllib.request import urlopen
from json import loads
from sys import exit


@click.command("flavours")
def flavours() -> None:
    """Show all available flavours for provisioning."""
    gist_reponse = urlopen("https://api.github.com/gists/c4709c540a7c29616c771ab642ed2b8b")
    if gist_reponse.getcode() == 200:
        gist_data = loads(gist_reponse.read().decode("utf-8"))
        flavour_dict = loads(gist_data["files"]["fr-flavours.json"]["content"])
        print(f":mag: Found {len(flavour_dict['fr-flavours'])} flavours:")
        pretty.pprint(flavour_dict["fr-flavours"])
    else:
        print(":heavy_exclamation_mark: Could not fetch flavours.")
        exit(1)