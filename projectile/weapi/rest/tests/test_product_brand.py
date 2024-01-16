from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateOrganizationProductBrandAPIViewTests(BaseAPITestCase):
    def setUp(self):
        super(PrivateOrganizationProductBrandAPIViewTests, self).setUp()

        self.product_brand = self.client.post(
            urlhelpers.user_organization_product_brand_url(),
            payloads.product_brand_payload(),
        )
        # Assert that the status code is correct
        self.assertEqual(self.product_brand.status_code, status.HTTP_201_CREATED)

    def test_create_organization_product_brand_api(self):
        # Test creating product brand for private organization

        response = self.product_brand

        # Assert that the status code is correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Assert that the return data is correct
        self.assertEqual(
            response.data["title"], payloads.product_brand_payload()["title"]
        )

    def test_organization_product_brand_list_api(self):
        # Test product brand list api for private organization

        response = self.client.get(urlhelpers.user_organization_product_brand_url())

        # Assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_organization_product_brand_api(self):
        # Test retrieving organization product brand list api

        response = self.client.get(
            urlhelpers.user_organization_product_brand_detail_url(
                self.product_brand.data["uid"]
            )
        )

        # Assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the return data is correct
        self.assertEqual(
            self.product_brand.data["title"],
            response.data["title"],
        )

    def test_patch_organization_product_brand(self):
        # Test patch organization product brand

        update_payload = {"title": "Aarong"}

        response = self.client.patch(
            urlhelpers.user_organization_product_brand_detail_url(
                self.product_brand.data["uid"]
            ),
            update_payload,
        )

        # Assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the return data is correct
        self.assertEqual(response.data["title"], update_payload["title"])

    def tests_delete_organization_product_brand(self):
        # Test delete logged in user organization product brand

        url = urlhelpers.user_organization_product_brand_detail_url(
            self.product_brand.data["uid"]
        )

        response = self.client.delete(url)

        # Assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_brand_delete_with_product(self):
        # Test deleting brand which is connected to any products

        product_response = self.client.post(
            urlhelpers.we_product_list_url(),
            payloads.product_payload_with_brand(self.product_brand.data["uid"]),
        )

        # Assert that the response status code is correct
        self.assertEqual(product_response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(
            urlhelpers.user_organization_product_brand_detail_url(
                self.product_brand.data["uid"]
            )
        )
        # Assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
