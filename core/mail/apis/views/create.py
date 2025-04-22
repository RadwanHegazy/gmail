from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from mail.apis.serializers import CreateMailSerializer

class CreateMailAPI (CreateAPIView) : 
    permission_classes = [IsAuthenticated]
    serializer_class = CreateMailSerializer
    