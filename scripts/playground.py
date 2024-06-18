import json
import pandas as pd
import requests as req

"""Interact with the API when testing locally"""

# Set port element to 80 for Docker testing;
base_url = "http://localhost:80"
# Execute the lines below if api is hosted on a server
# server_ip = "12.345.578.910"
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

# Get all responses as a DataFrame
responses = pd.DataFrame(req.get(base_url + "/responses").json())
responses_noconsent = pd.DataFrame(req.get(base_url + "/responses/noconsent").json())
perc_discriminated = round(
    responses[responses.garbage != True].discriminated.sum()
    / len(responses[responses.garbage != True])
    * 100,
    1
)
n_by_sex = responses[responses.garbage != True].groupby(["sex"]).count()
n_female = n_by_sex.filter(like="female", axis=0)["id"].iloc[0]
n_male = n_by_sex.filter(like="male", axis=0)["id"].iloc[1]
mean_age = responses[responses.garbage != True].age.mean()
median_age = responses[responses.garbage != True].age.median()
eth_counts = (
    responses[responses.garbage != True]["ethnicity"].value_counts(normalize=True)
)
ethnicity = (
    "\n".join(
        [
            f"\t{eth}: {round(count * 100, 1)}%"
            for eth, count in eth_counts.items()
        ]
    )
)
race_counts = (
    responses[responses.garbage != True]["race"].value_counts(normalize=True)
)
race = (
    "\n".join(
        [
            f"\t{race}: {round(count * 100, 1)}%"
            for race, count in race_counts.items()
        ]
    )
)


# How many responses are garbage
print(
    f"{len(responses)} valid responses have been received\n"
    f"{len(responses_noconsent)} respondents have not consented to participation\n"
    f"{round(responses.garbage.sum()/len(responses), 3)*100}%"
    + " of responses are garbage\n"
    "Current active batch id: "
    + f"{req.get(base_url + '/bandit/batch/current/').json()['id']}\n"
    + f"{perc_discriminated}% of valid responses have discriminated\n"
    + "Respondent sex:\n"
    + f"    - Female: {round(n_female/(n_female + n_male), 3)*100}%\n"
    + f"    -   Male: {round(n_male/(n_female + n_male), 3)*100}\n"
    + f"Mean (median) respondent age: {round(mean_age, 1)} ({median_age})\n"
    + "Respondent ethnicity:\n"
    + f"{ethnicity}\n"
    + "Respondent race:\n"
    + f"{race}\n"
)