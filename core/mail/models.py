from typing import override
from django.db import models
from users.models import User
from uuid import uuid4
from cryptography.fernet import Fernet
import mimetypes


class Attachment (models.Model) : 
    file = models.FileField(upload_to="mail-uploads/")
    content_type = models.CharField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @override
    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.file:
            # Get the content type based on the file extension
            content_type, _ = mimetypes.guess_type(self.file.name)
            self.content_type = content_type or 'application/octet-stream'
        return super().save(*args, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

class MAIL_STATUS(models.Choices) : 
    okay = 'okay'
    deleted = 'deleted'
    spammed = 'spammed'
    starred = 'starred'

class Mail (models.Model) : 
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid4,
    )

    sender = models.ForeignKey(
        User,
        related_name='mail_sender',
        on_delete=models.SET_NULL,
        null=True
    )

    reciver = models.ForeignKey(
        User,
        related_name='mail_reciver',
        on_delete=models.SET_NULL,
        null=True
    )
    
    attachments = models.ManyToManyField(
        Attachment,
        related_name = "mail_attachmets",
        blank = True
    )


    header = models.CharField(max_length=100)
    body = models.BinaryField()
    datetime = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    status = models.CharField(
        max_length=10, 
        choices=MAIL_STATUS, 
        default='okay'
    )
        

    def __str__(self) : 
        return self.header

    def soft_delete(self) : 
        self.status = MAIL_STATUS.deleted.value
        self.save()

    
    @property
    def sender_full_name(self) : 
        return self.sender.full_name

    @property
    def get_body (self) : 
        return self.__fernet.decrypt(
            bytes(self.body)
        ).decode()

    def set_body (self, body : str) :
        self.body = self.__fernet.encrypt(
            body.encode()
        )


    @property
    def __fernet(self) : 
        key = self.sender.hash_key + self.reciver.hash_key
        fernet = Fernet(
            key
        )
        return fernet

