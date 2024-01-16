from rest_framework import status

from catalogio.choices import ServiceStatus

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateServicesApiTests(BaseAPITestCase):
    def setUp(self):
        super(PrivateServicesApiTests, self).setUp()

        # Creating services
        self.service_one = self.client.post(
            urlhelpers.we_services_list_url(), payloads.service_payload()
        )
        self.service_two = self.client.post(
            urlhelpers.we_services_list_url(), payloads.service_payload_two()
        )

    def test_create_service(self):
        response = self.service_one

        # Assert that the status code are correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], payloads.service_payload()["name"])

    def test_service_list(self):
        # instance create calling
        self.service_one
        self.service_two

        response = self.client.get(urlhelpers.we_services_list_url())

        # Assert that the status code are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_retrieve_service(self):
        service_response = self.service_one

        response = self.client.get(
            urlhelpers.services_detail_url(service_response.data["uid"])
        )

        # Assert that the status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_service(self):
        service_response = self.service_one
        payload = {
            "name": "Test Service2",
            "description": "Test Service Description",
            "status": ServiceStatus.ACTIVE,
        }
        response = self.client.patch(
            urlhelpers.services_detail_url(service_response.data["uid"]), payload
        )

        # Assert that the status code are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], payload["name"])

    def test_delete_service(self):
        service_response = self.service_one
        response = self.client.delete(
            urlhelpers.services_detail_url(service_response.data["uid"])
        )

        # Assert that the status code is correct
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
