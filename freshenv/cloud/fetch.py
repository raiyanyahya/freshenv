
from docker import APIClient, errors
from botocore import exceptions
import boto3
from os import remove
from freshenv.cloud.config import get_config
from freshenv.start import start


def fetch_environment_from_aws(environment_name: str, config_obj: dict) -> None:
    try:
        session = boto3.session.Session(profile_name=config_obj["aws_profile"])
        s3_client = session.client('s3')
        s3_client.head_bucket(Bucket=config_obj["bucket"])
        print(":link: Downloading environment from the cloud.")
        s3_client.download_file(config_obj["bucket"], environment_name + ".tar", environment_name + ".tar")
        print(":white_check_mark: Environment downloaded successfully.")
    except exceptions.ClientError as client_error:
        if client_error.response['Error']['Code'] == 'NoSuchBucket':
            print(":person_shrugging: Bucket does not exist.")
    except exceptions.ProfileNotFound:
        print(":person_shrugging: config profile does not exist.")
    except Exception as e:
        print(f"Unknown exception: {e}")


def import_container(environment_name: str) -> None:
    try:
        client = APIClient(base_url="unix://var/run/docker.sock")
        client.import_image(environment_name + ".tar", environment_name)
        print(":white_check_mark: Environment imported successfully.")
        remove(environment_name + ".tar")
    except errors.APIError:
        print(":cold_sweat: Could not import environment. Please contact the developer or report an issue. :ticket:")
    except errors.DockerException:
        print(":cross_mark_button: Docker not installed or running. ")
    except Exception as e:
        print(f"Unknown exception: {e}")

def fetch_environment(environment_name: str, plan: str) -> None:
    """Fetch a custom environment from the cloud."""
    if plan == "personal":
        config_obj = get_config(f"cloud.{plan}")
        if not config_obj:
            return
        if config_obj and config_obj["provider"]:
            provider = config_obj["provider"]
            if provider == "aws":
                fetch_environment_from_aws(environment_name, config_obj)
                import_container(environment_name)
                start(environment_name)
            else:
                print(f":building_construction:  {provider} provider not supported.")
        else:
            print(":person_facepalming: No provider configured.")
    else:
        print(":white_sun_with_small_cloud:  The freshenv cloud plan is coming soon. Please visit the website for more information.")
