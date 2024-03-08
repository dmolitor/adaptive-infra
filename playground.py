import json
import requests as req

base_url = "http://127.0.0.1:8000"

def json_pprint(x):
    print(json.dumps(x, indent=4))

# Make sure it's alive
print(req.get(base_url).text)

# Retrieve the bandit table
json_pprint(req.get(base_url + "/bandit").json())

# Retrieve the parameters table
json_pprint(req.get(base_url + "/bandit/parameters").json())

# Add a new row of parameters for bandit arm three
target_arm = 3
(
    req
    .post(
        base_url + f"/bandit/parameters/{target_arm}",
        json={"labels": ["hello"], "params": {"alpha": 1, "beta": 2}}
    )
    .raise_for_status()
)
# Print updated bandit arms
json_pprint(req.get(base_url + "/bandit/parameters").json())

# Increment both the alpha and beta parameters for arm 3
(
    req
    .post(
        base_url + f"/bandit/parameters?arm_id={target_arm}&alpha=true&beta=false"
    )
    .raise_for_status()
)
# Print updated bandit arms
json_pprint(req.get(base_url + "/bandit").json())

# Submit an example response form (Or just fill out the survey form!!)
# If you want to fill in several sample surveys, you will need to kill and
# restart the survey otherwise it'll just duplicate the results.
example_form = {
    "consent": True,
    "prolific_id": "12345678910",
    "in_usa": True,
    "commitment": "unsure",
    "captcha": "purple",
    "candidate_preference": 0,
    "candidate_older": 0,
    "age": 26,
    "race": "race_white",
    "ethnicity": "hisp_latin_spanish_no",
    "sex": "male"
}
req.post(base_url + "/responses", json=example_form).raise_for_status()

# Print all responses
json_pprint(req.get(base_url + "/responses").json())

# Get randomized context comparison data
json_pprint(req.get(base_url + "/randomize").json())