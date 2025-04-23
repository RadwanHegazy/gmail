from ast import List
from mail.models import Mail
from rest_framework import serializers
from dj_notification.notify import send_notification
from .get import ListMailSerializer
class CreateMailSerializer ( serializers.ModelSerializer ) : 
    body = serializers.CharField()

    class Meta:
        model = Mail
        fields = [
            'reciver',
            'body',
            'header'
        ]

    def validate(self, attrs):
        request = attrs.get('request')
        
        if attrs['reciver'] == request.user :
            raise serializers.ValidationError({
                'message' : "Can't sent messages to your self"
            })

        attrs['sender'] = request.user
        return attrs
    
    def save(self, **kwargs):
        data = self.validated_data
        real_time_data = data.copy()
        body = data.pop('body')
        model = Mail.objects.create(**data)
        model.set_body(body)
        model.save()

        serializer = ListMailSerializer(real_time_data)
        send_notification(
            to_user_id=real_time_data.get('reciver'),
            **serializer.data
        )
        return model

    def to_representation(self, instance):
        return {}