import boto3
from fabric.connection import Connection
import os
from pathlib import Path
import random
import re
import sys
import time
import traceback
from typing import List

args = sys.argv[1:]
if not args:
    raise ValueError("No command line arguments detected; three expected")
BUFFER = 20
INSTANCE_TYPE_MASTER = args[0]
INSTANCE_TYPE_NODE = args[1]
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


def connect_ssh(ip: str) -> Connection:
    con = Connection(
        host=ip,
        user="ubuntu",
        connect_kwargs={
            "key_filename": f"{os.path.expanduser('~/.aws')}/{get_key(ec2)}.pem"
        },
    )
    con.open()
    if not con.is_connected:
        raise ConnectionError(f"Failed to connect to {con.user}@{con.host}")
    return con


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
    client, name="AdaptiveKey" + str(random.sample(range(int(1e4)), 1)[0])
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
    response = client.describe_images(Filters=[{"Name": "name", "Values": [name]}])
    check_http_status(response)
    image = response.get("Images")
    if len(image) > 1:
        raise ValueError(f"Only 1 image expected; {len(image)} found")
    return image[0]["ImageId"]


def get_volume_id(name: str, client) -> str:
    """Retrieve the ID of a volume"""
    response = client.describe_volumes(Filters=[{"Name": "tag:Name", "Values": [name]}])
    check_http_status(response)
    volumes = response.get("Volumes")
    if len(volumes) != 1:
        raise ValueError(f"Exactly 1 volume expected; {len(volumes)} found")
    return volumes[0]["VolumeId"]


def get_group_id(name: str, client) -> str:
    """Retrieve the ID of a security group"""
    response = client.describe_security_groups(
        Filters=[{"Name": "group-name", "Values": [name]}]
    )
    check_http_status(response)
    groups = response.get("SecurityGroups")
    if len(groups) != 1:
        raise ValueError(f"Exactly 1 group expected; {len(groups)} found")
    return groups[0]["GroupId"]


def get_instance_public_ips(instance_ids: List[str], client) -> List[str]:
    response = client.describe_instances(InstanceIds=instance_ids)
    check_http_status(response)
    instance = response.get("Reservations")[0].get("Instances")
    return [x["PublicIpAddress"] for x in instance]


def server_exists(client, name: str = "AdaptiveServerMaster") -> bool:
    response = client.describe_instances(
        Filters=[{"Name": "tag:Name", "Values": [name]}]
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


def launch_instance(
    client,
    instance_type: str,
    instance_n: int,
    instance_role: str = "Master",
    verbose: bool = True,
):
    # Prepping configuration
    if verbose:
        print("Preparing instance configuration ...")
    adaptive_key = get_key(client)
    adaptive_ami = get_ami_id("aws-docker-adaptive", client)
    adaptive_security_group = get_group_id("AdaptiveExperiment", client)
    instance_params = {
        "ImageId": adaptive_ami,
        "InstanceType": instance_type,
        "KeyName": adaptive_key,
        "MinCount": instance_n,
        "MaxCount": instance_n,
        "Monitoring": {"Enabled": False},
        "Placement": {"AvailabilityZone": "us-east-1a"},
        "SecurityGroupIds": [adaptive_security_group],
        "TagSpecifications": [
            {
                "ResourceType": "instance",
                "Tags": [
                    {
                        "Key": "Name",
                        "Value": f"AdaptiveServer{instance_role}",
                    },
                ],
            },
        ],
    }
    # Launching instance
    if verbose:
        print(f"Launching {instance_role} instance(s) ...")
    instance_response = client.run_instances(**instance_params)
    check_http_status(instance_response)
    instance_ids = [x["InstanceId"] for x in instance_response["Instances"]]
    # Waiting for instance to be ready to go
    if verbose:
        print(f"Waiting for {instance_role} instance(s) to be healthy ...")
    waiter = client.get_waiter("instance_status_ok")
    waiter.wait(InstanceIds=instance_ids, WaiterConfig={"Delay": 10, "MaxAttempts": 48})
    return instance_ids


def launch_master_instance(client, verbose: bool = True) -> str:
    adaptive_volume = get_volume_id("AdaptiveVolume", client)
    # Launch instance
    [instance_id] = launch_instance(
        client,
        instance_type=INSTANCE_TYPE_MASTER,
        instance_n=1,
        instance_role="Master",
        verbose=True,
    )
    # Attach volume
    attach_response = client.attach_volume(
        Device="/dev/sdd", InstanceId=instance_id, VolumeId=adaptive_volume
    )
    check_http_status(attach_response)
    # Wait for volume to be in use
    if verbose:
        print("Waiting for volume to be in use ...")
    waiter = client.get_waiter("volume_in_use")
    waiter.wait(
        VolumeIds=[adaptive_volume],
        WaiterConfig={"Delay": 10, "MaxAttempts": 12},
    )
    return instance_id


def launch_node_instances(client, n: int, verbose: bool = True) -> List[str]:
    instance_ids = launch_instance(
        client,
        instance_type=INSTANCE_TYPE_NODE,
        instance_n=n,
        instance_role="Node",
        verbose=True,
    )
    return instance_ids


def mount_volume_to_drive(instance_id: str, volume: str, client) -> None:
    [public_ip] = get_instance_public_ips([instance_id], client)
    # Initialize SSH connection
    con = connect_ssh(ip=public_ip)
    # Make sure that device /dev/xvdd or /dev/nvme1n1 exists
    devices = ["/dev/xvdd", "/dev/nvme1n1"]
    target_device = []
    for device in devices:
        device_exists = (
            con.run(
                f"[ -b {device} ] && echo true || echo false", hide=True
            ).stdout.strip()
            == "true"
        )
        if device_exists:
            target_device.append(device)
    if not target_device:
        raise FileNotFoundError("Neither device /dev/xvdd nor /dev/nvme1n1 was found")
    elif len(target_device) == 2:
        raise FileExistsError("Both devices (/dev/xvdd; /dev/nvme1n1) were found")
    # Check whether the drive has a file system yet
    filesys = (
        con.run(f"sudo file -s {target_device[0]}", hide=True)
        .stdout.strip()
        .removeprefix(f"{target_device[0]}: ")
    )
    if filesys == "data":
        print(f"Creating a file system on device {target_device[0]} ...")
        con.run(f"sudo mkfs -t xfs {target_device[0]}")
    # Make a directory where we will mount the drive
    data_dir_exists = (
        con.run("[ -d ./data ] && echo true || echo false", hide=True).stdout.strip()
        == "true"
    )
    if not data_dir_exists:
        print(f"Creating mountpoint for device {target_device[0]} at {volume} ...")
        con.run(f"sudo mkdir {volume}")
    # Check if the volume is mounted yet
    volume_is_mtd = (
        con.run(
            f"sudo lsblk -o MOUNTPOINT {target_device[0]} | grep -v MOUNTPOINT",
            hide=True,
        ).stdout.strip()
        != ""
    )
    if not volume_is_mtd:
        print(f"Mounting {target_device[0]} at {volume} ...")
        con.run(f"sudo mount {target_device[0]} {volume}")
    # Give the file system correct permissions
    con.run(f"sudo chmod -R 777 {volume}")
    # Terminate SSH connection
    con.close()


def launch_swarm(master_id: str, node_ids: List[str], client) -> None:
    [master_ip] = get_instance_public_ips([master_id], client)
    node_ips = get_instance_public_ips(node_ids, client)
    # Initialize SSH connection to Master instance
    master_con = connect_ssh(ip=master_ip)
    # Upload swarm launch script and .env to master instance
    target_dir = master_con.run("echo $HOME", hide=True).stdout.strip()
    master_con.put(base_dir / "scripts" / "swarm-launch-aws.sh", target_dir)
    master_con.put(base_dir / ".env", target_dir)
    # Initialize swarm
    swarm_command = re.search(
        r"docker swarm join --token \S+ \S+",
        master_con.run(
            "sudo docker swarm init --force-new-cluster "
            + f"--advertise-addr {master_ip}"
        ).stdout.strip(),
    ).group(0)
    # Execute the script
    master_con.run("sudo /bin/bash swarm-launch-aws.sh")
    # Connect all node instances to master instance
    for node_ip in node_ips:
        print(f"Node: {node_ip}")
        node_con = connect_ssh(ip=node_ip)
        node_con.run("sudo " + swarm_command)
        node_con.close()
    # Scale up the swarm
    master_con.run(f"sudo docker service scale adaptive_stack_app={SWARM_N}")
    master_con.close()


if __name__ == "__main__":

    # Create EC2 service
    ec2 = boto3.client("ec2")
    check_http_status(ec2.describe_instances())

    # Check if the server is already running... If so do nothing.
    server_running = server_exists(ec2)

    if not server_running:
        # Launch the master instance
        master_id = launch_master_instance(ec2)
        print(f"Volume attached. Buffering for {BUFFER} seconds")
        time.sleep(BUFFER)
        # Launch fleet of node instances
        node_ids = launch_node_instances(ec2, n=1)
        try:
            # Mount the volume
            print("Mounting volume to Master instance")
            mount_volume_to_drive(master_id, POSTGRES_VOLUME, ec2)
            # Launch the adaptive app swarm
            print("Launching swarm")
            launch_swarm(master_id, node_ids, ec2)
        except Exception:
            print(traceback.format_exc())
            response = ec2.terminate_instances(InstanceIds=[master_id] + node_ids)
            check_http_status(response)
