from io import BytesIO
from django.shortcuts import render, redirect
from .forms import PhotoForm
import boto3

from django.conf import settings

# Create your views here.
def handle_photo_submission(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            # Process moderation using AWS Rekognition
            moderation_status = perform_moderation(request.FILES['image'].read())

            # if moderation_status is 'approved'; probably can handle better later, maybe return boolean instead
            if moderation_status == 'approved':
                form.save()
                return redirect('posts/photo-submission-success.html')
            return render(request, 'error.html', {'message': 'Inappropriate content detected'})


    else:
        form = PhotoForm()

    return render(request, 'posts/photo-submission.html', {'form': form})

def perform_moderation(image_data):
    # Use AWS Rekognition to performo moderation
    aws_region = settings.AWS_REGION
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    client = boto3.client('rekognition', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Create a binary stream from image data using BytesIO
    image_stream = BytesIO(image_data)

    moderation_response = client.detect_moderation_labels(
        Image={
            'Bytes': image_stream.read()
        }
    )

    # Process moderation response and return moderation status to store in db
    # print for now, TODO: delete later
    print(moderation_response.get('ModerationLabels'))
    if moderation_response.get('ModerationLabels'):
        return 'rejected'
    return 'approved'

def submission_success(request):
    return render(request, 'posts/photo-submission_success.html')