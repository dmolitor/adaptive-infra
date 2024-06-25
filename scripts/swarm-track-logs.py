from fabric.connection import Connection
import os
import sys

args = sys.argv[1:]
assert len(args) == 3, f"Expected 3 arguments; {len(args)} were provided"
ip = args[0]
key_fp = args[1]
service = args[2]

if service not in ["api", "app", "database"]:
    raise ValueError("service must be one of 'api', 'app', or 'database'")

if __name__ == "__main__":

    con = Connection(
        host=ip,
        user="ubuntu",
        connect_kwargs={"key_filename": f"{os.path.expanduser(key_fp)}"},
    )
    con.open()
    if not con.is_connected:
        raise ConnectionError(f"Failed to connect to {con.user}@{con.host}")

    con.run(f"sudo docker service logs -f adaptive_stack_{service}")
