from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.epic("GET cases")
class TestUserGet(BaseCase):
    @allure.description("This test tries to get user data when the user is not authorized.")
    def test_get_user_details_not_auth(self):
        #get data for user with id=2
        with allure.step("Get data for the user with id=2:"):
            response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.description("This test gets authorized user's data.")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        with allure.step("Login as user with id=2:"):
            response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        with allure.step("Read user's data:"):
            response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid}
            )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("This test tries to get user's data when authorized as another user.")
    def test_get_user_details_auth_as_different_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        with allure.step("Login as user with id=2:"):
            response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        different_user_id = "1"

        #print(user_id_from_auth_method)

        with allure.step("Read user's data:"):
            response2 = MyRequests.get(f"/user/{different_user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid})

        expected_fields = ["username"]
        Assertions.assert_json_has_keys(response2, expected_fields)

        # check that we cannot get the other user data fields (except for 'username')
        Assertions.assert_json_has_not_key(response2, "email")
        Assertions.assert_json_has_not_key(response2, "firstName")
        Assertions.assert_json_has_not_key(response2, "lastName")
        Assertions.assert_json_has_not_key(response2, "password")