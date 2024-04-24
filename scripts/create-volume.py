import boto3

def check_http_status(response: dict) -> None:
    """Simple checker of HTTP status"""
    code = response.get("ResponseMetadata")["HTTPStatusCode"]
    if code >= 400:
        raise ConnectionError(f"Returned HTTP status code {code}")
    return None

def make_volume(client, name: str = "AdaptiveVolume") -> bool:
    exists = volume_exists(client, name=name)
    if exists:
        return True
    create_response = client.create_volume(
        AvailabilityZone="us-east-1a",
        Size=100,
        VolumeType="gp3",
        TagSpecifications=[
            {
                "ResourceType": "volume",
                "Tags": [{"Key": "Name", "Value": name}]
            }
        ]
    )
    check_http_status(create_response)
    return True

def volume_exists(client, name: str = "AdaptiveVolume") -> bool:
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
    if len(volumes) > 0:
        return True
    return False

if __name__ == "__main__":
    # Make EC2 client and ensure it's alive
    ec2 = boto3.client("ec2")
    check_http_status(ec2.describe_instances())

    print("Provisioning EBS volume ...")
    make_volume(ec2)
    print("Successfully created volume ...")
