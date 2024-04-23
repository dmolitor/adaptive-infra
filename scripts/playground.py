import json
import requests as req

"""Interact with the API when testing locally"""

# Set port element to 80 for Docker testing;
base_url = "http://localhost:80"
# Execute the lines below if api is hosted on a server
# server_ip = "34.201.138.172"
# base_url = f"http://{server_ip}:80"

def json_pprint(x):
    print(json.dumps(x, indent=4))

# Make sure it's alive
print(req.get(base_url).text)

# Retrieve the bandit table
json_pprint(req.get(base_url + "/bandit").json())

# Print bandit parameters
json_pprint(req.get(base_url + "/bandit/parameters").json())

# Print the batch and Pi table
json_pprint(req.get(base_url + "/bandit/batch").json())
json_pprint(req.get(base_url + "/bandit/pi").json())

# Print all responses
json_pprint(req.get(base_url + "/responses").json())
# Print all no-consent records
json_pprint(req.get(base_url + "/responses/noconsent").json())

# Get the current batch id
json_pprint(req.get(base_url + "/bandit/batch/current/").json())