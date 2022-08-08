from docker import APIClient, errors
from rich import print



def upload_environment(environment_name: str) -> None:
    """Upload a custom environment to the cloud."""
    try:
        client = APIClient(base_url="unix://var/run/docker.sock")
        exported_container = client.export(container=environment_name)
        with open(environment_name + ".tar", "wb") as f:
            for chunk in exported_container:
                f.write(chunk)
    except errors.NotFound:
        print("Environment not found.")
    except errors.DockerException:
        print(":cross_mark_button: Docker not installed or running. ")
    except Exception as e:
        print(f"Unknown exception: {e}")
