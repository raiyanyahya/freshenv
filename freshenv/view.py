from typing import Dict, List
import click
from docker import APIClient


client = APIClient(base_url='unix://var/run/docker.sock')


def count_environents() -> int:
    return len(get_list_environments())   

def get_list_environments() -> List[Dict]:
    try:
        environment_list = client.containers(all=True,filters={"label": "maintainer=Raiyan Yahya <raiyanyahyadeveloper@gmail.com>"})
    except Exception as error:
        print('Unknown exception: {}'.format(error))
    return environment_list


@click.command('view')
def view() -> None:
    '''
    view local freshenv managed environments.
    '''
    container_list = get_list_environments()
    view_list = []
    for container in container_list:
        environment = {}
        environment['Environment Name'] = container.get("Names")[0]
        environment['State'] = container.get("State")
        view_list.append(environment)
    print(view_list)