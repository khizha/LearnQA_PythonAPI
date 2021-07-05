import requests
import json
import time

# run the task without token parameter to retrieve token and seconds values
response = requests.get(" https://playground.learnqa.ru/ajax/api/longtime_job")

as_dict = json.loads(response.text)

# get token and seconds data from the response
token = as_dict["token"]
task_length = as_dict["seconds"]

# run the task with token parameter
payload = {"token": token}
response = requests.get(" https://playground.learnqa.ru/ajax/api/longtime_job", params=payload)

as_dict = json.loads(response.text)

if as_dict["status"] == "Job is NOT ready":
    # wait for the time specified in 'seconds' parameter
    time.sleep(task_length)

# repeat the request
response = requests.get(" https://playground.learnqa.ru/ajax/api/longtime_job", params=payload)

as_dict = json.loads(response.text)
if as_dict["status"] == "Job is ready" and "result" in as_dict.keys():
    print("Job completed successfully")
else:
    print("ERROR")
