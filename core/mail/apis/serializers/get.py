from rest_framework import serializers
from mail.models import Mail, Attachment
from users.apis.serializers import MailUserSerializer

class AttachmentSerializer (
    serializers.ModelSerializer
) : 

    class Meta:
        model = Attachment
        fields = "__all__"

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
    attachments = AttachmentSerializer(many=True)

    class Meta:
        model = Mail
        fields = [
            'id',
            'sender',
            'header',
            'is_read',
            'datetime',
            'get_body',
            'attachments',
        ]