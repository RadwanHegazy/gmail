from django.db import models
from users.models import User
from uuid import uuid4

class MAIL_STATUS(models.Choices) : 
    okay = 'okay'
    deleted = 'deleted'
    spammed = 'spammed'
    starred = 'starred'

class Mail (models.Model) : 
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid4
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
    
    @property
    def sender_full_name(self) : 
        return self.sender.full_name

    @property
    def get_body (self) : 
        return "encrypted body"
