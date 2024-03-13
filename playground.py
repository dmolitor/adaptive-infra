import json
import requests as req

"""Interact with the API when testing locally"""

base_url = "http://127.0.0.1:8000"

def json_pprint(x):
    print(json.dumps(x, indent=4))

# Make sure it's alive
print(req.get(base_url).text)

# Retrieve the bandit table
json_pprint(req.get(base_url + "/bandit").json())

# Retrieve the parameters table
json_pprint(req.get(base_url + "/bandit/parameters").json())

# Print bandit parameters
json_pprint(req.get(base_url + "/bandit/parameters").json())

# Print the batch and Pi table
json_pprint(req.get(base_url + "/bandit/batch").json())
json_pprint(req.get(base_url + "/bandit/pi").json())

# Submit an example response form (Or just fill out the survey form!!)
# If you want to fill in several sample surveys, you will need to kill and
# restart the survey otherwise it'll just duplicate the results.
example_form = {
    "consent": True,
    "arm_id": 1,
    "batch_id": 1,
    "prolific_id": "12345678910",
    "in_usa": True,
    "commitment": "unsure",
    "captcha": "purple",
    "candidate_preference": 0,
    "candidate_older": 1,
    "candidate_older_truth": 1,
    "age": 26,
    "race": "race_white",
    "ethnicity": "hisp_latin_spanish_no",
    "sex": "male",
    "discriminated": True
}
req.post(base_url + "/responses", json=example_form).raise_for_status()

# Print all responses
json_pprint(req.get(base_url + "/responses").json())

# Get randomized context comparison data
json_pprint(req.get(base_url + "/randomize").json())

# Get the current batch id
cur_batch = req.get(base_url + "/bandit/batch/current/").json()