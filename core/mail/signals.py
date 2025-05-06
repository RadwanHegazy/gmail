from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from mail.models import Mail
from django.dispatch import receiver
from mail.documents import MailDocument
from cryptography.fernet import Fernet


@receiver(post_save, sender=Mail)
def action_after_save(created, instance, **kwargs) : 

    if created:
        instance.hash_key = Fernet.generate_key().decode()
        instance.save()

    cache.delete(f'{instance.sender.id}_mails')
    cache.delete(f'{instance.reciver.id}_mails')

    MailDocument().update(instance)


@receiver(post_delete, sender=Mail)
def action_before_delete(instance, **kwargs) : 
    cache.delete(f'{instance.sender.id}_mails')
    cache.delete(f'{instance.reciver.id}_mails')

    MailDocument().update(instance, action='delete')
