from rest_framework.generics import UpdateAPIView
from globals.permissions import IsMailReciver
from mail.apis.serializers import ReadMailSerializer, StarMailSerializer
from globals.cache import CacheView
from mail.models import Mail

class BaseUpdateView (
    CacheView,
    UpdateAPIView
) : 

    permission_classes = [IsMailReciver]
    serializer_class = None
    
    def get_cache_key(self) :
        return f"{self.request.user.id}_mails"

    def get_cache_value(self):
        return Mail.objects.filter(reciver=self.request.user)        

class EmailStarAPI (BaseUpdateView) : 
    serializer_class = StarMailSerializer

class EmailReadAPI(BaseUpdateView) : 
    serializer_class = ReadMailSerializer