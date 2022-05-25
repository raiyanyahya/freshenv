import click
from docker import APIClient, errors
from rich import print




@click.command("clean")
@click.option('--force', '-f', is_flag=True, help="Force remove freshenv flavours and environments.")
def clean(force: bool) -> None:
    """Remove all freshenv flavours and environments."""
    try:
        client = APIClient(base_url="unix://var/run/docker.sock")
        freshenv_containers = client.containers(all=True, filters={"name": "freshenv_*"})
        for container in freshenv_containers:
            client.remove_container(container=container['Id'], force=force)
        images_list = client.images(filters={"label": "maintainer=Raiyan Yahya <raiyanyahyadeveloper@gmail.com>"})
        for image in images_list:
            client.remove_image(image=image['Id'], force=force)
        custom_images = client.images(filters={"label": "maintainer=Custom Environment"})
        for custom_image in custom_images:
            client.remove_image(image=custom_image['Id'], force=force)
        print(":boom: freshenv flavours and environments removed.")
    except errors.APIError as e:
        if e.status_code == 409:
            print(":runner: Found a [bold green]running[/bold green] environment or a referenced flavour. Close the session first or use the [bold blue]--force[/bold blue] flag.")
        else:
            raise Exception(e)
    except errors.DockerException:
        print(":cross_mark_button: Docker not installed or running. ")
    except Exception as e:
        print(f"Unknown exception: {e}")
