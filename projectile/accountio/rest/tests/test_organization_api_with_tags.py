from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from weapi.rest.tests import urlhelpers, payloads


class OnboardingOrganizatinoWithTagsAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "tags@example.com", "tags1234password"
        )
        # authenticating staff as logged in user
        self.client.force_authenticate(self.user)

        # create tag using Post view
        self.client.post(urlhelpers.tag_url_list(), payloads.tag_payload())
        self.client.post(urlhelpers.tag_url_list(), payloads.tag_payload())

        self.tag_uid_list = []

        tag_list = self.client.get(urlhelpers.tag_url_list())
        self.assertEqual(tag_list.status_code, status.HTTP_200_OK)
        self.assertEqual(tag_list.data["count"], 2)

        # storing tags(uid) in a list
        self.tag_uid_list = [tag["uid"] for tag in tag_list.data["results"]]

    def test_create_onboarding_organization(self):

        onboarding_response = self.client.post(
            urlhelpers.organization_onboarding_url(),
            payloads.organization_onboard_with_tags_payload(tags=self.tag_uid_list[0]),
        )
        self.assertEqual(onboarding_response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(onboarding_response.data)

    def test_list_onboarding_organization(self):

        onboarding_response = self.client.post(
            urlhelpers.organization_onboarding_url(),
            payloads.organization_onboard_with_tags_payload(tags=self.tag_uid_list[0]),
        )
        self.assertEqual(onboarding_response.status_code, status.HTTP_201_CREATED)

        # authenticating initiator as auth user
        auth_user = get_user_model().objects.get(
            email=payloads.organization_onboard_with_tags_payload(
                tags=self.tag_uid_list[0]
            )["email"]
        )
        self.client.force_authenticate(auth_user)

        # getting user organization list
        organization = self.client.get(urlhelpers.we_url())
        self.assertEqual(organization.status_code, status.HTTP_200_OK)

        self.assertEqual(
            organization.data["tags"][0]["uid"],
            payloads.organization_onboard_with_tags_payload(tags=self.tag_uid_list[0])[
                "tag_uids"
            ],
        )
