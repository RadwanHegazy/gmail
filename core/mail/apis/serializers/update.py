from mail.models import Mail, MAIL_STATUS
from rest_framework import serializers


class StarMailSerializer (serializers.ModelSerializer) :

    class Meta:
        model = Mail
        fields = [
            'id',
            'status'
        ]
        read_only = ['status']

    def validate(self, attrs):
        attrs['status'] = MAIL_STATUS.starred
        return attrs
class ReadMailSerializer (serializers.ModelSerializer) :

    class Meta:
        model = Mail
        fields = [
            'id',
            'is_read'
        ]
        read_only = ['is_read']

    def validate(self, attrs):
        attrs['is_read'] = True
        return attrs

