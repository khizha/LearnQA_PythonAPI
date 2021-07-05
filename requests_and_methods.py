import requests
import json

response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print("\n")
print(f"HTTP request without 'method' parameter returns the following response: {response.text}")

print("\n")
payload = {"method": "HEAD"}
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=payload)
print(f"HTTP request with a wrong 'method' parameter returns the following response: {response.text}")

print("\n")
payload = {"method": "GET"}
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=payload)
print(f"HTTP request with a correct 'method' parameter returns the following response: {response.text}")

methods = ["GET", "POST", "PUT", "DELETE"]
print("\n")
for x in methods:
    payload = {"method": x}
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=payload)
    print(f"HTTP GET request with a 'method' parameter  set to {x} returns the following response: {response.text}")

print("\n")
for x in methods:
    payload = {"method": x}
    response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload)
    print(f"HTTP POST request with a 'method' parameter  set to {x} returns the following response: {response.text}")

print("\n")
for x in methods:
    payload = {"method": x}
    response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload)
    print(f"HTTP PUT request with a 'method' parameter  set to {x} returns the following response: {response.text}")

print("\n")
for x in methods:
    payload = {"method": x}
    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload)
    print(f"HTTP DELETE request with a 'method' parameter  set to {x} returns the following response: {response.text}")