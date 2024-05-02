import os
from utils_db import initialize_bandit

"""
This script initializes the Bandit table in the database and also
initializes the batch size for the current experiment.
"""

# Set the batch size!
BATCH_SIZE = int(os.environ["BATCH_SIZE"])

# Initialize the bandit table if it does not already exist
# Initialize the bandit (all its arms and corresponding parameters)
bandit = {
    "labels": ["arm1"],
    "params": {
        "arm1": {"alpha": 1, "beta": 1}
    },
    "meta": {
        "arm1": {
            "names": ["Rasheed Booker", "Neil Schwartz"],
            "description": [
                (
                    "Neat and clean, modern and cozy 1 bedroom apartment, "
                    + "including an office/living room area. Beautiful "
                    + "craftsman style single family home."
                ),
                (
                    "Stay in a spacious and bright apartment in our "
                    + "comfortable single-family home! Near to restaurants, "
                    + "attractions, and the beach."
                )
            ],
            "cost": [250, 300],
            "distance": [
                "15 minute walk from city center",
                (
                    "5 minutes walk from the beach, "
                    + "5 minute drive to the city center."
                )
            ],
            "host_rating": [4.95, 4.92]
        }
    },
    "pi": {"arm1": 1},
    "batch": {"remaining": BATCH_SIZE, "active": True}
}
initialize_bandit(bandit)