from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from accountio.rest.tests import payloads

from common.base_test import BaseAPITestCase

from weapi.rest.tests import urlhelpers as we_urlhelpers, payloads as we_payloads

from . import urlhelpers


class PublicProductApiTests(APITestCase):
    """Test unauthenticated product API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""

        response = self.client.get(urlhelpers.product_list_url())

        # Assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductApiTest(BaseAPITestCase):
    """Test authenticated product APIs"""

    def setUp(self):
        super(PrivateProductApiTest, self).setUp()

        # Get user organization list
        self.organization = self.client.get(urlhelpers.me_organization_list_url())

        # Get organization slug
        self.organization_slug = self.organization.data["results"][0]["organization"][
            "slug"
        ]

        # Create product for testing
        self.product = self.client.post(
            we_urlhelpers.we_product_list_url(), payloads.product_payload()
        )

        # Get product slug
        self.product_slug = self.product.data["slug"]

        # Create a payload with product UIDs
        self.uid_payload = {"product_uids": [self.product.data["uid"]]}

        # Create collection for testing
        self.collection = self.client.post(
            we_urlhelpers.collection_url(), we_payloads.collection_payload()
        )

    def test_retrieve_products(self):
        """Test for retrieve all products"""

        response = self.client.get(urlhelpers.product_list_url())

        # Assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the return code is correct
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["title"], self.product.data["title"]
        )

    def test_get_product_details(self):
        """Test for get product detail using slug"""

        url = urlhelpers.product_detail_url(self.product_slug)
        response = self.client.get(url)

        # Assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the return data is correct
        self.assertEqual(response.data["title"], self.product.data["title"])

        """Test Product Collections"""

    def test_retrieve_product_collection_list(self):
        """Test for retrieve product collection list"""

        post_response = self.client.post(
            we_urlhelpers.add_product_to_collection_url(self.collection.data["uid"]),
            self.uid_payload,
        )
        # Assert that the response status code is correct
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(urlhelpers.product_collection_list_url())
        # Assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_collection_details(self):
        """Test for get product collection detail using slug"""

        post_response = self.client.post(
            we_urlhelpers.add_product_to_collection_url(self.collection.data["uid"]),
            self.uid_payload,
        )
        # Assert that the response status code is correct
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(
            urlhelpers.product_collection_detail_url(self.collection.data["slug"])
        )

        # Assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the return data is correct
        self.assertEqual(response.data["title"], self.collection.data["title"])

    def test_retrieve_products_list_from_collection(self):
        """Test retrieving products list from a collection"""

        post_response = self.client.post(
            we_urlhelpers.add_product_to_collection_url(self.collection.data["uid"]),
            self.uid_payload,
        )

        # Assert that the response status code is correct
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(
            urlhelpers.collection_product_list_url(self.collection.data["slug"])
        )

        # Assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the return data is correct
        self.assertEqual(response.data["results"][0]["slug"], self.product.data["slug"])
