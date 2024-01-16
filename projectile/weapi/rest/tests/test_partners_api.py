from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateOrganizationPartnerApiTest(BaseAPITestCase):
    def setUp(self):
        super(PrivateOrganizationPartnerApiTest, self).setUp()

        # Create partners
        with open(payloads.generate_test_xlsx_file().name, "rb") as f:
            self.bulk_partners_response = self.client.post(
                urlhelpers.we_partners_bulk_create_url(),
                {"partner_list": f},
                format="multipart",
            )

            # Assert that the response is correct
            self.assertEqual(
                self.bulk_partners_response.status_code, status.HTTP_201_CREATED
            )

        self.partner_response = self.client.post(
            urlhelpers.we_partners_list_url(), payloads.partners_payload()
        )
        # Assert that the response status code is correct
        self.assertEqual(self.partner_response.status_code, status.HTTP_201_CREATED)

        self.partner_list_response = self.client.get(urlhelpers.we_partners_list_url())

    def test_create_organization_partner(self):
        # Test creating organization partners

        response = self.partner_response

        # Assert that the response status code are correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], payloads.partners_payload()["email"])

    def test_organization_partner_list(self):
        # Test organization partner list

        # Send a GET request for organization partner list
        response = self.partner_list_response

        # Assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_organization_partner(self):
        # Test retrieve organization partner

        # Send a GET request to the ListCreateAPIView
        response = self.client.get(
            urlhelpers.we_partners_detail_url(
                self.partner_list_response.data["results"][0]["uid"]
            )
        )
        # Assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the returned data is correct
        self.assertEqual(
            response.data["name"],
            response.data["name"],
        )

    def test_get_organization_partner_user(self):
        # Test get organization partner user list api

        response = self.client.get(
            urlhelpers.partner_user_list_url(
                self.partner_list_response.data["results"][0]["uid"]
            )
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_delete_organization_partner(self):
        # Test delete organization partner

        # Get the details url
        url = urlhelpers.we_partners_detail_url(
            self.partner_list_response.data["results"][0]["uid"]
        )

        # Send a DELETE request to the RetrieveDestroyAPIView
        response = self.client.delete(url)
        # Assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
