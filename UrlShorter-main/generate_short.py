import requests
import json

url = 'http://localhost/create_code'
data = {'url': 'https://www.youtube.com/shorts/m1evLJTZq0E', 'ttl': '20'}

# Send the request with application/json content type
response = requests.post(url, json=data)

print(response.text)