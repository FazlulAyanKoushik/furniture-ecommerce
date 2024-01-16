from rest_framework import status

from common.base_test import BaseAPITestCase

from . import urlhelpers, payloads


class PrivateProjectApiTests(BaseAPITestCase):
    """Test case for weapi projects participants"""

    def setUp(self):
        super(PrivateProjectApiTests, self).setUp()

        self.new_add_participant = self.client.post(
            urlhelpers.news_list_url(), payloads.news_payload()
        )
        self.assertEqual(self.new_add_participant.status_code, status.HTTP_201_CREATED)

        self.project = self.client.post(
            urlhelpers.project_list_url(), payloads.project_payload()
        )
        self.assertEqual(self.project.status_code, status.HTTP_201_CREATED)

        self.post_response = self.client.post(
            urlhelpers.participants_list_url(self.project.data["uid"]),
            payloads.project_participants_payload(self.user.uid),
        )
        self.assertEqual(self.post_response.status_code, status.HTTP_201_CREATED)

    def test_create_project_participant(self):
        """Test for creating project participants"""

        response = self.post_response

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_participants_list(self):
        """Test for getting project participants list"""

        response = self.client.get(
            urlhelpers.participants_list_url(self.project.data["uid"])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_participant(self):
        """Test for retrieving project participant"""

        response = self.client.get(
            urlhelpers.participants_detail_url(
                self.project.data["uid"], self.post_response.data["uid"]
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role"], self.post_response.data["role"])

    def test_update_participant(self):
        """Test for updating project participant"""

        payload = {"role": "updated"}

        response = self.client.patch(
            urlhelpers.participants_detail_url(
                self.project.data["uid"], self.post_response.data["uid"]
            ),
            payload,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role"], payload["role"])

    def test_delete_participant(self):
        """Test for deleting project participant"""

        response = self.client.delete(
            urlhelpers.participants_detail_url(
                self.project.data["uid"], self.post_response.data["uid"]
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
