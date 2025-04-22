from rest_framework.permissions import IsAuthenticated

class IsMailReciver (IsAuthenticated) : 

    def has_object_permission(self, request, view, obj):
        return request.user == obj.reciver