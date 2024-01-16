from rest_framework import status

from common.base_test import BaseAPITestCase

from ..tests import urlhelpers, payloads


class PrivateWeNewsApiTests(BaseAPITestCase):
    """Test case for we newsdesk"""

    def setUp(self):
        super(PrivateWeNewsApiTests, self).setUp()

        self.post_response = self.client.post(
            urlhelpers.news_list_url(), payloads.news_payload()
        )
        self.assertEqual(self.post_response.status_code, status.HTTP_201_CREATED)

        # storing news uid as post_uid
        self.post_uid = self.post_response.data["uid"]

    def test_create_news(self):
        """Test create news under weapi"""

        response = self.post_response

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payloads.news_payload()["title"])

    def test_get_news(self):
        """Test retrieve news from default organization"""

        # retrieving list of news from default organization by REST
        response = self.client.get(urlhelpers.news_list_url())

        # checking REST response for retrieving news list
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retireve_single_news(self):
        """Test retrieve single news by uid"""

        # REST request to getting single item
        response = self.client.get(urlhelpers.news_detail_url(post_uid=self.post_uid))

        # checking response from REST
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["object"]["title"], payloads.news_payload()["title"]
        )

    def test_update_news(self):
        """Test updating news post uid by default view"""

        update_payload = {"title": "Updated"}

        # REST patch request
        response = self.client.patch(
            urlhelpers.news_detail_url(post_uid=self.post_uid), update_payload
        )

        # checking REST patch response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], update_payload["title"])

    def test_delete_news(self):
        """Test deleting news by uid"""

        # REST request to delete
        response = self.client.delete(
            urlhelpers.news_detail_url(post_uid=self.post_uid)
        )

        # checking REST delete response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
