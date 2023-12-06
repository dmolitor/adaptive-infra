from utils import ip_private
import json
import requests

json_payload = {
  'meta': {
    'requestId': 'c28bad3b-feb6-43cb-8975-1d20423d38be',
    'httpStatus': '200 - OK'
  },
  'result': {
    'labels': {
      'QID2_DO': ['Coffee', 'Tea', 'Orange Juide'],
      'QID1': 'Eggs',
      'QID1_DO': ['Bacon', 'Eggs', 'Chocolate'],
      'finished': 'True',
      'status': 'Spam',
      'QID2': 'Coffee'
    },
    'responseId': 'R_1QasAWMu5RPGgTs',
    'displayedFields': ['QID1', 'QID2'],
    'displayedValues': {
      'QID1': [1, 2, 3],
      'QID2': [1, 2, 3]
    },
    'values': {
      'distributionChannel': 'anonymous',
      'QID2_DO': ['1', '2', '3'],
      'endDate': '2019-04-05T13:39:59Z',
      'duration': 5,
      'progress': 100,
      'locationLongitude': '-73.5682983398',
      'status': 8,
      'QID2': 1,
      'startDate': '2019-04-05T13:39:54Z',
      'recordedDate': '2019-04-05T13:39:59.900Z',
      'QID1': 2,
      'locationLatitude': '45.5115051270',
      'ipAddress': '70.80.9.27',
      'userLanguage': 'EN',
      'QID1_DO': ['1', '2', '3'],
      'finished': 1
    }
  }
}

url = f"http://{ip_private()}:8080"

if __name__ == "__main__":
    response = requests.post(url, json=json_payload)
