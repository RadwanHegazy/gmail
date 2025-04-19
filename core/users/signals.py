from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from spam.models import UserSpam


@receiver(post_save, sender=User)
def create_user_spam(created, instance:User, **kwargs) :
    if not created:
        return 

    instance.spam = UserSpam.objects.create()
    instance.save()

    