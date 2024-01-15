from django.shortcuts import render, redirect
from .forms import PhotoForm
import boto3

from django.conf import settings

# Create your views here.
def handle_photo_submission(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the photo to the db
            photo = form.save()

            # Process moderation using AWS Rekognition
            moderation_status = perform_moderation(photo.image.path)

            # Update the moderation status in the Photo model
            photo.moderation_status = moderation_status
            photo.save()

            return redirect('posts/photo-submission-success.html')
    else:
        form = PhotoForm()

    return render(request, 'posts/photo-submission.html', {'form': form})

def perform_moderation(image_path):
    # Use AWS Rekognition to performo moderation
    aws_region = settings.AWS_REGION
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    client = boto3.client('rekognition', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    with open(image_path, 'rb') as image_file:
        photo_data = image_file.read()

    moderation_response = client.detect_moderation_labels(
        Image={
            'Bytes': photo_data
        }
    )

    # Process moderation response and return moderation status to store in db
    # print for now, TODO: delete later
    print(moderation_response.get('ModerationLabels'))
    if moderation_response.get('ModerationLabels'):
        return 'rejected'
    return 'approved'

# def submission_success(request):
#     return render(request, 'posts/submission_success.html')