from rest_framework import status

from common.base_test import BaseAPITestCase

from weapi.rest.tests import urlhelpers as we_urlhelpers, payloads as we_payloads

from . import urlhelpers, payloads


class PublicShowroomApiTest(BaseAPITestCase):
    def setUp(self):
        super(PublicShowroomApiTest, self).setUp()

        # generating a image file
        self.image = we_payloads.generate_test_image()

        with open(self.image, "rb") as self.image_file:
            showroom_response = self.client.post(
                we_urlhelpers.showromm_list_url(),
                payloads.organization_showroom_list_payload(self.image_file),
                type="multipart",
            )
            self.assertEqual(showroom_response.status_code, status.HTTP_201_CREATED)

    def test_showroom_list(self):
        # send a GET request for an individual organization
        organization = self.client.get(urlhelpers.me_organization_list_url())

        response = self.client.get(
            urlhelpers.organization_showroom_list_url(
                organization.data["results"][0]["organization"]["slug"]
            )
        )

        # assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["caption"],
            payloads.organization_showroom_list_payload(self.image_file)["caption"],
        )
