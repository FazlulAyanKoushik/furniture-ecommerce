from rest_framework import status

from common.base_test import BaseAPITestCase

from . import urlhelpers, payloads


class PrivateProjectAPIViewApiTests(BaseAPITestCase):
    """Test case for weapi projects"""

    def setUp(self):
        super(PrivateProjectAPIViewApiTests, self).setUp()

        self.new_post_response = self.client.post(
            urlhelpers.news_list_url(), payloads.news_payload()
        )
        self.assertEqual(self.new_post_response.status_code, status.HTTP_201_CREATED)

        # Creating REST post response
        self.project_create_response = self.client.post(
            urlhelpers.project_list_url(), payloads.project_payload()
        )

        # checking REST post response
        self.assertEqual(
            self.project_create_response.status_code, status.HTTP_201_CREATED
        )

    def test_create_project(self):
        """Test create project response"""

        response = self.project_create_response

        # checking REST post response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payloads.project_payload()["title"])

    def test_retrieve_project_list(self):
        """Test retrieving list of projects"""

        # REST response for retrieving project list
        response = self.client.get(urlhelpers.project_list_url())

        # checking REST get response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["title"], payloads.project_payload()["title"]
        )

    def test_get_single_project(self):
        """Test retrieving single project"""

        # REST request for single project
        response = self.client.get(
            urlhelpers.project_detail_url(self.project_create_response.data["uid"])
        )

        # checking REST retrieve response
        self.assertEqual(response.data["title"], payloads.project_payload()["title"])

    def test_update_project(self):
        """Test update project"""

        # patch payload
        payload = {"title": "Updated"}

        response = self.client.patch(
            urlhelpers.project_detail_url(self.project_create_response.data["uid"]),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], payload["title"])

    def test_project_delete(self):
        """REST response test for deleting project"""

        # REST delete request
        response = self.client.delete(
            urlhelpers.project_detail_url(self.project_create_response.data["uid"])
        )

        # check REST delete response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
