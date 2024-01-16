import tempfile
from PIL import Image

from rest_framework import status

from accountio.choices import OrganizationStatus

from common.base_test import BaseAPITestCase

from weapi.rest.tests import payloads as we_payloads
from weapi.rest.tests import urlhelpers as we_urlhelpers

from . import urlhelpers



class PublicOrganizationProductApiTest(BaseAPITestCase):
    def setUp(self):
        super(PublicOrganizationProductApiTest, self).setUp()

        # getting user organization list
        self.organization = self.client.get(urlhelpers.me_organization_list_url())

        # get organization slug
        self.organization_slug = self.organization.data["results"][0]["organization"]["slug"]

        organization_update_payload = {
            "status": OrganizationStatus.ACTIVE,
            "kind" : "SUPPLIER"
        }
        organization_update = self.client.patch(urlhelpers.we_detail_url(), organization_update_payload)
        # create product with we_api
        self.organization_product = self.client.post(
            we_urlhelpers.we_product_list_url(), we_payloads.product_payload()
        )

    def test_get_product_organization(self):
        # response product
        response = self.client.get(urlhelpers.org_product_url(self.organization_slug))

        # assert that the returned data are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["slug"], self.organization_product.data["slug"])

    def test_retrieve_organization_product(self):
        # response product post
        response = self.client.get(
            urlhelpers.org_product_detail_url(
                self.organization_slug, self.organization_product.data["slug"]
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["title"], self.organization_product.data["title"]
        )


class PublicOrganizationProductImageApiTest(BaseAPITestCase):
    def setUp(self):
        super(PublicOrganizationProductImageApiTest, self).setUp()

        # getting user organization list
        self.organization = self.client.get(urlhelpers.me_organization_list_url())

        # organization_slug create
        self.organization_slug = self.organization.data["results"][0]["organization"][
            "slug"
        ]

        # create product with we_api
        self.organization_product = self.client.post(
            we_urlhelpers.we_product_list_url(), we_payloads.product_payload()
        )

    def test_get_organizations_product_images(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)

            payload = we_payloads.media_image_payload(image_file)

            post_response = self.client.post(
                we_urlhelpers.we_product_image_list_url(
                    self.organization_product.data["uid"]
                ),
                payload,
                type="multipart",
            )
            self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

            # response product
            response = self.client.get(
                urlhelpers.organization_product_image_list(
                    self.organization_slug, self.organization_product.data["slug"]
                )
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # assert that the returned data is correct
            self.assertEqual(response.data["count"], 1)
