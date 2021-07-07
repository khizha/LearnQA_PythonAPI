from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import random
import string

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )


    def test_edit_user_when_not_authorized(self):
        new_name = "Changed Name"
        user_id = 2

        response = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Auth token not supplied", f"Unexpected response content '{response.content}'"

    def test_edit_user_when_authorized_as_another_user(self):
        # REGISTER one user
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]

        # REGISTER another user
        register_data = self.prepare_registration_data()
        response11 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response11, 200)
        Assertions.assert_json_has_key(response11, "id")

        user_id_two = self.get_json_value(response11, "id")

        # LOGIN as the first created user
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        print(user_id_two)

        response3 = MyRequests.put(
            f"/user/{user_id_two}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        #print(response3.content)

        Assertions.assert_code_status(response3, 200)
        assert response3.content.decode("utf-8") == f"", f"Unexpected response content '{response3.content}'"

    def test_edit_email_of_just_created_user(self):
        # try to change the e-mail value to incorrect one with missing '@' sign

        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_email = 'abracadabraexample.com'

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == f"Invalid email format", f"Unexpected response content '{response3.content}'"

    def test_edit_firstname_of_just_created_user(self):
        # try to change the firstName attribute value to one-symbol long one

        # REGISTER
        register_data = self.prepare_registration_data()
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

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        short_first_name = random.choice(string.ascii_letters)

        #print(short_first_name)

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": short_first_name}
        )

        #print(response3.content)

        Assertions.assert_code_status(response3, 200)
        assert response3.content.decode("utf-8") == f"", f"Unexpected response content '{response3.content}'"