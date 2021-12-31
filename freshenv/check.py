import click
from docker import APIClient
from rich import print




@click.command("check")
def check() -> None:
    """Check system compatibility for running freshenv."""
    check_docker()

def check_docker():
    try:
        APIClient(base_url="unix://var/run/docker.sock")
        print(":white_heavy_check_mark: Docker installed and running. ")
    except Exception:
        print(":cross_mark_button: Docker not installed or running. ")
    