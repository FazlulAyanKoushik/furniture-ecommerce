from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateOrganizationProductTest(BaseAPITestCase):
    """Test case for creating products from weapi app"""

    def setUp(self):
        super(PrivateOrganizationProductTest, self).setUp()

        # Create a organization collection
        self.post_response = self.client.post(
            urlhelpers.collection_url(), payloads.collection_payload()
        )
        self.assertEqual(self.post_response.status_code, status.HTTP_201_CREATED)

        # Requesting to create a new product
        self.product_response = self.client.post(
            urlhelpers.we_product_list_url(), payloads.product_payload()
        )
        # Creating a payload with list of product UIDs
        self.payload = {"product_uids": [self.product_response.data["uid"]]}

        self.product_collection_response = self.client.post(
            urlhelpers.add_product_to_collection_url(self.post_response.data["uid"]),
            self.payload,
        )

    def test_create_organization_collection(self):
        # Test create organization collection api

        response = self.post_response

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payloads.collection_payload()["title"])

    def test_get_organization_collections(self):
        # Test get organization collection api

        get_response = self.client.get(urlhelpers.collection_url())

        # Assert that the response are correct
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            get_response.data["results"][0]["title"], self.post_response.data["title"]
        )

    def test_organization_collection_detail(self):
        # Test get organization collection detail api

        get_response = self.client.get(
            urlhelpers.collection_detail_url(self.post_response.data["uid"])
        )

        # Assert that the response are correct
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            get_response.data["kind"], payloads.collection_payload()["kind"]
        )

    def test_update_organization_collection(self):
        # Test update organization collection api

        update_payload = {"title": "Title Updated"}

        update_response = self.client.patch(
            urlhelpers.collection_detail_url(self.post_response.data["uid"]),
            update_payload,
        )

        # Assert that the response are correct
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data["title"], update_payload["title"])

    def test_deleting_organization_collection(self):
        # Test delete organization collection api

        delete_response = self.client.delete(
            urlhelpers.collection_detail_url(self.post_response.data["uid"])
        )

        # Assert that the response is correct
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_products_in_collection(self):
        # Test add product list into collection api

        response = self.product_collection_response

        # Assert that the response is correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_products_list_from_collection(self):
        # Test get products list from collection api

        response = self.client.get(
            urlhelpers.add_product_to_collection_url(self.post_response.data["uid"])
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], self.product_response.data["title"])
