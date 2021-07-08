from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest
import time
import random
import string
import allure

keys_list = ['password',
            'username',
            'firstName',
            'lastName',
             'email']

@allure.epic("REGISTER cases")
class TestUserRegister(BaseCase):

    @allure.description("This test successfully creates a new user.")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        with allure.step("Register a new user:"):
            response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("This test tries to create a user with already existing email.")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        with allure.step(f"Register a new user with the existing email '{email}':"):
            response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content '{response.content}'"

    @allure.description("This test tries to create a user with incorrect email.")
    def test_create_user_with_incorrect_email(self):
        # create user with incorrect email format (email without '@' sign)
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        with allure.step(f"Register a new user with an incorrect email '{email}':"):
            response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f"Unexpected response content '{response.content}'"

    @allure.story(f"Run test for every parameter from 'keys_list' list: {keys_list}")
    @pytest.mark.parametrize('key', keys_list)
    @allure.description("This test tries to create a user without one field.")
    def test_create_user_without_one_field(self, key):
        #data = self.prepare_registration_data()

        incomplete_data = self.prepare_incomplete_registration_data(key)
        time.sleep(1)

        with allure.step(f"Register a new user without '{key}' field:"):
            response = MyRequests.post("/user/", data=incomplete_data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {key}", f"Unexpected response content '{response.content}'"

    @allure.description("This test tries to create a user with one-symbol long name.")
    def test_create_user_with_one_symbol_name(self):

        short_name = random.choice(string.ascii_letters)

        data = self.prepare_registration_data()
        data['firstName'] = short_name

        with allure.step(f"Register a new user with firstName parameter set to '{short_name}':"):
            response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short", f"Unexpected response content '{response.content}'"

    @allure.description("This test tries to create a user with too long name.")
    def test_create_user_with_too_long_name(self):

        long_name = ''.join((random.choice(string.ascii_letters) for x in range(256)))

        data = self.prepare_registration_data()
        data['firstName'] = long_name

        with allure.step(f"Register a new user with firstName parameter set to '{long_name}':"):
         response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too long", f"Unexpected response content '{response.content}'"
