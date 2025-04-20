from rest_framework import serializers
from mail.models import Mail
from users.apis.serializers import MailUserSerializer

class ListMailSerializer (
    serializers.ModelSerializer
) : 

    class Meta:
        model = Mail
        fields = [
            'id',
            'sender_full_name',
            'header',
            'is_read',
            'datetime'
        ]


class RetriveMailSerializer (
    serializers.ModelSerializer
) :
    sender = MailUserSerializer()

    class Meta:
        model = Mail
        fields = [
            'id',
            'sender',
            'header',
            'is_read',
            'datetime',
            'get_body',
        ]