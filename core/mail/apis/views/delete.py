from mail.models import Mail
from rest_framework.generics import DestroyAPIView
from globals.permissions import IsMailReciver
from globals.cache import CacheView

class DeleteMailAPI (
    CacheView,
    DestroyAPIView
) : 

    permission_classes = IsMailReciver
    cache_model = Mail
    lookup_field = 'id'
    
    def get_cache_key(self) :
        return f"{self.request.user}_mails"

    def perform_destroy(self, instance):
        instance.soft_delete()