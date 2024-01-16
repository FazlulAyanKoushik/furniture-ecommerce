from rest_framework import status

from common.base_test import BaseAPITestCase

from . import urlhelpers, payloads


class PrivateOrganizationUserWeApiTest(BaseAPITestCase):
    """Test we user api"""

    def setUp(self):
        super(PrivateOrganizationUserWeApiTest, self).setUp()

    def test_create_organiczation_user(self):
        """Test create private organization user"""

        post_response = self.client.post(
            urlhelpers.we_user_list_url(),
            payloads.add_organization_user_payload()
        )

        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

