import json
import requests as req
import sys

PROLIFIC_API_TOKEN = sys.argv[1]
base_url = "https://api.prolific.com/api/v1/"

def json_pprint(x):
    print(json.dumps(x, indent=4))

resp = req.get(
    url=base_url + "studies/",
    headers={"Authorization": "Token " + PROLIFIC_API_TOKEN}
)
resp.raise_for_status()
keys = ["id", "name", "status"]
for study in resp.json()["results"]:
    json_pprint({k: study[k] for k in keys})