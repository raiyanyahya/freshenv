from docker import APIClient, errors
from rich import print
import boto3
from os import remove
from botocore import exceptions
from freshenv.cloud.config import get_config


def export_environment(environment_name: str) -> str:
    try:
        client = APIClient(base_url="unix://var/run/docker.sock")
        exported_container = client.export(container=environment_name)
        with open(environment_name + ".tar", "wb") as f:
            for chunk in exported_container:
                f.write(chunk)
        return f.name
    except errors.NotFound:
        print(" :man_shrugging: Environment not found. Please check if the environment exists.")
    except errors.APIError:
        print(":cold_sweat: Could not export environment. Please contact the developer or report an issue. :ticket:")
    except errors.DockerException:
        print(":cross_mark_button: Docker not installed or running. ")
    except Exception as e:
        print(f"Unknown exception: {e}")
    return ""


def remove_tar_file(file_name: str) -> None:
    remove(file_name)


def push_environment_to_aws(environment_name: str, config_obj: dict) -> None:
    try:
        session = boto3.session.Session(profile_name=config_obj["aws_profile"])
        s3_client = session.client('s3')
        s3_client.head_bucket(Bucket=config_obj["bucket"])
        print(":link: Uploading environment to the cloud.")
        file_name = export_environment(environment_name)
        if file_name == "":
            return
        s3_client.upload_file(file_name, config_obj["bucket"], file_name)
        print(":white_check_mark: Environment uploaded successfully.")
        remove_tar_file(file_name)
    except exceptions.ClientError as client_error:
        if client_error.response['Error']['Code'] == 'NoSuchBucket':
            print(":person_shrugging: Bucket does not exist.")
    except exceptions.ProfileNotFound:
        print(":person_shrugging: config profile does not exist.")


def push_environment(environment_name: str, plan: str) -> None:
    """Upload a custom environment to the cloud."""
    if plan == "personal":
        config_obj = get_config(f"cloud.{plan}")
        if not config_obj:
            return
        if config_obj and config_obj["provider"]:
            provider = config_obj["provider"]
            if provider == "aws":
                push_environment_to_aws(environment_name, config_obj)
            else:
                print(
                    f":building_construction:  {provider} provider not supported.")
        else:
            print(":person_facepalming: No provider configured.")
    else:
        print(":white_sun_with_small_cloud:  The freshenv cloud plan is coming soon. Please visit the website for more information.")
