from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from users.apis.serializers import ProfileSerializer


class ProfileAPIView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
