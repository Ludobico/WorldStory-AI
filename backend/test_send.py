import requests

url = "http://127.0.0.1:8000/stream"

data = {
    "message": "What NFL team won the Super Bowl in the year Justin Bierber was born?"
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=data, headers=headers)

print("Response status code:", response.status_code)
print("Response content:", response.content)
