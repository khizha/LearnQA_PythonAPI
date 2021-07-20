from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.epic("Deletion cases")
class TestUserDelete(BaseCase):
    @allure.description("This test tries to delete user with ID=2 and proves it is impossible. ")
    def test_delete_user_with_id_2(self):
        # login
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step("Login as user with id=2, using email and password:"):
            response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id")

        # try to delete currently logged user (id=2)
        with allure.step("Try to delete currently logged user (id=2):"):
            response2 = MyRequests.delete(f"/user/{user_id}",
                                        data=data,
                                        headers={"x-csrf-token": token},
                                        cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5.", f"Unexpected response content '{response2.content}'"

    @allure.description("This test tries to delete just created user. ")
    def test_delete_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        with allure.step("Create a new user:"):
            response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        with allure.step("Login as just created user:"):
            response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        with allure.step("Try to delete the created user:"):
            response3 = MyRequests.delete(f"/user/{user_id}",
                                        data=login_data,
                                        headers={"x-csrf-token": token},
                                        cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 200)

        # try to get the just deleted user's data by ID
        with allure.step("try to get the just deleted user's data by ID"):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == f"User not found", f"Unexpected response content '{response4.content}'"

    @allure.description("This test tries to delete a user being logged as another user. ")
    def test_delete_user_when_logged_in_as_another_user(self):
        # register a new user
        with allure.step("Register a new user"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # login as the created user to get cookies and headers
        with allure.step("Login as the created user to get cookies and headers"):
            response11 = MyRequests.post("/user/login", data=register_data)
        Assertions.assert_code_status(response11, 200)
        auth_sid = self.get_cookie(response11, "auth_sid")
        token = self.get_header(response11, "x-csrf-token")

        # register one more user
        with allure.step("Register one more user"):
            register_data_2 = self.prepare_registration_data()
            response2 = MyRequests.post("/user/", data=register_data_2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email2 = register_data_2["email"]
        password2 = register_data_2["password"]
        user_id2 = self.get_json_value(response2, "id")

        # login as the second created user
        with allure.step("Login as the second created user"):
            response21 = MyRequests.post("/user/login", data=register_data_2)
            Assertions.assert_code_status(response21, 200)


        # try to delete the first created user
        data = {
            'email': email,
            'password': password

        }

        with allure.step("Try to delete the first created user"):
            response3 = MyRequests.delete(f"/user/{user_id}",
                                        data=data,
                                        headers={"x-csrf-token": token},
                                        cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 200)
        assert response3.content.decode("utf-8") == f"", f"Unexpected response content '{response3.content}'"

        # check that the user 'user_id' was deleted
        response4 = MyRequests.get(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode(
            "utf-8") == f"User not found", f"Unexpected response content '{response4.content}'"
