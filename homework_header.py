import requests

def test_cookies():
    response = requests.get("https://playground.learnqa.ru/api/homework_header")

    print(response.headers)

    assert response.headers["x-secret-homework-header"] == "Some secret value", "Header 'x-secret-homework-header' has wrong value"