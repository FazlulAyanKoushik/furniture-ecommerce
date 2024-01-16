from rest_framework import status

from common.base_test import BaseAPITestCase

from ..tests import payloads, urlhelpers


class PublicProjectApiTests(BaseAPITestCase):
    def setUp(self):
        super(PublicProjectApiTests, self).setUp()

    def test_project_list(self):
        # send a POST request to the ListCreateAPIView with the data for a new project
        create_project = self.client.post(
            urlhelpers.project_list_url(), payloads.project_payload()
        )
        # assert that the response status code is correct
        self.assertEqual(create_project.status_code, status.HTTP_201_CREATED)

        # organization url
        organization_url = urlhelpers.me_organization_list_url()
        # send a GET request for an individual organization
        response = self.client.get(organization_url)

        # send a GET request to the public project ListAPIView
        response = self.client.get(
            urlhelpers.public_organization_project_list_url(
                response.data["results"][0]["organization"]["slug"]
            )
        )

        # assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # assert that the returned data is correct
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["title"], payloads.project_payload()["title"]
        )

    def test_get_single_project(self):
        # send a POST request to the ListCreateAPIView with the data for a new project
        project_create_response = self.client.post(
            urlhelpers.project_list_url(), payloads.project_payload()
        )
        # assert that the response status code is correct
        self.assertEqual(project_create_response.status_code, status.HTTP_201_CREATED)

        # organization url
        organization_url = urlhelpers.me_organization_list_url()
        # send a GET request for an individual organization
        response = self.client.get(organization_url)

        # send a GET request to the public project ListAPIView
        response = self.client.get(
            urlhelpers.public_organization_project_retrieve_url(
                response.data["results"][0]["organization"]["slug"],
                project_create_response.data["slug"],
            )
        )
        # assert that the returned data is correct
        self.assertEqual(response.data["title"], payloads.project_payload()["title"])
