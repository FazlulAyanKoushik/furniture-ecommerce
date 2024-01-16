from rest_framework import status

from accountio.choices import OrganizationStatus

from common.base_test import BaseAPITestCase


from ..tests import payloads, urlhelpers     

class PublicOrganizationsByProjectTest(BaseAPITestCase):

    def setUp(self):
        super(PublicOrganizationsByProjectTest, self).setUp()

        self.create_project = self.client.post(
            urlhelpers.project_list_url(), payloads.project_payload()
        )
        self.assertEqual(self.create_project.status_code, status.HTTP_201_CREATED) 

        self.update_organization_payload = {
            "status": OrganizationStatus.ACTIVE,
            "kind": "SUPPLIER",
        }
        self.onboarding_response.organization_update = self.client.patch(
            urlhelpers.we_detail_url(), self.update_organization_payload
        )


    def test_get_organizations_by_projects(self):

        response = self.client.get(
            urlhelpers.public_organizations_by_project_url()
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
        
        
