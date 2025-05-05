from mail.models import Mail, User, Attachment
from rest_framework import serializers

class CreateMailSerializer ( serializers.ModelSerializer ) : 
    body = serializers.CharField()
    reciver = serializers.UUIDField()
    class Meta:
        model = Mail
        fields = [
            'reciver',
            'body',
            'header'
        ]

    def validate(self, attrs):
        request = self.context.get('request')
        reciver_id = attrs['reciver']

        reciver = User.objects.filter(id=reciver_id).exclude(id=request.user.id)

        if not reciver.exists() :
            raise serializers.ValidationError({
                'message' : "invalid reciver"
            })
      


        attrs['sender'] = str(request.user.id)
        attrs['reciver'] = str(reciver.first().id)
        attach_list = request.FILES.getlist('attachments') if request.FILES else []
        attrs['attachments'] = [] 

        for attach in attach_list:
            attch_obj = Attachment.objects.create(
                file = attach,
            )
            attrs['attachments'].append(attch_obj.id)

        return attrs
    
    def save(self, **kwargs):
        from globals.tasks import check_before_send
        check_before_send.delay(**self.validated_data)
        

    def to_representation(self, instance):
        return {}