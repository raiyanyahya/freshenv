import boto3
from botocore import exceptions
from rich import print
from rich.tree import Tree
from freshenv.cloud.config import get_config


def list_environments_from_aws(config_obj: dict) -> None:
    """List your custom cloud environments from AWS."""
    try:
        session = boto3.session.Session(profile_name=config_obj["aws_profile"])
        s3_client = session.client('s3')
        bucket_objs = s3_client.list_objects_v2(Bucket=config_obj["bucket"])
        print(":link: Listing your cloud environments.")
        tree = Tree("Cloud Environments")
        if "Contents" in bucket_objs and len(bucket_objs["Contents"]) > 0:
            for obj in bucket_objs["Contents"]:
                tree.add(obj["Key"])
        else:
            tree.add("No cloud environments found.")
        print(tree)
    except exceptions.ClientError as client_error:
        if client_error.response['Error']['Code'] == 'NoSuchBucket':
            print(":person_shrugging_medium_skin_tone: Bucket does not exist.")
    except exceptions.ProfileNotFound:
        print(":person_shrugging_medium_skin_tone: Profile does not exist.")

def list_environments(plan: str) -> None:
    """List your custom cloud environments."""
    if plan == "personal":
        config_obj = get_config(plan)
        if config_obj and config_obj.get("provider") == 'aws':
            list_environments_from_aws(config_obj)