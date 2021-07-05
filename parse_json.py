import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'

# parse json_text, the result is a Python dictionary:
y = json.loads(json_text)

print(y['messages'][1]["message"])
