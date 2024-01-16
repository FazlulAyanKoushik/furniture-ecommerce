import tempfile

from PIL import Image

from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateProjectFileTest(BaseAPITestCase):
    """Test case for Project file endpoints"""

    def setUp(self):
        super(PrivateProjectFileTest, self).setUp()

        # Send a POST request to the ListCreateAPIView with the data for a new project instance
        self.project_create_response = self.client.post(
            urlhelpers.project_list_url(), payloads.project_payload()
        )
        self.assertEqual(
            self.project_create_response.status_code, status.HTTP_201_CREATED
        )

        # File item payload
        self.payload = payloads.file_item_payload(payloads.generate_test_doc_file())

        # Send a POST request to the ListCreateAPIView with the data for a new project file item  instance
        self.project_file_response = self.client.post(
            urlhelpers.project_file_list_url(self.project_create_response.data["uid"]),
            self.payload,
            type="multipart",
        )
        self.assertEqual(
            self.project_create_response.status_code, status.HTTP_201_CREATED
        )

    def test_project_file_create(self):
        # Test projectile file create api

        response = self.project_file_response

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], self.payload["status"])

    def test_project_list(self):
        # Test project file list api

        get_response = self.client.get(
            urlhelpers.project_file_list_url(self.project_create_response.data["uid"])
        )

        # Assert that the response are correct
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data["count"], 1)

    def test_project_file_detail(self):
        # Test project file detail api

        response = self.client.get(
            urlhelpers.project_file_detail_url(
                self.project_create_response.data["uid"],
                self.project_file_response.data["uid"],
            )
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.project_file_response.data["name"])

    def test_project_file_update(self):
        # Test project file update api

        # Payload for update
        update_payload = {"description": "Update Description"}

        response = self.client.patch(
            urlhelpers.project_file_detail_url(
                self.project_create_response.data["uid"],
                self.project_file_response.data["uid"],
            ),
            update_payload,
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], update_payload["description"])

    def test_project_file_delete(self):
        # Test project file delete api

        response = self.client.delete(
            urlhelpers.project_file_detail_url(
                self.project_create_response.data["uid"],
                self.project_file_response.data["uid"],
            )
        )

        # Assert that the response is correct
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_file_size_extension_dotextension_autofigured(self):
        # Test file name, size, extension, and dotextension categorized automatically

        # Assert that the response are correct
        self.assertEqual(self.project_file_response.data["name"], "test drive")
        self.assertIsNotNone(self.project_file_response.data["size"])
        self.assertEqual(self.project_file_response.data["extension"], "Word")
        self.assertIn("docx", self.project_file_response.data["dotextension"])

    def test_file_extension_other(self):
        # Test if file extension is other

        # Create temporary image file
        with tempfile.NamedTemporaryFile(suffix=".bmp") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="BMP")
            image_file.seek(0)

            # Media image payload
            payload = payloads.file_item_payload(image_file)

            # Send a POST request to the ListCreateAPIView with the data for a new project file item  instance
            project_file = self.client.post(
                urlhelpers.project_file_list_url(
                    self.project_create_response.data["uid"]
                ),
                payload,
                type="multipart",
            )

            # Assert that the response are correct
            self.assertEqual(project_file.status_code, status.HTTP_201_CREATED)
            self.assertEqual(project_file.data["extension"], "Others")
