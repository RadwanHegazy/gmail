from rest_framework import serializers
from users.models import User


class SpamUserSerializer (serializers.Serializer) : 
    spam_user_id = serializers.UUIDField()

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user

        spam_user_id = attrs.get('spam_user_id')
        spammed_user = User.objects.filter(id=spam_user_id).exclude(id=user.id)

        if not spammed_user.exists():
            raise serializers.ValidationError({
                'message' : 'invalid spam_user_id'
            })

        attrs['spammed_user'] = spammed_user.first()
        attrs['user'] = user
        return attrs

    
    def save(self, **kwargs):
        spammed_user : User = self.validated_data.get('spammed_user')
        user : User = self.validated_data.get('user')

        spammed_user.spam.spammed_by.add(user)
        spammed_user.save()



    def to_representation(self, instance):
        return {}