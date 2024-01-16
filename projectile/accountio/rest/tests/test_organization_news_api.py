from rest_framework import status

from weapi.rest.tests import payloads, urlhelpers as we_urlhelpers

from common.base_test import BaseAPITestCase

from . import urlhelpers


class PrivateOrganizationNewsApiTests(BaseAPITestCase):
    """Tests for specific organization news"""

    # override setUp method
    def setUp(self):
        # inherit from base setUp method
        super(PrivateOrganizationNewsApiTests, self).setUp()

        # getting user organization list
        self.organization = self.client.get(urlhelpers.me_organization_list_url())
        self.organization_slug = self.organization.data["results"][0]["organization"][
            "slug"
        ]

        # create new organization
        self.organization_news = self.client.post(
            we_urlhelpers.news_list_url(), payloads.news_payload()
        )
        self.assertEqual(self.organization_news.status_code, status.HTTP_201_CREATED)

    def test_retrieve_news(self):
        """Test retrieve news of a specific organization"""

        # retrieving news list with organization slug
        response = self.client.get(
            urlhelpers.organization_news_url(self.organization_slug)
        )

        # check rest response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.organization_news.data["title"], response.data["results"][0]["title"]
        )

    def test_get_single_news(self):
        """Test getting a single news from organization"""

        # retrieving single news from detail view
        response = self.client.get(
            urlhelpers.organization_news_detail_url(
                self.organization_slug, self.organization_news.data["slug"]
            )
        )

        # checking rest response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.organization_news.data["title"])
