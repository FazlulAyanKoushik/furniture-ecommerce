from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateProjectFileTest(BaseAPITestCase):
    """Test case for news post file endpoints"""

    def setUp(self):
        super(PrivateProjectFileTest, self).setUp()

        # send a POST request to the ListCreateAPIView with the data for a new project instance
        self.new_post_response = self.client.post(
            urlhelpers.news_list_url(), payloads.news_payload()
        )

        self.assertEqual(self.new_post_response.status_code, status.HTTP_201_CREATED)

        # File item payload
        self.payload = payloads.file_item_payload(payloads.generate_test_doc_file())

        # Send a POST request to the ListCreateAPIView with the data for a new file item  instance
        self.news_file_response = self.client.post(
            urlhelpers.news_post_file_list_url(self.new_post_response.data["uid"]),
            self.payload,
            type="multipart",
        )

    def test_news_post_file_create(self):
        # Test create news post file api

        response = self.news_file_response

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], self.payload["status"])

    def test_news_post_list(self):
        # Test news post list api

        get_response = self.client.get(
            urlhelpers.news_post_file_list_url(self.new_post_response.data["uid"])
        )

        # Assert that the response are correct
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data["count"], 1)

    def test_news_post_file_detail(self):
        # Test news post file detail api

        response = self.client.get(
            urlhelpers.news_post_file_detail_url(
                self.new_post_response.data["uid"], self.news_file_response.data["uid"]
            )
        )
        
        # Assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], self.news_file_response.data["status"])

    def test_news_post_file_delete(self):
        # Test news post file delete api

        response = self.client.delete(
            urlhelpers.news_post_file_detail_url(
                self.new_post_response.data["uid"], self.news_file_response.data["uid"]
            )
        )

        # Assert that the response is correct
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
