import boto3


def check_http_status(response: dict) -> None:
    """Simple checker of HTTP status"""
    code = response.get("ResponseMetadata")["HTTPStatusCode"]
    if code >= 400:
        raise ConnectionError(f"Returned HTTP status code {code}")
    return None


def group_exists(client, name: str = "AdaptiveExperiment") -> bool:
    response = client.describe_security_groups(
        Filters=[{"Name": "group-name", "Values": [name]}]
    )
    check_http_status(response)
    groups = response.get("SecurityGroups")
    if len(groups) > 0:
        return True
    return False


def make_security_group(client, name: str = "AdaptiveExperiment") -> bool:
    exists = group_exists(client, name=name)
    if exists:
        return True
    create_response = client.create_security_group(
        Description="Allows SSH and limited HTTP(S) access", GroupName=name
    )
    check_http_status(create_response)
    ip_response = client.authorize_security_group_ingress(
        GroupId=create_response.get("GroupId"),
        IpPermissions=[
            {
                "FromPort": 22,
                "IpProtocol": "tcp",
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                "ToPort": 22,
            },
            {
                "FromPort": 80,
                "IpProtocol": "tcp",
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                "ToPort": 80,
            },
            {
                "FromPort": 8000,
                "IpProtocol": "tcp",
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                "ToPort": 8000,
            },
        ],
    )
    check_http_status(ip_response)
    return True


if __name__ == "__main__":
    # Make EC2 client and ensure it's alive
    ec2 = boto3.client("ec2")
    check_http_status(ec2.describe_instances())

    print("Provisioning security group ...")
    make_security_group(ec2)
    print("Successfully created security group ...")
