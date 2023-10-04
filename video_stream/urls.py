from django.urls import path
from .views import VideoCamera, video_feed

urlpatterns = [
    path('video_feed/' ,video_feed, name='video_feed'),
]


