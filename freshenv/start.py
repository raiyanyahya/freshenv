from typing import Dict, List
import click
from docker import APIClient
import dockerpty

client = APIClient(base_url='unix://var/run/docker.sock')


@click.command('start')
def start() -> None:
    '''
    view local freshenv managed environments.
    '''
    container = client.containers(all=True,filters={"name": "freshenv_3"})[0]
    dockerpty.start(client, container)
    