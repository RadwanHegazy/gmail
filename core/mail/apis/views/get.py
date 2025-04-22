from rest_framework.generics import ListAPIView
from globals.cache import CacheView
from mail.apis.serializers import ListMailSerializer
from mail.models import Mail, MAIL_STATUS
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

class BaseListView (
    CacheView,
    ListAPIView
) : 

    """
        Base class for manage the email endpoints.
    """

    serializer_class = ListMailSerializer
    permission_classes = [IsAuthenticated]

    def get_cache_key(self):
        return f"{self.request.user.id}_mails"
    
    def get_cache_value(self):
        user = self.request.user
        return Mail.objects.filter(
            Q(sender=user) | 
            Q(reciver=user),
        )

class ListInboxAPI (
    BaseListView
) :  
    """
    Endpoint for get the list of the incoming and safe emails.
    """
    def get_cache_value(self):
        return Mail.objects.filter(
            status = MAIL_STATUS.okay
        )



class ListSentAPI (
    BaseListView
) : 
    """
    Endpoint for get list of the user sent emails.
    """

    def get_queryset(self):
        return super().get_queryset().filter(
            sender = self.request.user
        )

class ListSpamAPI (
    BaseListView
) : 
    """
    Endpoint for get list of spammed emails.
    """

    def get_queryset(self):
        return super().get_queryset().filter(
            reciver = self.request.user,
            status = MAIL_STATUS.spammed
        )

class ListDeleteAPI (
    BaseListView
) : 
    """
    Endpoint for get list of deleted emails.
    """
    
    def get_queryset(self):
        return super().get_queryset().filter(
            reciver = self.request.user,
            status = MAIL_STATUS.deleted
        )



class ListStarAPI (
    BaseListView
) : 
    """
    Endpoint for get list of starred emails.
    """

    def get_queryset(self):
        return super().get_queryset().filter(
            reciver = self.request.user,
            status = MAIL_STATUS.starred
        )
        

