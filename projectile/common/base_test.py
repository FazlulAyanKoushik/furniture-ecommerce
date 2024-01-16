from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from weapi.rest.tests import urlhelpers, payloads


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@example.com", "new1234password"
        )

        # onboarding new organization
        self.onboarding_response = self.client.post(
            urlhelpers.organization_onboarding_url(),
            payloads.organization_onboard_payload(),
        )

        self.assertEqual(self.onboarding_response.status_code, status.HTTP_201_CREATED)

        # authenticating initiator as auth user
        self.auth_user = get_user_model().objects.get(
            email=payloads.organization_onboard_payload()["email"]
        )

        self.client.force_authenticate(self.auth_user)

    def tearDown(self):
        self.client.logout()
