from rest_framework.generics import CreateAPIView
from users.apis.serializers import RegisterSerializer

class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    
