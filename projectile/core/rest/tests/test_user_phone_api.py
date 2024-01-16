# from django.contrib.auth import get_user_model

# from rest_framework import status
# from rest_framework.test import APIClient, APITestCase

# from otpio.choices import UserPhoneStatus

# from . import payloads, urlhelpers


# class PrivateUserPhoneApiTests(APITestCase):
#     """Test authenticated userphone API access"""

#     def setUp(self):
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(
#             email="user@example.com", password="new123password"
#         )

#         self.client.force_authenticate(self.user)

#         # create userphone
#         self.userphone = self.client.post(
#             urlhelpers.phone_list_url(), payloads.phone_payload()
#         )
#         self.assertEqual(self.userphone.status_code, status.HTTP_201_CREATED)

#         # get userphone uid
#         userphone_response = self.client.get(urlhelpers.phone_list_url())
#         self.userphone_uid = userphone_response.data["results"][0]["uid"]

#     def tearDown(self):
#         self.client.logout()

#     def test_create_userphone(self):
#         """Test create userphone response"""

#         response = self.userphone

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_get_userphone(self):
#         """Test get userphone list"""

#         response = self.client.get(urlhelpers.phone_list_url())

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["count"], 1)

#     def test_retrieve_userphone(self):
#         """Test retrieve userphone detail"""

#         response = self.client.get(urlhelpers.phone_detail_url(self.userphone_uid))

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["phone"], self.userphone.data["phone"])

#     def test_update_userphone(self):
#         """Test update userphone"""

#         payload = {"status": UserPhoneStatus.ACTIVE}

#         response = self.client.patch(
#             urlhelpers.phone_detail_url(self.userphone_uid), payload
#         )

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["status"], payload["status"])

#     def test_delete_userphone(self):
#         """Test delete userphone"""

#         response = self.client.delete(
#             urlhelpers.phone_detail_url(self.userphone_uid)
#         )

#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
