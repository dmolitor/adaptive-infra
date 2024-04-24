import boto3
from fabric.connection import Connection
import os
from pathlib import Path
import random
import sys
import time
import traceback

args = sys.argv[1:]
if not args:
    raise ValueError("No command line arguments detected; three expected")
BUFFER = 20
INSTANCE_TYPE = args[0]
POSTGRES_VOLUME = args[1]
SWARM_N = int(args[2])

base_dir = Path(__file__).resolve().parent.parent
# For interactive use run the line below
# base_dir = Path().resolve()

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

def get_instance_public_ip(instance_id: str, client) -> str:
    response = client.describe_instances(InstanceIds=[instance_id])
    check_http_status(response)
    instance = response.get("Reservations")[0].get("Instances")
    return instance[0]["PublicIpAddress"]

def server_exists(client, name: str = "AdaptiveServer") -> bool:
    response = client.describe_instances(
        Filters=[
            {
                "Name": "tag:Name",
                "Values": [name]
            }
        ]
    )
    check_http_status(response)
    reservations = response.get("Reservations")
    statuses = []
    for reservation in reservations:
        for instance in reservation["Instances"]:
            statuses.append(instance["State"]["Name"])
    if "pending" in statuses or "running" in statuses:
        return True
    else:
        return False

def launch_image(client, verbose: bool = True) -> bool:
    # Prepping configuration
    if verbose:
        print("Preparing instance configuration ...")
    adaptive_key = get_key(client)
    adaptive_ami = get_ami_id("aws-docker-adaptive", client)
    adaptive_volume = get_volume_id("AdaptiveVolume", client)
    adaptive_security_group = get_group_id("AdaptiveExperiment", client)
    instance_params = {
        "ImageId": adaptive_ami,
        "InstanceType": INSTANCE_TYPE,
        "KeyName": adaptive_key,
        "MinCount": 1,
        "MaxCount": 1,
        "Monitoring": {"Enabled": False},
        "Placement": {"AvailabilityZone": "us-east-1a"},
        "SecurityGroupIds": [adaptive_security_group],
        "TagSpecifications": [
            {
                "ResourceType": "instance",
                "Tags": [
                    {
                        "Key": "Name",
                        "Value": "AdaptiveServer",
                    },
                ],
            },
        ]
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
    # Mount volume
    mount_response = client.attach_volume(
        Device="/dev/sdd",
        InstanceId=instance_id,
        VolumeId=adaptive_volume
    )
    check_http_status(mount_response)
    # Wait for volume to be in use
    print("Waiting for volume to be in use ...")
    waiter = client.get_waiter("volume_in_use")
    waiter.wait(
        VolumeIds=[adaptive_volume],
        WaiterConfig={"Delay": 10, "MaxAttempts": 12}
    )
    return instance_id

def mount_volume_to_drive(instance_id: str, volume: str, client) -> None:
    public_ip = get_instance_public_ip(instance_id, client)
    # Initialize SSH connection
    con = Connection(
        host=public_ip,
        user="ubuntu",
        connect_kwargs={
            "key_filename": f"{os.path.expanduser('~/.aws')}/{get_key(ec2)}.pem"
        }
    )
    con.open()
    if not con.is_connected:
        raise ConnectionError(f"Failed to connect to {con.user}@{con.host}")
    # Make sure that device /dev/xvdd exists
    device_exists = (
        con
        .run("[ -b /dev/xvdd ] && echo true || echo false", hide=True)
        .stdout
        .strip() == "true"
    )
    if not device_exists:
        raise FileNotFoundError("Device /dev/xvdd was not found")
    # Check whether the drive has a file system yet
    filesys = (
        con
        .run("sudo file -s /dev/xvdd", hide=True)
        .stdout
        .strip()
        .removeprefix("/dev/xvdd: ")
    )
    if filesys == "data":
        print("Creating a file system on device /dev/xvdd ...")
        con.run("sudo mkfs -t xfs /dev/xvdd")
    # Make a directory where we will mount the drive
    data_dir_exists = (
        con
        .run("[ -d ./data ] && echo true || echo false", hide=True)
        .stdout
        .strip() == "true"
    )
    if not data_dir_exists:
        print(f"Creating mountpoint for device /dev/xvdd at {volume} ...")
        con.run(f"sudo mkdir {volume}")
    # Check if the volume is mounted yet
    volume_is_mtd = (
        con
        .run(
            "sudo lsblk -o MOUNTPOINT /dev/xvdd | grep -v MOUNTPOINT",
            hide=True
        )
        .stdout
        .strip() != ""
    )
    if not volume_is_mtd:
        print(f"Mounting /dev/xvdd at {volume} ...")
        con.run(f"sudo mount /dev/xvdd {volume}")
    # Give the file system correct permissions and ownership
    con.run(f"sudo chmod -R 777 {volume}")
    # Terminate SSH connection
    con.close()

def launch_swarm(instance_id: str, client) -> None:
    public_ip = get_instance_public_ip(instance_id, client)
    # Initialize SSH connection
    con = Connection(
        host=public_ip,
        user="ubuntu",
        connect_kwargs={
            "key_filename": f"{os.path.expanduser('~/.aws')}/{get_key(ec2)}.pem"
        }
    )
    con.open()
    if not con.is_connected:
        raise ConnectionError(f"Failed to connect to {con.user}@{con.host}")
    # Upload swarm launch script to server
    target_dir = con.run("echo $HOME", hide=True).stdout.strip()
    con.put(base_dir / "scripts" / "swarm-launch-aws.sh", target_dir)
    # Execute the script
    con.run("sudo /bin/bash swarm-launch-aws.sh")
    # Scale up the swarm
    con.run(f"sudo docker service scale adaptive_stack_app={SWARM_N}")

if __name__ == "__main__":

    # Create EC2 service
    ec2 = boto3.client("ec2")
    check_http_status(ec2.describe_instances())

    # Check if the server is already running... If so do nothing.
    server_running = server_exists(ec2)

    if not server_running:
        # Launch the server
        instance_id = launch_image(ec2)
        try:
            print("Mounting volume")
            # Mount the volume
            mount_volume_to_drive(instance_id, POSTGRES_VOLUME, ec2)
            print(f"Drive mounted. Buffering for {BUFFER} seconds")
            time.sleep(BUFFER)
            print("Launching swarm")
            # Launch the adaptive app swarm
            launch_swarm(instance_id, ec2)
        except Exception:
            print(traceback.format_exc())
            response = ec2.terminate_instances(
                InstanceIds=[instance_id]
            )
            check_http_status(response)
