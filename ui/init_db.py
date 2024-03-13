from utils_db import initialize_bandit

"""
This script initializes the Bandit table in the database and also
initializes the batch size for the current experiment.
"""

# Set the batch size!
BATCH_SIZE = 1

# Initialize the bandit table if it does not already exist
# Initialize the bandit (all its arms and corresponding parameters)
bandit = {
    "labels": ["arm1", "arm2", "arm3", "arm4"],
    "params": {
        "arm1": {"alpha": 1, "beta": 1},
        "arm2": {"alpha": 1, "beta": 1},
        "arm3": {"alpha": 1, "beta": 1},
        "arm4": {"alpha": 1, "beta": 1}
    },
    "meta": {
        "arm1": {
            "names": ["Laurie Schmitt", "Allison O'Connell"],
            "ages": [49, 62],
            "political_exp": ["Member of Congress", "State legislator"],
            "career_exp": ["Restaurant owner", "Small business owner"]
        },
        "arm2": {
            "names": ["Laurie Schmitt", "Allison O'Connell"],
            "ages": [49, 62],
            "political_exp": ["No experience", "No experience"],
            "career_exp": ["Restaurant owner", "Small business owner"]
        },
        "arm3": {
            "names": ["Tanisha Rivers", "Keisha Mosely"],
            "ages": [70, 26],
            "political_exp": ["Member of Congress", "State legislator"],
            "career_exp": ["Restaurant owner", "Small business owner"]
        },
        "arm4": {
            "names": ["Tanisha Rivers", "Keisha Mosely"],
            "ages": [49, 62],
            "political_exp": ["No experience", "No experience"],
            "career_exp": ["Restaurant owner", "Small business owner"]
        }
    },
    "pi": {"arm1": 0.25, "arm2": 0.5, "arm3": 0.75, "arm4": 1},
    "batch": {"remaining": BATCH_SIZE, "active": True}
}
initialize_bandit(bandit)