from django.urls import path
from .api_views import UploadProfilePictureView, GetProfilePictureView

urlpatterns = [
    path('upload-profile-picture/', UploadProfilePictureView.as_view(), name='upload-profile-picture'),
    path('profile-picture/', GetProfilePictureView.as_view(), name='get-profile-picture'),
]