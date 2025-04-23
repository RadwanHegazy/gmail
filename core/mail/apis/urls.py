from django.urls import path
from mail.apis.views import (
    get,
    create,
    retrive,
    update,
    delete
)


urlpatterns = [
    path('get/v1/inbox/', get.ListInboxAPI.as_view(), name='inbox'),    
    path('get/v1/star/', get.ListStarAPI.as_view(), name='starred_emails'),    
    path('get/v1/delete/', get.ListDeleteAPI.as_view(), name='deleted_emails'),    
    path('get/v1/spam/', get.ListSpamAPI.as_view(), name='spammed_emails'),
    path('get/v1/sent/', get.ListSentAPI.as_view(), name='sent_emails'),
    path('get/v1/mail/<int:id>/', retrive.RetriveMailAPI.as_view(), name='get_email'),

    path('create/v1/', create.CreateMailAPI.as_view(),name='create_email'),

    path('update/v1/star/', update.EmailStarAPI.as_view(),name='star_mail'),
    path('update/v1/read/', update.EmailReadAPI.as_view(),name='read_mail'),

    path('delete/v1/<int:id>/', delete.DeleteMailAPI.as_view(), name='delete_mail')
]