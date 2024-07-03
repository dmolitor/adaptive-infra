import json
import pandas as pd
import requests as req

"""Interact with the API when testing locally"""

# Set port element to 80 for Docker testing;
base_url = "http://localhost:80"
# Execute the lines below if api is hosted on a server
# server_ip = ""
# base_url = f"http://{server_ip}:80"


def json_pprint(x):
    print(json.dumps(x, indent=4))


# Make sure it's alive
print(req.get(base_url).text)

# Retrieve the bandit table
json_pprint(req.get(base_url + "/bandit").json())

# Print bandit parameters
json_pprint(
    sorted(
        sorted(
            req.get(base_url + "/bandit/parameters").json(), key=lambda x: x["arm_id"]
        ),
        key=lambda y: y["batch_id"],
    )
)

# Print the batch and Pi table
json_pprint(req.get(base_url + "/bandit/batch").json())
json_pprint(req.get(base_url + "/bandit/pi").json())
json_pprint(req.get(base_url + "/bandit/pi/batch?batch_id=1").json())

batches = req.get(base_url + "/bandit/batch").json()
json_pprint(batches)

# Print all responses
responses = req.get(base_url + "/responses").json()
json_pprint(responses)
json_pprint(
    sorted(
        [
            {
                "id": x["id"],
                "arm_id": x["arm_id"],
                "batch": x["batch_id"],
                "context": x["context_batch_id"],
                "prolific_id": x["prolific_id"],
                "discriminated": x["discriminated"],
                "garbage": x["garbage"],
            }
            for x in responses
            if not x["garbage"]
        ],
        key=lambda x: x["batch"],
    )
)

# Check if a prolific ID exists in the database
id = ""
req.post(base_url + f"/responses/duplicated?prolific_id={id}").json()

# Print all no-consent records
json_pprint(req.get(base_url + "/responses/noconsent").json())

# Get the current batch id
deac = False
cur_batch = req.get(base_url + f"/bandit/batch/current?deactivate={deac}").json()
json_pprint(cur_batch)

# Assert responses are returned correctly
responses = pd.DataFrame(req.get(base_url + "/responses").json())
assert req.get(base_url + "/responses/n").json() == len(responses)
assert req.get(base_url + "/responses/n?filter=True").json() == len(
    responses[responses["garbage"] != True]
)

# Test creation of new batch
new_batch_req = req.post(
    base_url + "/bandit/batch",
    json={"batch_id": cur_batch["id"], "remaining": 1, "maximum": True, "active": True},
)
new_batch_req.raise_for_status()
# Confirm new batch has incremented
assert new_batch_req.json()["id"] == (cur_batch["id"] + 1)

# Print summary of responses
responses_noconsent = pd.DataFrame(req.get(base_url + "/responses/noconsent").json())
perc_discriminated = round(
    responses[responses.garbage != True].discriminated.sum()
    / len(responses[responses.garbage != True])
    * 100,
    1,
)
n_by_sex = responses[responses.garbage != True].groupby(["sex"]).count()
n_female = n_by_sex.filter(like="female", axis=0)["id"].iloc[0]
n_male = n_by_sex.filter(like="male", axis=0)["id"].iloc[1]
mean_age = responses[responses.garbage != True].age.mean()
median_age = responses[responses.garbage != True].age.median()
eth_counts = responses[responses.garbage != True]["ethnicity"].value_counts(
    normalize=True
)
ethnicity = "\n".join(
    [f"\t{eth}: {round(count * 100, 1)}%" for eth, count in eth_counts.items()]
)
race_counts = responses[responses.garbage != True]["race"].value_counts(normalize=True)
race = "\n".join(
    [f"\t{race}: {round(count * 100, 1)}%" for race, count in race_counts.items()]
)


# How many responses are garbage
print(
    f"{len(responses)} valid responses have been received\n"
    f"{len(responses_noconsent)} respondents have not consented to participation\n"
    f"{round(responses.garbage.sum()/len(responses) * 100, 1)}%"
    + " of responses are garbage\n"
    "Current active batch id: "
    + f"{req.get(base_url + '/bandit/batch/current/').json()['id']}\n"
    + f"{perc_discriminated}% of valid responses have discriminated\n"
    + "Respondent sex:\n"
    + f"    - Female: {round(n_female/(n_female + n_male) * 100, 1)}%\n"
    + f"    -   Male: {round(n_male/(n_female + n_male) * 100, 1)}%\n"
    + f"Mean (median) respondent age: {round(mean_age, 1)} ({median_age})\n"
    + "Respondent ethnicity:\n"
    + f"{ethnicity}\n"
    + "Respondent race:\n"
    + f"{race}\n"
)
