import os
import itertools
from utils_db import initialize_bandit

"""
This script initializes the Bandit table in the database and also
initializes the batch size for the current experiment.
"""

# Set the batch size!
BATCH_SIZE = int(os.environ["BATCH_SIZE"])

# Initialize the bandit table if it does not already exist
# Initialize the bandit (all its arms and corresponding parameters)
meta_generator = {
    "prior_trips": [
        [
            "Has visited once for vacation",
            "Two trips, both during the holidays"
        ],
        [
            "Has traveled to the U.S. every other summer since childhood",
            "Has visited the U.S. many times as a tourist"
        ]
    ],
    "education": [["College degree", "No formal education"]],
    "reason": [
        [
            "Escaping political/religious persecution",
            "Escalating violence in home country"
        ],
        [
            "Seeking better employment opportunities",
            "Greater access to high-paying jobs"
        ]
    ],
    "origin": [["Poland", "Germany"], ["Sudan", "Somalia"]],
    "profession": [
        ["Waiter", "Janitor"],
        ["Information Technology Specialist", "Construction Worker"]
    ]
}

# Create all possible metadata combinations
meta_dicts = []
combinations = itertools.product(
    *(meta_generator[key] for key in meta_generator)
)
for combination in combinations:
    temp_dict = dict(zip(meta_generator.keys(), combination))
    meta_dicts.append(temp_dict)

bandit_metadata = {}
for i, d in enumerate(meta_dicts):
    bandit_metadata[f"arm{i+1}"] = d

# Create the parameters for each bandit arm
arm_params = {"alpha": 1, "beta": 1}
bandit_params = {}
for k in bandit_metadata.keys():
    bandit_params[k] = arm_params

# Create the Pi values for each bandit arm
bandit_pis = {}
for i, k in enumerate(bandit_metadata.keys()):
    bandit_pis[k] = (i+1)/len(bandit_metadata)

# Initialize the bandit table
bandit = {
    "labels": list(bandit_metadata.keys()),
    "params": bandit_params,
    "meta": bandit_metadata,
    "pi": {"arm1": 1},
    "batch": {"remaining": BATCH_SIZE, "active": True}
}
initialize_bandit(bandit)