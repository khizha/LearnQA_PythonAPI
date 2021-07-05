import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)

number_of_responses = len(response.history)

print(f"Total number of redirects: {number_of_responses}")
print(f"Resulting URL: {response.url}")


