from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateOrganizationProductTest(BaseAPITestCase):
    """Test case for creating products with tags"""

    def setUp(self):
        super(PrivateOrganizationProductTest, self).setUp()

        # Create service(after creating the service, a tag will be created automatically)
        self.client.post(urlhelpers.we_services_list_url(), payloads.service_payload())

        self.tag_uid_list = []

        # Get tag list
        tag_list = self.client.get(urlhelpers.we_services_list_url())

       # Assert that the response are correct
        self.assertEqual(tag_list.status_code, status.HTTP_200_OK)
        self.assertEqual(tag_list.data["count"], 1)

        # storing tags(uid) in a list
        self.tag_uid_list = [tag["uid"] for tag in tag_list.data["results"]]

    def test_product_create_with_tags(self):
        """ "Test Creating product with single tag"""

        product_response = self.client.post(
            urlhelpers.we_product_list_url(),
            # sending list of tag uids
            payloads.product_payload_with_tags(tags=self.tag_uid_list[0]),
        )

        # Assert that the response are correct
        self.assertEqual(product_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(product_response.data["tags"][0]["uid"], self.tag_uid_list[0])

    def test_retrieve_product_list_with_tags_list(self):
        """Testing retrieving single product with list of tags in it"""

        product_response = self.client.post(
            urlhelpers.we_product_list_url(),
            # sending list of tag uids
            payloads.product_payload_with_tags(tags=self.tag_uid_list),
        )

        # Assert that the response is correct
        self.assertEqual(product_response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(urlhelpers.we_product_list_url())

        # Assert that the response is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # checking if tags under product are in the tags list
        for tag in product_response.data["tags"]:
            self.assertIn(tag["uid"], self.tag_uid_list)

    def test_update_product_tag_list(self):
        """Test updating tag list under a product"""

        product_response = self.client.post(
            urlhelpers.we_product_list_url(),
            # sending list of tag uids
            payloads.product_payload_with_tags(tags=self.tag_uid_list),
        )

        # Assert that the response are correct
        self.assertEqual(product_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(product_response.data["tags"]), 1)

        response = self.client.patch(
            urlhelpers.we_product_detail_url(product_response.data["uid"]),
            payloads.product_payload_with_tags(tags=self.tag_uid_list[0]),
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["tags"]), 1)

    def test_remove_tags_from_product(self):
        """Test updating tag list under a product"""

        product_response = self.client.post(
            urlhelpers.we_product_list_url(),
            # sending list of tag uids
            payloads.product_payload_with_tags(tags=self.tag_uid_list),
        )

        # Assert that the response are correct
        self.assertEqual(product_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(product_response.data["tags"]), 1)

        payload = {"title": "Space X6-03", "tag_uids": []}
        response = self.client.patch(
            urlhelpers.we_product_detail_url(product_response.data["uid"]), payload
        )

        # Assert that the response is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_without_tags(self):
        """Test updating a product without changing tags"""

        product_response = self.client.post(
            urlhelpers.we_product_list_url(),
            # sending list of tag uids
            payloads.product_payload_with_tags(tags=self.tag_uid_list),
        )

        # Assert that the response are correct
        self.assertEqual(product_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(product_response.data["tags"]), 1)

        payload = {"title": "update"}
        response = self.client.patch(
            urlhelpers.we_product_detail_url(product_response.data["uid"]), payload
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], payload["title"])
        self.assertEqual(len(response.data["tags"]), 1)

    def test_delete_product_with_tags_in_it(self):
        """Test deleting products with tags"""

        product_response = self.client.post(
            urlhelpers.we_product_list_url(),
            # sending list of tag uids
            payloads.product_payload_with_tags(tags=self.tag_uid_list),
        )

        # Assert that the response are correct
        self.assertEqual(product_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(product_response.data["tags"]), 1)

        response = self.client.delete(
            urlhelpers.we_product_detail_url(product_response.data["uid"])
        )

        # Assert that the response is correct
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_tag_update_with_endpoint(self):
        """Test updating tags in product by product tag detail endpoint"""
        product_response = self.client.post(
            urlhelpers.we_product_list_url(),
            # sending list of tag uids
            payloads.product_payload_with_tags(tags=self.tag_uid_list),
        )

        # Assert that the response is correct
        self.assertEqual(product_response.status_code, status.HTTP_201_CREATED)

        response = self.client.patch(
            urlhelpers.product_tag_update_url(
                product_response.data["uid"], self.tag_uid_list[0]
            ),
            {"name": "Updated"},
        )

        # Assert that the response is correct
        self.assertEqual(response.data["name"], "Updated")
