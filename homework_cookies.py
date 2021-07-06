import requests

def test_cookies():
    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")

    for cookie in response.cookies:
        print('cookie domain = ' + cookie.domain)
        print('cookie name = ' + cookie.name)
        print('cookie value = ' + cookie.value)
        print('*************************************')


    assert response.cookies["HomeWork"] == "hw_value", f"Cookie 'Homework' has wrong value"