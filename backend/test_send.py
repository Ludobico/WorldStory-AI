import requests
import json

url = "http://127.0.0.1:8000/stream_chat"
message = "What NFL team won the Super Bowl in the year Justin Bierber was born???"
data = {"content": message}
headers = {
    "Content-Type": "application/json"
}

with requests.post(url, data=json.dumps(data), headers=headers, stream=True) as r:
    for chunk in r.iter_content(chunk_size=1024):
        print(chunk)
