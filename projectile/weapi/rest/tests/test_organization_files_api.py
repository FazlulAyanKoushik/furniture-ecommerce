from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateOrganizationFileTest(BaseAPITestCase):
    """Test case for Organization file endpoints"""

    def setUp(self):
        # Inherit from base setUp method
        super(PrivateOrganizationFileTest, self).setUp()

        # Create new product instance
        self.product_response = self.client.post(
            urlhelpers.we_product_list_url(), payloads.product_payload()
        )
        # Assert that the response is correct
        self.assertEqual(self.product_response.status_code, status.HTTP_201_CREATED)

        # File item payload
        payload = payloads.file_item_payload(payloads.generate_test_doc_file())

        # Create new file item instance
        self.file_response = self.client.post(
            urlhelpers.product_file_list_url(self.product_response.data["uid"]),
            payload,
            type="multipart",
        )
        # Assert that the response is correct
        self.assertEqual(self.file_response.status_code, status.HTTP_201_CREATED)

    def test_organization_file_list(self):
        # Test organization file list api

        response = self.client.get(urlhelpers.we_file_list_url())

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_organization_file_detail(self):
        # Test organization file detail api

        response = self.client.get(
            urlhelpers.we_file_detail_url(self.file_response.data["uid"])
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("docx", response.data["dotextension"])

    def test_update_organization_file(self):
        # Test organization file update api

        payload = {"name": "Test name updated"}
        response = self.client.patch(
            urlhelpers.we_file_detail_url(self.file_response.data["uid"]), payload
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(payload["name"], response.data["name"])

    def test_delete_organization_file(self):
        # Test organization file delete api

        response = self.client.delete(
            urlhelpers.we_file_detail_url(self.file_response.data["uid"])
        )

        # Assert that the response is correct
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
