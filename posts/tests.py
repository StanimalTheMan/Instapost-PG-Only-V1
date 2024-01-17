from django.test import TestCase
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Post
from .forms import PhotoForm
from .views import handle_photo_submission, perform_moderation

class PhotoSubmissionTestCase(TestCase):

    @patch('.views.perform_moderation')
    def test_photo_rejected_not_saved(self, mock_perform_moderation):
        # Mock moderation check to simulate rejection
        mock_perform_moderation.return_value = 'rejected'

        # Create a photo form with a dummy image file
        image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        form_data = {'title': 'Test Photo', 'image': image_file}
        form = PhotoForm(data=form_data)

        # Simulate form submission
        response = handle_photo_submission(self.client.post('/submit-photo/', form_data))

        # Assert that the moderation check was called
        mock_perform_moderation.assert_called_once_with(image_file.read())

        # Assert that the photo is not saved to the database
        self.assertEqual(Post.objects.count(), 0)

        # Assert that the user is redirected to an error page (you can customize this based on your actual implementation)
        self.assertEqual(response.status_code, 200)  # Adjust the status code as needed
        self.assertContains(response, 'Inappropriate content detected')
