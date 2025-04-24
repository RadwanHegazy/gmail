from rest_framework import serializers
from mail.models import Mail
from users.apis.serializers import MailUserSerializer

class MailSearchSerializer(serializers.ModelSerializer):
    sender = MailUserSerializer()

    class Meta:
        model = Mail
        fields = ['id', 'sender', 'header', 
                 'datetime', 'is_read', 'status']