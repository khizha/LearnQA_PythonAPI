from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest
import time
import random
import string

keys_list = ['password',
            'username',
            'firstName',
            'lastName',
             'email']

class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content '{response.content}'"

    def test_create_user_with_incorrect_email(self):
        # create user with incorrect email format (email without '@' sign)
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f"Unexpected response content '{response.content}'"

    @pytest.mark.parametrize('key', keys_list)
    def test_create_user_without_one_field(self, key):
        #data = self.prepare_registration_data()

        incomplete_data = self.prepare_incomplete_registration_data(key)
        time.sleep(1)

        response = MyRequests.post("/user/", data=incomplete_data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {key}", f"Unexpected response content '{response.content}'"

    def test_create_user_with_one_symbol_name(self):

        short_name = random.choice(string.ascii_letters)

        data = self.prepare_registration_data()
        data['firstName'] = short_name

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short", f"Unexpected response content '{response.content}'"
