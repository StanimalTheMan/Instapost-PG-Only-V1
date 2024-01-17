from django.urls import path
from .views import handle_photo_submission, submission_success

urlpatterns = [
    path('submit-photo/', handle_photo_submission, name='submit-photo'),
    path('submission-success/', submission_success, name='photo-submission-success'),
]