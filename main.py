import requests

payload = {"name": "User"}
response = requests.get("https://playground.learnqa.ru/api/hello", params=payload)
#response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)