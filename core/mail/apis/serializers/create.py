from mail.models import Mail
from rest_framework import serializers

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
        body = data.pop('body')
        model = Mail.objects.create(**data)
        model.set_body(body)
        model.save()
        return model

    def to_representation(self, instance):
        return {}