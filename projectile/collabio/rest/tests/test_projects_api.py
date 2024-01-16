from rest_framework import status

from common.base_test import BaseAPITestCase

from ..tests import payloads, urlhelpers

class GlobalProjectApiTests(BaseAPITestCase):

    def setUp(self):
        super(GlobalProjectApiTests, self).setUp()

        # send a POST request to the ListCreateAPIView with the data for a new project
        self.post_response = self.client.post(
            urlhelpers.project_list_url(), payloads.project_payload()
        )
        # assert that the response status code is correct
        self.assertEqual(self.post_response.status_code, status.HTTP_201_CREATED)

    def test_project_list(self):
        """Test for getting project list"""

        # send a GET request to the public project ListAPIView
        response = self.client.get(urlhelpers.public_project_list_url())

        # assert that the return data is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["title"], payloads.project_payload()["title"]
        )

    def test_get_single_project(self):
        """Test for retrieving single project"""

        # send a GET request to the public project ListAPIView
        response = self.client.get(
            urlhelpers.public_project_detail_url(self.post_response.data["slug"])
        )
        
        # assert that the returned data is correct
        self.assertEqual(response.data["title"], payloads.project_payload()["title"])
