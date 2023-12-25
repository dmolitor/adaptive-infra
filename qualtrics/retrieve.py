from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from utils import ip_private
import urllib
import sys
import requests
import os
import json

## Manually put these in to run code!!!!!
API_TOKEN = ""
DATA_CENTER = ""


def getReponse(d, dataCenter, apiToken):
    responseId = d["ResponseID"]
    surveyId = d["SurveyID"]

    headers = {
        "content-type": "application/json",
        "x-api-token": apiToken,
    }

    url = "https://{0}.qualtrics.com/API/v3/surveys/{1}/responses/{2}".format(
        dataCenter, surveyId, responseId
    )

    rsp = requests.get(url, headers=headers)
    response_json = rsp.json()
    with open(
        "/Users/dmolitor/Documents/code/adaptive-infra/responses.json", "w+"
    ) as fp:
        json.dump(response_json, fp)


def parsey(c):
    print(f"c: {c}")
    x = c.decode().split("&")
    print(f"x: {x}")
    d = {}
    for i in x:
        print(f"i: {i}")
        a, b = i.split("=")
        d[a] = b

    d["CompletedDate"] = urllib.parse.unquote(d["CompletedDate"])

    return d


class Handler(BaseHTTPRequestHandler):
    # GET
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        d = parsey(post_data)

        try:
            # apiToken = os.environ['APIKEY']
            # dataCenter = os.environ['DATACENTER']
            apiToken = API_TOKEN
            dataCenter = DATA_CENTER
        except KeyError:
            print("set environment variables APIKEY and DATACENTER")
            sys.exit(2)

        getReponse(d, dataCenter, apiToken)


def run():
    print("starting server...")
    server_address = (ip_private(), 8080)

    httpd = HTTPServer(server_address, Handler)
    print("running server...")
    httpd.serve_forever()


try:
    run()
except KeyboardInterrupt:
    sys.exit(0)
