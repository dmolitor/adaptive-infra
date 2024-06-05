import boto3


def check_http_status(response: dict) -> None:
    """Simple checker of HTTP status"""
    code = response.get("ResponseMetadata")["HTTPStatusCode"]
    if code >= 400:
        raise ConnectionError(f"Returned HTTP status code {code}")
    return None


def running_image_ids(client, name: str = "AdaptiveServer") -> list[str]:
    response = client.describe_instances(
        Filters=[{"Name": "tag:Name", "Values": [name]}]
    )
    check_http_status(response)
    reservations = response.get("Reservations")
    statuses = []
    instance_ids = []
    for reservation in reservations:
        for instance in reservation["Instances"]:
            statuses.append(instance["State"]["Name"])
            instance_ids.append(instance["InstanceId"])
    running_ids = [
        id
        for status, id in zip(statuses, instance_ids)
        if status == "pending" or status == "running"
    ]
    return running_ids


if __name__ == "__main__":

    # Create EC2 service
    ec2 = boto3.client("ec2")
    check_http_status(ec2.describe_instances())

    # Get any running adaptive instance IDs
    swarm_server = running_image_ids(ec2)

    # Only shut down if it's non-empty
    if swarm_server:
        print(f"Terminating the following instances: {swarm_server} ...")
        terminate_response = ec2.terminate_instances(InstanceIds=swarm_server)
        check_http_status(terminate_response)
