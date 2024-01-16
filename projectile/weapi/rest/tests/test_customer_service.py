from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class CustomerServiceTestCase(BaseAPITestCase):
    def setUp(self):
        # Inherit from base setUp method
        super(CustomerServiceTestCase, self).setUp()

        # Create customer service
        self.post_customer_service = self.client.post(
            urlhelpers.customer_service_list_url(), payloads.customer_service_payload()
        )

        # Get customer service uid
        self.customer_service_uid = self.post_customer_service.data["uid"]

    def test_create_customer_service(self):
        # Test create customer service api

        response = self.post_customer_service

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["name"], payloads.customer_service_payload()["name"]
        )

    def test_get_customer_service(self):
        # Test get customer service api

        response = self.client.get(urlhelpers.customer_service_list_url())

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["status"],
            payloads.customer_service_payload()["status"],
        )

    def test_retrive_customer_service(self):
        # Test retrieve customer service api

        response = self.client.get(
            urlhelpers.customer_service_detail_url(self.customer_service_uid)
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["status"], payloads.customer_service_payload()["status"]
        )

    def test_update_customer_service(self):
        # Test update customer service api

        update_payload = {"name": "Updated Title"}

        response = self.client.patch(
            urlhelpers.customer_service_detail_url(self.customer_service_uid),
            update_payload,
        )

        #Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], update_payload["name"])

    def test_delete_customer_service(self):
        # Test delete customer service api

        response = self.client.delete(
            urlhelpers.customer_service_detail_url(self.customer_service_uid)
        )

        # Assert that the response is correct
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    
