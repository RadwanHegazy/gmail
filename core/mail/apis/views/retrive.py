
from rest_framework.generics import RetrieveAPIView
from globals.cache import CacheView
from mail.apis.serializers import RetriveMailSerializer
from globals.permissions import IsMailReciver
from mail.models import Mail
from django.db.models import Q

class RetriveMailAPI (
    CacheView,
    RetrieveAPIView
) :

    permission_classes = [IsMailReciver]
    serializer_class = RetriveMailSerializer
    
    def get_cache_key(self) :
        return f'{self.request.user.id}_mails'

    def get_cache_value(self):
        user = self.request.user
        return Mail.objects.filter(
            Q(sender=user) |
            Q(reciver=user)
        )

    def get(self, request, *args, **kwargs):
        model = self.get_object()
        model.is_read = True
        model.save()
        return super().get(request, *args, **kwargs)
