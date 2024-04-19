from botocore import client
import boto3
import os
from pathlib import Path
import random
import tempfile

base_dir = Path(__file__).resolve().parent.parent
# For interactive use run the line below
# base_dir = Path().resolve()

# TODO: set EC2 instance specs in the .env file
INSTANCE_TYPE=""

def check_http_status(response: dict) -> None:
    """Simple checker of HTTP status"""
    code = response.get("ResponseMetadata")["HTTPStatusCode"]
    if code >= 400:
        raise ConnectionError(f"Returned HTTP status code {code}")
    return None

def local_key(name: str):
    """Is a key stored locally"""
    local_key_path = os.path.expanduser("~/.aws") + f"/{name}.pem"
    return os.path.isfile(local_key_path)

def existing_keys(client) -> dict:
    """Return a dictionary of all existing keys that are stored locally"""
    key_response = client.describe_key_pairs()
    check_http_status(key_response)
    keys = key_response.get("KeyPairs")
    if not keys:
        return {}
    keys = {k["KeyName"]: k["KeyPairId"] for k in keys}
    local_keys = {}
    for k, v in keys.items():
        if local_key(k):
            local_keys[k] = v
    return local_keys

def create_key(
    client,
    name="AdaptiveKey" + str(random.sample(range(int(1e4)), 1)[0])
) -> str:
    """Create a public/private key pair"""
    response = client.create_key_pair(KeyName=name)
    check_http_status(response)
    private = response.get("KeyMaterial")
    pem_path = os.path.expanduser("~/.aws") + f"/{name}.pem"
    with open(pem_path, "w") as file:
        file.write(private)
    os.chmod(pem_path, 0o400)
    return name

def get_key(client) -> str:
    """Get a private key pair for launching an instance"""
    local_keys = existing_keys(client)
    if not local_keys:
        key_name = create_key(client)
    else:
        key_name = list(local_keys.keys())[0]
    return key_name

def get_ami_id(name: str, client) -> str:
    """Retrieve the ID of an AMI from its name"""
    response = client.describe_images(
        Filters=[
            {"Name": "name", "Values": [name]}
        ]
    )
    check_http_status(response)
    image = response.get("Images")
    if len(image) > 1:
        raise ValueError(f"Only 1 image expected; {len(image)} found")
    return image[0]["ImageId"]

def get_volume_id(name: str, client) -> str:
    """Retrieve the ID of a volume"""
    response = client.describe_volumes(
        Filters=[
            {
                "Name": "tag:Name",
                "Values": [name]
            }
        ]
    )
    check_http_status(response)
    volumes = response.get("Volumes")
    if len(volumes) != 1:
        raise ValueError(f"Exactly 1 volume expected; {len(volumes)} found")
    return volumes[0]["VolumeId"]

def get_group_id(name: str, client) -> str:
    """Retrieve the ID of a security group"""
    response = client.describe_security_groups(
        Filters=[
            {
                "Name": "group-name",
                "Values": [name]
            }
        ]
    )
    check_http_status(response)
    groups = response.get("SecurityGroups")
    if len(groups) != 1:
        raise ValueError(f"Exactly 1 group expected; {len(groups)} found")
    return groups[0]["GroupId"]

def launch_image(client, type: str = "t2.micro", verbose: bool = True) -> bool:
    # Prepping configuration
    if verbose:
        print("Preparing instance configuration ...")
    adaptive_key = get_key(client)
    adaptive_ami = get_ami_id("aws-docker-adaptive", client)
    adaptive_volume = get_volume_id("AdaptiveVolume", client)
    adaptive_security_group = get_group_id("AdaptiveExperiment", client)
    with open(base_dir / "scripts" / "swarm-launch-aws.sh", "r") as file:
        adaptive_userdata = file.read()
    instance_params = {
        "ImageId": adaptive_ami,
        "InstanceType": type,
        "KeyName": adaptive_key,
        "MinCount": 1,
        "MaxCount": 1,
        "Monitoring": {"Enabled": True},
        "SecurityGroupIds": [adaptive_security_group],
        "UserData": adaptive_userdata
    }
    # Launching instance
    if verbose:
        print("Launching instance ...")
    instance_response = client.run_instances(**instance_params)
    check_http_status(instance_response)
    instance_id = instance_response["Instances"][0]["InstanceId"]
    # Waiting for instance to be ready to go
    print("Waiting for instance to be healthy ...")
    waiter = client.get_waiter("instance_status_ok")
    waiter.wait(
        InstanceIds=[instance_id],
        WaiterConfig={"Delay": 10, "MaxAttempts": 48}
    )
    # TODO: mount volume
    # TODO: connect to instance via SSH and launch swarm


# Create EC2 service
ec2 = boto3.client("ec2")
check_http_status(ec2.describe_instances())

# Create new public/private key
key_manager = KeyManager()
key_manager.create_key(client=ec2)