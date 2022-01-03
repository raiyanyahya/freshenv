import click
from docker import APIClient, errors
from rich import print
from freshenv.provision import create_environment
import dockerpty
from requests import exceptions
import os
from sys import exit
freshenv_test_image = "ghcr.io/raiyanyahya/freshenv-busybox/freshenv-busybox"

def check_docker():
    try:
        client = APIClient(base_url="unix://var/run/docker.sock")
        print(":heavy_check_mark: Docker installed and running.")
        return client
    except Exception:
        print(":cross_mark_button: Docker not installed or running. ")
        exit(1)


def remove_old_tests(client: APIClient):
    try:
        client.remove_container(container="freshenv_system_test",force=True)
        client.remove_image(image=freshenv_test_image, force=True)
        print(":heavy_check_mark: Test images removed.")
    except errors.APIError as e:
        if e.status_code == 404:
             print(":heavy_check_mark: No test images found. Moving on...")
    except Exception:
        print(":cross_mark_button: Could not remove freshenv test image. A freshenv test environment maybe still running.")
        exit(1)

def run_test_environment(client: APIClient):
    try:
        container = create_environment(flavour="freshenv-busybox", command="ls", ports=["3000","4000"],name="system_test", client=client)
        dockerpty.start(client, container, stdout=open(os.devnull, "w"))
        print(":heavy_check_mark: Succesfully provisioned test environment.")
    except (exceptions.HTTPError, errors.NotFound):
        client.pull(freshenv_test_image)
        container = create_environment(flavour="freshenv-busybox", command="ls", ports=["3000","4000"], name="system_test", client=client)
        dockerpty.start(client, container,open(os.devnull, "w"))
        print(":heavy_check_mark: Succesfully provisioned test environment.")
    except Exception:
        print(":cross_mark_button: Could not provision test environment.")
        exit(1)

@click.command("check")
def check() -> None:
    """Check system compatibility for running freshenv."""
    client = check_docker()
    remove_old_tests(client)
    run_test_environment(client)
    remove_old_tests(client)
    print(":sunrise: All test passed. Everything looks good.")
    