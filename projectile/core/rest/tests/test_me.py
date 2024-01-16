import logging

from django.contrib.auth import get_user_model

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from common.base_test import BaseAPITestCase

from ...choices import UserStatus
from . import payloads, urlhelpers

logger = logging.getLogger(__name__)


class PrivateMeUserApiTest(BaseAPITestCase):
    def setUp(self):
        super(PrivateMeUserApiTest, self).setUp()

    def test_retrieve_me(self):
        """Test for retrieving me detail"""

        response = self.client.get(urlhelpers.me_detail_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_me(self):
        """Test for updating me"""

        payload = {
            "summary": "Summary update",
        }

        response = self.client.patch(urlhelpers.me_detail_url(), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["summary"], payload["summary"])

    def test_update_password(self):
        """Test for updating password"""

        payload = {
            "old_password": "pass123word",
            "password": "update1234password",
            "confirm_password": "update1234password",
        }

        response = self.client.patch(urlhelpers.me_password_url(), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_me_status(self):
        """Test for updating me status"""

        payload = {
            "old_password": "new1234password",
            "password": "update1234password",
            "confirm_password": "update1234password",
            "status": "PAUSE",
        }

        response = self.client.patch(urlhelpers.me_status_url(), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PrivateMeUserEmailApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@example.com", "new1234password"
        )

        self.client.force_authenticate(self.user)

        self.post_response = self.client.post(
            urlhelpers.me_user_email_list_url(), payloads.me_user_email_payload()
        )
        self.assertEqual(self.post_response.status_code, status.HTTP_201_CREATED)

        self.post_response_uid = self.post_response.data["uid"]

    def test_create_me_user_email(self):
        """Test for creating me user email"""

        response = self.post_response

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["email"], payloads.me_user_email_payload()["email"]
        )

    def test_get_me_user_email(self):
        """Test for get me user email list"""

        response = self.client.get(urlhelpers.me_user_email_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_me_user_email(self):
        """Test for retrieving me user email detail"""

        response = self.client.get(
            urlhelpers.me_user_email_list_detail(self.post_response_uid)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uid"], self.post_response_uid)

    def test_update_me_user_email(self):
        """Test for updating me user email"""

        payload = {"status": UserStatus.ACTIVE}

        response = self.client.patch(
            urlhelpers.me_user_email_list_detail(self.post_response_uid), payload
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], payload["status"])

    def test_delete_me_user_email(self):
        """Test for deleting me user email"""

        response = self.client.delete(
            urlhelpers.me_user_email_list_detail(self.post_response_uid)
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PrivateMeOrganizationApiTest(BaseAPITestCase):
    """Test we user api"""

    def setUp(self):
        super(PrivateMeOrganizationApiTest, self).setUp()

    def test_retrieve_me_organization_list(self):
        """Test retrieving organization list in which logged-in user belongs"""

        response = self.client.get(urlhelpers.me_organization_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_setting_default_to_an_organization(self):
        """Test set_default to an organization"""

        organization_list_response = self.client.get(
            urlhelpers.me_organization_list_url()
        )

        self.assertEqual(organization_list_response.status_code, status.HTTP_200_OK)

        organization_uid = organization_list_response.data["results"][0]["uid"]

        # updating an organization as is_default is false
        response = self.client.patch(
            urlhelpers.me_organization_select_url(organization_uid)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
