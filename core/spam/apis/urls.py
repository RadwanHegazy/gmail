from django.urls import path
from .views import create

urlpatterns = [
    path('create/v1/', create.CreateSpamAPI.as_view(), name='create_spam')
]