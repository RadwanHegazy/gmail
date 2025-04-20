from django.urls import path
from mail.apis.views import (
    get
)


urlpatterns = [
    path('get/v1/inbox/', get.ListInboxAPI.as_view(), name='inbox'),    
    path('get/v1/star/', get.ListStarAPI.as_view(), name='starred_emails'),    
    path('get/v1/delete/', get.ListDeleteAPI.as_view(), name='deleted_emails'),    
    path('get/v1/spam/', get.ListSpamAPI.as_view(), name='spammed_emails'),
    path('get/v1/sent/', get.ListSentAPI.as_view(), name='sent_emails'),
]