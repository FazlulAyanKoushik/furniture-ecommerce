from rest_framework import status

from common.base_test import BaseAPITestCase

from weapi.rest.tests import urlhelpers as we_urlhelpers, payloads

from . import urlhelpers


class GlobalBrandListApiTest(BaseAPITestCase):
    def setUp(self):
        super(GlobalBrandListApiTest, self).setUp()

        self.product_brand = self.client.post(
            we_urlhelpers.user_organization_product_brand_url(),
            payloads.product_brand_payload(),
        )
        # Assert that the status code is correct
        self.assertEqual(self.product_brand.status_code, status.HTTP_201_CREATED)

    def test_get_public_brand_list(self):
        response = self.client.get(urlhelpers.global_brands_list_url())

        # Assert that the status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["title"],
            payloads.product_brand_payload()["title"],
        )
