from rest_framework.generics import CreateAPIView
from spam.apis.serializers import SpamUserSerializer
from rest_framework.permissions import IsAuthenticated

class CreateSpamAPI (CreateAPIView) : 
    serializer_class = SpamUserSerializer
    permission_classes = [IsAuthenticated]
