from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from mail.models import Mail
from django.dispatch import receiver
from mail.documents import MailDocument

@receiver(post_save, sender=Mail)
def action_after_save(created, instance, **kwargs) : 
    cache.delete(f'{instance.sender.id}_mails')
    cache.delete(f'{instance.reciver.id}_mails')

    try:
        instance_doc = MailDocument.get(id=instance.id)
        instance_doc.update(instance)
    except:
        MailDocument.init(instance)

@receiver(post_delete, sender=Mail)
def action_before_delete(instance, **kwargs) : 
    cache.delete(f'{instance.sender.id}_mails')
    cache.delete(f'{instance.reciver.id}_mails')

    try:
        instance_doc = MailDocument.get(id=instance.id)
        instance_doc.delete()
    except:
        pass

