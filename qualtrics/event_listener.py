from utils import ip_private
import requests


def get_event_listeners(token, data_center):
    url = f"https://{data_center}.qualtrics.com/API/v3/eventsubscriptions/"
    headers = {
        "X-API-TOKEN": token,
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    return response


def event_listener(token, survey_id, data_center, pub_url):
    headers = {
        "X-API-TOKEN": token,
        "Content-Type": "application/json",
    }
    json_data = {
        "topics": f"surveyengine.completedResponse.{survey_id}",
        "publicationUrl": pub_url,
        "encrypt": False,
    }
    post_url = f"https://{data_center}.qualtrics.com/API/v3/eventsubscriptions/"
    response = requests.post(post_url, headers=headers, json=json_data)
    return response


if __name__ == "__main__":
    pub_url = f"http://{ip_private()}:8080"
