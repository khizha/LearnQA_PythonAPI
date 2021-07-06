import pytest
import requests

agents_list = [
    {'agent': 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
     'platform': 'Mobile',
     'browser': 'No',
     'device': 'Android'},

    {'agent': 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
     'platform': 'Mobile',
     'browser': 'Chrome',
     'device': 'iOS'},

    {'agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
     'platform': 'Googlebot',
     'browser': 'Unknown',
     'device': 'Unknown'},

    {'agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
     'platform': 'Web',
     'browser': 'Chrome',
     'device': 'No'},

    {'agent': 'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
     'platform': 'Mobile',
     'browser': 'No',
     'device': 'iPhone'}
]


@pytest.mark.parametrize('user_agent', agents_list)
def test_user_agent_check(user_agent):

    response = requests.get(
        "https://playground.learnqa.ru/ajax/api/user_agent_check",
        headers={"User-Agent": user_agent['agent']}
    )

    response_as_dict = response.json()

    assert user_agent['platform'] == response_as_dict['platform'], f"'platform' parameter is wrong for {user_agent['agent']} User Agent: {response_as_dict['platform']} instead of {user_agent['platform']}"
    assert user_agent['browser'] == response_as_dict['browser'], f"'browser' parameter is wrong for {user_agent['agent']} User Agent: {response_as_dict['browser']} instead of {user_agent['browser']}"
    assert user_agent['device'] == response_as_dict['device'], f"'device' parameter is wrong for {user_agent['agent']} User Agent: {response_as_dict['device']} instead of {user_agent['device']}"