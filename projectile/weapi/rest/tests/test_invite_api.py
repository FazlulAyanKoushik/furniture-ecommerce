"""Test required sending mail which is not possible from local development"""


# from django.contrib.auth import get_user_model

# from rest_framework import status

# from accountio.rest.tests import payloads, urlhelpers as accountio_urlhelpers

# from common.base_test import BaseAPITestCase

# from invitio.choices import OrganizationInviteResponse

# from . import urlhelpers


# class PrivateOrganizationNewsApiTests(BaseAPITestCase):
#     def setUp(self):
#         super(PrivateOrganizationNewsApiTests, self).setUp()

#         # getting user organization list
#         self.organization = self.client.get(urlhelpers.me_organization_list_url())
#         self.organization_slug = self.organization.data["results"][0]["organization"][
#             "slug"
#         ]

#         # create another user
#         self.another_user = get_user_model().objects.create_user(
#             "another_user@example.com", "new1234password"
#         )
#         # onboarding another organization
#         self.onboarding_response_two = self.client.post(
#             urlhelpers.organization_onboarding_url(),
#             payloads.organization_onboard_payload_two(),
#         )

#         # authenticating initiator as auth user
#         self.new_user = get_user_model().objects.get(
#             email=payloads.organization_onboard_payload_two()["email"]
#         )
#         self.client.force_authenticate(self.new_user)
#         # adding another organization staff
#         we_user_create_response = self.client.post(
#             urlhelpers.we_user_list_url(),
#             payloads.user_payload(self.another_user),
#         )
#         self.assertEqual(we_user_create_response.status_code, status.HTTP_201_CREATED)

#         self.new_organization = self.client.get(urlhelpers.me_organization_list_url())
#         self.new_organization_slug = self.new_organization.data["results"][0][
#             "organization"
#         ]["slug"]

#         self.assertEqual(
#             self.onboarding_response_two.status_code, status.HTTP_201_CREATED
#         )

#     def test_get_organization_invitation(self):
#         """Test for getting organization invitation list"""

#         self.client.force_authenticate(self.user)

#         post_response = self.client.post(
#             accountio_urlhelpers.organization_invitation_create_url(
#                 self.new_organization_slug
#             ),
#             payloads.organization_invitation_paylaod(),
#         )

#         self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

#         response = self.client.get(urlhelpers.we_invite_list_url())

#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_retrieve_organization_invitation(self):
#         """Test for retrieve organization invitation"""

#         self.client.force_authenticate(self.user)

#         post_response = self.client.post(
#             accountio_urlhelpers.organization_invitation_create_url(
#                 self.new_organization_slug
#             ),
#             payloads.organization_invitation_paylaod(),
#         )
#         self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

#         self.client.force_authenticate(self.another_user)

#         get_response = self.client.get(urlhelpers.we_invite_list_url())
#         token = get_response.data["results"][0]["token"]

#         response = self.client.get(urlhelpers.we_invite_detail_url(token))

#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_update_organization_invitation(self):
#         """Test for update organization invitation"""

#         self.client.force_authenticate(self.user)

#         post_response = self.client.post(
#             accountio_urlhelpers.organization_invitation_create_url(
#                 self.new_organization_slug
#             ),
#             payloads.organization_invitation_paylaod(),
#         )
#         self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

#         self.client.force_authenticate(self.another_user)

#         get_response = self.client.get(urlhelpers.we_invite_list_url())
#         token = get_response.data["results"][0]["token"]

#         payload = {
#             "response": OrganizationInviteResponse.ACCEPTED,
#         }

#         response = self.client.patch(urlhelpers.we_invite_detail_url(token), payload)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["response"], payload["response"])
