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
        attrs['attchments'] = request.FILES.getlist('attchments') if request.FILES else []
        return attrs
    
    def save(self, **kwargs):
        from globals.tasks import check_before_send
        check_before_send.delay(**self.validated_data)
        

    def to_representation(self, instance):
        return {}