from rest_framework import status

from django.contrib.auth import get_user_model

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateOrganizationInvitationApiTests(BaseAPITestCase):
    # Test for invite organization partner and invitation already exist

    def setUp(self):
        super(PrivateOrganizationInvitationApiTests, self).setUp()

        # get user organization list
        self.organization = self.client.get(urlhelpers.me_organization_list_url())

        # get organization slug
        self.organization_slug = self.organization.data["results"][0]["organization"][
            "slug"
        ]

        # create another user
        self.another_user = get_user_model().objects.create_user(
            "another_user@example.com", "new1234password"
        )
        # onboarding another organization
        self.onboarding_response_two = self.client.post(
            urlhelpers.organization_onboarding_url(),
            payloads.organization_onboard_payload_two(),
        )

        # authenticating initiator as auth user
        self.new_user = get_user_model().objects.get(
            email=payloads.organization_onboard_payload_two()["email"]
        )
        self.client.force_authenticate(self.new_user)

        # adding another organization staff
        we_user_create_response = self.client.post(
            urlhelpers.we_user_list_url(),
            payloads.user_payload(self.another_user),
        )
        self.assertEqual(we_user_create_response.status_code, status.HTTP_201_CREATED)

        self.new_organization = self.client.get(urlhelpers.me_organization_list_url())
        self.new_organization_slug = self.new_organization.data["results"][0][
            "organization"
        ]["slug"]

        self.assertEqual(
            self.onboarding_response_two.status_code, status.HTTP_201_CREATED
        )

    def test_create_organization_invitation(self):
        # Test for creating organization invitation

        self.client.force_authenticate(self.new_user)

        response = self.client.post(
            urlhelpers.organization_invitation_create_url(self.new_organization_slug),
            payloads.organization_invitation_paylaod(),
        )

        # assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_organization_invitation_already_exist(self):
        # Test that the organization invitation is already exists

        self.client.force_authenticate(self.user)

        response = self.client.post(
            urlhelpers.organization_invitation_create_url(self.new_organization_slug),
            payloads.organization_invitation_paylaod(),
        )

        # assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
