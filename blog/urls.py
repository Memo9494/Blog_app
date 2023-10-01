from django.urls import path
from .views import BlogListView, BlogDetailView

urlpatterns = [
    #Django adds an automatic primary key, ir can be eather pk or id
    path('post/<int:pk>/',BlogDetailView.as_view(),name='post_detail'),
    path('',BlogListView.as_view(),name='home'),
]
